"""
	This module contains OpenStack services as they are
"""

#some constants
def _enum(**enums):
	return type('Enum', (), enums)

METRICS = _enum(VCPU='vcpu', RAM='ram', DISK='disk')

# $ nova flavor-list
# +----+-----------+-----------+------+-----------+\+-------+-\+-------------+
# | ID | Name      | Memory_MB | Disk | Ephemeral |/| VCPUs | /| extra_specs |
# +----+-----------+-----------+------+-----------+\+-------+-\+-------------+
# | 1  | m1.tiny   | 512       | 1    | 0         |/| 1     | /| {}          |
# | 2  | m1.small  | 2048      | 10   | 20        |\| 1     | \| {}          |
# | 3  | m1.medium | 4096      | 10   | 40        |/| 2     | /| {}          |
# | 4  | m1.large  | 8192      | 10   | 80        |\| 4     | \| {}          |
# | 5  | m1.xlarge | 16384     | 10   | 160       |/| 8     | /| {}          |
# +----+-----------+-----------+------+-----------+\+-------+-\+-------------+
FLAVORS = _enum(
	TINY={
		'name': 'tiny',
		METRICS.VCPU: 1,
		METRICS.RAM: 512,
		METRICS.DISK: 1
	},
	SMALL={
		'name': 'small',
		METRICS.VCPU: 1,
		METRICS.RAM: 2048,
		METRICS.DISK: 10
	},
	MEDIUM={
		'name': 'medium',
		METRICS.VCPU: 1,
		METRICS.RAM: 4096,
		METRICS.DISK: 10
	},
	LARGE={
		'name': 'large',
		METRICS.VCPU: 1,
		METRICS.RAM: 8192,
		METRICS.DISK: 10
	},
	XLARGE={
		'name': 'xlarge',
		METRICS.VCPU: 1,
		METRICS.RAM: 16384,
		METRICS.DISK: 10
	}
)

FLAVOR_LIST = [FLAVORS.TINY, FLAVORS.SMALL, FLAVORS.MEDIUM, FLAVORS.LARGE, FLAVORS.XLARGE]
