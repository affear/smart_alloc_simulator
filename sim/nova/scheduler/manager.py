from oslo import messaging
from oslo.config import cfg
from sim.nova import rpc
from sim.nova.scheduler.filter_scheduler import FilterScheduler
import logging
from sim.utils import log_utils
from sim import config
# as they do in OpenStack
config.init_conf()

CONF = cfg.CONF
CONF.import_opt('scheduler_topic', 'sim.nova.scheduler.rpcapi')

log_utils.setup_logger('scheduler', CONF.logs.scheduler_log_file)

class SchedulerManager(object):
	logger = logging.getLogger('scheduler')

	def _log_info(self, task_name, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, task_name)
		args.insert(0, 'executing')
		args = map(lambda a: str(a), args)
		self.logger.info(' '.join(args))

	def select_destinations(self, ctx, flavor):
		hosts = FilterScheduler().select_destinations(flavor)
		# return ID to avoid circular dependency in serialization
		host = hosts[0].id if hosts else None # our "weighting" to choose the first one (for now)
		self._log_info('selected host', host)
		return host


if __name__ == '__main__':
	server = rpc.get_server(CONF.scheduler_topic, [SchedulerManager(), ])
	server.start()