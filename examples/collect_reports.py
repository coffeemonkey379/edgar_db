import os
from itertools import product
import logging

from edgar_db import collect_edgar, load_engine_url, build_cache
from edgar_db.logger import LOGGER

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
prompt_handler = logging.StreamHandler()
prompt_handler.setFormatter(formatter)
prompt_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logging.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(prompt_handler)
LOGGER.addHandler(file_handler)


years = range(2013, 2024)
quarters = range(1, 5)
# Stored username & password in environment variables
username, password = os.environ.get("LOCAL_DB").split(";")

db_url = load_engine_url(username, password, database="edgar_dev_extra_types")
build_cache(db_url)

for year, quarter in product(years, quarters):
    try:
        collect_edgar(year, quarter, db_url)
    except:
        pass
