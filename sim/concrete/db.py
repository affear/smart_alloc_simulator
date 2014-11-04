from peewee import *
from oslo.config import cfg
from sim.nova import METRICS
CONF = cfg.CONF
CONF.import_group('concrete', 'sim.concrete')

db = SqliteDatabase(CONF.concrete.db_file, fields={'json': 'json'})

# logging
from sim.utils.log_utils import setup_logger
import logging
setup_logger('db', CONF.logs.db_log_file)
logger = logging.getLogger('db')

def log_stats():
	'''
		Prints the current status of the hosts
	'''
	logger.info(list(Host.select()))

class Base(Model):
	class Meta:
		database = db

class Host(Base):
	'''
		Class that declares the compute_node table which simulates the 
		compute_nodes table in nova db; it includes only fields useful for the simulation.
	'''

	def __repr__(self):
		return "{\nhostname : %s\n vcpus : %d/%d\n memory_mb : %d/%d\n local_gb : %d/%d\n running_vms : %d\n}" \
			% (
				self.hostname,
				self.vcpus_used,
				self.vcpus,
				self.memory_mb_used,
				self.memory_mb,
				self.local_gb_used,
				self.local_gb,
				self.running_vms
			)


	#Base metrics (virtual CPUs, RAM, Disk) with their usage counterpart
	vcpus = IntegerField(default=0)
	memory_mb = IntegerField(default=0)
	local_gb = IntegerField(default=0)
	vcpus_used = IntegerField(default=0)
	memory_mb_used = IntegerField(default=0)
	local_gb_used = IntegerField(default=0)

	#Number of VMs running on the host
	@property
	def running_vms(self):
		return self.vms.count()

	#Hostname
	@property
	def hostname(self):
		return 'compute' + str(self.id)

	def stats_up(self, flavor):
		assert self.vcpus_used + flavor[METRICS.VCPU] <= self.vcpus
		assert self.memory_mb_used + flavor[METRICS.RAM] <= self.memory_mb
		assert self.local_gb_used + flavor[METRICS.DISK] <= self.local_gb

		self.vcpus_used += flavor[METRICS.VCPU]
		self.memory_mb_used += flavor[METRICS.RAM]
		self.local_gb_used += flavor[METRICS.DISK]
		self.save()

	def stats_down(self, flavor):
		assert self.vcpus_used - flavor[METRICS.VCPU] >= 0
		assert self.memory_mb_used - flavor[METRICS.RAM] >= 0
		assert self.local_gb_used - flavor[METRICS.DISK] >= 0

		self.vcpus_used -= flavor[METRICS.VCPU]
		self.memory_mb_used -= flavor[METRICS.RAM]
		self.local_gb_used -= flavor[METRICS.DISK]
		self.save()

#accessor field
import json
class JSONField(Field):
	db_field = 'json'

	def db_value(self, value):
		return json.dumps(value)

	def python_value(self, value):
		return json.loads(value)


class VM(Base):
	id = IntegerField(primary_key=True)
	flavor = JSONField()
	host = ForeignKeyField(Host, related_name='vms')

	def __repr__(self):
		return 'flavor: %s, host_id: %d' % (self.flavor['name'], self.host.id)

	def prepared(self):
		self.host.stats_up(self.flavor)

	def move(self, new_flavor, new_host):
		self.host.stats_down(self.flavor)
		self.flavor = new_flavor
		self.host = new_host
		self.host.stats_up(self.flavor)
		self.save()

	def terminate(self):
		self.host.stats_down(self.flavor)
		self.delete_instance()

if __name__ == "__main__":
	from sim.utils import log_utils
	import logging

	# Create DB
	db.create_tables([Host, VM], True)

	log_utils.setup_logger('db', CONF.logs.db_log_file)
	logger = logging.getLogger('db')

	#Populates the db with PM
	# This is much faster
	with db.transaction():
		for pm in CONF.concrete.pms:
			try:
				Host.create(
					vcpus=pm[METRICS.VCPU],
					memory_mb=pm[METRICS.RAM],
					local_gb=pm[METRICS.DISK]
				)
			except Exception as e:
				logger.error(e)

	for h in Host.select():
		print h
