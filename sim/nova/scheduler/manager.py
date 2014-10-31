from oslo import messaging
from oslo.config import cfg
from sim.nova.scheduler import filter_scheduler
import logging
from sim.utils import log_utils

class SchedulerManager(object):
	logger = logging.getLogger('scheduler')

	def _log_info(self, *args):
		args = list(args)
		args.insert(0, 'slecting destination for: ')
		args = map(lamba a: str(a), args)
		logger.info(' '.join(args))

	def select_destinations(self, ctx, flavor):
		self._log_info(id, flavor['name'])
		return filter_scheduler.select_destinations(id,flavor)


if __name__ == '__main__':


	CONF = cfg.CONF
	CONF.import_opt('scheduler_topic', 'sim.nova.scheduler.rpcapi')
	CONF.import_opt('host', 'sim.nova.compute')

	log_utils.setup_logger('scheduler', CONF.logs.scheduler_log_file)

	transport = messaging.get_transport(cfg.CONF)
	target = messaging.Target(topic=CONF.scheduler_topic, server=CONF.compute)
	endpoints = [ComputeTaskManager(), ]
	server = messaging.get_rpc_server(transport, target, endpoints,
																			executor='blocking')
	server.start()
	#server.wait()
