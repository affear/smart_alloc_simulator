"""
	Run this script to generate a random simulation file
"""
from sim.novaclient import commands

# Virtual classes for commands
class _VirtualCommand(object):
	'''
		The abstract command interface
	'''
	name = 'abstract command'

	def _gen_command(self, *args):
		cmd = self.name
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
		raise NotImplementedError

	def get_concrete_command(self, str_args):
		'''
			returns the concrete command associated with the virtual one
		'''
		raise NotImplementedError

	class Meta:
		abstract = True

import random
import sim.nova
class CreateCommand(_VirtualCommand):
	name = 'boot'

	def execute_virtual(self, status):
		flavor = random.choice(sim.nova.FLAVOR_LIST)
		status['vms'].append(
			{
				'id': status['id'],
				'flavor': flavor
			}
		)
		status['id'] += 1

		return self._gen_command(flavor['name'], status['id'] - 1) 

	def get_concrete_command(self, str_args):
		'''
			cmd structure:
			boot {flavor} {id}
		'''
		args = str_args.split(' ')
		return commands.CreateCommand(
			id=int(args[2]),
			flavor=getattr(sim.nova.FLAVORS, args[1].upper())
		)

class TerminateCommand(_VirtualCommand):
	name = 'down'

	def execute_virtual(self, status):
		vm_index = random.randint(0, len(status['vms']) - 1)
		del_vm = status['vms'].pop(vm_index)
		return self._gen_command(del_vm['id'])

	def get_concrete_command(self, str_args):
		'''
			cmd structure:
			down {id}
		'''
		args = str_args.split(' ')
		return commands.TerminateCommand(id=int(args[1]))

class ResizeCommand(_VirtualCommand):
	name = 'resize'

	def execute_virtual(self, status):
		new_flavor = random.choice(sim.nova.FLAVOR_LIST)
		vm_index = random.randint(0, len(status['vms']) - 1)
		status['vms'][vm_index]['flavor'] = new_flavor
		return self._gen_command(status['vms'][vm_index]['id'], new_flavor['name'])

	def get_concrete_command(self, str_args):
		'''
			cmd structure:
			resize {id} {flavor}
		'''
		args = str_args.split(' ')
		return commands.ResizeCommand(
			id=int(args[1]),
			flavor=getattr(sim.nova.FLAVORS, args[2].upper())
		)

import sys
import inspect
#exporting the list of commands as
# {
#		cmd_name: Class,
#		...
# }
def _filter_command_fn(obj):
		return inspect.isclass(obj) and \
			not obj.__name__.startswith('_') \
			and obj.__name__.endswith('Command')

CMDS = {}
for name, cs in inspect.getmembers(sys.modules[__name__], _filter_command_fn):
	CMDS[cs().name] = cs

#file generation
if __name__ == '__main__':
	NUM_T = 10
	NUM_PM = 5
	
	cmds_history = {
		'history': [],
		'cfg': {
			'pms': NUM_PM
			#other configuration parameters
		}
	}

	status = {
		'id': 0,
		'vms': []
	}

	for t in xrange(NUM_T):
		if len(status['vms']) > 0:
			cmd = random.choice(CMDS.values())().execute_virtual(status)
		else: #there are no virtual machines... let's spawn one!
			cmd = CMDS['boot']().execute_virtual(status)
		cmds_history['history'].append(cmd)

	import json
	from sim.utils import HISTORY_FILE
	with open(HISTORY_FILE, 'w') as out:
		json.dump(cmds_history, out)

	print 'File sim_history.json succesfully generated!'
