from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext	.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.types import TypeDecorator, VARCHAR
from contextlib import contextmanager
from sim.nova import FLAVORS
from sim.nova import METRICS

DB_FILE_NAME = 'compute_node.db'

Base = declarative_base()

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

import json

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

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

	#Number of VMs running on the host
	running_vms = Column(Integer, nullable=True)

	#Hostname
	hostname = Column(Text, nullable=False)

	vms = relationship('VM')

	@staticmethod
	def create(id, vcpus, memory_mb, local_gb, hostname):

		with session_scope() as session:
			if session.query(Host).filter(Host.id == id).count() > 0:
				raise ExistingIdError(id)
			else:
				#Adds the new host and commits
				new_host = Host(id=id, vcpus=vcpus, memory_mb=memory_mb, local_gb=local_gb, vcpus_used=0, local_gb_used=0, memory_mb_used=0, running_vms=0, hostname=hostname)
				session.add(new_host)
				return new_host	

	@staticmethod
	@contextmanager
	def get(id):

		with session_scope() as session:
			#Checks if the id already exists
			host = session.query(Host).filter(Host.id == id).one()

			if not host:
				raise MissingIdError(id)
			else:
				yield host

	@staticmethod
	@contextmanager
	def get_all():
		with session_scope() as session:
			hosts = session.query(Host).all()
			yield hosts


	@staticmethod
	@contextmanager
	def remove_vm(vm_id):
	
		if session.query(Host).filter(Host.id == id).delete() == 0:
			raise MissingIdError(id)
		else:
			session.commit()


class VM(Base):

	__tablename__ = "vm"

	id = Column(Integer, primary_key=True, autoincrement=False)

	host_id = Column(Integer, ForeignKey('compute_node.id'))

	flavor = Column(JSONEncodedDict(255), nullable=False)

	@staticmethod
	def create(vm_id, flavor, host_id):

		with session_scope() as session:	

			vm = VM(id=vm_id, flavor=flavor)
			
			vm.host_id = host_id				
			session.add(vm)
			return vm


	def move(self, flavor, host_id):

		with session_scope() as session:
			self.host_id = host_id
			self.flavor = flavor				
			session.add(self)
			return self

	@staticmethod
	@contextmanager
	def get(vm_id):

		with session_scope() as session:
			yield session.query(VM).filter(VM.id == vm_id).one()



		


def remove_vm(vm_id):

	with session_scope() as session:
		host = Host()._get(session, host_id)

		new_vcpus_used = host.vcpus_used - flavor[METRICS.VCPU]
		new_memory_gb_used = host.memory_mb_used - flavor[METRICS.RAM]
		new_local_gb_used = host.local_gb_used - flavor[METRICS.DISK]

		Host()._update_host(sessio, host_id, vcpus_used=new_vcpus_used, local_gb_used=new_local_gb_used, memory_mb_used=new_memory_gb_used)

def add_vm_to_host(vm_id, host_id):

	with session_scope() as session:
		host = Host()._get(session, host_id)

		new_vcpus_used = host.vcpus_used + flavor[METRICS.VCPU]
		new_memory_gb_used = host.memory_mb_used + flavor[METRICS.RAM]
		new_local_gb_used = host.local_gb_used + flavor[METRICS.DISK]

		Host()._update_host(sessio, host_id, vcpus_used=new_vcpus_used, local_gb_used=new_local_gb_used, memory_mb_used=new_memory_gb_used)




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

