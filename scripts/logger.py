import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Ensure the 'logs' directory exists
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(logs_dir, exist_ok=True)

error_handler = logging.FileHandler(os.path.join(logs_dir, 'error.log'))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

info_handler = logging.FileHandler(os.path.join(logs_dir, 'info.log'))
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(error_handler)
logger.addHandler(info_handler)
logger.addHandler(stream_handler)