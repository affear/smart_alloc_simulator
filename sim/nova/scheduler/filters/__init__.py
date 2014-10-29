from oslo.config import cfg

CONF = cfg.CONF

filter_opts = [
	cfg.StrOpt(
		'default_filters',
		default=['RamFilter', 'VCPUsFilter', 'StorageFilter'],
		help='Filters to be used when not specified in the request'
		),
]

CONF.register_opts(filter_opts)