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

	def __init__(self, flavor, id):
		super(CreateCommand, self).__init__()
		self.flavor = flavor
		self.id = id

	def execute(self):
		super(CreateCommand, self).execute()
		print ' '.join(['-->', self.flavor['name'], str(self.id)])

class TerminateCommand(_Command):
	name = 'down'

	def __init__(self, id):
		super(TerminateCommand, self).__init__()
		self.id = id

	def execute(self):
		super(TerminateCommand, self).execute()
		print ' '.join(['-->', str(self.id)])

class ResizeCommand(_Command):
	name = 'resize'

	def __init__(self, flavor, id):
		super(ResizeCommand, self).__init__()
		self.flavor = flavor
		self.id = id

	def execute(self):
		super(ResizeCommand, self).execute()
		print ' '.join(['-->', self.flavor['name'], str(self.id)])