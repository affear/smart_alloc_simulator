from sim.novaclient import commands
# export simulation configurations
from oslo.config import cfg

sim_group = cfg.OptGroup(name='sim')
sim_opts = [
	cfg.IntOpt(
		name='no_t',
		default=10,
		help='The number of steps of the simulation'
	),
	cfg.StrOpt(
		name='ops_file',
		default='sim.f.ops.json',
		help='The output file of this script'
	),
	cfg.StrOpt(
		name='out_file',
		default='sim.f.out.json',
		help='The output file of the simulation'
	),
	cfg.StrOpt(
		name='out_min_file',
		default='sim.f.out.min.json',
		help='The minified output file of of the simulation'
	),
]
CONF = cfg.CONF
CONF.register_group(sim_group)
CONF.register_opts(sim_opts, sim_group)

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
	CONF(default_config_files=['sim.conf', ])
	NUM_T = CONF.sim.no_t
	
	cmds_history = {}

	status = {
		'id': 0,
		'vms': []
	}

	for t in xrange(NUM_T):
		if len(status['vms']) > 0:
			cmd = random.choice(CMDS.values())().execute_virtual(status)
		else: #there are no virtual machines... let's spawn one!
			cmd = CMDS['boot']().execute_virtual(status)
		cmds_history[t] = cmd

	import json
	with open(CONF.sim.ops_file, 'w') as out:
		json.dump(cmds_history, out)

	print ' '.join(['File', CONF.sim.ops_file, 'succesfully generated!'])