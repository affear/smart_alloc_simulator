from oslo.config import cfg
import socket

CONF = cfg.CONF

netconf_opts = [
	cfg.StrOpt(
		'host',
		default=socket.gethostname(),
		help='Name of this node.  This can be an opaque identifier.  '
					'It is not necessarily a hostname, FQDN, or IP address. '
					'However, the node name must be valid within '
					'an AMQP key, and if using ZeroMQ, a valid '
					'hostname, FQDN, or IP address'
	),
]

CONF.register_opts(netconf_opts)