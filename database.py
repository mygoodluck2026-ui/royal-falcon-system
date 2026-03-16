import sqlite3

conn=sqlite3.connect("shipments.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS shipments(
code TEXT PRIMARY KEY,
origin TEXT,
destination TEXT,
location TEXT,
status TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
code TEXT,
location TEXT,
status TEXT
)
""")

conn.commit()
conn.close()
