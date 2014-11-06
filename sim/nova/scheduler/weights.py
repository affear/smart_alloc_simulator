from oslo.config import cfg
import logging
from sim.utils import log_utils

CONF = cfg.CONF

class WeightedHost(object):
	"""Object containing an host and its weight"""
	def __init__(self, host, weight):
		self.host = host
		self.weight = weight
		

weights_opts = [
	cfg.ListOpt(
		'weighers',
		default=['memory_mb_used=1.0',
		],
		help='Weighers to be used when not specified in the config file. The names of the metrics '
		'must be the same as the host attributes (memory_mb_used, local_gb_used...)'
		),
]

CONF.register_opts(weights_opts)
logger = logging.getLogger('scheduler')

def _parse_options(opts):
	opts_list = []

	for opt in opts:
		key, sep, value = opt.partition('=')
		opts_list.append((key, value))

	return opts_list

def _weight_host(host, selected_weighers):
	value = 0.0

	for(name, ratio) in selected_weighers_list:
		try:
			value += getattr(host, name) * ratio
		except AttributeError:
			logger.error('Metric ' + name + ' not found')

	return value

def _order_hosts(hosts, selected_weighers):
	weighted_hosts = []
	ordered_weighted_hosts = []
	ordered_hosts = []

	for h in host:
		weight = _weight_host(h, selected_weighers)
		h.append(WeightedHost(h, weight))

	ordered_weighted_hosts = sorted(weighted_hosts, key = lambda host: host.weight)

	for h in ordered_hosts:
		ordered_hosts.append(h.host)

	return ordered_hosts



def get_weighed_hosts(hosts, weighers=None):
	if not weighers:
		selected_weighers = _parse_options(CONF.weighers)
	else:
		selected_weighers = weighers

	return _order_hosts(hosts, selected_weighers)


