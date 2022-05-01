# Purpur Tentakel
# Spielewiese 1
# Python 3.10

import sqlite3

connection = sqlite3.connect(database='test.tx')
connection.execute("PRAGMA key = '123456'")
