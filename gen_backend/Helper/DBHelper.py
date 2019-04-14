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

    # def __init__(self):
    #     self.book1 = ""
    #     self.book2 = ""
    #     self.title = ""
    #     self.url = ""

    def __init__(self, book1, book2, title):
        self.book1 = book1
        self.book2 = book2
        self.title = title
        self.url = ""

    def insert(self):
        sqlite_file = 'db.sqlite3'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()

        c.execute("INSERT INTO Story (book1, book2, title, url) VALUES ('{b1}', '{b2}', '{t}', '{u}')".\
            format(b1=self.book1, b2=self.book2,t=self.title, u=self.url))
        
        conn.commit()
        conn.close()

    def isRecordExist(self):
        """
        Return if the record exist or not
        :param book1:
        :param book2:
        :param title:
        :return:
        """
        sqlite_file = 'db.sqlite3'
        conn = sqlite3.connect(sqlite_file)
        c = conn.cursor()
        sql = "SELECT * FROM Story WHERE book1='{b1}' AND book2='{b2}' AND title ='{t}'".format(b1=self.book1, b2=self.book2, t=self.title)
        c.execute(sql)
        data = c.fetchall()
        conn.close()
        if len(data) > 0:
            print('Record exist already, skip.')
            return True
        return False
