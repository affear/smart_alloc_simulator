# The OpenStack Way
from oslo.config import cfg
from sim.nova import rpc
DEFAULT_CONFIG_FILE = 'sim.conf'
CONF = cfg.CONF

def init_conf(): # in OpenStack, it is parse_args()
	CONF(default_config_files=[DEFAULT_CONFIG_FILE, ])
	rpc.init(CONF)