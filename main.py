import asyncio
from consumer import SyncConsumer

if __name__ == "__main__":
    consumer = SyncConsumer()
    asyncio.run(consumer.start_consuming())