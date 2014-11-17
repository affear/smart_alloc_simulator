from sim.nova.compute import rpcapi

## This command should ideally be run every time
## someone calls a command using novaclient and nova-api service,
## but we run it here, because we do not have nova-api
from sim import config
config.init_conf()

class _Command(object):
	'''
		The abstract command interface
	'''
	name = 'abstract command'

	def __init__(self):
		self.compute_rpcapi = rpcapi.ComputeTaskAPI()

	def execute(self, smart=False):
		raise NotImplementedError

	class Meta:
		abstract = True

#concrete implementations
class CreateCommand(_Command):
	name = 'boot'

	def __init__(self, flavor, id):
		super(CreateCommand, self).__init__()
		self.flavor = flavor
		self.id = id

	def execute(self, smart=False):
		self.compute_rpcapi.build_instance(flavor=self.flavor, id=self.id, smart=smart)

class TerminateCommand(_Command):
	name = 'down'

	def __init__(self, id):
		super(TerminateCommand, self).__init__()
		self.id = id

	def execute(self, smart=False):
		self.compute_rpcapi.delete(id=self.id, smart=smart)

class ResizeCommand(_Command):
	name = 'resize'

	def __init__(self, flavor, id):
		super(ResizeCommand, self).__init__()
		self.flavor = flavor
		self.id = id

	def execute(self, smart=False):
		self.compute_rpcapi.resize(id=self.id, flavor=self.flavor, smart=smart)
