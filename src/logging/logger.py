import logging
import os
from datetime import datetime

LOG_FILE = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "_app.log"

LOGPATH = os.path.join(os.getcwd(), 'logs', LOG_FILE)

os.makedirs(os.path.dirname(LOGPATH), exist_ok=True)

logging.basicConfig(
    filename=LOGPATH,
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d - %(name)s - %(levelname)s - %(message)s'
)


