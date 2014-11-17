from oslo.config import cfg
from oslo.db.sqlalchemy import session as db_session
from oslo.db.sqlalchemy import models
from oslo.db.sqlalchemy.utils import model_query
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

# init db conf using config file
from sim.config import load_conf_file
load_conf_file()

BASE = declarative_base()

_FACADE = None

def _create_facade_lazily():
	global _FACADE
	if _FACADE is None:
			_FACADE = db_session.EngineFacade.from_config(cfg.CONF)
	return _FACADE

def get_engine():
	facade = _create_facade_lazily()
	return facade.get_engine()

def get_session(**kwargs):
	facade = _create_facade_lazily()
	return facade.get_session(**kwargs)

class SimData(BASE, models.TimestampMixin, models.ModelBase):
	'''
		The class to gather simulation data
	'''
	__tablename__ = 'simdata'

	id = Column(Integer, primary_key=True)
	avg_consumption = Column(Integer, default=0)
	avg_no_pms = Column(Integer, default=0)
	no_nodestfound = Column(Integer, default=0)
	smart = Column(Boolean, default=False)

	# accessor methods
	@classmethod
	def filter_sim(cls, session, smart):
		return model_query(cls, session).filter(cls.smart == smart).all()

	@classmethod
	def _avg_on_param(cls, param, smart=False):
		s = get_session()
		with s.begin():
			sims = cls.filter_sim(s, smart)
			if not sims:
				return 0
			return sum([getattr(sim, param) for sim in sims]) / float(len(sims))

	@classmethod
	def get_avg_consumption(cls, smart=False):
		return cls._avg_on_param('avg_consumption', smart)

	@classmethod
	def get_avg_no_pms(cls, smart=False):
		return cls._avg_on_param('avg_no_pms', smart)

	@classmethod
	def get_avg_nodestfound(cls, smart=False):
		return cls._avg_on_param('no_nodestfound', smart)

# create db (only creates if not present)
BASE.metadata.create_all(get_engine())