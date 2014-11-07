from oslo import messaging
from oslo.config import cfg
from sim.nova import rpc
from sim.nova.scheduler import rpcapi as scheduler_rpcapi
from sim.nova.scheduler.manager import NoDestinationFoundException
from sim.concrete import db
from sim.utils import log_utils
import logging
from functools import wraps
from sim import config
# as they do in OpenStack
config.init_conf()

CONF = cfg.CONF
CONF.import_opt('host', 'sim.nova.compute')
CONF.import_opt('compute_topic', 'sim.nova.compute.rpcapi')

log_utils.setup_logger('compute', CONF.logs.compute_log_file)

class ComputeManager(object):
	logger = logging.getLogger('compute')
	scheduler_client = scheduler_rpcapi.SchedulerAPI()
	hostname = CONF.host

	def _log(self, method, task_name, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, task_name)
		args = map(lambda a: str(a), args)
		method(' '.join(args))

	def build_instance(self, ctx, id, flavor):
		# 1. select destinations from scheduler --> https://github.com/openstack/nova/blob/master/nova/conductor/manager.py#L613
		# 2. spawn green thread to do the job --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L1980
		# 3. notify start --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2085
		# 4. claim resources --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2089
		# 5. save instance to DB --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2100
		# 6. spawn --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2104
		# 7. notify end --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2173
		
		notifier = rpc.get_notifier(self.hostname)
		# 1
		try:
			dest_id = self.scheduler_client.select_destinations(flavor)
		except messaging.RemoteError as r:
			if r.exc_type == NoDestinationFoundException.__name__:
				self._log(self.logger.warning, 'boot', r.value)
				raise NoDestinationFoundException(r.value)
			else:
				raise r

		dest = db.Host.get(dest_id)
		# 2 ...
		# 3
		notifier.info({}, 'compute.instance.create.start', {'flavor': flavor})
		# 4 ...
		# 5
		vm = db.VM(id=id, flavor=flavor, host=dest)
		vm.save(created=True)
		# 6
		# SPAWNING... we cannot spawn real VMs
		# 7
		notifier.info({}, 'compute.instance.create.end', {'vm': vm})

		self._log(self.logger.info, 'boot', vm)

	def delete(self, ctx, id):
		# 1. delete image --> https://github.com/openstack/nova/blob/master/nova/compute/api.py#L1544
		# 2. notify delete start --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2446
		# 3. shutdown instance --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2448
		# 4. save to DB --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2465
		# 5. notify delete end --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L817

		notifier = rpc.get_notifier(self.hostname)
		# 1 ... we do not have image stored
		# 2
		try:
			vm = db.VM.get(id)
		except db.VMNotFoundException as e:
			self.logger.error(e.message)
			raise e

		notifier.info({}, 'compute.instance.delete.start', {'vm': vm})
		# 3 & 4
		vm.terminate()
		# 5
		notifier.info({}, 'compute.instance.delete.end', {'vm_id': id})

		self._log(self.logger.info, 'delete', id)

	def resize(self, ctx, id, flavor):
		# A bit less precise desciption than other methods...
		# Sorry, but it is a heavy job

		# NB:
		# from resize method doc --> https://github.com/openstack/nova/blob/master/nova/compute/api.py#L2500:

		# Resize (ie, migrate) a running instance.
		# If flavor_id is None, the process is considered a migration, keeping
		# the original flavor_id. If flavor_id is not None, the instance should
		# be migrated to a new host and resized to the new flavor_id.

		# NB (from OS doc):
		# Quotas are operational limits.
		# For example, the number of gigabytes allowed for each tenant can be controlled so that cloud resources are optimized.
		# Quotas can be enforced at both the tenant (or project) and the tenant-user level.

		# Quotas are not at PM level, but are set per tenant/user by the admin.

		# 1. try to reserve quotas based on new flavor --> https://github.com/openstack/nova/blob/master/nova/compute/api.py#L2551
		# 2. if too big then HTTPBadRequest. NO autonomic behavior!
		# (TooManyInstances is subclass of QuotaError) --> https://github.com/openstack/nova/blob/master/nova/api/openstack/compute/servers.py#L1178

		# 3. else we can go on, and execute live migration task --> https://github.com/openstack/nova/blob/master/nova/conductor/manager.py#L561
		# 4. find the host (scheduler) --> https://github.com/openstack/nova/blob/master/nova/conductor/tasks/live_migrate.py#L159
		# 5. perform live migration

		notifier = rpc.get_notifier(self.hostname)
		# 1 & 2 ... we do not have quotas (and also users)
		try:
			vm = db.VM.get(id)
		except db.VMNotFoundException as e:
			self.logger.error(e.message)
			raise e

		notifier.info({}, 'compute.instance.resize.start', {'vm': vm})
		# stats down to perform a right calculus for the host
		vm.host.stats_down(vm.flavor).save()
		try:
			dest_id = self.scheduler_client.select_destinations(flavor)
		except messaging.RemoteError as r:
			if r.exc_type == NoDestinationFoundException.__name__:
				self._log(self.logger.warning, 'resize', r.value)
				raise NoDestinationFoundException(r.value)
			else:
				raise r
		finally:
			vm.host.stats_up(vm.flavor).save()

		dest = db.Host.get(dest_id)
		# ok, now we can move
		vm.move(new_flavor=flavor, new_host=dest)
		# notify end
		notifier.info({}, 'compute.instance.resize.end', {'vm': vm})

		self._log(self.logger.info, 'resize', id, flavor['name'])

if __name__ == '__main__':
	server = rpc.get_server(CONF.compute_topic, [ComputeManager(), ])
	server.start()