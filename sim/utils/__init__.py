HISTORY_FILE = 'sim_history.json'

import logging

LOG_FILE = 'sim.log'

logger = logging.getLogger('sim')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler = logging.FileHandler(LOG_FILE, mode='w')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)