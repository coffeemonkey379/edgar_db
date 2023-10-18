import os

from edgar_db import collect_edgar, load_engine_url, build_cache

# Stored username & password in environment variables
username, password = os.environ.get("LOCAL_DB").split(";")

db_url = load_engine_url(username, password, database="edgar_dev")
build_cache(db_url)

year = 2022
quarter = 4

collect_edgar(year, quarter, db_url)
