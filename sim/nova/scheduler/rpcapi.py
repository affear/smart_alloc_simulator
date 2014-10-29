from oslo import 
from oslo.config import cfg

transport = messaging.get_transport(cfg.CONF)
target = messaging.Target(topic='scheduler')
client = messaging.RPCClient(transport, target)

class SchedulerAPI(object):
	
	def select_destinations(self, id, flavor):
		client.cast({}, 'select_destinations', id=id, flavor=flavor)
