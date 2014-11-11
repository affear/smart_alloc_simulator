import logging
logger = logging.getLogger('consolidator')

class BaseEndpoint(object):
	'''
		The class to extend to have a working endpoint.
		Set self.event_type to answer to a certain event.
		Override the methods below to set the answer at some level
		for the specified event_type.
	'''
	event_type = ''

	def on_audit(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_critical(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_debug(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_error(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_info(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_sample(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

	def on_warning(self, ctxt, publisher_id, payload, metadata):
		logger.info(' '.join([self.event_type, ':', str(payload)]))

class Foo(BaseEndpoint):
	event_type = 'foo.event'

class Lol(BaseEndpoint):
	event_type = 'lol.event'

class Bar(object):
	# not in _endpoints!
	def on_info():
		pass