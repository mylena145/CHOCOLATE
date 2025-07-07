import psycopg2
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432',
    client_encoding='utf8',
    options='-c client_encoding=utf8'
)
print('Connexion OK')
conn.close()