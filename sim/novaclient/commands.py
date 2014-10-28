from sim.nova.compute import rpcapi
import logging

class _Command(object):
	'''
		The abstract command interface
	'''
	name = 'abstract command'

	def execute(self):
		raise NotImplementedError

	def _log_info(self, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, self.name)
		args.insert(0, 'executing')
		args = map(lambda a: str(a), args)
		logging.info(' '.join(args))

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
		self._log_info(self.flavor['name'], self.id)

class TerminateCommand(_Command):
	name = 'down'

	def __init__(self, id):
		super(TerminateCommand, self).__init__()
		self.id = id

	def execute(self):
		self._log_info(self.id)

class ResizeCommand(_Command):
	name = 'resize'

	def __init__(self, flavor, id):
		super(ResizeCommand, self).__init__()
		self.flavor = flavor
		self.id = id

	def execute(self):
		self._log_info(self.flavor['name'], self.id)
