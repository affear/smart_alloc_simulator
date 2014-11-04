from oslo import messaging
from oslo.config import cfg
from sim.nova import rpc
from sim.nova.scheduler import rpcapi as scheduler_rpcapi
from sim.concrete import db
import logging

class ComputeManager(object):
	logger = logging.getLogger('compute')
	scheduler_client = scheduler_rpcapi.SchedulerAPI()

	def _log_info(self, task_name, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, task_name)
		args.insert(0, 'executing')
		args = map(lambda a: str(a), args)
		self.logger.info(' '.join(args))
		#TODO change 'compute1' to get real hostname
		self.notifier = rpc.get_notifier('compute1')

	def build_instance(self, ctx, id, flavor):
		# 1. select destinations from scheduler --> https://github.com/openstack/nova/blob/master/nova/conductor/manager.py#L613
		# 2. spawn green thread to do the job --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L1980
		# 3. notify start --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2085
		# 4. claim resources --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2089
		# 5. save instance to DB --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2100
		# 6. spawn --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2104
		# 7. notify end --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2173
		
		#host = self.scheduler_client.select_destinations(flavor)
		#vm = db.VM.create(id=id, flavor=flavor, host=host)
		#self._log_info('boot', vm)
		#TODO remove comments and make it work
		self.notifier.info({}, 'compute.create', {'msg': 'vm created'})


	def delete(self, ctx, id):
		# 1. delete image --> https://github.com/openstack/nova/blob/master/nova/compute/api.py#L1544
		# 2. notify delete start --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2446
		# 3. shutdown instance --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2448
		# 4. save to DB --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L2465
		# 5. notify delete end --> https://github.com/openstack/nova/blob/master/nova/compute/manager.py#L817

		self._log_info('delete', id)

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

		self._log_info('resize', id, flavor['name'])

if __name__ == '__main__':
	from sim.utils import log_utils
	from sim import config

	# as they do in OpenStack
	config.init_conf()
	CONF = cfg.CONF
	CONF.import_opt('compute_topic', 'sim.nova.compute.rpcapi')
	#CONF.import_opt('compute_log_file', 'sim.utils.log_utils')
	log_utils.setup_logger('compute', CONF.logs.compute_log_file)

	server = rpc.get_server(CONF.compute_topic, [ComputeManager(), ])
	server.start()