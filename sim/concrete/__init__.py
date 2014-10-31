from oslo.config import cfg

concrete_group = cfg.OptGroup(name='concrete')
concrete_opts = [
	cfg.IntOpt(
		'no_pms',
		default=5,
		help='The number of physical machines'
	),
]
CONF = cfg.CONF
CONF.register_group(concrete_group)
CONF.register_opts(concrete_opts, concrete_group)