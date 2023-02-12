import asyncio
import os
from pathlib import Path
import requests
import execjs
import socket
import time
import uuid
import json

import nonebot
from nonebot import get_driver, on_command, on_message
from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent, Bot, GroupMessageEvent, MessageEvent, MessageSegment
from nonebot.params import CommandArg

from .config import Config

from .server import Server
from .translate import OCR
OCR = OCR()
# from .server import serve

global_config = get_driver().config
config = Config.parse_obj(global_config)

MARK_ISCLOCKINLISTENERON = False
server = None

# command = on_command("test")


# def start_thread_loop(loop: asyncio.windows_events.ProactorEventLoop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
#
#
# @serve
# async def test(addr):
#     while len(nonebot.get_bots().values()) <= 0:
#         time.sleep(0.5)
#     bot: Bot = tuple(nonebot.get_bots().values())[0]
#     await bot.send_private_msg(user_id=2134692955, message=Message(addr))
#
#
# loop = asyncio.new_event_loop()
# print(type(loop))
# th = Thread(target=start_thread_loop, args=(loop,))
# th.start()
#
# asyncio.run_coroutine_threadsafe(test, loop)
# print("shit")

# def start(bot: Bot):
#     asyncio.run(serverStart(bot))
# #
# #
# async def serverStart(bot: Bot):
#     await bot.send_private_msg(user_id=2134692955, message=Message(time.strftime("[ %Y-%m-%d %H:%M:%S ] Socket opened", time.localtime())))
#     await bot.send_private_msg(user_id=2134692955, message=Message(time.strftime("[ %Y-%m-%d %H:%M:%S ] Socket opened", time.localtime())))
#     await bot.send_private_msg(user_id=2134692955, message=Message(time.strftime("[ %Y-%m-%d %H:%M:%S ] Socket opened", time.localtime())))


# @inte.handle()
# async def _(event: PrivateMessageEvent, bot: Bot, args: Message = CommandArg()):
#     # print(type(inte))
#     global MARK_ISCLOCKINLISTENERON
#     global server
#     # global th
#     args = args.extract_plain_text().split()
#     if len(args) != 1:
#         await inte.finish(Message("Wrong input"))
#     match args[0]:
#         case "start":
#             if MARK_ISCLOCKINLISTENERON:
#                 await inte.finish(Message("already started"))
#             # await serverStart(bot)
#             # Thread(target=start, args=(bot,), daemon=True).start()
#             server = Server(bot, event.user_id)
#             Thread(target=server._test, daemon=True).start()
#             MARK_ISCLOCKINLISTENERON = True
#             await inte.finish(Message("started"))
#         case "stop":
#             await server.stop()
#             MARK_ISCLOCKINLISTENERON = False
#             await inte.finish(Message("stopped"))
#         case _:
#             # print(th.is_alive())
#             await inte.finish(Message("what're you saying?"))


url = "https://cc-api.sbaliyun.com/v1/completions"
headers = {
    "Content-Type": "application/json",
    "referer": "https://chatgpt.sbaliyun.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
print(os.getcwd())
with open("./src/plugins/testshit/cry.js", "r") as f:
    js = execjs.compile(f.read())

def get(context: str):
    data = {"prompt": js.call("encode", context)}
    data = json.dumps(data)
    for _ in range(5):
        try:
            res = requests.post(url, headers=headers, data=data)
            if res.status_code != 200:
                return f"{res.status_code} - 请求失败"
            text = ""
            for i in res.json()["choices"]:
                text += i["text"]
                text += "\n"
            text = text.replace("本内容由https://chatgpt.sbaliyun.com/独家提供!", "")
            text = text.strip()
            return text
        except:
            print("请求超时")
    return "请求超时"

def rule_at(event: GroupMessageEvent):
    return event.is_tome()

def rule_noat(event: GroupMessageEvent):
    return not event.is_tome()

at = on_message(rule=rule_at)
@at.handle()
async def _(event: GroupMessageEvent, bot:Bot):
    group_id = event.group_id
    if event.group_id == 43621821:
        print(event.user_id)
        user_id = event.user_id
        text = event.get_plaintext()
        if len(text) == 0:
            await at.finish("你什么也没有输入")
        mid = await bot.send_group_msg(group_id=group_id, message=f'[CQ:at,qq={user_id}] {"正在思考中..."}')
        reply = get(context=text)
        await bot.delete_msg(message_id=mid["message_id"])
        await bot.send_group_msg(group_id=group_id, message=f'[CQ:at,qq={user_id}] {reply}')


noat = on_message(rule=rule_noat)
@noat.handle()
async def _(event: GroupMessageEvent, bot:Bot):
    text = event.get_plaintext()
    if ("原神" in text) | ("元神" in text) | ("genshin" in text) | ("Genshin" in text) | ("op" in text) | ("原批" in text) | ("原皮" in text):
        await noat.finish(Message("我趣，原批!"))


private_chat = on_command("chat")
@private_chat.handle()
async def _(event: PrivateMessageEvent, bot:Bot):
    if event.user_id == 2134692955:
        text = event.get_plaintext()
        if len(text) == 0:
            await at.finish("你什么也没有输入")
        await private_chat.send("正在思考中...")
        reply = get(context=text)
        await private_chat.finish(reply)


async def sendTicket(lifetime:int):
    data = {
        "ticket": uuid.uuid1().hex,
        "timeout": int((time.time() + lifetime) * 1000)
    }

    ticket = json.dumps(data)
    print(ticket)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8082))
    s.send(ticket.encode())
    s.close()
    return data


ticket = on_command("ticket-gen")
@ticket.handle()
async def _(event: MessageEvent, bot:Bot, args: Message = CommandArg()):
    lifetime = 300
    data = await sendTicket(lifetime)
    ipAddr = "47.94.146.109:8080"
    url = "http://"+ipAddr+"/test2/test?ticket="+data["ticket"]
    t = time.localtime(data["timeout"]/1000)
    c = url + \
        "\nticket有效5分钟，不要在人多的地方打开\n" + \
        f'{time.strftime("%Y-%m-%d %H:%M:%S", t)} 后失效'
    mid = await ticket.send(c)
    await asyncio.sleep(lifetime)
    await bot.delete_msg(message_id=mid["message_id"])



def translate(event: MessageEvent):
    messages = event.get_message()
    for i in messages["image"]:
        url = i.get("data")["url"]
        result = OCR.ocr(url)
        if isinstance(result, str):
            return result
        else:
            return Message(MessageSegment.image(file=result))
    return None



translate_waiter = {}

trans_private = on_command("trans")
@trans_private.handle()
async def _(event: PrivateMessageEvent, bot:Bot, args: Message = CommandArg()):
    translate_waiter[event.user_id] = time.time()+300
    reply = "请在五分钟内发送图片"
    await trans.finish(message=f'{reply}')



trans_group = on_command("trans")
@trans_group.handle()
async def _(event: GroupMessageEvent, bot:Bot, args: Message = CommandArg()):
    translate_waiter[event.user_id] = time.time()+300
    reply = "请在五分钟内发送图片"
    await bot.send_group_msg(group_id=event.group_id, message=f'[CQ:at,qq={event.user_id}] {reply}')



trans = on_message()
@trans.handle()
async def _(event: MessageEvent, bot:Bot):
    if translate_waiter.__contains__(event.user_id):
        if translate_waiter[event.user_id] >= time.time():
            msg = translate(event)
            if msg != None:
                translate_waiter.pop(event.user_id)
                await trans.finish(msg)
        else:
            translate_waiter.pop(event.user_id)




# testarea = on_message()
# @testarea.handle()
# async def _(event: MessageEvent, bot:Bot):
#     if event.user_id == 2134692955:
#         messages = event.get_message()
#         print(messages)
#         for i in messages["image"]:
#             url = i.get("data")["url"]
#             result = OCR.ocr(url)
#             if isinstance(result, str):
#                 await testarea.finish(result)
#             else:
#                 await testarea.finish(Message(MessageSegment.image(file=result)))
#         print("no pic")




_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").
        resolve()))

