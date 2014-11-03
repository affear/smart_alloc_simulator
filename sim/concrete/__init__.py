from oslo.config import cfg
from nova import enum, METRICS

PM_TYPES = enum(
	STD_PM={
		METRICS.VCPU: 12,
		METRICS.RAM: 16000,
		METRICS.DISK: 2000,
	},
	HALF_PM={
		METRICS.VCPU: 6,
		METRICS.RAM: 8000,
		METRICS.DISK: 1000,
	},
	DOUBLE_PM={
		METRICS.VCPU: 24,
		METRICS.RAM: 32000,
		METRICS.DISK: 4000,
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