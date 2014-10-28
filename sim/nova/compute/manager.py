from oslo import messaging
from oslo.config import cfg
from sim.nova.compute import logger

class ComputeTaskManager(object):

	def _log_info(self, task_name, *args):
		args = list(args)
		args.insert(0, ':')
		args.insert(0, task_name)
		args.insert(0, 'executing')
		args = map(lambda a: str(a), args)
		logger.info(' '.join(args))

	def build_instance(self, ctx, id, flavor):
		self._log_info('boot', id, flavor['name'])

	def delete(self, ctx, id):
		self._log_info('delete', id)

	def resize(self, ctx, id, flavor):
		self._log_info('resize', id, flavor['name'])

if __name__ == '__main__':
	transport = messaging.get_transport(cfg.CONF)
	target = messaging.Target(topic='compute', server='compute1')
	endpoints = [ComputeTaskManager(), ]
	server = messaging.get_rpc_server(transport, target, endpoints,
																			executor='blocking')
	server.start()
	server.wait()