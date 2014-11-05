from oslo.config import cfg

CONF = cfg.CONF

filter_opts = [
	cfg.ListOpt(
		'default_filters',
		default=['sim.nova.scheduler.filters.ram_filter.RamFilter', 
		'sim.nova.scheduler.filters.core_filter.CoreFilter', 
		'sim.nova.scheduler.filters.disk_filter.DiskFilter'],
		help='Filters to be used when not specified in the request'
		),
]

CONF.register_opts(filter_opts)


class BaseFilter(object):
	
	def host_passes(self, host, flavor):
		raise NotImplementedError()
