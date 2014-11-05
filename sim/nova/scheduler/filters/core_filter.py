from sim.nova import METRICS
from sim.concrete import db
from sim.nova.scheduler.filters import BaseFilter

class CoreFilter(BaseFilter):

	def host_passes(self, host, flavor):
		"""Returns True if the host has enough vcpus to handle the flavor"""
		assert type(host) is db.Host

		return host.vcpus - host.vcpus_used > flavor[METRICS.VCPU]
