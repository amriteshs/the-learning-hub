from app import *


# create connection to database and execute query to retrieve its contents
def execute_query(query):
	try:
		conn = psycopg2.connect("host=comp9323.postgres.database.azure.com dbname=postgres user=comp9323_admin@comp9323 password=password_123")
		cursor = conn.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		conn.close()
		
		return data
	except Exception as e:
		return


# create connection to database and execute query to modify (insert / delete) its contents
def insert_query(query):
	try:
		conn = psycopg2.connect("host=comp9323.postgres.database.azure.com dbname=postgres user=comp9323_admin@comp9323 password=password_123")
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		conn.close()
		
		return 'success'
	except Exception as e:
		return 'fail'
