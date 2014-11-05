from oslo import messaging
from oslo.config import cfg
from sim.nova import rpc
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
		self.client = rpc.get_client(CONF.compute_topic)

	def build_instance(self, id, flavor):
		# wait to have synchronous calls
		self.client.call({}, 'build_instance', id=id, flavor=flavor)

	def delete(self, id):
		# wait to have synchronous calls
		self.client.call({}, 'delete', id=id)

	def resize(self, id, flavor):
		return self.client.call({}, 'resize', id=id, flavor=flavor)

