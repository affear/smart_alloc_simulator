from oslo.config import cfg

CONF = cfg.CONF

filter_opts = [
	cfg.ListOpt(
		'default_filters',
		default=['RamFilter', 'VCPUsFilter', 'StorageFilter'],
		help='Filters to be used when not specified in the request'
		),
]

CONF.register_opts(filter_opts)


class BaseFilter(object):
	
	def host_passes(self, host, flavor):
		raise NotImplementedError()
