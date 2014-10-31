"""Initialize and pupulates the DB"""

if __name__ == "__main__":
	from sim.concrete import db
	from sqlalchemy.orm import sessionmaker	
	from sqlalchemy import create_engine
	from oslo.config import cfg

	#Creates the DB
	engine = create_engine('sqlite:///' + db.DB_FILE_NAME)
	db.Base.metadata.create_all(engine)

	CONF = cfg.CONF
	CONF.import_group('concrete', 'sim.concrete')

	#Populates the db with PM
	for i in range(1, CONF.concrete.no_pms + 1):
		try:
			db.create(i,8,16000,120,"compute" + str(i))

		except Exception as e:
			print e

