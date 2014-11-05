from sim.nova import METRICS
from sim.concrete import db
from sim.nova.scheduler.filters import BaseFilter

class DiskFilter(BaseFilter):

	def host_passes(self, host, flavor):
		"""Returns True if the host has enough free disk space to handle the flavor"""
		assert type(host) is db.Host

		return host.local_gb - host.local_gb_used > flavor[METRICS.DISK]

