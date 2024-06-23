import sqlite3

def init():
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS CaseInfo(UUID text, Summary text, AgreeList text, Person1, Person2);")
    return cur


def insert(cur, uuid, summary, agreeList, person1, person2):
    con = get_conn()
    cur.execute('INSERT INTO CaseInfo VALUES(?, ?, ?, ?, ?);', 
                (uuid, summary, agreeList, person1, person2))
    con.commit()
    
def read(cur, uuid):
    cur.execute('SELECT * FROM CaseInfo Where UUID = ? limit 1', (uuid,))

    return cur
    # for row in cur:
    #     print(row)

def get_conn():
    con = sqlite3.connect(':memory:')
    con = sqlite3.connect('./main.db')
    return con