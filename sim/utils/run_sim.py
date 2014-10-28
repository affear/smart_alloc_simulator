# The real simulation
if __name__ == '__main__':
	import json
	from sim.utils import HISTORY_FILE
	from sim.utils.sim_file_gen import CMDS 
	cmds_list = []
	with open(HISTORY_FILE, 'r') as f:
		data = json.load(f)
		#TODO use cfg to create PMs and so on so forth
		def mapping_fn(cmd_string):
			keyword = cmd_string.split(' ')[0]
			return CMDS[keyword]().get_concrete_command(cmd_string)

		cmds_list = map(mapping_fn, data['history'])

	def do_sim():
		for cmd in cmds_list:
			cmd.execute()

	print "Simulation started"
	do_sim()
	print "Simulation ended"