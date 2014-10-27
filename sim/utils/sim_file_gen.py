"""
	Run this script to generate a random the simulation file
"""
from sim.novaclient import commands
import random

NUM_T = 10
MAX_OPS_PER_T = 5
COMMANDS = commands.CMDS

cmds_history = {
	'history': [],
	'opt_cfg': 'optional'
}

if __name__ == '__main__':
	for t in xrange(NUM_T):
		t_dict = {}
		num_ops = random.randint(0, MAX_OPS_PER_T)
		cmd_list = [random.choice(COMMANDS.values()).name for x in xrange(num_ops)]
		k = 't%d' % t
		t_dict[k] = cmd_list
		cmds_history['history'].append(t_dict)
		
	print cmds_history
