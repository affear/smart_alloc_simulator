from sim.nova.compute import rpcapi
from sim.nova import rpc
from sim.concrete import db
from sim.utils.openstack.common.periodic_task import periodic_task
from threading import Lock
from oslo.config import cfg
import logging

#TODO remove
from sim import config
config.init_conf()

logger = logging.getLogger('consolidator')

consolidator_opts = [
	cfg.StrOpt(
		'consolidator',
		default='sim.nova.consolidator.StupidConsolidator',
		help='The class used for consolidation'
	),
	cfg.IntOpt(
		'consolidator_period',
		default=60,
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

class BaseConsolidator(object):
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
		self.status = db.Host.get_all()
		self._migrations = []
		self._migrations_lock = Lock()

	class Migration(object):
		def __init__(self, vm_id, to_host_id):
			super(BaseConsolidator.Migration, self).__init__()
			self.vm_id = vm_id
			self.to_host_id = to_host_id

		def __repr__(self):
			return 'vm {} --> host {}'.format(self.vm_id, self.to_host_id)

	def consolidate(self):
		res = self.do_consolidate()
		with self._migrations_lock:
			self._migrations.extend(res)
			#TODO maybe reorder migrations?

	def do_consolidate(self):
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

	@periodic_task(spacing=CONF.consolidator_period)
	def execute_migrations(self):
		migrations = None
		with self._migrations_lock:
			# copy the list
			migrations = list(self._migrations)
			# empty original list
			self._migrations = []

		notifier = rpc.get_notifier(CONF.host)

		for migration in migrations:
			notifier.info({}, 'consolidator.instance.migrate.start', {'instance': migration.vm_id})
			logger.info('executing migration: ' + str(migration))
			#TODO something like self.compute_rpcapi.live_migrate(...)
			# wait until live_migrate will be added
			notifier.info({}, 'consolidator.instance.migrate.end', {'instance': migration.vm_id})

class StupidConsolidator(BaseConsolidator):
	'''
		Sample consolidator implementation
	'''

	def do_consolidate(self, to_handle):
		pass