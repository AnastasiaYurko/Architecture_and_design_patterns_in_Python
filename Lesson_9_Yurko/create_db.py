import sqlite3

try:
    con = sqlite3.connect('patterns.sqlite')
    cur = con.cursor()
    print("База данных создана и успешно подключена к SQLite")
    sqlite_select_query = "select sqlite_version();"
    cur.execute(sqlite_select_query)
    record = cur.fetchall()
    print("Версия базы данных SQLite: ", record)
    with open('create_db.sql', 'r') as f:
        text = f.read()
    cur.executescript(text)
    cur.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (con):
        con.close()
        print("Соединение с SQLite закрыто")
