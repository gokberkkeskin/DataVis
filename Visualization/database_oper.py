import glob
import sqlite3 as sl

import pandas as pd

con1 = sl.connect('../DataProcess/platform-1.db')
con2 = sl.connect('../DataProcess/platform-2.db')

def prepare_db():
    with con1:
        con1.execute("""
            CREATE TABLE IF NOT EXISTS TBL_REPORT_COUNTS (
                REPORT_NAME TEXT NOT NULL,
                PROCESS_NAME TEXT NOT NULL,
                COUNT INTEGER
            );
        """)

    with con2:
        con2.execute("""
            CREATE TABLE IF NOT EXISTS TBL_REPORT_COUNTS (
                REPORT_NAME TEXT NOT NULL,
                PROCESS_NAME TEXT NOT NULL,
                COUNT INTEGER
            );
        """)


def fill_sample_data():
    sql1 = 'INSERT INTO TBL_REPORT_COUNTS (REPORT_NAME, PROCESS_NAME, COUNT) values(?, ?, ?)'
    data1 = [
        ('REPORT 1', 'PROCESS 2', 19546),
        ('REPORT 2', 'PROCESS 2', 1345),
        ('REPORT 3', 'PROCESS 3', 50)
    ]

    with con1:
        con1.executemany(sql1, data1)

    sql2 = 'INSERT INTO TBL_REPORT_COUNTS (REPORT_NAME, PROCESS_NAME, COUNT) values(?, ?, ?)'
    data2 = [
        ('REPORT 1', 'PROCESS 2', 19549),
        ('REPORT 2', 'PROCESS 2', 1345),
        ('REPORT 3', 'PROCESS 3', 5905)
    ]

    with con2:
        con2.executemany(sql2, data2)

def list_databases():
    search_path = '../DataProcess/'
    files = glob.glob(search_path + '*.db', recursive=False)

    linux_style_files = []

    for f in files:
        linux_style_filename = f.replace('\\', '/')
        linux_style_files.append([linux_style_filename, linux_style_filename.partition('../DataProcess/')[2]])

    df = pd.DataFrame(linux_style_files)
    df.columns = ["DB_PATH", "DB_NAME"]
    return df

def list_tables(db_path):
    con_db1 = sl.connect(db_path)

    with con_db1:
        data = con2.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return data



if __name__ == "__main__":
    prepare_db()
    fill_sample_data()

    with con1:
        data = con1.execute("SELECT * FROM TBL_REPORT_COUNTS")
        for row in data:
            print(row)

    with con2:
        data = con2.execute("SELECT * FROM TBL_REPORT_COUNTS")
        for row in data:
            print(row)

    print(list_databases())



    I=0
    #
    # print(files)

