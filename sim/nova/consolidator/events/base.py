class BaseEndpoint(object):
	'''
		To have a working endpoint, inherit from this class
		and import all from your module in sim.nova.consolidator.events.__init__.py
		Set self.event_type to answer to a certain event.
		Prefix with 'on_' a method name to make it answer
		to a certain level. E.g.:

			event_type = 'foo.event'

			def on_info(self, ctxt, publisher_id, payload, metadata):
				pass

			def on_warning(self, ctxt, publisher_id, payload, metadata):
				pass
	'''
	event_type = ''