from sim.nova import METRICS
from sim.concrete import db
from sim.nova.scheduler.filters import BaseFilter

class RamFilter(BaseFilter):

	def host_passes(self, host, flavor):
		"""Returns True if the host is Ram-capable to handle the flavor"""
		assert type(host) is db.Host

		return host.memory_mb - host.memory_mb_used > flavor[METRICS.RAM]
