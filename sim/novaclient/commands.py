from sim.nova.compute import rpcapi

class _Command(object):
	"""docstring for Command"""

	def execute(self):
		print "executing " + self.name

	class Meta:
		abstract = True

class CreateCommand(_Command):
	name = 'boot'

class TerminateCommand(_Command):
	name = 'down'

class ResizeCommand(_Command):
	name = 'resize'

class LiveMigrateCommand(_Command):
	name = 'migrate'

#exporting the list of commands
import sys
import inspect

def _filter_command_fn(obj):
	return inspect.isclass(obj) and not obj.__name__.startswith('_') and obj.__name__.endswith('Command')

CMDS = {}
for name, cs in inspect.getmembers(sys.modules[__name__], _filter_command_fn):
	CMDS[name.lower()[:(len(name)-len('Command'))]] = cs()