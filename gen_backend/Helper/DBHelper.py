import sqlite3

"""
SQLite Database
- Tables
    - Story
        - book1 
        - book2
        - title
        - url
    - StorySummary
        - book1
        - book2
        - url
"""
class DBHelper:

    def __init__(self, book1, book2):
        self.book1 = book1
        self.book2 = book2
        self.title = ""
        self.url = ""
    
    def createConn(self):
        self.sqlite_file = '../db/db.sqlite3'
        self.conn = sqlite3.connect(self.sqlite_file)
        self.c = self.conn.cursor() 
    def executesql(self, sql):
        self.createConn()
        self.c.execute(sql)
        data = self.c.fetchall()
        self.conn.commit()
        self.closeConn()
        return data

    def closeConn(self):
        self.conn.commit()
        self.conn.close()
    def isRecordExistSummary(self):
        """
        Return if the record exist or not
        :param book1:
        :param book2:
        :param title:
        :return:
        """
        self.createConn()
        sql = "SELECT * FROM Summary WHERE book1='{b1}' AND book2='{b2}' ".format(b1=self.book1, b2=self.book2)
        self.c.execute(sql)
        data = self.c.fetchall()
        self.conn.close()
        if len(data) > 0:
            print('Record exist already, skip.')
            return True
        return False
    def isRecordExist(self):
        """
        Return if the record exist or not
        :param book1:
        :param book2:
        :param title:
        :return:
        """
        self.createConn()
        sql = "SELECT * FROM Story WHERE book1='{b1}' AND book2='{b2}' AND title ='{t}'".format(b1=self.book1, b2=self.book2, t=self.title)
        self.c.execute(sql)
        data = self.c.fetchall()
        self.conn.close()
        if len(data) > 0:
            print('Record exist already, skip.')
            return True
        return False
    def insertSummary(self):
        if not self.isRecordExistSummary():
            self.createConn()
            self.c.execute("INSERT INTO Summary (book1, book2, url) VALUES ('{b1}', '{b2}', '{u}')".\
                format(b1=self.book1, b2=self.book2, u=self.url))
            self.conn.commit()
            self.closeConn()

    def insert(self):
        if not self.isRecordExist():
            self.createConn()
            self.c.execute("INSERT INTO Story (book1, book2, title, url) VALUES ('{b1}', '{b2}', '{t}', '{u}')".\
                format(b1=self.book1, b2=self.book2,t=self.title, u=self.url))
            self.closeConn()
    
