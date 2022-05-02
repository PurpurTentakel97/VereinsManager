# Purpur Tentakel
# Spielewiese 1
# Python 3.10

from datetime import datetime
from config import config_sheet as c

c.create_config()

print(c.config.date_format['long_save'])

print(datetime.strftime(datetime.now(), c.config.date_format['long_save']))

print(len(datetime.strftime(datetime.now(), c.config.date_format['long_save'])))
