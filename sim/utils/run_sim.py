# The real simulation
if __name__ == '__main__':
	from sim.utils import log_utils
	from sim.utils.sim_file_gen import CMDS
	from sim.concrete.db import get_snapshot, VMNotFoundException
	from sim.nova.scheduler.manager import NoDestinationFoundException
	from sim.novaclient import commands
	from sim import db
	from sim import config
	from oslo.config import cfg
	from oslo.messaging import RemoteError
	import json, logging

	config.init_conf()
	CONF = cfg.CONF

	# logging
	log_utils.setup_logger('sim', CONF.logs.sim_log_file)
	logger = logging.getLogger('sim')

	cmds_list = {}
	# getting commands from file and
	# generating a command list of concrete commands
	with open(CONF.sim.ops_file, 'r') as ops:
		data = json.load(ops)
		
		for t in data:
			cmd_string = data[t]
			keyword = cmd_string.split(' ')[0]
			concrete_cmd = CMDS[keyword]().get_concrete_command(cmd_string)
			cmds_list[t] = concrete_cmd

	# this function does the real job.
	# It executes concrete commands and adds
	# a snapshot at every time t
	def do_sim():
		# dict in which we will store the snapshots
		# at every time t
		snapshots = {}
		total = {}
		t_real = 0
		avg_k = 0
		avg_pms = 0
		no_X = 0
		no_boot = 0
		no_resize = 0
		no_delete = 0

		# Some work to handle remote exceptions
		exs = {
			NoDestinationFoundException.__name__: NoDestinationFoundException,
			VMNotFoundException.__name__: VMNotFoundException
		}

		keys = sorted([int(k) for k in cmds_list.keys()])
		for k in keys:
			t = str(k)
			logger.info('t' + t)
			try:
				cmds_list[t].execute()

				if type(cmds_list[t]) == commands.CreateCommand: no_boot += 1
				if type(cmds_list[t]) == commands.ResizeCommand: no_resize += 1
				if type(cmds_list[t]) == commands.TerminateCommand: no_delete += 1

				s = get_snapshot()
				avg_k += s[0]
				avg_pms += s[1]
				snapshots[t_real] = s
			except RemoteError as r:
				try:
					raise exs[r.exc_type](r.value)
				except KeyError:
					# the remote exception is not in the dict
					raise r
				except NoDestinationFoundException:
					snapshots[t_real] = 'X'
					no_X += 1
				except VMNotFoundException:
					# do nothing, but jump the time increment...
					# this op hasn't happened! shhhhhh
					continue
			t_real += 1

		total['t_real'] = t_real
		total['avg_k'] = float(avg_k) / t_real
		total['avg_pms'] = float(avg_pms) / t_real
		total['no_X'] = no_X
		total['no_boot'] = no_boot
		total['no_resize'] = no_resize
		total['no_delete'] = no_delete
		total['snapshots'] = snapshots

		return total

	# start the simulation
	logger.info('Simulation started')
	data = do_sim()
	logger.info('Simulation ended')

	# now that the simulation is complete,
	# we can filter snapshot to generate:
	# - a minimized snapshot history
	#		(which will be interpolated by Google Charts)
	# - the average of statistics

	# first of all, store sim data to db
	session = db.get_session()
	with session.begin():
		simdata = db.SimData(
			avg_consumption=data['avg_k'],
			avg_no_pms=data['avg_pms'],
			no_nodestfound=data['no_X'],
			#smart = Column(Boolean, default=False)
		)
		session.add(simdata)

	# add total metrics to data
	# smart
	data['tot_avg_k_smart'] = db.SimData.get_avg_consumption(smart=True)
	data['tot_avg_pms_smart'] = db.SimData.get_avg_no_pms(smart=True)
	data['tot_avg_x_smart'] = db.SimData.get_avg_nodestfound(smart=True)
	# not smart
	data['tot_avg_k'] = db.SimData.get_avg_consumption()
	data['tot_avg_pms'] = db.SimData.get_avg_no_pms()
	data['tot_avg_x'] = db.SimData.get_avg_nodestfound()

	# dump to file (not minimized)
	with open(CONF.sim.out_file, 'w') as out:
		json.dump(data, out)
	
	#minimize
	STEP = 10
	minimized = {}
	for t in data['snapshots']:
		if t % STEP == 0: minimized[t] = data['snapshots'][t]

	data['snapshots'] = minimized

	# dump to MINIMIZED file
	with open(CONF.sim.out_min_file, 'w') as out_min:
		json.dump(data, out_min)

	print 'Simulation ended! Read logs for details'