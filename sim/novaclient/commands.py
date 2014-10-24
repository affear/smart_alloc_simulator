from sim.nova.compute import rpcapi

class _Command(object):
	"""docstring for Command"""

	def execute(self):
		print "executing " + self.name

	class Meta:
		abstract = True

class CreateCommand(_Command):
	name = 'boot'
