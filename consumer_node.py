import pika
import os
import time

# Decalring values using ENV variables provided during deployment
RABBITMQ_HOSTNAME = os.getenv("RABBITMQ_HOSTNAME", "")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "")

# Wait for RabbitMQ to be ready
def wait_for_rabbitmq():
    while True:
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOSTNAME, credentials=credentials)
            )
            connection.close()
            print("RabbitMQ is up. Connecting...")
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ to be ready...")
            time.sleep(5)

# Connect to RabbitMQ Broker
wait_for_rabbitmq()
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOSTNAME, credentials=credentials)
)
channel = connection.channel()

# Declare queue
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# Consumer function
def callback(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}", flush=True)
    time.sleep(60)

# Set up consumer
channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit, kill the pod.")
channel.start_consuming()