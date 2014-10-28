# The real simulation
if __name__ == '__main__':
	from sim.utils import HISTORY_FILE, LOG_FILE
	from sim.utils.sim_file_gen import CMDS 
	import json
	import logging

	# configure logging
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		filemode='w',
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# from now on:
	# import logging
	# logging.whatever('whatever msg')

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

	logging.info('Simulation started')
	do_sim()
	logging.info('Simulation ended')
	print 'Simulation ended! Results in ' + LOG_FILE