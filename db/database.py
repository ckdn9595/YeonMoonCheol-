import sqlite3

# 전역 연결 객체와 커서 초기화
con = sqlite3.connect('./main.db')
cur = con.cursor()


def init():
    cur.execute(
        "CREATE TABLE IF NOT EXISTS CaseInfo(UUID text, Summary text, AgreeList text, Person1 text, Person2 text);")
    con.commit()


def insert(uuid, summary, agreeList, person1, person2):
    cur.execute('INSERT INTO CaseInfo VALUES(?, ?, ?, ?, ?);',
                (uuid, summary, agreeList, person1, person2))
    con.commit()


def read(uuid):
    cur.execute('SELECT * FROM CaseInfo WHERE UUID = ? LIMIT 1', (uuid,))
    return cur.fetchone()
