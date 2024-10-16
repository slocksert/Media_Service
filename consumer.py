import pika
import json
import logging
from decouple import config
from selenium_service import SeleniumService

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)

logging.getLogger("pika").setLevel(logging.WARNING)

class SyncConsumer:

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
            except Exception as e:
                logging.error(f"Erro ao conectar ao RabbitMQ: {e}")

    def callback(self, ch, method, properties, body):
        video = json.loads(body.decode('utf-8'))
        data = self.download_video(video)

        if data:
            self.channel.basic_publish(
                exchange='',
                routing_key=config('DATA_SENT_QUEUE'),
                body=data.to_json().encode()
            )
            logging.debug(f"Dados enviados: {data.to_json()}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logging.error("Erro ao processar os dados recebidos.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def download_video(self, video):
        try:
            selenium_service_instance = SeleniumService()  # nova instância
            return selenium_service_instance.download_video(video)
        except Exception as e:
            logging.error(f"Erro ao baixar vídeo: {e}")
            return None

    def start_consuming(self):
        self.connect()
        logging.debug(f"Serviço Selenium iniciado... HOST: {config('RABBITMQ_URL')}")

        self.channel.basic_consume(
            queue=config('VIDEO_SENT_QUEUE'),
            on_message_callback=self.callback,
            auto_ack=False
        )
        self.channel.start_consuming()
