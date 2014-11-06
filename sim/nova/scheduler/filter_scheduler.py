from sim.concrete import db
from sim.nova.scheduler import filters
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

		def _class_import(class_path):
			"""Returns the class given its path as a string"""
			mod_path = '.'.join(class_path.split('.')[0:-1])
			class_name = class_path.split('.')[-1]
			mod = __import__(mod_path)
			components = mod_path.split('.')
			for comp in components[1:]:
				mod = getattr(mod, comp)
			clazz = getattr(mod, class_name)
			return clazz

		def _filter(host, filters, flavor):			
			for f in filters:
				if not f.host_passes(host, flavor):
					return False
			return True

		selected_hosts = []
		filters = []

		for sf in selected_filters:
			filterClass = _class_import(sf)
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

		selected_destinations = self._schedule(all_hosts, selected_filters, flavor)

		return selected_destinations