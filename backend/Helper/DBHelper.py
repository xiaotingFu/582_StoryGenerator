import sqlite3

"""

SQLite Database
- Tables
    - Story
        - Book1 
        - Book2
        - Article name
        - Article URL
"""

class DBHelper:

    def __init__(self):
        self.book1 = ""
        self.book2 = ""
        self.title = ""
        self.url = ""

    # def __init__(self, book1, book2, title, url):
    #     self.book1 = book1
    #     self.book2 = book2
    #     self.title = title
    #     self.url = url

    def insert(self):
        sqlite_file = 'db.sqlite3'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute("INSERT INTO Story (book1, book2, title, url) VALUES ('{b1}', '{b2}', '{t}', '{u}')".\
            format(b1=self.book1, b2=self.book2,t=self.title, u=self.url))
        
        conn.commit()
        conn.close()

    def select(self, book1, book2):
        sqlite_file = 'db.sqlite3'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = "SELECT url FROM Story WHERE book1='{b1}' AND book2='{b2}'".format(b1=book1, b2=book2)
        c.execute(sql)
        all_rows = c.fetchall()
        conn.commit()
        conn.close()
        for row in all_rows:
            print(row[0])
        return None

DBHelper().select("Harry Potter", "Twilight")
