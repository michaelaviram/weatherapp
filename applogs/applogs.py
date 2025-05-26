import logging
from datetime import datetime

current_time = datetime.now()

logging.basicConfig(filename=f'applogs/record-{current_time.strftime("%d-%m-%Y")}.log',
					level=logging.DEBUG,
					format="%(asctime)s %(levelname)s %(message)s")

