# configure logging
import logging

LOG_FILE='compute.log'

logger = logging.getLogger('compute')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler = logging.FileHandler(LOG_FILE, mode='w')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)