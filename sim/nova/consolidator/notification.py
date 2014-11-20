from oslo import messaging
from oslo.config import cfg
from sim.utils import log_utils
from sim.nova.consolidator import get_consolidator
import logging

log_utils.setup_logger('consolidator', cfg.CONF.logs.consolidator_log_file)
logger = logging.getLogger('consolidator')

_cons = get_consolidator()

class EntryEndpoint(object):
	allowed_priorities = [
		'info',
		'warning',
		'error',
		'audit',
		'debug'
	]

	def __init__(self):
		super(EntryEndpoint, self).__init__()

		def _notify(ctxt, publisher_id, event_type, payload, metadata):
			_cons.consolidate(ctxt, event_type, payload)

		#set method for each priority
		for p in self.allowed_priorities:
			setattr(self, p, _notify)

if __name__ == '__main__':
	from sim import config
	config.init_conf()
	
	transport = messaging.get_transport(cfg.CONF)
	targets = [messaging.Target(topic='notifications'),]
	endpoints = [EntryEndpoint()]

	server = messaging.get_notification_listener(transport, targets, endpoints)
	# the default executor is blocking!
	# se every request is executed as in a queue!
	# even in openstack they do this:
	# https://github.com/openstack/ceilometer/blob/master/ceilometer/notification.py#L104
	server.start()
	server.wait()