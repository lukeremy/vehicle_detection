import sqlite3

class vehicleDB:
    def __init__(self, sql_file):
        conn = sqlite3.connect(sql_file)
        self.c = conn.cursor()

    def createTable(self):
        print "test"
