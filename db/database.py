import os
import sqlite3
import streamlit as st

# SQLite 연결 생성 함수


@st.cache_resource
def get_connection():
    # 데이터베이스 파일이 존재하지 않는 경우 생성
    if not os.path.exists('main.db'):
        open('main.db', 'a').close()
        os.chmod('main.db', 0o666)  # 파일 권한 설정

    return sqlite3.connect('main.db', check_same_thread=False)

# 데이터베이스 초기화


def init():
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS CaseInfo(UUID text, Summary text, AgreeList text, Person1 text, sender text);")
    con.commit()

# 데이터 삽입


def insert(uuid, summary, agree_list, person1, sender):
    con = get_connection()
    cur = con.cursor()
    cur.execute('INSERT INTO CaseInfo VALUES(?, ?, ?, ?, ?);',
                (uuid, summary, agree_list, person1, sender))
    con.commit()

# 데이터 조회


def read(uuid):
    con = get_connection()
    cur = con.cursor()
    cur.execute('SELECT * FROM CaseInfo WHERE UUID = ? LIMIT 1', (uuid,))
    return cur.fetchone()
