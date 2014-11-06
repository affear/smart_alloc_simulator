from oslo.config import cfg
from sim.nova import METRICS, FLAVORS
from sim.utils.log_utils import setup_logger
from sets import Set
import logging, memcache, pickle

CONF = cfg.CONF
CONF.import_group('concrete', 'sim.concrete')

_CACHE = memcache.Client(['127.0.0.1:11211'], debug=0)

# logging
setup_logger('db', CONF.logs.db_log_file)
logger = logging.getLogger('db')

class VMNotFoundException(Exception):
	pass
# methods to access cache
def _get(key):
	try:
		return pickle.loads(_CACHE.get(key))
	except:
		raise VMNotFoundException('Could not get {}'.format(key))

def _set(key, obj):
	_CACHE.set(key, pickle.dumps(obj))

def _delete(key):
	_CACHE.delete(key)

class BaseCachedObject(object):
	@classmethod
	def _get_key(cls, id):
		return '#'.join([cls.__name__, str(id)])

	@property
	def key(self):
			return type(self)._get_key(self.id)
	
	@classmethod
	def get(cls, id):
		return _get(cls._get_key(id))

	def save(self, created=False):
		_set(self.key, self)
		self.post_save(created)

	def delete(self):
		_delete(self.key)

	def reload(self):
		return type(self).get(self.id)

	def post_save(self, created=False):
		'''
			Hook on save mathod
		'''
		pass

class Host(BaseCachedObject):
	'''
		Class that declares the compute_node table which simulates the 
		compute_nodes table in nova db; it includes only fields useful for the simulation.
	'''

	def __repr__(self):
		s = '''

				hostname: {},
				vcpus: {}/{},
				memory_mb: {}/{},
				local_gb: {}/{},
				running_vms: {},
				kxvcpu: {},
				vms: {}
		'''
		return s.format(
			self.hostname,
			self.vcpus_used,
			self.vcpus,
			self.memory_mb_used,
			self.memory_mb,
			self.local_gb_used,
			self.local_gb,
			self.running_vms,
			self.kxvcpu,
			' '.join(self.vms)
		)

	#Base metrics (virtual CPUs, RAM, Disk) with their usage counterpart
	#vcpus = 0
	#memory_mb = 0
	#local_gb = 0
	#vcpus_used = 0
	#memory_mb_used = 0
	#local_gb_used = 0

	#fake consumption
	#kxvcpu = 0

	def __init__(self, id=0, vcpus=0, memory_mb=0, local_gb=0, kxvcpu=0):
		super(Host, self).__init__()
		self.id = id
		self.vcpus = vcpus
		self.memory_mb = memory_mb
		self.local_gb = local_gb
		self.kxvcpu = kxvcpu

		self.vms = Set()
		self.vcpus_used = 0
		self.memory_mb_used = 0
		self.local_gb_used = 0

	#Number of VMs running on the host
	@property
	def running_vms(self):
			return len(self.vms)
	
	#Hostname
	@property
	def hostname(self):
		return 'compute' + str(self.id)

	def post_save(self, created=False):
		if created:
			_add_host(self.key)

	def stats_up(self, flavor):
		assert self.vcpus_used + flavor[METRICS.VCPU] <= self.vcpus
		assert self.memory_mb_used + flavor[METRICS.RAM] <= self.memory_mb
		assert self.local_gb_used + flavor[METRICS.DISK] <= self.local_gb

		self.vcpus_used += flavor[METRICS.VCPU]
		self.memory_mb_used += flavor[METRICS.RAM]
		self.local_gb_used += flavor[METRICS.DISK]
		return self

	def stats_down(self, flavor):
		assert self.vcpus_used - flavor[METRICS.VCPU] >= 0
		assert self.memory_mb_used - flavor[METRICS.RAM] >= 0
		assert self.local_gb_used - flavor[METRICS.DISK] >= 0

		self.vcpus_used -= flavor[METRICS.VCPU]
		self.memory_mb_used -= flavor[METRICS.RAM]
		self.local_gb_used -= flavor[METRICS.DISK]
		return self

	@staticmethod
	def get_all():
		h_keys = _get(ALL_HOSTS_KEY)
		return [_get(key) for key in h_keys]

class VM(BaseCachedObject):
	#flavor = FLAVORS.TINY
	#_host_id = None

	def __init__(self, id=0, flavor=FLAVORS.TINY, host=None):
		super(VM, self).__init__()
		self.id = id
		self.flavor = flavor
		self.host = host
		if host:
			self._host_id = host.id

	@property
	def host(self):
		# we always recharge the host... we could cache it
		# this is way you will find things like:
		# h = self.host, because we don't want
		# to invoke self.host too many times
		return Host.get(self._host_id)
	@host.setter
	def host(self, h):
		h.vms.add(self.key)
		h.save()
		self._host_id = h.id
	
	def __repr__(self):
		return 'flavor: %s, host_id: %d' % (self.flavor['name'], self._host_id)

	def post_save(self, created=False):
		if created:
			self.host.stats_up(self.flavor).save()

	def move(self, new_flavor, new_host):
		old_host = self.host

		if old_host.id == new_host.id:
			#this is a local migration!
			old_host.stats_down(self.flavor).stats_up(new_flavor).save()
		else:
			#live migrate:
			#remove from current host
			old_host.vms.remove(self.key)
			old_host.stats_down(self.flavor).save()
			#add to new host
			new_host.vms.add(self.key)
			new_host.stats_up(new_flavor).save()

		#update self
		self.flavor = new_flavor
		self._host_id = new_host.id
		self.save()

	def terminate(self):
		h = self.host
		h.vms.remove(self.key)
		h.stats_down(self.flavor).save()
		self.delete()

def log_stats():
	'''
		Prints the current status of the hosts
	'''
	logger.info(Host.get_all())

def get_snapshot():
	'''
		Returns a tuple of total consumption and number of pms
		at the moment the function is called (k, no_pms).
		The consumption is calculated multiplying the consumption per vcpu by
		vcpus currently used.
	'''
	active_hosts = filter(lambda h: h.running_vms > 0, Host.get_all())
	no_pms = len(active_hosts)
	def reduce_fn(accum, host):
		accum += host.vcpus_used * host.kxvcpu
		return accum
	k = reduce(reduce_fn, active_hosts, 0)
	return k, no_pms


def init_db():
	i = 0
	for pm in CONF.concrete.pms:
		try:
			h = Host(
				id=i,
				vcpus=pm[METRICS.VCPU],
				memory_mb=pm[METRICS.RAM],
				local_gb=pm[METRICS.DISK],
				kxvcpu=pm[METRICS.KXVCPU]
			)
			h.save(created=True)
			i += 1
			logger.info(h.hostname + ' pm created')
		except Exception as e:
			logger.error(e)

#TODO very unefficient
def _add_host(key):
	_HOSTS = _get(ALL_HOSTS_KEY)
	_HOSTS.add(key)
	_set(ALL_HOSTS_KEY, _HOSTS)

# a way to store all hosts keys to later get them
ALL_HOSTS_KEY = 'all_hosts'
try:
	_HOSTS = _get(ALL_HOSTS_KEY)
	if not _HOSTS: raise
except:
	_HOSTS = Set()
	_set(ALL_HOSTS_KEY, _HOSTS)
	init_db()