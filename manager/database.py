import sqlite3
import os

SQL3_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS photo(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    size INTEGER,
    md5 TEXT
)
"""


class PhotoRecord:
    def __init__(self, path, size, md5):
        self.path = path
        self.size = size
        self.md5 = md5


class DatabaseManager:

    connect = None

    @classmethod
    def createManager(cls, baseDir):
        return DatabaseManager(baseDir)

    def __init__(self, baseDir):
        self.baseDir = baseDir

    def connectDB(self):
        if self.connect is not None:
            print("oops")
            return

        dbDir = f'{self.baseDir}/.database'
        dbFile = f'{dbDir}/photo.db'
        if not os.path.exists(dbDir):
            os.makedirs(dbDir)
        self.connect = sqlite3.connect(dbFile)
        cursor = self.connect.cursor()
        cursor.execute(SQL3_CREATE_TABLE)
        self.connect.commit()

    def closeDB(self):
        if self.connect is None:
            return

        self.connect.commit()
        self.connect.close()
        self.connect = None

    def queryBySize(self, size):
        if self.connect is None:
            return []

        cmd = f'SELECT path, size, md5 FROM photo WHERE size={size}'
        cursor = self.connect.cursor()
        cursor.execute(cmd)
        result = []
        for row in cursor.execute(cmd):
            record = PhotoRecord(row[0], row[1], row[2])
            result.append(record)
        return result

    def insertRecord(self, path, size, md5):
        if self.connect is None:
            return

        cmd = f'INSERT INTO photo(path, size, md5) VALUES(\'{path}\', {size}, \'{md5}\')'
        cursor = self.connect.cursor()
        cursor.execute(cmd)
        self.connect.commit()

    def deleteRecord(self, record):
        if self.connect is None:
            return

        cmd = f'DELETE FROM photo WHERE path=\'{record.path}\' AND size={record.size} AND md5=\'{record.md5}\''
        cursor = self.connect.cursor()
        cursor.execute(cmd)
        self.connect.commit()
