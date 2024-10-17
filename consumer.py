import json
import logging
from time import sleep
from decouple import config
import pika

from service_factory import ServiceFactory

class Consumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        while True:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=config('RABBITMQ_HOST')
                    )
                )
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=config('VIDEO_SENT_QUEUE'), durable=False)
                self.channel.basic_qos(prefetch_count=1)
                logging.info("Conectado ao RabbitMQ.")
                return
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Erro ao conectar ao RabbitMQ: {e}. Tentando novamente em 5 segundos...")
                sleep(5)

    def callback(self, ch, method, properties, body):
        try:
            logging.debug("Received message")
            video = json.loads(body.decode('utf-8'))
            logging.debug(f"Decoded video: {video}")
            platform = video.get('platform')
            service = ServiceFactory.get_service(platform)

            if service:
                logging.debug(f"Service found for platform: {platform}")
                data = service.download_video(video)
                if data:
                    logging.debug(f"Data received: {data.to_dict()}")
                    self.channel.basic_publish(
                        exchange='',
                        routing_key=config('DATA_SENT_QUEUE'),
                        body=json.dumps(data.to_dict())
                    )
                    logging.debug("Message published to DATA_SENT_QUEUE")
                else:
                    logging.error("No data received from service")
            else:
                logging.error(f"Service not found for platform: {platform}")
        except Exception as e:
            logging.error(f"An error occurred in callback: {str(e)}")

    def start_consuming(self):
        while True:
            try:
                self.connect()
                self.channel.basic_consume(
                    queue=config('VIDEO_SENT_QUEUE'), 
                    on_message_callback=self.callback,
                    auto_ack=True
                )
                logging.debug("Starting to consume messages")
                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Conexão perdida: {e}. Tentando reconectar...")
                sleep(5)  # Espera antes de tentar reconectar
            except Exception as e:
                logging.error(f"Erro inesperado: {e}")
                break