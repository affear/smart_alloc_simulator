from peewee import *

db = SqliteDatabase('db_file.db')


class Base(Model):
	class Meta:
		database = db

class Host(Base):
	""""Class that declares the compute_node table which simulates the 
	compute_nodes table in nova db; it includes only fields useful for the simulation.
	"""

	def __repr__(self):

		return "{\nhostname : %s\n vcpus : %d/%d\n memory_mb : %d/%d\n local_gb : %d/%d\n running_vms : %d\n}" % (self.hostname, self.vcpus_used, self.vcpus,self.memory_mb_used,self.memory_mb,self.local_gb_used,self.local_gb,self.running_vms)


	#Base metrics (virtual CPUs, RAM, Disk) with their usage counterpart
	vcpus = IntegerField(default=0)
	memory_mb = IntegerField(default=0)
	local_gb = IntegerField(default=0)
	vcpus_used = IntegerField(default=0)
	memory_mb_used = IntegerField(default=0)
	local_gb_used = IntegerField(default=0)

	#Number of VMs running on the host
	running_vms = IntegerField(default=0)

	#Hostname
	@property
	def hostname(self):
	    return 'compute' + str(self.id)
	

	class Meta:
		database = db


class VM(Base):

	id = IntegerField(primary_key=True)

	flavor = TextField()

	host = ForeignKeyField(Host, related_name='vms')
