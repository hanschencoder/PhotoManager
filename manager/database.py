import sqlite3
import os


class PhotoRecord:

    def __init__(self, path, size, md5):
        self.path = path
        self.size = size
        self.md5 = md5


SQL3_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS photo(
    _id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    size INTEGER,
    md5 TEXT
)
"""


def connect(baseDir):
    dbDir = f'{baseDir}/.database'
    dbFile = f'{dbDir}/photo.db'
    if not os.path.exists(dbDir):
        os.makedirs(dbDir)
    connect = sqlite3.connect(dbFile)
    cursor = connect.cursor()
    cursor.execute(SQL3_CREATE_TABLE)
    connect.commit()
    return connect


def close(connect):
    connect.commit()
    connect.close()


def queryBySize(connect, size):
    cmd = f'SELECT path, size, md5 FROM photo WHERE size={size}'
    cursor = connect.cursor()
    cursor.execute(cmd)
    result = []
    for row in cursor.execute(cmd):
        record = PhotoRecord(row[0], row[1], row[2])
        result.append(record)
    return result


def insertRecord(connect, path, size, md5):
    cmd = f'INSERT INTO photo(path, size, md5) VALUES(\'{path}\', {size}, \'{md5}\')'
    cursor = connect.cursor()
    cursor.execute(cmd)
    connect.commit()


def deleteRecord(connect, record):
    cmd = f'DELETE FROM photo WHERE path=\'{record.path}\' AND size={record.size} AND md5=\'{record.md5}\''
    cursor = connect.cursor()
    cursor.execute(cmd)
    connect.commit()
