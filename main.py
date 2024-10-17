import logging
from consumer import Consumer

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    consumer = Consumer()
    consumer.start_consuming()