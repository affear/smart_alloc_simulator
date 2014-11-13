from oslo import messaging
from oslo.config import cfg
from sim.utils import log_utils
import logging, inspect, pkgutil
from sim.nova.consolidator import events
from sim.nova.consolidator.events.base import BaseEndpoint

log_utils.setup_logger('consolidator', cfg.CONF.logs.consolidator_log_file)
logger = logging.getLogger('consolidator')

allowed_priorities = [
	'info',
	'warning',
	'error',
	'audit',
	'debug'
]

class EntryEndpoint(object):
	def __init__(self):
		super(EntryEndpoint, self).__init__()

		self._endpoints = {}
		# Filling self._endpoints as
		# {
		#		level0: {
		#			event_type0: handler0,	
		#			event_type1: handler1,	
		#			event_type2: handler2,
		#			...	
		#		},
		#		level1: {
		#			...	
		#		},
		#		...
		# }

		for priority in allowed_priorities:
			self._endpoints[priority] = {}

		# Now we have:
		# {
		#		level0: {},
		#		level1: {},
		#		level2: {},
		#		...
		# }

		def _filter_level_fn(member):
			'''
				Returns a member if it is a method and its name starts with 'on_'
			'''
			return inspect.ismethod(member) and member.__name__.startswith('on_')

		def _filter_endpoint_fn(cls):
			'''
				Returns a member if it is a class
				and it inherits from BaseEndpoint
			'''
			if not inspect.isclass(cls) or cls == BaseEndpoint:
				return False
			base_classes = inspect.getmro(cls)
			return BaseEndpoint in base_classes

		for importer, mod_name, ispkg in pkgutil.iter_modules(events.__path__):
			# all submodules
			submodule = importer.find_module(mod_name).load_module(mod_name)
			for cls_name, cls in inspect.getmembers(submodule, _filter_endpoint_fn):
				if not getattr(cls, 'event_type', None):
					continue
				for method_name, handler in inspect.getmembers(cls, _filter_level_fn):
					# remove 'on_'
					lvl_name = method_name[3:]
					if not lvl_name in allowed_priorities:
						continue
					self._endpoints[lvl_name][cls.event_type] = getattr(cls(), method_name)

		# OK, finished

		# now set attributes on self
		def get_notify_fn(level):
			def notify(ctxt, publisher_id, event_type, payload, metadata):
				self._notify(level, event_type, ctxt, publisher_id, payload, metadata)
			return notify

		for level in allowed_priorities:
			setattr(self, level, get_notify_fn(level))

	def _notify(self, level, event_type, *args):
		priority = self._endpoints.get(level, None)
		if priority:
			handler = priority.get(event_type, None)
			if handler:
				handler(*args)

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