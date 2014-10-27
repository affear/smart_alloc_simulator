from sim.nova.compute import rpcapi

class _Command(object):
	'''
		The abstract command interface
	'''
	name = 'abstract command'

	def execute(self):
		print 'executing ' + self.name

	class Meta:
		abstract = True

#concrete implementations
class CreateCommand(_Command):
	name = 'boot'

class TerminateCommand(_Command):
	name = 'down'

class ResizeCommand(_Command):
	name = 'resize'