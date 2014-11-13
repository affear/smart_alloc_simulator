from sim.nova.compute import rpcapi
from sim.concrete import db
from threading import Lock
from oslo.config import cfg

consolidator_opts = [
	cfg.StrOpt(
		'consolidator',
		default='sim.nova.consolidator.StupidConsolidator',
		help='The class used for consolidation'
	),
]

CONF = cfg.CONF
CONF.register_opts(consolidator_opts)

CONSOLIDATOR = None

def get_consolidator():
	global CONSOLIDATOR
	if not CONSOLIDATOR:
		from sim import utils
		cls = utils.class_for_name(CONF.consolidator)
		CONSOLIDATOR = cls()
	return CONSOLIDATOR

class BaseConsolidator(object):
	'''
		Base class for consolidators.
		If you want to access the consolidator,
		please don't do it by direct access, but calling the
		`get_consolidator` method provided by this module.
	'''
	status = None
	_cache = None
	lock = None

	def __init__(self):
		super(BaseConsolidator, self).__init__()
		self.status = db.Host.get_all()
		self.lock = Lock()

class StupidConsolidator(BaseConsolidator):
	'''
		Sample consolidator implementation
	'''
	pass