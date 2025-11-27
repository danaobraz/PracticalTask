import time
import random
import psycopg2
from prometheus_client import start_http_server, Counter, Histogram

DB_REQUESTS = Counter(
    'db_ops_total',
    'Total number of DB operations',
    ['type']
)

DB_LATENCY = Histogram(
    'db_latency_seconds',
    'Latency of DB operations in seconds',
    ['type'],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, float("inf"))
)

DB_ERRORS = Counter(
    'db_errors_total',
    'Total number of DB errors'
)


def get_db_connection():
    try:
        return psycopg2.connect(
            host="db",
            database="testdb",
            user="user",
            password="password"
        )
    except Exception:
        return None


def main():
    start_http_server(8000)
    print("Metrics server started on port 8000")

    conn = None
    cur = None
    items = ['apple', 'banana', 'orange', 'milk', 'bread']

    while True:
        try:
            if conn is None or conn.closed != 0:
                print("Connecting to DB...")
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    cur.execute("CREATE TABLE IF NOT EXISTS sales (id SERIAL PRIMARY KEY, amount INT, item TEXT)")
                    conn.commit()
                    print("DB Connection established")
                else:
                    time.sleep(2)
                    continue

            op_type = random.choice(['insert', 'select'])

            with DB_LATENCY.labels(type=op_type).time():
                if op_type == 'insert':
                    item = random.choice(items)
                    amount = random.randint(1, 100)
                    cur.execute("INSERT INTO sales (amount, item) VALUES (%s, %s)", (amount, item))
                    conn.commit()

                elif op_type == 'select':
                    cur.execute("SELECT count(*) FROM sales")
                    cur.fetchone()

            DB_REQUESTS.labels(type=op_type).inc()

            time.sleep(random.uniform(0.05, 0.5))

        except Exception as e:
            print(f"Error occurred: {e}")
            DB_ERRORS.inc()

            if conn:
                try:
                    conn.close()
                except:
                    pass
            conn = None
            cur = None
            time.sleep(2)


if __name__ == '__main__':
    main()