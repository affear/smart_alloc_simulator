HISTORY_FILE = 'sim_history.json'

import logging

LOG_FILE = 'sim.log'

l = logging.getLogger('sim')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler = logging.FileHandler(LOG_FILE, mode='w')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

l.setLevel(logging.INFO)
l.addHandler(fileHandler)
l.addHandler(streamHandler)