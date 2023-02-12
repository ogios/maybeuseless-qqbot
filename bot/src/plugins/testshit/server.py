import asyncio
import socket
import time
import traceback
from threading import Thread

import nonebot
from nonebot.adapters.onebot.v11 import Message, Bot


async def serve(func):
    serverSocket = socket.socket()
    serverSocket.bind(("127.0.0.1", 55501))
    serverSocket.listen(1)
    print(func.__name__)
    # client, addr = serverSocket.accept()
    await func(time.strftime("[ %Y-%m-%d %H:%M:%S ] Socket opened", time.localtime()))
    await asyncio.sleep(5)




class Server:
    def __init__(self, bot: Bot, uid: int):
        (bot,) = nonebot.get_bots().values()
        self.socket = socket.socket()
        self.bot = bot
        self.uid = uid
        self.OPEN = False

    def send(self, msg: str):
        Thread(target=self._send, args=(msg,), daemon=True).start()

    def _send(self, msg:str):
        asyncio.run(self.__send(msg))

    async def __send(self, msg: str):
        await self.bot.send_private_msg(user_id=self.uid, message=Message(msg))

    # def test(self):
    #     # self._test()
    #     asyncio.run(self._test())

    def _test(self):
        self.OPEN = True
        self.send("Socket opened")
        # await self.bot.send_private_msg(user_id=self.uid, message=Message())
        while self.OPEN:
            print(1)
            shit = time.strftime("[ %Y-%m-%d %H:%M:%S ] [SUCCESS] 已打卡", time.localtime())
            print(2)
            self.send(shit)
            # await self.bot.send_private_msg(user_id=self.uid, message=Message(shit))
            print(3)
            time.sleep(5)
            print(4)
        self.send("Socket close")
        # await self.bot.send_private_msg(user_id=self.uid, message=Message("Socket closed"))

    async def start(self):
        self.socket.bind(("127.0.0.1", 55501))
        self.socket.listen(1)
        while 1:
            client, addr = self.socket.accept()
            print(time.strftime("[ %Y-%m-%d %H:%M:%S ] ", time.localtime()))
            msg = client.recv(256).decode()
            if msg == "1":
                shit = time.strftime("[ %Y-%m-%d %H:%M:%S ] [SUCCESS] 已打卡", time.localtime())
                await self.bot.send_private_msg(user_id=self.uid, message=Message(shit))
            if msg == "0":
                shit = time.strftime("[ %Y-%m-%d %H:%M:%S ] [FATAL] 未知错误", time.localtime())
                await self.bot.send_private_msg(user_id=self.uid, message=Message(shit))

    async def stop(self):
        self.socket.close()
        self.OPEN = True
        await self.bot.send_private_msg(user_id=self.uid, message=Message("Socket closed"))
