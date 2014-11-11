'''
	TODO delete this file
'''
from sim.nova.consolidator.events.base import BaseEndpoint
import logging

logger = logging.getLogger('consolidator')

class Buzz(BaseEndpoint):
	event_type = 'buzz.event'

	def on_error(self, ctxt, publisher_id, payload, metadata):
		logger.info(self.event_type + str(payload))