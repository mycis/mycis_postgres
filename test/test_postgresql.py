import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="Tu1106", host="127.0.0.1", port="5432")

print "Opened database successfully"
