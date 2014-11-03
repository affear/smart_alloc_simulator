"""Initialize and pupulates the DB"""

if __name__ == "__main__":
	from sim.concrete.db import db, Host, VM
	from oslo.config import cfg
	from sim.utils import log_utils
	from sim.nova import METRICS
	from sim.nova import FLAVORS
	
	import logging

	#Creates the DB
	db.create_tables([Host,VM], True)

	CONF = cfg.CONF
	CONF.import_group('concrete', 'sim.concrete')

	log_utils.setup_logger('db', CONF.logs.db_log_file)
	logger = logging.getLogger('db')


	#Populates the db with PM
	for pm in CONF.concrete.pms:
		try:
			host = Host.create(vcpus=pm[METRICS.VCPU], memory_mb=pm[METRICS.RAM], local_gb=pm[METRICS.DISK])
		except Exception as e:
			logger.error(e)


	# #vm = VM.create(id=1, flavor=FLAVORS.TINY,host=Host.select().where(Host.id == 1).get())
	# for vm in Host.select().where(Host.id == 1).get().vms.iterator():
	# 	print vm.flavor