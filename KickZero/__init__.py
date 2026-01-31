import asyncio
import aiohttp
import websockets
import json
import inspect

class Context:
    def __init__(self,user,content,bot_class):
        self.author = user
        self.content = content
        self.bot = bot_class
    async def send_message(self,message):
        return await self.bot.send_message(message)
    async def reply(self,message):
        return await self.bot.send_message(f"@{self.author} {message}")
class KickBot():
    user_name = None
    app_key = None
    cluster = None
    chat_id = None
    bearer_token = None
    prefix = "!"
    live_chat = True
    commands = {}
    on_message_func = None
    def __init__(self,user_name,app_key,cluster,chat_id,bearer_token,prefix,live_chat):
        KickBot.user_name = user_name.lower()
        KickBot.app_key = app_key
        KickBot.cluster = cluster
        KickBot.chat_id = chat_id
        KickBot.bearer_token = bearer_token if bearer_token.startswith("Bearer ") else f"Bearer {bearer_token}"
        KickBot.prefix = prefix
        KickBot.live_chat = live_chat
    @staticmethod
    async def send_message(ctx):
        url = f"https://kick.com/api/v2/messages/send/{KickBot.chat_id}"
        headers = {
                "Authorization": KickBot.bearer_token,
                "Content-Type": "application/json; charset=utf-8", # UTF-8 olduğunu belirttik
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            }
        payload = {
        "content": str(ctx),
        "type": "message"
            }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                    status_code = response.status 
                    try:
                        response_json = await response.json()
                        response_text = response_json.get("message", "Bilinmeyen Hata")
                    except:
                        response_text = await response.text()
                    if status_code in [200, 201]:
                        return 0
                    else:
                        caller = inspect.stack()[1]
                        print('❌ Mesaj gönderilemedi!')
                        print(f'Satır: {caller.lineno} | Fonksiyon: {caller.function} ') 
                        print(f'Hata kodu: {status_code} | Yanıt: {response_text} \n')
                        if "User is not authenticated" in str(response_text):
                            print('HATA: Bearer token geçersiz veya süresi dolmuş!')
                        return 1
        except Exception as e:
            print(f'API Hatası: {e}')
            return 1
    @classmethod
    def command(cls, name=None):
        def decorator(func):
            cmd_name = name if name else func.__name__
            cls.commands[cmd_name] = func
            return func
        return decorator

    @classmethod
    def on_message(cls):
        def decorator(func):
            cls.on_message_func = func
            return func
        return decorator
    @staticmethod 
    async def start():
        uri = f"wss://ws-{KickBot.cluster}.pusher.com/app/{KickBot.app_key}?protocol=7&client=js&version=7.6.0&flash=false"
        print(f"KickBot Başlatıldı. (Prefix: {KickBot.prefix} | Kanal: {KickBot.live_chat})")
        while True:
            try:
                async with websockets.connect(uri,ping_interval=20,ping_timeout=20) as ws:
                    # Sup To CH
                    await ws.send(json.dumps({
                        "event": "pusher:subscribe",
                        "data": {"channel": f"chatrooms.{KickBot.chat_id}.v2"}
                        }))
                    while True:
                        raw_data = await ws.recv()
                        msg = json.loads(raw_data)
                        if msg.get("event") == "App\\Events\\ChatMessageEvent":
                            inner_data = json.loads(msg["data"])
                            user = inner_data['sender']['username']
                            content = inner_data['content']
                            if user.lower() == KickBot.user_name:
                                print(f"Bot: {content}")
                                continue
                            ctx = Context(user, content, KickBot)

                            if KickBot.live_chat:
                                print(f'💬 [{ctx.author}] : {ctx.content}')
                            if KickBot.on_message_func:
                                await KickBot.on_message_func(ctx)
                            if content.startswith(KickBot.prefix):
                                parts = content[len(KickBot.prefix):].split()
                                if parts:
                                    cmd_name = parts[0].lower()
                                    args = parts[1:]
                                    if cmd_name in KickBot.commands:
                                        await KickBot.commands[cmd_name](ctx,args)
                            elif msg.get("event") == "pusher:ping":
                                await ws.send(json.dumps({"event":"pusher:pong"}))
            except Exception as e:
                print(f"Hata {e} 5 saniye sonra tekrar denenicek")
                await asyncio.sleep(5)