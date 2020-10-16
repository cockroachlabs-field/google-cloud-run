import psycopg2
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World')
    status = connect()
    return 'Hello {}!'.format(name) + " Status: " + status.__str__()

def connect():
    dsn = os.environ.get('COCKROACH_URI')
    status = ""

    print("Connecting to database...")
    # Try Connecting
    try:
        conn = psycopg2.connect(dsn=dsn)
        conn.set_session(autocommit=True)
        status = "DB Connection Success"
        print(status)

    except psycopg2.Error as e:
        status = " DB Connection Failed: " + e.pgcode.__str__() + " error code: " + e.pgerror.__str__()
        print(status)

    # Try Executing SQL
    try:
        cur = conn.cursor()
        cur.execute(""" select 'SQL Executed!' """)
        rec = cur.fetchone()[0].__str__()
        print(rec)
        status = status + " " + rec

    except psycopg2.Error as e:
        status = status + " but SQL Execution Failed :(" + e.pgcode.__str__() + " error code: " + e.pgerror.__str__()

    cur.close()
    conn.close()

    return status

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))




