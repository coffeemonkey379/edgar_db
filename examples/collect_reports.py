import os
from itertools import product
import logging

from edgar_db import collect_edgar, load_engine_url, build_cache
from edgar_db.logger import LOGGER

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
prompt_handler = logging.StreamHandler()
prompt_handler.setFormatter(formatter)
prompt_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(prompt_handler)

# Stored username & password in environment variables
username, password = os.environ.get("LOCAL_DB").split(";")

db_url = load_engine_url(username, password, database="edgar_dev")
build_cache(db_url)

year = 2022
quarter = 3

collect_edgar(year, quarter, db_url)

years = range(2014, 2022)
quarters = range(4)
