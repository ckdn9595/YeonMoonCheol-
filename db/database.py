import sqlite3

# SQLite 연결 생성 함수
@st.experimental_singleton
def get_connection():
    return sqlite3.connect('./main.db', check_same_thread=False)

# 데이터베이스 초기화


def init():
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS CaseInfo(UUID text, Summary text, AgreeList text, Person1 text, Person2 text);")
    con.commit()

# 데이터 삽입


def insert(uuid, summary, agree_list, person1, person2):
    con = get_connection()
    cur = con.cursor()
    cur.execute('INSERT INTO CaseInfo VALUES(?, ?, ?, ?, ?);',
                (uuid, summary, agree_list, person1, person2))
    con.commit()

# 데이터 조회


def read(uuid):
    con = get_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM CaseInfo WHERE UUID = ? LIMIT 1', (uuid,))
    return cur.fetchone()
