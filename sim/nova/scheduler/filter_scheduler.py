from sim.concrete import db
import sim.nova.scheduler.filters
from oslo.config import cfg

CONF = cfg.CONF

class FilterScheduler(object):
	"""FilterScheduler simulator"""

	#We don't consider the possibility to pass a bundle of instances to be spawned
	def select_destinations(self, flavor):

		dest = []
		all_hosts = db.get_all()



		return dest

	def _schedule():


	def _get_all_host_states(self):
		""""Returns the list containing the hosts"""

		hosts = []

		return hosts

