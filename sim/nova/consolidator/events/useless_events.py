'''
	TODO delete this file
'''
from sim.nova.consolidator.events import BaseEndpoint
import logging

logger = logging.getLogger('consolidator')

class Foo(BaseEndpoint):
	event_type = 'foo.event'

	def on_info(self, ctxt, publisher_id, payload, metadata):
		logger.info(self.event_type + str(payload))

class Lol(BaseEndpoint):
	event_type = 'lol.event'

	def on_info(self, ctxt, publisher_id, payload, metadata):
		logger.info(self.event_type + str(payload))

class Bar(object):
	# not in _endpoints!
	event_type = 'bar.event'

	def on_info():
		pass