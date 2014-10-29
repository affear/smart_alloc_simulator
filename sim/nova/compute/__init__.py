# configure logging
import logging

COMPUTE_LOG_FILE = 'compute.log'
SCHEDULER_LOG_FILE = 'scheduler.log'

def setup_logger(name, file_name):
	logger = logging.getLogger(name)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fileHandler = logging.FileHandler(file_name, mode='w')
	fileHandler.setFormatter(formatter)
	streamHandler = logging.StreamHandler()
	streamHandler.setFormatter(formatter)

	logger.setLevel(logging.INFO)
	logger.addHandler(fileHandler)
	logger.addHandler(streamHandler)


setup_logger('compute', COMPUTE_LOG_FILE)
setup_logger('scheduler', SCHEDULER_LOG_FILE)