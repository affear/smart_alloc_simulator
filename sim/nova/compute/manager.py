from oslo import messaging
from oslo.config import cfg
import logging

class ComputeManager(object):
	logger = logging.getLogger('compute')

	def _log_info(self, task_name, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, task_name)
		args.insert(0, 'executing')
		args = map(lambda a: str(a), args)
		self.logger.info(' '.join(args))

	def build_instance(self, ctx, id, flavor):
		self._log_info('boot', id, flavor['name'])

	def delete(self, ctx, id):
		self._log_info('delete', id)

	def resize(self, ctx, id, flavor):
		self._log_info('resize', id, flavor['name'])

if __name__ == '__main__':
	from sim.utils import log_utils
	from sim.nova import rpc
	from sim import config

	# as they do in OpenStack
	config.init_conf()
	CONF = cfg.CONF
	CONF.import_opt('compute_topic', 'sim.nova.compute.rpcapi')
	#CONF.import_opt('compute_log_file', 'sim.utils.log_utils')
	log_utils.setup_logger('compute', CONF.logs.compute_log_file)

	server = rpc.get_server(CONF.compute_topic, [ComputeManager(), ])
	server.start()