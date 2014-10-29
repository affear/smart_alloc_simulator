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
	log_utils.setup_logger('compute', log_utils.COMPUTE_LOG_FILE)

	transport = messaging.get_transport(cfg.CONF)
	target = messaging.Target(topic='compute', server='compute1')
	endpoints = [ComputeManager(), ]
	server = messaging.get_rpc_server(transport, target, endpoints,
																			executor='blocking')
	server.start()
	#server.wait()