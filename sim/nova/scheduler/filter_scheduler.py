from sim.concrete import db
from sim.nova.scheduler import filters
from sim.nova.scheduler import weights
from oslo.config import cfg


CONF = cfg.CONF
CONF.import_opt('default_filters', 'sim.nova.scheduler.filters')


class FilterScheduler(object):
	"""FilterScheduler simulator"""

	def _select_filters(self, filters):
		if not filters:
			selected_filters = CONF.default_filters
		else:
			selected_filters = filters
		return selected_filters

	def _schedule(self, all_hosts, selected_filters, flavor):
		def _filter(host, filters, flavor):			
			for f in filters:
				if not f.host_passes(host, flavor):
					return False
			return True

		selected_hosts = []
		filters = []

		from sim import utils
		for sf in selected_filters:
			filterClass = utils.class_for_name(sf)
			filters.append(filterClass())

		for h in all_hosts:
			if _filter(h, filters, flavor):
				selected_hosts.append(h)

		return selected_hosts


	#We don't consider the possibility to pass a bundle of instances to be spawned
	def select_destinations(self, flavor, filters=None):
		""""Returns a list of destinations ordered from the best suitable to the worst"""

		all_hosts = db.Host.get_all()
		selected_filters = self._select_filters(filters)

		#Filtering
		selected_destinations = self._schedule(all_hosts, selected_filters, flavor)
		#Weighing
		weighted_destinations = weights.get_weighed_hosts(selected_destinations)
		return weighted_destinations
