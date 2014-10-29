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

	def __repr__(self):

		return "{\nhostname : %s\n vcpus : %d/%d\n memory_mb : %d/%d\n local_gb : %d/%d\n running_vms : %d\n}" % (self.hostname, self.vcpus_used, self.vcpus,self.memory_mb_used,self.memory_mb,self.local_gb_used,self.local_gb,self.running_vms)


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
		
class MissingIdError(Exception):
	def __init__(self, missingId):
		self.missingId = missingId
	def __str__(self):
		return repr("Entity with id %d doesn't exist" % self.missingId)

def _open_session():
	"""Opens and returns the DB session"""
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

#CRUD Operations

def create(id, vcpus, memory_mb, local_gb, hostname):

	session = _open_session()

	#Checks if the id already exists
	if session.query(Host).filter(Host.id == id).count() > 0:
		raise ExistingIdError(id)
	else:
		#Adds the new host and commits
		new_host = Host(id=id, vcpus=vcpus, memory_mb=memory_mb, local_gb=local_gb, vcpus_used=0, local_gb_used=0, memory_mb_used=0, running_vms=0, hostname=hostname)
		session.add(new_host)
		session.commit()
		return new_host

def get(id):
	
	session = _open_session()

	#Checks if the id already exists
	host = session.query(Host).filter(Host.id == id).one()
	if not host:
		raise MissingIdError(id)
	else:
		return host
	
def get_all():

	session = _open_session()

	hosts = session.query(Host).all()
	return hosts

def update(id, **kwargs):
		
	session = _open_session()

	#Checks if the id already exists
	host = session.query(Host).filter(Host.id == id).all()
	if not host:
		raise MissingIdError(id)
	else:
		session.query(Host).filter(Host.id == id).update(kwargs)
		session.commit()



def delete(id):
	
	session = _open_session()

	if session.query(Host).filter(Host.id == id).delete() == 0:
		raise MissingIdError(id)
	else:
		session.commit()

def db_init():
	""""Creates the DB"""
	engine = create_engine('sqlite:///compute_node.db')
	Base.metadata.create_all(engine)


def db_populate():
	"""Populates the DB"""
	try:
		create(1,8,1024,60,"compute1")
		create(2,12,8000,160,"compute2")
		create(3,8,16000,120,"compute3")
		create(4,8,8000,60,"compute4")
		create(5,12,8000,100,"compute5")
		create(6,8,1024,60,"compute6")
	except Exception as e:
		print e


if __name__ == '__main__':
	db_init()
	db_populate()



