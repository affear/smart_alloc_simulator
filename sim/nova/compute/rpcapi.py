from oslo import messaging
from oslo.config import cfg

transport = messaging.get_transport(cfg.CONF)
target = messaging.Target(topic='compute')
client = messaging.RPCClient(transport, target)

class ComputeTaskAPI(object):
	def build_instance(self, id, flavor):
		#TODO implement the rest
		client.cast({}, 'build_instance', id=id, flavor=flavor)

	def delete(self, id):
		#TODO implement the rest
		client.cast({}, 'delete', id=id)

	def resize(self, id, flavor):
		#TODO implement the rest
		return client.call({}, 'resize', id=id, flavor=flavor)

