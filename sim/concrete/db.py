from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext	.declarative import declarative_base
from sqlalchemy.orm import sessionmaker	
from sqlalchemy import create_engine


Base = declarative_base()
engine = create_engine('sqlite:///compute_node.db')
Base.metadata.bind = engine

class Host(Base):
	""""Class that declares the compute_node table which simulates the 
	compute_nodes table in nova db; it includes only fields useful for the simulation.
	"""

	__tablename__ = "compute_node"

	id = Column(Integer, primary_key=True, autoincrement=False)

	#Base metrics (virtual CPUs, RAM, Disk) with their usage counterpart
	vcpus = Column(Integer, nullable=False)
	memory_mb = Column(Integer, nullable=False)
	local_gb = Column(Integer, nullable=False)
	vcpus_used = Column(Integer, nullable=False)
	memory_mb_used = Column(Integer, nullable=False)
	local_gb_used = Column(Integer, nullable=False)

	# #Hypervisor info
	# hypervisor_type = Column(Text, nullable=False)
	# hypervisor_version = Column(Integer, nullable=False)

	# #CPU info (Json)
	# cpu_info = Column(String(250), nullable=False)
	
	#Number of VMs running on the host
	running_vms = Column(Integer, nullable=True)

	#Hostname
	hostname = Column(Text, nullable=False)

	# #List of supported instances
	# supported_instances = Column(Text(), nullable=True)

class ExistingIdError(Exception):
	def __init__(self, existingId):
		self.existingId = existingId
	def __str__(self):
		return repr("Entity with id %d already exists" % self.existingId)
		

#CRUD Operations

def create(id, vcpus, memory_mb, local_gb, hostname):

	#Opens the DB session
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	#Checks if the id already exists
	q = session.query(Host).filter(Host.id == id)
	if session.query(q.exists()):
		raise ExistingIdError(id)

	#Adds the new host and commits
	new_host = Host(id=id, vcpus=vcpus, memory_mb=memory_mb, local_gb=local_gb, vcpus_used=0, local_gb_used=0, memory_mb_used=0, running_vms=0, hostname=hostname)
	session.add(new_host)
	session.commit()

def remove():
	pass
	

def update():
	pass

def delete():
	pass

def db_init():
	""""Creates the DB"""
	engine = create_engine('sqlite:///compute_node.db')
	Base.metadata.create_all(engine)


def db_populate():
	"""Populates the DB"""
	try:
		create(2,8,1024,60,"compute1")
	except ExistingIdError as e:
		print e


if __name__ == '__main__':
	db_init()
	db_populate()



