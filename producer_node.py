import pika
import os
import time

RABBITMQ_QUEUE=os.getenv("RABBITMQ_QUEUE", "")

def produce_data():
    '''Simple module to create a rabbitmq connection with broker and 
    declare queue using TCP 5672 port. 
    '''
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOSTNAME", ""),
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_USERNAME", ""), os.getenv("RABBITMQ_PASSWORD", "")
            ),
        )
    )
    channel = connection.channel()

    # Queue Declaration.
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    message = "Hello World!"
    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_QUEUE,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
        
    )

    print(f"Sent '{message}'")
    connection.close()


if __name__ == "__main__":
    while True:
        produce_data()
        time.sleep(5)
