# The real simulation
if __name__ == '__main__':
	from sim.utils import log_utils
	from sim.utils.sim_file_gen import CMDS 
	from sim import config
	from oslo.config import cfg
	import json, logging

	config.init_conf()
	CONF = cfg.CONF

	cmds_list = []
	with open(CONF.sim.history_file, 'r') as f:
		data = json.load(f)
		#TODO use cfg to create PMs and so on so forth
		def mapping_fn(cmd_string):
			keyword = cmd_string.split(' ')[0]
			return CMDS[keyword]().get_concrete_command(cmd_string)

		cmds_list = map(mapping_fn, data)

	def do_sim():
		for cmd in cmds_list:
			cmd.execute()

	log_utils.setup_logger('sim', CONF.logs.sim_log_file)
	logger = logging.getLogger('sim')

	logger.info('Simulation started')
	do_sim()
	logger.info('Simulation ended')
	print 'Simulation ended! Read logs for details'