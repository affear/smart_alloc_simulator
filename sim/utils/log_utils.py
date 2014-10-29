import logging

COMPUTE_LOG_FILE = 'logs/compute.log'
SCHEDULER_LOG_FILE = 'logs/scheduler.log'

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