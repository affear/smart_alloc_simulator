# The real simulation
if __name__ == '__main__':
	HISTORY_FILE = 'sim_history.json'
	from sim.utils import log_utils
	from sim.utils.sim_file_gen import CMDS 
	import json
	import logging

	cmds_list = []
	with open(HISTORY_FILE, 'r') as f:
		data = json.load(f)
		#TODO use cfg to create PMs and so on so forth
		def mapping_fn(cmd_string):
			keyword = cmd_string.split(' ')[0]
			return CMDS[keyword]().get_concrete_command(cmd_string)

		cmds_list = map(mapping_fn, data)

	def do_sim():
		for cmd in cmds_list:
			cmd.execute()

	log_utils.setup_logger('sim', log_utils.SIM_LOG_FILE)
	logger = logging.getLogger('sim')

	logger.info('Simulation started')
	do_sim()
	logger.info('Simulation ended')
	print 'Simulation ended! Read logs for details'