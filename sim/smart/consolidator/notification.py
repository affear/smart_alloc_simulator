from oslo import messaging
from oslo.config import cfg
from sim.utils import log_utils
import logging
log_utils.setup_logger('consolidator', cfg.CONF.logs.consolidator_log_file)
logger = logging.getLogger('consolidator')

class Endpoints(object):
	def info(self, ctxt, publisher_id, event_type, payload, metadata):
		logger.info(payload)

if __name__ == '__main__':
	from sim import config
	config.init_conf()

	transport = messaging.get_transport(cfg.CONF)
	targets = [messaging.Target(topic='notifications'),]
	endpoints = [Endpoints()]

	server = messaging.get_notification_listener(transport, targets, endpoints)
	server.start()