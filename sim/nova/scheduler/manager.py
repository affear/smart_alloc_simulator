from oslo import messaging
from oslo.config import cfg
from sim.nova import rpc
from sim.nova.scheduler import filter_scheduler
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
		hosts = filter_scheduler.FilterScheduler().select_destinations(flavor)
		self._log_info('select destination', hosts)
		return hosts


if __name__ == '__main__':
	server = rpc.get_server(CONF.scheduler_topic, [SchedulerManager(), ])
	server.start()