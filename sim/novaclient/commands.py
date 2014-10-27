from sim.nova.compute import rpcapi

class _Command(object):
	'''
		The abstract command interface
	'''
	name = 'abstract command'

	def execute(self):
		print 'executing ' + self.name

	def _gen_command(self, *args):
		cmd = ' '.join(['nova', self.name])
		for arg in args:
			cmd = ' '.join([cmd, str(arg)])
		return cmd

	def execute_virtual(self, vms):
		'''
			Generates and virtually executes
			a complete and random command
			starting from the virtual status.
			It returns the command executed.
			Such as:
				nova boot tiny
				nova terminate 42
		'''
		return self.name

	class Meta:
		abstract = True

#concrete implementations
import random
import sim.nova
class CreateCommand(_Command):
	name = 'boot'

	def execute_virtual(self, vms):
		flavor = random.choice(sim.nova.FLAVOR_LIST)
		vms.append(flavor)
		return self._gen_command(flavor['name']) 

class TerminateCommand(_Command):
	name = 'down'

	def execute_virtual(self, vms):
		vm_index = random.randint(0, len(vms) - 1)
		vms.pop(vm_index)
		return self._gen_command(vm_index)

class ResizeCommand(_Command):
	name = 'resize'

	def execute_virtual(self, vms):
		new_flavor = random.choice(sim.nova.FLAVOR_LIST)
		vm_index = random.randint(0, len(vms) - 1)
		vms[vm_index] = new_flavor
		return self._gen_command(vm_index, new_flavor['name'])

#exporting the list of commands as
# {
#		cmd_name: Class,
#		...
# }
import sys
import inspect

def _filter_command_fn(obj):
	return inspect.isclass(obj) and not obj.__name__.startswith('_') and obj.__name__.endswith('Command')

CMDS = {}
for name, cs in inspect.getmembers(sys.modules[__name__], _filter_command_fn):
	CMDS[name.lower()[:(len(name)-len('Command'))]] = cs