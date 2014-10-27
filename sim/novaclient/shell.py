from sim.novaclient import commands
import sys
import inspect

def _filter_command_fn(obj):
	return inspect.isclass(obj) and not obj.__name__.startswith('_') and obj.__name__.endswith('Command')

CMDS = {}
for name, cs in inspect.getmembers(commands, _filter_command_fn):
	CMDS[name.lower()[:(len(name)-len('Command'))]] = cs()