import os
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    # Establish connection to PostgreSQL
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'postgres'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        port=os.environ.get('DB_PORT', '5432')
    )

def init_db():
    # Initialize the database table and initial value
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS counter_table (id SERIAL PRIMARY KEY, val INTEGER);')
    cur.execute('SELECT COUNT(*) FROM counter_table;')
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO counter_table (val) VALUES (0);')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/pingpong', methods=['GET'])
def ping_pong():
    # Increment counter in database and return new value
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE counter_table SET val = val + 1 RETURNING val;')
    counter = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f"pong {counter}"

@app.route('/pings')
def pings():
    """Returns the current counter value from database"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT val FROM counter_table LIMIT 1;')
    counter = cur.fetchone()[0]
    cur.close()
    conn.close()
    return str(counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
