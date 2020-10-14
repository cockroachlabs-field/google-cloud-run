import psycopg2
import time
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World')
    return 'Hello {}!'.format(name) + connect().__str__()

def connect():
    host = os.environ.get('COCKROACH_HOST')
    port = os.environ.get('COCKROACH_PORT')
    database = os.environ.get('COCKROACH_DB')
    user = os.environ.get('COCKROACH_USER')
    password = os.environ.get('COCKROACH_PASS')
    sslmode = os.environ.get('COCKROACH_SSLMODE')
    sslrootcert = os.environ.get('COCKROACH_ROOTCERT')

    try:
        conn = psycopg2.connect(database=database, user=user, host=host, port=port, sslmode=sslmode, sslrootcert=sslrootcert, password=password)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        cur.execute(""" select 'Connected!' """ )
        t = cur.fetchone()[0].__str__()
        print("DB Connection Success")

    except psycopg2.Error as e:
        t = "Failed"
        print("DB Connection Failed")

    cur.close()
    conn.close()

    return " Connection successful? " + t

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))




