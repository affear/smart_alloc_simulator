from sim.nova.compute import rpcapi
from sim.nova import rpc
from sim.concrete import db
from sim.utils.openstack.common import periodic_task
from sim.utils import log_utils
from threading import Lock
from oslo.config import cfg
import logging
from sim import config
config.init_conf()

log_utils.setup_logger('consolidator', cfg.CONF.logs.consolidator_log_file)
logger = logging.getLogger('consolidator')

consolidator_opts = [
	cfg.StrOpt(
		'consolidator',
		default='sim.nova.consolidator.StupidConsolidator',
		help='The class used for consolidation'
	),
	cfg.IntOpt(
		'consolidator_period',
		default=3,
		help='The period (in seconds) by which migrations are applied'
	),
]

CONF = cfg.CONF
CONF.register_opts(consolidator_opts)

CONSOLIDATOR = None

def get_consolidator():
	global CONSOLIDATOR
	if not CONSOLIDATOR:
		from sim import utils
		cls = utils.class_for_name(CONF.consolidator)
		CONSOLIDATOR = cls()
	return CONSOLIDATOR

class BaseConsolidator(periodic_task.PeriodicTasks):
	'''
		Base class for consolidators.
		If you want to access the consolidator,
		please don't do it by direct access, but calling the
		`get_consolidator` method provided by this module.

		No need to worry about multithreading until the executor
		used by the notification listener is __blocking__!
	'''
	# current status to be updated at any time
	status = None
	# output of consolidation algorithm
	_migrations = None
	_migrations_lock = None
	compute_rpcapi = rpcapi.ComputeTaskAPI()

	def __init__(self):
		super(BaseConsolidator, self).__init__()
		self._migrations = []
		self._migrations_lock = Lock()

	class Migration(object):
		def __init__(self, vm_id, to_host_id):
			super(BaseConsolidator.Migration, self).__init__()
			self.vm_id = vm_id
			self.to_host_id = to_host_id

		def __repr__(self):
			return 'vm {} --> host {}'.format(self.vm_id, self.to_host_id)

	def consolidate(self, ctxt, event_type, payload):
		if not ctxt.get('smart', None):
			#if we are not in a smart simulation, we do not react
			logger.debug('Not in a SMART simulation...')
			return

		# update status
		#self.status = db.Host.get_all()
		res = self.do_consolidate(ctxt, event_type, payload)
		with self._migrations_lock:
			self._migrations.extend(res)

	def do_consolidate(self, ctxt, event_type, payload):
		'''
			The real consolidation algorithm.
			Returns a list of migrations.

			Example implementation:

			def do_consolidate(self, to_handle):
				status = self.status
				migrations = []

				for host in status:
					to_host_id = choose_host(to_handle.vm)
					vm_id = to_handle.vm.id

					migration = self.Migration(vm_id, to_host_id)
					migrations.push(migration)

				return migrations
		'''
		raise NotImplementedError

	def periodic_tasks(self, context):
		"""Tasks to be run at a periodic interval."""
		return self.run_periodic_tasks(context)

	@periodic_task.periodic_task(spacing=CONF.consolidator_period)
	def execute_migrations(self, ctxt):
		logger.debug('periodic_task: EXECUTE MIGRATIONS')

		migrations = None
		with self._migrations_lock:
			# copy the list
			migrations = list(self._migrations)
			# empty original list
			self._migrations = []

		notifier = rpc.get_notifier(CONF.host)

		for migration in migrations:
			notifier.info({}, 'consolidator.instance.live_migrate.start', {'instance': migration.vm_id})
			self.compute_rpcapi.live_migrate(
				vm_id=migration.vm_id,
				#TODO load VM from db and set to vm.flavor
				flavor=None,
				host_id=migration.host_id
			)
			notifier.info({}, 'consolidator.instance.live_migrate.end', {'instance': migration.vm_id})

class StupidConsolidator(BaseConsolidator):
	'''
		Sample consolidator implementation
	'''

	def do_consolidate(self, ctxt, event_type, payload):
		logger.info(' '.join([str(ctxt), event_type, str(payload)]))
		return []

if __name__ == '__main__':
	from sim.utils.openstack.common import service

	_cons = get_consolidator()

	class NotificationService(service.Service):
		def __init__(self):
			super(NotificationService, self).__init__()
			self.manager = _cons

		def start(self):
			self.tg.add_dynamic_timer(self.periodic_tasks)

		def periodic_tasks(self):
			"""Tasks to be run at a periodic interval."""
			#TODO think of something for the ctxt
			ctxt = {'some': 'context'}
			return self.manager.periodic_tasks(ctxt)

	s = NotificationService()
	launcher = service.launch(s)
	launcher.wait()