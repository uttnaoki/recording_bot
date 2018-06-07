import sqlite3
import os

def initialize_db(dbname, table):
    conn = sqlite3.connect(dbname)
    conn.cursor().execute(table)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    dbdir = 'DB/'
    dbname = dbdir + 'sqlite3.db'

    # DBディレクトリ がなければ作成
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)

    # dbファイル が既にあれば，削除
    if os.path.isfile(dbname):
        os.remove(dbname)

    # sushida の初期化
    table_sushida = '''create table sushida (
                       id verchar(16) PRIMARY KEY,
                       name varchar(32),
                       result int
                       )'''
    initialize_db(dbname, table_sushida)
