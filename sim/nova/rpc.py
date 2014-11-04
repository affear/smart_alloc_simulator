# The OpenStack Way
from oslo import messaging
from oslo.config import cfg

TRANSPORT = None
NOTIFIER = None

def init(conf):
	global TRANSPORT, NOTIFIER
	TRANSPORT = messaging.get_transport(conf)
	NOTIFIER = messaging.Notifier(TRANSPORT)

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

def get_notifier(publisher_id):
		assert NOTIFIER is not None
		return NOTIFIER.prepare(publisher_id=publisher_id)
