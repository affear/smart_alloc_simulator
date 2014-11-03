"""Initialize and pupulates the DB"""

if __name__ == "__main__":
	from sim.concrete import db
	from sqlalchemy.orm import sessionmaker	
	from sqlalchemy import create_engine
	from oslo.config import cfg
	from sim.utils import log_utils
	from sim.nova import METRICS
	import logging

	#Creates the DB
	engine = create_engine('sqlite:///' + db.DB_FILE_NAME)
	db.Base.metadata.drop_all(engine)
	db.Base.metadata.create_all(engine)

	CONF = cfg.CONF
	CONF.import_group('concrete', 'sim.concrete')

	log_utils.setup_logger('db', CONF.logs.db_log_file)
	logger = logging.getLogger('db')


	i=0
	#Populates the db with PM
	for pm in CONF.concrete.pms:
		try:
			db.Host.create(id=i, vcpus=pm[METRICS.VCPU], memory_mb=pm[METRICS.RAM], local_gb=pm[METRICS.DISK], hostname='compute' + str(i))
			i += 1
		except Exception as e:
			logger.error(e)

	with db.Host.get_all() as host:
		print host
