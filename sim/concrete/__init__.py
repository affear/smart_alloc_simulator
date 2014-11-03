from oslo.config import cfg
from nova import enum

PM_TYPES = enum(
	STD_PM={
		'vcpus': 12,
		'memory_mb': 16000,
		'local_gb': 2000,
	},
	HALF_PM={
		'vcpus': 6,
		'memory_mb': 8000,
		'local_gb': 1000,
	},
	DOUBLE_PM={
		'vcpus': 24,
		'memory_mb': 32000,
		'local_gb': 4000,
	}
)

concrete_group = cfg.OptGroup(name='concrete')
concrete_opts = [
	cfg.ListOpt(
		'pms',
		default=[
			PM_TYPES.STD_PM,
			PM_TYPES.STD_PM,
			PM_TYPES.STD_PM,
			PM_TYPES.STD_PM,
			PM_TYPES.STD_PM,
			PM_TYPES.HALF_PM,
			PM_TYPES.HALF_PM,
			PM_TYPES.HALF_PM,
			PM_TYPES.HALF_PM,
			PM_TYPES.DOUBLE_PM,
		],
		help='The phisycal machines used during the simulation'
	),
]
CONF = cfg.CONF
CONF.register_group(concrete_group)
CONF.register_opts(concrete_opts, concrete_group)