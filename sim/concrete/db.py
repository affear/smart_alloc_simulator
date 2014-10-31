from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext	.declarative import declarative_base
from sqlalchemy.orm import sessionmaker	
from sqlalchemy import create_engine
from contextlib import contextmanager

DB_FILE_NAME = 'compute_node.db'

Base = declarative_base()

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

	def _create(self, session, id, vcpus, memory_mb, local_gb, hostname):

		if session.query(Host).filter(Host.id == id).count() > 0:
			raise ExistingIdError(id)
		else:
			#Adds the new host and commits
			new_host = Host(id=id, vcpus=vcpus, memory_mb=memory_mb, local_gb=local_gb, vcpus_used=0, local_gb_used=0, memory_mb_used=0, running_vms=0, hostname=hostname)
			session.add(new_host)
			session.commit()
			return new_host	

	def _get(self, session, id):

		#Checks if the id already exists
		host = session.query(Host).filter(Host.id == id).one()

		if not host:
			raise MissingIdError(id)
		else:
			return host

	def _get_all(self, session):

		hosts = session.query(Host).all()
		return hosts

	def _update(self, session, id, **kwargs):
		
		#Checks if the id already exists
		host = session.query(Host).filter(Host.id == id).all()
		if not host:
			raise MissingIdError(id)
		else:
			updated_host = session.query(Host).filter(Host.id == id).update(kwargs)
			session.commit()
			return updated_host

	def _delete(self, session, id):
	
		if session.query(Host).filter(Host.id == id).delete() == 0:
			raise MissingIdError(id)
		else:
			session.commit()


#CRUD Operations

def create_host(id, vcpus, memory_mb, local_gb, hostname):

	with session_scope() as session:
		Host()._create(session, id, vcpus, memory_mb, local_gb, hostname)

@contextmanager
def get_host(id):
	host = None
	
	with session_scope() as session:
		yield Host()._get(session, id)
@contextmanager	
def get_all_hosts():

	with session_scope() as session:
		yield Host()._get_all(session)

def update_host(id, **kwargs):
		
	with session_scope() as session:
		Host()._update(session, id, **kwargs)

def delete_host(id):

	with session_scope() as session:
		Host()._delete(session, id)


#Exceptions

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


@contextmanager
def session_scope():
	engine = create_engine('sqlite:///' + DB_FILE_NAME)
	Session = sessionmaker(bind=engine)
	session = Session()

	try:
		yield session
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()