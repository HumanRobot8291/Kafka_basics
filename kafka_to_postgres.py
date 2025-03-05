
from kafka import KafkaConsumer
import psycopg2

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="Kafka_test",
    user="postgres",
    password="root",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Consume messages and insert into PostgreSQL
for message in consumer:
    text = message.value.decode('utf-8')
    cursor.execute("SET search_path TO schema1")
    cursor.execute("INSERT INTO kafka_logs (message) VALUES (%s)", (text,))

    conn.commit()
    print(f"Inserted: {text}")

# Close connection (optional, will run indefinitely)
cursor.close()
conn.close()
