# The OpenStack Way
from oslo import messaging
from oslo.config import cfg

TRANSPORT = None

def init(conf):
	global TRANSPORT
	TRANSPORT = messaging.get_transport(conf)

def get_client(topic):
	assert TRANSPORT is not None
	target = messaging.Target(topic=topic)
	return messaging.RPCClient(TRANSPORT, target)


def get_server(topic, endpoints):
	assert TRANSPORT is not None
	assert type(endpoints) is list
	cfg.CONF.import_opt('host', 'sim.nova.compute')
	target = messaging.Target(topic=topic, server=cfg.CONF.host)
	return messaging.get_rpc_server(TRANSPORT, target, endpoints)
