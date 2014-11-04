from oslo import messaging 
from oslo.config import cfg

rpcapi_opts = [
	cfg.StrOpt(
		'scheduler_topic',
		default='scheduler',
		help='The topic scheduler listen on'
	),
]

CONF = cfg.CONF
CONF.register_opts(rpcapi_opts)

class SchedulerAPI(object):

	def __init__(self):
		super(SchedulerAPI, self).__init__()
		transport = messaging.get_transport(cfg.CONF)
		target = messaging.Target(topic=CONF.scheduler_topic)
		self.client = messaging.RPCClient(transport, target)

	def select_destinations(self, flavor):
		return client.call({}, 'select_destinations', flavor=flavor)
