from sim.nova import METRICS
from sim.concrete import db

class RamFilter(object):

	def host_passes(self, host, flavor):
		"""Returns True if the host is Ram-capable to handle the flavor"""
		assert type(host) is db.Host

		return host.memory_mb > host.flavor[METRICS.RAM]