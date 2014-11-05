from oslo import messaging 
from oslo.config import cfg
from sim.nova import rpc

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
		self.client = rpc.get_client(CONF.scheduler_topic)

	def select_destinations(self, flavor):
		self.client.prepare()
		return self.client.call({}, 'select_destinations', flavor=flavor)
