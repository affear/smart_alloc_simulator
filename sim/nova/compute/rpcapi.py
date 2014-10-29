from oslo import messaging
from oslo.config import cfg

# as they do in OpenStack
rpcapi_opts = [
	cfg.StrOpt(
		'compute_topic',
		default='compute',
		help='The topic compute nodes listen on'
	),
]

CONF = cfg.CONF
CONF.register_opts(rpcapi_opts)

class ComputeTaskAPI(object):
	def __init__(self):
		super(ComputeTaskAPI, self).__init__()
		transport = messaging.get_transport(cfg.CONF)
		target = messaging.Target(topic=CONF.compute_topic)
		self.client = messaging.RPCClient(transport, target)

	def build_instance(self, id, flavor):
		#TODO implement the rest
		self.client.cast({}, 'build_instance', id=id, flavor=flavor)

	def delete(self, id):
		#TODO implement the rest
		self.client.cast({}, 'delete', id=id)

	def resize(self, id, flavor):
		#TODO implement the rest
		return self.client.call({}, 'resize', id=id, flavor=flavor)

