import sqlite3
from time import sleep
class DB:
	def __init__(self):
		self.connection = sqlite3.connect('vs.db')
		self.cursor = self.connection.cursor()
		self.cursor.execute("""DROP TABLE IF EXISTS stack;""")
		sqlCommand = """
		CREATE TABLE stack(
		tag VARCHAR2(50) PRIMARY KEY,
		votes INTEGER,
		views INTEGER,
		answers INTEGER);"""
		self.cursor.execute(sqlCommand)
		self.connection.commit()
	def close(self):
		self.connection.close()

	def insert(self, tag, vote, view, answer):
		sqlCommand = """INSERT INTO stack (tag, votes, views, asnwers) 
		VALUES (""" + tag + """, """ + str(vote) + """, """ + str(view) + """, """ + str(answer) + """) ON DUPLICATE KEY
		UPDATE view = (SELECT views FROM stack WHERE tag = """ + tag + """) + """ + str(view) + """,
		vote = (SELECT votes FROM stack WHERE tag = """ + tag + """) + """ + str(vote) + """,
		answer = (SELECT answers FROM stack WHERE tag = """ + tag + """) + """ + str(answer) + """;"""
		print (sqlCommand)
		#sleep(100)
		
		self.cursor.execute(sqlCommand)
		self.connection.commit()
