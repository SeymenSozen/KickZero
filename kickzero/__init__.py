import asyncio
import aiohttp
import websockets
import json
import inspect
import colorama
import re
import sys # sys mutlaka kalmalı
from typing import Optional, Dict, Callable, Any
from colorama import Fore, Style


if "kickzero" not in sys.modules:
    sys.modules["kickzero"] = sys.modules[__name__]

__all__ = ['kickbot', 'message_context', 'decorators']

class zerror:
    """
    ### 🇹🇷 [TR] Hata ve Log Yöneticisi (Error Logger)
    Projedeki tüm konsol çıktılarını, hata mesajlarını ve uyarıları merkezi bir 
    noktadan yönetir. Renkli çıktılar, emojiler ve çoklu dil (TR/EN) desteği sunar. 
    Sınıf başlatılmadan (Singleton mantığıyla) doğrudan sınıf üzerinden kullanılır.

    ### 🇺🇸 [EN] Global Error and Log Manager
    Centralizes all console outputs, error messages, and warnings across the project. 
    Features colored outputs, emojis, and multi-language (TR/EN) support. 
    Operates directly on the class level (Singleton) without instantiation.

    ---
    ### 🛠️ Değişkenler / Attributes (Variables):

    #### 🖨️ L1: Çıktı Kontrolleri / Output Toggles
    - print_errors (bool): Hata mesajları gösterilsin mi? (Show error logs?)
    - print_warns (bool): Uyarı mesajları gösterilsin mi? (Show warning logs?)
    - print_notes (bool): Not mesajları gösterilsin mi? (Show note logs?)
    - print_success (bool): Başarı mesajları gösterilsin mi? (Show success logs?)
    - print_messages (bool): Standart mesajlar gösterilsin mi? (Show standard messages?)

    #### 🎭 L2: Görsel Ayarlar / Visual Settings
    - use_colors (bool): Çıktılar renkli mi olsun? (Enable colored terminal output?)
    - use_emojis (bool): Emojiler genel olarak açık mı olsun? (Global emoji toggle?)
    - preety_print (bool): Gelişmiş okunabilirlik sağlansın mı? (Use pretty formatting?)

    #### 😊 L3: Detaylı Emoji Kontrolleri / Granular Emoji Toggles
    - print_error_emoji (bool): Hatalarda [❌] gösterilsin mi? (Show emoji on errors?)
    - print_warnn_emoji (bool): Uyarılarda [🔔] gösterilsin mi? (Show emoji on warnings?)
    - print_note_emoji (bool): Notlarda [📝] gösterilsin mi? (Show emoji on notes?)
    - print_succes_emoji (bool): Başarılarda [✅] gösterilsin mi? (Show emoji on success?)
    - print_message_emoji (bool): Mesajlarda [💬] gösterilsin mi? (Show emoji on messages?)

    #### 🌍 L4: Sistem Ayarları / System Settings
    - lang (str): Çıktı dili, "tr" veya "en". (Global output language)

    ---
    ### ⚡ Metodlar / Methods:
    - log(level, msg_tr, msg_en, msg): Belirtilen seviyeye (error, warn, note, vb.) ve 
      sistemin o anki diline göre formatlanmış renkli log çıktısı verir. 
      (Prints a color-formatted log based on the specified level and language.)
    """
    print_errors: bool = True 
    print_warns: bool = True 
    print_notes: bool = True
    print_success: bool = True
    print_error_emoji: bool = True 
    print_warnn_emoji: bool = True
    print_note_emoji: bool = True
    print_succes_emoji: bool = True
    print_messages: bool = True
    print_message_emoji: bool = True
    pretty_print: bool = True
    use_emojis: bool = True
    use_colors: bool = True
    lang: str = "en" 
    @classmethod
    def log(cls: 'zerror', level: str, msg_tr: str = "", msg_en: str = "",msg: str = ""):
        emoji, color = "", ""
        lvl = level.lower()
        if lvl in ["err", "error"] and not cls.print_errors: return
        elif lvl in ["warn", "warnn", "warning"] and not cls.print_warns: return
        elif lvl in ["note", "not"] and not cls.print_notes: return
        elif lvl in ["succ", "success"] and not cls.print_success: return
        elif lvl in ["msg", "mesaj", "message"] and not cls.print_messages: return
        if cls.lang.lower() in ["tr", "en"]:
            message = msg if msg else msg_tr if cls.lang.lower() == "tr" else msg_en
        else:
            print(f"{Fore.RED}[❌] {Style.BRIGHT}[Hata/Error] {Fore.WHITE}Dil tr veya en seçilmeli{Style.RESET_ALL}")
            return
        if lvl in ["err", "error"]:
            level_text = "hata" if cls.lang == "tr" else "error"
            emoji = "[❌] " if cls.use_emojis and cls.print_error_emoji else ""
            color = Fore.RED if cls.use_colors else ""
        elif lvl in ["warn", "warnn", "warning"]:
            level_text = "uyarı" if cls.lang == "tr" else "warning"
            emoji = "[🔔] " if cls.use_emojis and cls.print_warnn_emoji else ""
            color = Fore.YELLOW if cls.use_colors else ""
        elif lvl in ["note", "not"]:
            level_text = "not" if cls.lang == "tr" else "note"
            emoji = "[📝] " if cls.use_emojis and cls.print_note_emoji else ""
            color = Fore.CYAN if cls.use_colors else "" 
        elif lvl in ["succ", "success"]:
            level_text = "başarı" if cls.lang == "tr" else "success"
            emoji = "[✅] " if cls.use_emojis and cls.print_succes_emoji else ""
            color = Fore.GREEN if cls.use_colors else ""
        elif lvl in ["msg", "mesaj", "message"]:
            level_text = "mesaj" if cls.lang == "tr" else "message"
            emoji = "[💬] " if cls.use_emojis and cls.print_message_emoji else ""
            color = Fore.WHITE if cls.use_colors else ""
        else:
            level_text = lvl
            color = Fore.WHITE
        print(f"{color}{emoji}{Style.BRIGHT}[{level_text.upper()}] {Fore.WHITE}{message}{Style.RESET_ALL}")

class tasks: 
    """
    ### 🇹🇷 [TR] Görev ve Rutin Yöneticisi
    Botun arka planda çalışması gereken periyodik görevlerini (timers), başlangıç 
    fonksiyonlarını ve sistem kontrollerini koordine eder. Asenkron (asyncio) 
    yapısı sayesinde ana akışı bozmadan paralel iş yükleri oluşturur.

    ### 🇺🇸 [EN] Task and Routine Manager
    Coordinates the bot's background periodic tasks (timers), startup functions, 
    and system checks. Uses asynchronous (asyncio) operations to create parallel 
    workloads without interrupting the main execution flow.

    ---
    ### ⚡ Metodlar / Methods:

    #### 🚀 L1: Başlatıcılar / Startup Executers
    - run_ready_funcs(bot): Bot bağlandığında `@on_ready` ile işaretlenmiş tüm 
      fonksiyonları birer 'task' olarak başlatır. (Starts all @on_ready functions 
      as individual tasks upon connection.)
    
    #### ⏱️ L2: Zamanlayıcılar / Timer Coordination
    - run_timer_tasks(bot): `@timer_task` ile tanımlanan periyodik döngüleri kurar. 
      Fonksiyonun parametre alıp almadığını kontrol ederek (inspect), gerekirse 
      sahte bir bağlam (fake context) ile besler. (Sets up periodic loops defined 
      by @timer_task. Checks function signatures to feed them with a fake context 
      if required.)

    #### 🔍 L3: Sistem Denetimi / System Check
    - check(bot): Botun temel bilgilerini ve bağlı olduğu kanalları doğrulayarak 
      konsola durum raporu geçer. (Verifies basic bot info and connected channels, 
      then logs a status report to the console.)
    """
    @staticmethod
    async def run_ready_funcs(bot:'kickbot'):
        for ready_func in bot._on_ready_tasks: asyncio.create_task(ready_func())
    @staticmethod
    async def run_timer_tasks(bot:'kickbot'):
        async def _internal_worker(task_info):
            while True:
                await asyncio.sleep(task_info["interval"])
                try:
                    sig = inspect.signature(task_info["func"])
                    if len(sig.parameters) > 0:
                        fake_data = {"content":"Timer","sender":{"username":"System"}}
                        await task_info["func"](message_context(fake_data,bot))
                    else:
                        await task_info["func"]()
                except Exception as e:
                    zerror.log(level="warn", 
                               msg_tr=f"Timer Hatası ({task_info['func'].__name__}): {e}", 
                               msg_en=f"Timer Error ({task_info['func'].__name__}): {e}")
        for task in bot._timer_tasks:
            asyncio.create_task(_internal_worker(task))
        zerror.log(level="succ", 
                   msg_tr="Tüm zamanlayıcılar arka planda başlatıldı.", 
                   msg_en="All timers started in the background.")
    @staticmethod
    async def check(bot:'kickbot'):
        if len(bot._on_ready_tasks) == 0:
                zerror.log(
                    level="succ", 
                    msg_tr=f"Bot {bot.user_name} adıyla giriş yaptı ve filodaki {len(bot.channels)} kanalı dinliyor!", 
                    msg_en=f"Bot logged in as {bot.user_name} and listening to {len(bot.channels)} channels in the fleet!")

class engine:
    """
    ### 🇹🇷 [TR] WebSocket ve Bağlantı Motoru
    Kick.com'un kullandığı Pusher (WebSocket) altyapısı ile olan tüm iletişimi 
    yönetir. Kanallara abone olma (subscribe), ping-pong (keep-alive) trafiği 
    ve gelen ham verilerin ilgili işlemcilere (processors) dağıtılmasından sorumludur.

    ### 🇺🇸 [EN] WebSocket and Connection Engine
    Manages all communication with the Pusher (WebSocket) infrastructure used 
    by Kick.com. Responsible for channel subscriptions, keep-alive (ping-pong) 
    traffic, and routing raw incoming data to the appropriate processors.

    ---
    ### ⚡ Metodlar / Methods:

    #### 🔌 L1: Bağlantı Kurucu / Connection Establisher
    - connect(bot): Belirlenen 'cluster' ve 'app_key' üzerinden Kick WebSocket 
      sunucusuna fiziksel bağlantıyı başlatır. (Establishes the physical connection 
      to the Kick WebSocket server using the defined cluster and app_key.)

    #### 📡 L2: Radar Abonelikleri / Subscription Services
    - subscribe_to_chatroom(ch, ws): Sohbet mesajlarını ve mod aksiyonlarını dinlemek 
      için kanala abone olur. (Subscribes to the channel to listen for chat messages 
      and mod actions.)
    - subscribe_to_channel_points(ch, ws): Kanal puanı (Reward) kullanımlarını yakalamak 
      için abone olur. (Subscribes to capture channel point/reward redemptions.)
    - subscribe_to_channel_events(ch, ws): [Beta] Takipçi ve diğer kanal olaylarını 
      yakalamak için abone olur. (Subscribes to capture followers and other channel events.)
    - subscribe_all(bot, ws): Filodaki tüm benzersiz kanallar için tüm abonelik 
      türlerini topluca başlatır. (Bulk starts all subscription types for every 
      unique channel in the fleet.)

    #### 💓 L3: Yaşam Sinyali / Keep Alive
    - keep_alive(bot, ws): Sunucudan gelen 'ping' sinyallerine 'pong' ile yanıt 
      vererek bağlantının kopmasını engeller. (Prevents connection loss by responding 
      with 'pong' to incoming 'ping' signals from the server.)

    #### 🚥 L4: Olay Dağıtıcı / Event Dispatcher
    - process_all_events(bot, ws): Sürekli dinleme yaparak gelen verinin türünü 
      ayrıştırır (Chat, Reward, Ping) ve ilgili işlemciye yönlendirir. (Constantly 
      listens to parse the event type and routes it to the specific processor.)
    """
    @staticmethod
    def connect(bot):
        websocket = websockets.connect(uri=f"wss://ws-{bot.cluster}.pusher.com/app/{bot.app_key}?protocol=7&client=js&version=7.6.0")
        return websocket
    @staticmethod
    async def subscribe_to_chatroom(ch, websocket):
        await websocket.send(json.dumps({ "event": "pusher:subscribe","data": {"channel": f"chatrooms.{ch.chat_id}.v2"}})) # Mod actions ve chat   
    @staticmethod
    async def subscribe_to_channel_points(ch, websocket): 
        await websocket.send(json.dumps({ "event": "pusher:subscribe","data": {"channel": f"chatroom_{ch.chat_id}"}}))
    """ st Untested Beta"""
    @staticmethod
    async def subscribe_to_channel_events(ch, websocket): # Kicks puanları ve takipler
        await websocket.send(json.dumps({"event": "pusher:subscribe","data": {"channel": f"channel_{ch.channel_id}"}}))
    """ en Untested Beta """

    @staticmethod
    async def subscribe_all(bot, websocket):
        # ⚓ DÜZELTME: Sadece isimle kaydedilen gerçek objeleri alıyoruz
        unique_channels = []
        for key, value in bot.channels.items():
             if not key.isdigit() and value not in unique_channels:
                 unique_channels.append(value)
                 
        for ch in unique_channels:
            await engine.subscribe_to_chatroom(ch, websocket)   
            await engine.subscribe_to_channel_points(ch, websocket)
            await engine.subscribe_to_channel_events(ch, websocket)
            
            zerror.log(level="note", msg_tr=f"[{ch.name}] Radar abonelikleri tamamlandı!", msg_en=f"[{ch.name}] Radar subscriptions completed!")
    @staticmethod
    async def keep_alive(bot,websocket):
        await websocket.send(json.dumps({"event": "pusher:pong"})) 
    @staticmethod
    async def process_all_events(bot,websocket):
        raw_data = await websocket.recv()
        data = json.loads(raw_data)
        if data.get("event") == "App\\Events\\ChatMessageEvent":
            await processor.process_chat(bot,raw_data)
        elif data.get("event") == "RewardRedeemedEvent":
            await processor.process_channel_points(bot,raw_data)
        elif data.get("event") == "pusher:ping":
            await engine.keep_alive(bot,websocket)

class processor:
    """
    ### 🇹🇷 [TR] Veri İşleme ve Olay Dağıtıcı (Event Dispatcher)
    Kick sunucularından gelen ham WebSocket verilerini analiz eder, uygun bağlam 
    (context) nesnelerini oluşturur ve tetikleyicileri (commands, messages, rewards) 
    çalıştırır. Botun mantıksal karar merkezidir.

    ### 🇺🇸 [EN] Data Processor and Event Dispatcher
    Analyzes raw WebSocket data from Kick servers, creates appropriate context 
    objects, and executes triggers (commands, messages, rewards). It serves 
    as the logical decision center of the bot.

    ---
    ### ⚡ Metodlar / Methods:

    #### ⚔️ L1: Dinamik Fonksiyon Çalıştırıcı / Dynamic Executor
    - execute(fx, ctx, args): Hedef fonksiyonun parametre yapısını (inspect) 
      analiz eder ve uygun argümanlarla güvenli bir şekilde çalıştırır. 
      (Analyzes the target function's signature and executes it safely 
      with the appropriate arguments.)

    #### 💬 L2: Sohbet İşleyici / Chat Processor
    - process_chat(bot, raw_data): Gelen sohbet verisini çözümler; canlı sohbeti 
      ekrana basar, genel mesaj izleyicilerini, özel kelime tetikleyicilerini 
      ve komutları paralel olarak tetikler. (Parses incoming chat data; logs 
      live chat, triggers global watchers, word triggers, and commands in parallel.)

    #### 💎 L3: Kanal Ödülü İşleyici / Reward Processor
    - process_channel_points(bot, raw_data): Kanal puanı ile alınan ödülleri 
      yakalar; ödül ismine göre kayıtlı fonksiyonları bulur ve ödülü kullanan 
      kişinin bilgilerini ilgili göreve iletir. (Captures reward redemptions; 
      matches reward titles with registered functions and forwards user info to the task.)
    """
    @staticmethod
    async def execute(fx,ctx,args):
        try:
            sig = inspect.signature(fx)
            params_count = len(sig.parameters)
            if params_count == 2: await fx(ctx,args)
            elif params_count == 1: await fx(ctx)
            else: await fx()
        except Exception as e:
            zerror.log(level="error", msg_tr=f"{fx.__name__} çalışırken hata: {e}", msg_en=f"Error running {fx.__name__}: {e}")
    @staticmethod
    async def process_chat(bot:'kickbot',raw_data):
        data = json.loads(raw_data)
        inner_data = json.loads(data["data"])
        ctx = message_context(inner_data,bot)
        async def display_messages():
            if bot.display_live_chat and (not ctx.is_bot or bot.display_bot_messages):
                perms = " | ".join(ctx.badge_texts) if ctx.badge_texts else (r"İzleyici" if zerror.lang == "tr" else r"Viewer")
                msg_log = f"{Fore.YELLOW}{ctx.author}{Fore.WHITE}: {ctx.content} {Fore.BLACK}({perms})"
                zerror.log(level="message", msg=msg_log)
        async def process_message_funcs():
            if not (bot.filter_bot_messages and ctx.is_bot):
                for watcher in bot._on_message_tasks:
                    asyncio.create_task(processor.execute(watcher,ctx,[]))
            if ctx.is_bot: return
            for trigger,configs in bot._message_handlers.items():
                for config in configs:
                    if ctx.is_bot and not config.get("execute_bot",False): continue
                    is_lower = config.get("lower",True)
                    msg_c = ctx.content.lower() if is_lower else ctx.content
                    trig_c = trigger.lower() if is_lower else trigger
                    is_trig = (msg_c == trig_c) if config.get("exact",True) else msg_c.startswith(trig_c)
                    if is_trig:
                        args = ctx.content.split()[len(trig_c.split()):]
                        asyncio.create_task(processor.execute(config["func"],ctx,args))
        async def process_command_funcs():
            if ctx.content.startswith(bot.prefix):
                parts = ctx.content[len(bot.prefix):].split()
                if parts:
                    cmd_raw = parts[0]
                    cmd_lower = parts[0].lower()
                    cmd_configs = bot._commands.get(cmd_raw, []) + (bot._commands.get(cmd_lower,[]) if cmd_lower != cmd_raw else [])
                    for cmd_info in cmd_configs:
                        if ctx.is_bot and not cmd_info.get("execute_bot",False): continue
                        asyncio.create_task(processor.execute(cmd_info["func"],ctx,parts[1:]))
        asyncio.create_task(display_messages())
        asyncio.create_task(process_message_funcs())
        asyncio.create_task(process_command_funcs())
    @staticmethod
    async def process_channel_points(bot:'kickbot',raw_data):
        data = json.loads(raw_data)
        rctx = points_context(data,bot)
        ### Log
        log_msg = f"{Fore.MAGENTA}{rctx.username}{Fore.WHITE}, {Fore.GREEN}'{rctx.title}'{Fore.WHITE} ödülünü kullandı! {Fore.BLACK}(Kanal: {rctx.channel})"
        if rctx.input:
            log_msg += f" {Fore.CYAN}(Mesaj: {rctx.input})"
        ## Dedektör Taraması
        title_lower = rctx.title.lower()
        reward_configs = bot._reward_handlers.get(title_lower, [])
        for config in reward_configs:
            asyncio.create_task(processor.execute(config["func"], rctx, []))
        zerror.log(level="succ", msg=log_msg)

### contexts
class message_context:
    """
    ### 🇹🇷 [TR] Bağlam Merkezi (context)
    Kick.com API'den gelen verileri, botun o anki çalışma durumuyla birleştirir.
    Bu sınıf; mesajın içeriğine, gönderen kişinin yetkilerine ve botun fonksiyonlarına 
    tek bir noktadan (`ctx`) erişim sağlar.

    ### 🇺🇸 [EN] Command context
    Unifies data from the Kick.com API with the bot's current operational state.
    This class provides a single point of access (`ctx`) to message content, 
    sender permissions, and bot methods.

    ---
    ### 🛠️ Değişkenler / Attributes (Variables):

    #### 📦 L1: Akış Verileri / Stream Data
    - id (str): Mesajın benzersiz kimliği. (Unique message ID)
    - chatroom_id (int): Mesajın düştüğü odanın ID'si. (Target chatroom ID)
    - content (str): Mesajın ham metni. (Raw message content)
    - created_at (str): Gönderilme zamanı. (Creation timestamp)

    #### 👤 L2: Aktör / The Actor (Sender)
    - author (str): Kullanıcı adı. (Sender's username)
    - author_id (int): Kullanıcının kalıcı sayısal ID'si. (User's permanent ID)
    - slug (str): URL uyumlu kullanıcı adı. (Sender's URL slug)

    #### 🎨 L3: Görsel Kimlik / Visual Identity
    - color (str): Kullanıcı renk kodu. (User hex color)
    - badges (list): Sahip olunan ham rozetler. (Raw badge list)
    - badge_texts (list): Rozetlerin isimleri. (Badge display names)

    #### 🛡️ L4: Yetki Kalkanları / Permission Shields
    - is_broadcaster (bool): Kanal sahibi mi? (Is broadcaster?)
    - is_mod (bool): Moderatör mü? (Is moderator?)
    - is_sub (bool): Abone mi? (Is subscriber?)
    - is_vip (bool): VIP mi? (Is VIP?)
    - is_staff (bool): Kick görevlisi mi? (Is Kick staff?)
    - is_verified (bool): Onaylı hesap mı? (Is verified?)

    #### 🤖 L5: Sistem Kontrolü / System Check
    - bot (kickbot): Ana bot sınıfına olan bağlantı. (Reference to main kickbot instance)
    - is_bot (bool): Bu mesajı botun kendisi mi attı? (Did the bot send this message?)
    
    ---
    ### ⚡ Metodlar / Methods:
    - reply(content): Kullanıcıyı etiketleyerek cevap verir. (Reply with mention)
    - send(content): Kanala düz metin gönderir. (Send plain text)
    """
    bot: 'kickbot'
    id: str
    chatroom_id: int
    content: str
    type: str
    created_at: str
    sender_id: int
    author: str
    slug: str
    color: str
    badges: list
    badge_texts: list
    is_broadcaster: bool
    is_mod: bool
    is_sub: bool
    is_vip: bool
    is_staff: bool
    is_verified: bool
    is_og: bool
    metadata: dict
    message_ref: str
    is_bot: bool
    
    #Garanti seviyeler, ekle 
    def __init__(self,data:dict,bot:'kickbot'): 
        self.bot = bot
        # --- L1: Ana Veriler ---
        self.id = data.get("id")
        self.chatroom_id = data.get("chatroom_id")
        self.content = data.get("content")
        self.type = data.get("type")
        self.created_at = data.get("created_at")
        # --- L2: Gönderici (Sender) --
        Sender = data.get("sender",{})
        self.sender_id = Sender.get("id")
        self.author = Sender.get("username")
        self.slug = Sender.get("slug")
        # --- L3: Kimlik ve Rozetler (Identity) ---
        Identity = Sender.get("identity",{})
        self.color = Identity.get("color")
        self.badges = Identity.get("badges",[])
        # --- L4: Yetki ve Rozet İşleme ---
        BadgeTypes = [badge.get("type") for badge in self.badges]
        self.is_broadcaster = "broadcaster" in BadgeTypes
        self.is_mod         = "moderator" in BadgeTypes
        self.is_sub         = "subscriber" in BadgeTypes
        self.is_vip         = "vip" in BadgeTypes
        self.is_staff       = "staff" in BadgeTypes
        self.is_verified    = "verified" in BadgeTypes
        self.is_og          = "og" in BadgeTypes
        #L4.1 İleride Eklenicek
        self.badge_texts = [badge.get("text") for badge in self.badges]
        # --- L5: Meta Veri (Metadata) ---
        self.metadata = data.get("metadata", {})
        self.message_ref = self.metadata.get("message_ref")
        # | 
        AuthorName = str(self.author).lower()
        BotName = str(self.bot.user_name).lower()
        self.is_bot = (AuthorName == BotName)
        # ---Ş6 Channel
        self.channel = self.bot._get_channel(self.chatroom_id)
    async def reply(self, content: str):
        if hasattr(self, 'channel') and self.channel and type(self.channel) != str:
            return await self.channel.send(f"@{self.author} {content}")
        zerror.log(level="error", msg_tr="Kanal bulunamadı! Timer görevlerinden mesaj atıyorsanız ctx.bot.find_channel('isim').send() kullanmalısınız.")

    async def send(self, content: str):
        if hasattr(self, 'channel') and self.channel and type(self.channel) != str:
            return await self.channel.send(content)
            
        # Kanalı belli değilse ana gemiye at
        return await self.bot.send_message(content)
class points_context:
    """
    ### 🇹🇷 [TR] Kanal Puanı Bağlamı (Reward Context)
    Kick.com üzerindeki sadakat puanı (Stream Rewards) kullanımlarını temsil eder.
    Ödülü kimin, hangi kanalda ve hangi girdiyle (input) kullandığını takip eder.

    ### 🇺🇸 [EN] Reward Redemption Context
    Represents stream reward redemptions on Kick.com. Tracks who used the 
    reward, in which channel, and with what user input.

    ---
    ### 🛠️ Değişkenler / Attributes (Variables):

    #### 💎 L1: Ödül Detayları / Reward Details
    - title (str): Kullanılan ödülün tam adı. (Title of the redeemed reward)
    - input (str): Kullanıcının ödülle birlikte gönderdiği mesaj. (User's input message)
    - color (str): Ödülün paneldeki arka plan renk kodu. (Reward's hex background color)

    #### 👤 L2: Aktör / The Actor (User)
    - username (str): Ödülü kullanan kişinin adı. (Username of the redeemer)
    - user_id (int): Kullanıcının sayısal ID'si. (Permanent ID of the user)

    #### 📡 L3: Konum / Location
    - channel (channel_context): Ödülün tetiklendiği kanal objesi. (Channel object where the reward was used)
    - channel_id (int): Kanalın sayısal ID'si. (Permanent ID of the channel)

    #### 🤖 L4: Sistem / System
    - bot (kickbot): Ana bot motoruna erişim. (Reference to the main kickbot instance)

    ---
    ### ⚡ Metodlar / Methods:
    - reply(content): Ödülü kullanan kişiyi etiketleyerek cevap verir. (Reply with mention)
    - send(content): Ödülün kullanıldığı kanala düz metin gönderir. (Send plain text)
    """
    bot: 'kickbot'
    title: str
    user_id: int
    channel_id: int
    username: str
    user_input: str
    color: str
    channel: dict
    def __init__(self,data: dict,bot:'kickbot'):
        self.bot = bot
        self.event = data.get("event", "")
        raw_inner = data.get("data", "{}")
        inner_data:dict = json.loads(raw_inner) if isinstance(raw_inner, str) else raw_inner
        self.title = inner_data.get("reward_title", "")
        self.user_id = inner_data.get("user_id", 0)
        self.channel_id = inner_data.get("channel_id", 0)
        raw_channel_str = data.get("channel", "")
        extracted_chat_id = raw_channel_str.split("_")[-1] if "_" in raw_channel_str else raw_channel_str
        self.channel = self.bot._get_channel(extracted_chat_id)
        self.username = inner_data.get("username", "")
        self.input = inner_data.get("user_input", "")
        self.color = inner_data.get("reward_background_color", "")
    async def reply(self,content:str):
        return await self.bot.send_message(f"@{self.username} {content}")
    async def send(self,content:str):
        return await self.bot.send_message(f"{content}")
class channel_context:
    """
    ### 🇹🇷 [TR] Kanal Bağlamı (Channel Context)
    Botun bağlı olduğu her bir bağımsız kanalı (odayı) temsil eder. 
    Kanal bazlı mesaj gönderme işlemlerinin merkezidir.

    ### 🇺🇸 [EN] Channel Context
    Represents each independent channel (room) the bot is connected to. 
    The hub for channel-specific message sending operations.

    ---
    ### 🛠️ Değişkenler / Attributes (Variables):

    #### ⚓ L1: Kimlik Bilgileri / Identity
    - name (str): Kanalın görünen adı/kullanıcı adı. (Channel's display name)
    - channel_id (int): Kanalın ana sayısal ID'si. (Main channel ID)
    - chat_id (int): Sohbet odasının benzersiz API ID'si. (Unique API chatroom ID)

    #### 🤖 L2: Sistem / System
    - bot (kickbot): Bağlı olduğu ana bot sınıfı. (The main kickbot instance it belongs to)

    ---
    ### ⚡ Metodlar / Methods:
    - send(content): Bu kanala özel asenkron mesaj gönderir. (Sends an async message specifically to this channel.)
    """
    def __init__(self, bot:'kickbot',name:'str',channel_id: int,chat_id:int):
        self.bot = bot
        self.name:str = name
        self.channel_id: int = channel_id
        self.chat_id: int = chat_id
    async def send(self,content:str):
        url = f"https://kick.com/api/v2/messages/send/{self.chat_id}"
        headers = {"Authorization": self.bot.bearer_token,"Content-Type": "application/json","User-Agent": "Mozilla/5.0"}
        payload = {"content": str(content), "type": "message"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status not in [200, 201]:
                    zerror.log(level="error", 
                               msg_tr=f"[{self.name}] Mesaj gönderilemedi! Kod: {resp.status}",
                               msg_en=f"[{self.name}] Failed to send message! Code: {resp.status}")
                return resp.status

class decorators:
    @classmethod
    def command(cls, name: str = None, lower: bool = True, execute_bot: bool = False):
        """
        ### 🇹🇷 [TR] Komut Kaydedici
        Prefix (!) ile başlayan komutları listeye ekler. 
        Aynı isimde birden fazla fonksiyon tanımlanabilir.
        
        ### 🇺🇸 [EN] Command Registerer
        Registers prefix (!) commands into a list. 
        Multiple functions can be defined under the same name.
        """
        def Decorator(fx: Callable):
            RawName = name if name else fx.__name__
            CommandName = RawName.lower() if lower else RawName
            # ⚓ Liste kontrolü ve ekleme
            if CommandName not in kickbot._commands:
                kickbot._commands[CommandName] = []
            kickbot._commands[CommandName].append({"func": fx, "execute_bot": execute_bot})
            return fx
        return Decorator
    @classmethod
    def message(cls, content: str, exact: bool = None, lower: bool = True, execute_bot: bool = False):
        """
        ### 🇹🇷 [TR] Kelime Takip Kaydedici
        Belirli kelimeleri bir listeye ekler. Birden fazla fonksiyon aynı kelimeyi dinleyebilir.
        
        ### 🇺🇸 [EN] Word Watcher Registerer
        Adds specific words to a list. Multiple functions can listen to the same word.
        """
        def Decorator(fx: Callable):
            sig = inspect.signature(fx)
            final_exact = (len(sig.parameters) == 1) if exact is None else exact
            if content not in kickbot._message_handlers:
                kickbot._message_handlers[content] = []
            kickbot._message_handlers[content].append({
                "func": fx, "exact": final_exact, "lower": lower, "execute_bot": execute_bot
            })
            return fx
        return Decorator
    @classmethod
    def on_message(cls):
        """
        ### 🇹🇷 [TR] Genel Mesaj İzleyici
        Tüm mesajları dinleyen fonksiyonları 'liste'ye ekler.
        
        ### 🇺🇸 [EN] Global Message Watcher
        Appends functions listening to all messages to the 'list'.
        """
        def Decorator(func: Callable):
            kickbot._on_message_tasks.append(func)
            return func
        return Decorator
    @classmethod
    def on_ready(cls):
        """
        ### 🇹🇷 [TR] Hazır Olma Görevleri
        Bot açıldığında çalışacak görevleri listeye ekler.
        
        ### 🇺🇸 [EN] On Ready Tasks
        Appends tasks to execute when bot is ready to the list.
        """
        def Decorator(func: Callable):
            kickbot._on_ready_tasks.append(func)
            return func
        return Decorator
    @classmethod
    def timer_task(cls, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        ### 🇹🇷 [TR] Zamanlanmış Görevler
        Periyodik görevleri paketleyip listeye ekler.
        """
        def Decorator(fx: Callable):
            total_time = (hours * 3600) + (minutes * 60) + seconds
            if total_time > 0:
                kickbot._timer_tasks.append({"func": fx, "interval": total_time})
            return fx
        return Decorator
    ## ⚓
    @classmethod
    def on_rewards_redemption(cls,title:str):
        def Decorator(fx: Callable):
            title_lower = title.lower()
            if title_lower not in kickbot._reward_handlers:
                kickbot._reward_handlers[title_lower] = []
            kickbot._reward_handlers[title_lower].append({"func":fx})
            return fx 
        return Decorator
 
    # ⚓
class kickbot:
    _commands: Dict[str, list] = {}           
    _message_handlers: Dict[str, list] = {}    
    _timer_tasks: list = [] 
    _on_message_tasks: list = []              
    _on_ready_tasks: list = []
    _reward_handlers: Dict[str, list] = {}
    
    # ⚓ GEREKSİZ DEĞİŞKENLER SİLİNDİ, SADECE TEMEL TAŞLAR KALDI
    user_name: str = ""
    bearer_token: str = ""
    app_key: str = ""
    cluster: str = "us2"
    prefix: str = "!"

    def __init__(self, user_name, bearer_token, **kwargs): # ⚓ channel_name parametresi silindi!
        _raw_lang = kwargs.get("framework_lang", "en")
        if not isinstance(_raw_lang, str):
            print(f"[❌] [ERROR/HATA] framework_lang must be a string! | framework_lang bir metin (string) olmalı! (Provided/Verilen: {type(_raw_lang).__name__})")
            sys.exit(1)
        zerror.lang = _raw_lang.lower()
        
        def __validate(param_value, expected_types: list, param_name: Optional[str] = "",param_name_tr: Optional[str] = "",param_name_en: Optional[str]=""):
            is_invalid_bool = isinstance(param_value, bool) and bool not in expected_types
            if not any(isinstance(param_value, t) for t in expected_types) or is_invalid_bool:
                _is_tr = zerror.lang.lower() == "tr"
                _sep = " veya " if _is_tr else " or "
                _final_name = (param_name_tr if _is_tr else param_name_en) if param_name == "" else param_name
                types_str = _sep.join([t.__name__ for t in expected_types])
                zerror.log(level="error", 
                           msg_tr=f"{_final_name} şu tiplerden biri olmalı: {types_str}! (Verilen: {type(param_value).__name__})", 
                           msg_en=f"{_final_name} must be one of these: {types_str}! (Provided: {type(param_value).__name__})")
                zerror.log(level="warn", msg_tr=f"Çıkış yapılıyor...", msg_en=f"Exiting...")
                sys.exit(1)
                
        __validate(user_name,[str],param_name_tr="Kullanıcı Adı",param_name_en="User Name"); self.user_name = user_name.lower()
        __validate(bearer_token, [str], param_name="Bearer Token"); _bt = bearer_token.strip(); self.bearer_token = f"Bearer {_bt[7:].strip()}" if _bt.lower().startswith("bearer ") else f"Bearer {_bt}"
        
        if "prefix" in kwargs: 
            _val = kwargs.get("prefix","!") 
            __validate(_val,[str,int], param_name="Prefix")
            self.prefix = _val
        else:
            self.prefix = '!'
            
        if "cluster" in kwargs: 
            _val = kwargs.get("cluster","us2")
            __validate(_val,[str],param_name="Cluster")
            self.cluster = _val
        else:
            self.cluster = "us2"
            
        if "display_live_chat" in kwargs: 
            _val = kwargs.get("display_live_chat",True)
            __validate(_val,[bool],param_name="DisplayLiveChat")
            self.display_live_chat = _val
        else:
            self.display_live_chat = True
            
        if "display_bot_messages" in kwargs: 
            _val = kwargs.get("display_bot_messages",True)
            __validate(_val,[bool],param_name="DisplayBotMessages")
            self.display_bot_messages = _val
        else:
            self.display_bot_messages = True
            
        if "filter_bot_messages" in kwargs: 
            _val = kwargs.get("filter_bot_messages",True)
            __validate(_val,[bool],param_name="filter_bot_messages")
            self.filter_bot_messages = _val
        else:
            self.filter_bot_messages = True
            
        if "app_key" in kwargs: 
            _val = kwargs.get("app_key",False)
            __validate(_val,[str,int],param_name="App Key")
            self.app_key = _val
        else: 
            self.app_key = 0
            
        # ⚓ SADECE BOŞ FİLO SÖZLÜĞÜ KALDI (Kullanıcı add_channel ile dolduracak)
        self.channels: Dict[str, 'channel_context'] = {}
    # --- ⭐ SARI METODLAR (Yıldızlı Yetenekler) ---

    """"""

    def add_channel(self,name:str,channel_id:int,chat_id:int):
        channel = channel_context(self,name,channel_id,chat_id)
        self.channels[name.lower()] = channel
        self.channels[str(channel_id)] = channel
        self.channels[str(chat_id)] = channel 
        zerror.log(level="note", msg_tr=f"Yeni kanal eklendi: {name}")
        return channel
    def _get_channel(self,identifier) -> Optional['channel_context']:
        return self.channels.get(str(identifier).lower())
    def find_channel(self, identifier) -> Optional['channel_context']:
        """Kanalı isminden veya ID'sinden bulup objesini döndürür (get_channel ile aynıdır)."""
        return self._get_channel(identifier)
    
    """"""

    def command(self, name: str = None, *, lower: bool = True, execute_bot: bool = False):
        """
        ### 🇹🇷 [TR] Komut Kaydedici
        Prefix (örn: !) ile başlayan tetikleyicileri bir listeye ekler. 
        Aynı isimde birden fazla fonksiyon tanımlanabilir.

        ### 🇺🇸 [EN] Command Registerer
        Registers triggers starting with a prefix (e.g., !) into a list.
        Multiple functions can be defined under the same command name.

        ---
        **Args:**
        - name (str): 🇹🇷 Komut ismi (örn: 'selam'). Boş bırakılırsa fonksiyon adını alır. / 🇺🇸 Command name.
        - lower (bool): 🇹🇷 True ise '!SELAM' ve '!selam' aynı kabul edilir. / 🇺🇸 Case insensitivity.
        - execute_bot (bool): 🇹🇷 Botların bu komutu kullanmasına izin verir. / 🇺🇸 Allows bots to trigger this.
        """
        return decorators.command(name, lower=lower, execute_bot=execute_bot)

    def message(self, content: str, *, exact: bool = None, lower: bool = True, execute_bot: bool = False):
        """
        ### 🇹🇷 [TR] Kelime/Mesaj İzleyici Kaydedici
        Belirli bir kelime veya cümle chate yazıldığında tetiklenecek fonksiyonları kaydeder.
        
        ### 🇺🇸 [EN] Word/Message Watcher Registerer
        Registers functions to be triggered when a specific word or phrase is typed in chat.

        ---
        **Args:**
        - content (str): 🇹🇷 Takip edilecek kelime. / 🇺🇸 Word to follow.
        - exact (bool): 🇹🇷 Tam eşleşme mi? (True: Sadece 'sa', False: 'sa nasılsın' içinde de yakalar). / 🇺🇸 Exact match?
        - lower (bool): 🇹🇷 Büyük/küçük harf duyarsızlığı. / 🇺🇸 Case insensitivity.
        - execute_bot (bool): 🇹🇷 Bot mesajları bu izleyiciyi tetiklesin mi? / 🇺🇸 Should bot messages trigger this?
        """
        return decorators.message(content, exact, lower, execute_bot)

    def on_message(self):
        """
        ### 🇹🇷 [TR] Genel Mesaj İzleyici Kaydedici
        Gelen her mesajda (komut olsun ya da olmasın) çalışacak fonksiyonları bir listeye ekler.
        Artık birden fazla genel izleyici tanımlayabilirsiniz.

        ### 🇺🇸 [EN] Global Message Watcher Registerer
        Appends functions to a list that will execute on every incoming message 
        (whether it's a command or not). Multiple global watchers can now be defined.
        
        ---
        **Args:** (Yok / None)
        """
        return decorators.on_message()

    def on_ready(self):
        """
        ### 🇹🇷 [TR] Hazır Olma Görevi Kaydedici
        Bot Kick sunucularına başarıyla bağlandığında çalışacak fonksiyonları listeye ekler.
        Artık birden fazla 'on_ready' fonksiyonu tanımlayabilirsiniz.

        ### 🇺🇸 [EN] On Ready Task Registerer
        Appends functions to a list that will execute once the bot successfully 
        connects to Kick servers. Multiple 'on_ready' functions can now be defined.
        
        ----
        **Args:** (None / Yok)
        """
        return decorators.on_ready()

    def timer_task(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        """
        ### 🇹🇷 [TR] Zamanlanmış Görev Kaydedici
        Belirlenen saat, dakika veya saniye aralıklarıyla sürekli çalışacak fonksiyonları listeye ekler.
        
        ### 🇺🇸 [EN] Scheduled Task Registerer
        Appends functions to a list that will execute repeatedly at defined 
        hour, minute, or second intervals.

        ---
        **Args:**
        - hours (int): 🇹🇷 Kaç saatte bir çalışsın? / 🇺🇸 Every X hours.
        - minutes (int): 🇹🇷 Kaç dakikada bir çalışsın? / 🇺🇸 Every X minutes.
        - seconds (int): 🇹🇷 Kaç saniyede bir çalışsın? / 🇺🇸 Every X seconds.
        """
        return decorators.timer_task(hours, minutes, seconds)
    
    """"""

    def on_rewards_redemption(self,title:str):
        return decorators.on_rewards_redemption(title=title)

   
    r"""
    ### 🛡️ [DEPRECATED / V2.0] - Emekli Metodlar (Legacy Methods)
    
    🇹🇷 [TR] Aşağıdaki `__fetch_chat_id` ve `__fetch_app_key` metodları, Kick'in Cloudflare korumasını 
    artırması ve dinamik yapıya geçmesi nedeniyle v2.0 sürümüyle birlikte emekli edilmiştir. 
    Bağlantı kararlılığı için `chat_id` ve `app_key` parametrelerinin manuel girilmesi zorunludur.

    🇺🇸 [EN] The following `__fetch_chat_id` and `__fetch_app_key` methods have been deprecated 
    with v2.0 due to enhanced Cloudflare protections and Kick's dynamic infrastructure. 
    For connection stability, `chat_id` and `app_key` parameters must now be provided manually.
    

    @classmethod
    async def __fetch_chat_id(cls) -> bool:
        ---
        ### 🇹🇷 [TR] Gizli Koordinat Belirleyici (Name Mangling)
        Hedef kanalın (`channel_name`) Kick API üzerindeki benzersiz sohbet odası kimliğini (Chat ID) bulur.
        Bu metod çift alttan tire (`__`) ile korunmaktadır, sınıf dışından doğrudan erişilemez.

        ### 🇺🇸 [EN] Private Coordinate Resolver
        Fetches the unique chatroom ID for the target `channel_name` via Kick API.
        Protected by name mangling (`__`), preventing direct external access.
        ---
        __url = f"https://kick.com/api/v1/channels/{cls.channel_name}"
        __headers = {
            "accept": "application/json",
            "authorization": cls.bearer_token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
            "referer": "https://kick.com/"
        }
        Zerror.log(level="warn",msg_tr="Chat id tanımlanmamış, otomatik olarak alınıyor...",msg_en="Chat id is undefined, fetching...")
        try:
            async with aiohttp.ClientSession(headers=__headers) as __session:
                async with __session.get(__url) as __resp:
                    if __resp.status == 200:
                        __data = await __resp.json()
                        cls.chat_id = __data.get("chatroom", {}).get("id")
                        if cls.chat_id:
                            Zerror.log(level="succ", 
                                       msg_tr=f"Chat ID başarıyla alındı: {cls.chat_id} | İPUCU: Botun daha hızlı başlaması için bu ID'yi 'chat_id' parametresine manuel ekle!", 
                                       msg_en=f"Chat ID fetched: {cls.chat_id} | HINT: To run the bot faster, define this ID manually to the 'chat_id' parameter!")
                            return True
                    Zerror.log(level="error", 
                               msg_tr=f"Chat ID alınırken bir hata oluştu! Sunucu yanıtı: {__resp.status}", 
                               msg_en=f"An error occurred while fetching Chat ID! Server response: {__resp.status}")
                    return False
        except Exception as __e:
            Zerror.log(level="error", 
                        msg_tr=f"Chat ID alınırken kritik bir hata oluştu: {__e}", 
                        msg_en=f"A critical error occurred while fetching Chat ID: {__e}")
            return False
    @classmethod
    async def __fetch_app_key(cls) -> Optional[str]:
        ---
        ### 🇹🇷 [TR] Dinamik Anahtar Avcısı
        Kick'in ana sayfasındaki JavaScript chunk'larını tarayarak güncel Pusher 
        App Key'i (anahtarı) bulur ve geri döndürür.

        ### 🇺🇸 [EN] Dynamic Key Hunter
        Fetches the current Pusher App Key by scanning JavaScript chunks 
        on Kick's main page and returns it.
        ---
        _base_url = "https://kick.com"
        # Tarayıcı gibi görünmek için maske takıyoruz
        _headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        Zerror.log(level="warnn", 
                   msg_tr="App Key tanımlanmamış; güncel anahtar JavaScript paketleri içinde aranıyor...", 
                   msg_en="App Key is undefined; searching for current key within JavaScript chunks...")
        try:
            async with aiohttp.ClientSession(headers=_headers) as _session:
                # 1. Ana sayfaya sızıp HTML iskeletini alıyoruz
                async with _session.get(_base_url, timeout=10) as _resp:
                    if _resp.status != 200:
                        Zerror.log(level="error", 
                                   msg_tr=f"Kick ana sayfasına ulaşılamadı! Durum kodu: {_resp.status}", 
                                   msg_en=f"Could not reach Kick main page! Status code: {_resp.status}")
                        return None
                    _html = await _resp.text()

                # 2. HTML içindeki tüm .js dosyalarını (chunk'ları) buluyoruz
                _scripts = re.findall(r'src="([^"]+\.js)"', _html)
                
                for _script_url in _scripts:
                    # Kısa yolları tam URL'ye çeviriyoruz
                    if not _script_url.startswith('http'):
                        _script_url = f"{_base_url}{_script_url}"
                    
                    # Sadece potansiyel hazine olan 'chunks' klasörüne bakıyoruz
                    if "_next/static/chunks/" in _script_url:
                        try:
                            async with _session.get(_script_url, timeout=5) as _s_resp:
                                if _s_resp.status == 200:
                                    _js_content = await _s_resp.text()
                                    
                                    # Nokta atışı: NEXT_PUBLIC_PUSHER_KEY kalıbını arıyoruz
                                    _match = re.search(r'NEXT_PUBLIC_PUSHER_KEY\s*:\s*"([^"]+)"', _js_content)
                                    if _match:
                                        _found_key = _match.group(1)
                                        Zerror.log(level="succ", 
                                                   msg_tr=f"App Key başarıyla yakalandı: {_found_key} | İPUCU: Daha hızlı açılış için bu anahtarı 'app_key' parametresine manuel ekle!", 
                                                   msg_en=f"App Key captured: {_found_key} | HINT: To start the bot faster, provide this key manually to the 'app_key' parameter!")
                                        return _found_key
                        except:
                            continue # Bir dosya okunamazsa pes etme, sonrakine geç
                            
        except Exception as _e:
            Zerror.log(level="error", 
                       msg_tr=f"App Key avı sırasında kritik bir hata oluştu: {_e}", 
                       msg_en=f"A critical error occurred during App Key hunt: {_e}")
        return None
    """

    """"""

    async def send_message(self, content: str, identifier=None):
        """
        ### 🇹🇷 [TR] Genel Mesaj Gönderme / 🇺🇸 [EN] Global Message Sender
        Belirtilen kanala (isim veya ID ile) veya varsayılan (ilk eklenen) kanala mesaj gönderir.
        """
        # Eğer özel bir tanımlayıcı (İsim veya ID) verilmişse o kanalı bul
        if identifier:
            target_channel = self._get_channel(identifier)
        else:
            # Belirtilmemişse, listeye eklenen ilk kanalı seç (Ana kanal)
            target_channel = next(iter(self.channels.values())) if self.channels else None

        if target_channel:
            return await target_channel.send(content)
        
        zerror.log(level="error", 
                   msg_tr=f"[{identifier}] adında/ID'sinde bir kanal bulunamadı! add_channel() ile eklediğine emin ol.", 
                   msg_en=f"No channel found with identifier [{identifier}]! Make sure you added it with add_channel().")
        return False

    """"""

    async def __start(self):
        try:
            colorama.init(autoreset=True)      
            await tasks.check(self)
            await tasks.run_ready_funcs(self)
            await tasks.run_timer_tasks(self)
            zerror.log(level="succ", msg_tr=f"KickZero Framework Aktif! (Kaptan: {self.user_name})", msg_en=f"KickZero Framework Active! (Captain: {self.user_name})")
            while True:
                try:
                    async with engine.connect(self) as websocket:
                        await engine.subscribe_all(self,websocket)
                        while True:
                            await engine.process_all_events(self,websocket)

                except Exception as e:
                    zerror.log(level="warn", msg_tr=f"Bağlantı koptu, 5sn sonra tekrar bağlanılıyor: {e}", msg_en=f"Connection lost, reconnecting in 5s: {e}")
                    await asyncio.sleep(5)
        
        except KeyboardInterrupt:
            print("\n") 
            zerror.log(level="warn", msg_tr="Bot durduruluyor...", msg_en="Bot stopping...")
            sys.exit(0)
            return
        except Exception as e:
            zerror.log(level="error", msg_tr=f"Kritik Başlatma Hatası: {e}", msg_en=f"Critical Startup Error: {e}")
    def run(self):
        try:
            asyncio.run(self.__start())
        except KeyboardInterrupt:
            zerror.log(
                level="note", 
                msg_tr=f"{Fore.MAGENTA}Bot durduruldu.", 
                msg_en=f"{Fore.MAGENTA}Bot has been stopped."
            )
            pass
        except Exception as e:
            zerror.log(level="error", 
                       msg_tr=f"Bot başlatılırken beklenmedik bir hata: {e}", 
                       msg_en=f"Unexpected error while starting the bot: {e}")