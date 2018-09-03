import sqlite3
import os

class Db():
    def __init__(self, dbname):
        self.dbname = dbname
        if os.path.exists("dbs/{0}".format(dbname)):
            self.conn = sqlite3.connect("dbs/" + dbname, isolation_level=None)
        else:
            self.conn = sqlite3.connect("dbs/" + dbname, isolation_level=None)
            self.createTable()

    def createTable(self):
        if self.conn.execute("DROP TABLE IF EXISTS dict;") and self.conn.execute("CREATE TABLE dict(id INTEGER PRIMARY KEY, word TEXT, mean TEXT, othmean TEXT, pron TEXT);"):

            return True
        else:
            return False

    def searchMean(self, word):
        cur = self.conn.cursor()
        word = str(word).strip()
        datas = cur.execute("SELECT * FROM dict WHERE word LIKE ?", (word,)).fetchone()
        if datas is None:
            return False
        return datas

    def insertWord(self, word, mean, othmean, pron):

        if self.conn.execute("INSERT INTO dict(word, mean, othmean, pron) VALUES(?, ?, ?, ?)", (str(word).strip(), str(mean), str(othmean), str(pron))):
            return True
        else:
            return False
