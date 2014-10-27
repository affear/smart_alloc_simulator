"""
	Run this script to generate a random the simulation file
"""
from sim.novaclient import commands
import random

NUM_T = 10
NUM_PM = 5
COMMANDS = commands.CMDS

cmds_history = {
	'history': [],
	'cfg': {
		'pms': NUM_PM
		#other configuration parameters
	}
}

status = []

if __name__ == '__main__':
	for t in xrange(NUM_T):
		t_dict = {}
		if len(status) > 0:
			cmd = random.choice(COMMANDS.values())().execute_virtual(status)
		else: #there are no virtual machines... let's spawn one!
			cmd = [COMMANDS['create']().execute_virtual(status), ]
		k = 't%d' % t
		t_dict[k] = cmd
		cmds_history['history'].append(t_dict)

	import json
	with open('sim_history.json', 'w') as out:
		json.dump(cmds_history, out)

	print 'File sim_history.json succesfully generated!'
