import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

from currency_exchange import exchange
FORMAT = '%(name)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=logging.INFO,
    filename='chat.log',
    filemode='w',
    format=FORMAT
)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def send_currency_exchange(self, message, ):
        if message == 'exchange':
            rate = await exchange()
            await self.send_to_clients(f"{'exchange'}: {rate}")
            logging.info(f'Exchange rate for today')
        if message.startswith('exchange') and message != 'exchange':
            days: int = message[1]
            rate = await exchange(days)
            await self.send_to_clients(f"{'exchange'}: {rate}")
            logging.info(f'Exchange rate for {days} day')

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}")
            if message.startswith('exchange'):
                await self.send_currency_exchange(message)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())