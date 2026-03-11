import sqlite3

conn = sqlite3.connect("monitor.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents(
id INTEGER PRIMARY KEY AUTOINCREMENT,
bot TEXT,
time TEXT
)
""")

conn.commit()


def add_incident(bot):

    cursor.execute(
        "INSERT INTO incidents(bot,time) VALUES (?,datetime('now'))",
        (bot,)
    )

    conn.commit()


def get_incidents():

    cursor.execute(
        "SELECT bot,time FROM incidents ORDER BY id DESC LIMIT 20"
    )

    return cursor.fetchall()