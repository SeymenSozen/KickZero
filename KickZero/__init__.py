import asyncio
import aiohttp
import websockets
import json
import inspect
import colorama
import sys # sys mutlaka kalmalı
from typing import Optional, Dict, Callable, Any
from colorama import Fore, Style


if "kickzero" not in sys.modules:
    sys.modules["kickzero"] = sys.modules[__name__]

__all__ = ['KickBot', 'Context', 'Decorators']




## Preetier
class Zerror:
    print_errors: bool = True 
    print_warnns: bool = True 
    print_notes: bool = True
    print_success: bool = True
    print_error_emoji: bool = True 
    print_warnn_emoji: bool = True
    print_note_emoji: bool = True
    print_succes_emoji: bool = True
    print_messages: bool = True
    print_message_emoji: bool = True
    preety_print: bool = True
    use_emojis: bool = True
    use_colors: bool = True
    lang: str = "tr" 
    @classmethod
    def log(cls:'Zerror',level:str,msg_tr:str="",msg_en:str=""):
        emoji, color = "", ""
        if level.lower() in ["err" ,"error"] and not cls.print_errors : return  
        elif level.lower() in ["warn", "warning"] and not cls.print_warnns : return
        elif level.lower() in ["note", "not"] and not cls.print_notes  : return
        elif level.lower() in ["succ","success"] and not cls.print_success : return
        elif level.lower() in ["msg","mesaj","message"] and not cls.print_messages: return
        if cls.lang.lower() in ["tr","en"]: message = msg_tr if cls.lang.lower() == "tr" else msg_en
        else: print(f"{Fore.RED}[❌] {Style.BRIGHT}[Hata/Error] {Fore.WHITE}Dil tr veya en olarak seçilmeli / lan must be seleceted in tr or en{Style.RESET_ALL}"); return 
        if level.lower() in ["err" ,"error"]: 
            level = "hata" if cls.lang.lower() == "tr" else "error"
            emoji = "[❌] " if cls.use_emojis and cls.print_error_emoji else ""
            color = Fore.RED if cls.use_colors else ""
        elif level.lower() in ["warn", "warning"]:
            level = "uyarı" if cls.lang.lower() == "tr" else "warning"
            emoji = "[⚠️] " if cls.use_emojis and cls.print_warnn_emoji else ""
            color = Fore.YELLOW if cls.use_colors else ""
        elif level.lower() in ["succ", "success"]:
            level = "başarı" if cls.lang.lower() == "tr" else "success"
            emoji = "[✅] " if cls.use_emojis and cls.print_succes_emoji else ""
            color = Fore.GREEN if cls.use_colors else ""
        elif level.lower() in ["msg","mesaj","message"]:
            level = "mesaj" if cls.lang.lower() == "tr" else "message"
            emoji = "[💬] " if cls.use_emojis and cls.print_message_emoji else ""
        print(f"{color}{emoji}{Style.BRIGHT}[{level.upper()}] {Fore.WHITE}{message}{Style.RESET_ALL}") 

## Data Class
class Context:
    """
    ### 🇹🇷 [TR] Bağlam Merkezi (Context)
    Kick.com API'den gelen verileri, botun o anki çalışma durumuyla birleştirir.
    Bu sınıf; mesajın içeriğine, gönderen kişinin yetkilerine ve botun fonksiyonlarına 
    tek bir noktadan (`ctx`) erişim sağlar.

    ### 🇺🇸 [EN] Command Context
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
    - bot (KickBot): Ana bot sınıfına olan bağlantı. (Reference to main KickBot instance)
    - is_bot (bool): Bu mesajı botun kendisi mi attı? (Did the bot send this message?)
    
    ---
    ### ⚡ Metodlar / Methods:
    - reply(content): Kullanıcıyı etiketleyerek cevap verir. (Reply with mention)
    - send(content): Kanala düz metin gönderir. (Send plain text)
    """
    bot: 'KickBot'
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
    def __init__(self,data:dict,bot:'KickBot'): 
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
    async def reply(self,content: str):
        return await self.bot.send_message(f"@{self.author} {content}")
    async def send(self,content:str):
        return await self.bot.send_message(content)

class Events:
    """
    ### 🇹🇷 [TR] Olay Yöneticisi (Event Handler)
    Pusher/WebSocket üzerinden gelen ham verileri yakalar, işler ve botun 
    ilgili komut veya mesaj fonksiyonlarına dağıtır. 
    
    Bu sınıf, gelen verinin bir 'Mesaj', 'Bağış', veya 'Takip' olup olmadığını 
    anlayan merkezi bir santral görevi görür.

    ### 🇺🇸 [EN] Event Handler
    Intercepts raw data from Pusher/WebSocket, processes it, and dispatches it 
    to the bot's command or message functions. 
    Acts as a central switchboard to identify if the incoming data is a 
    'Message', 'Donation', or 'Follow'.

    ---
    ### ⚙️ Temel Görevler / Core Responsibilities:
    1. **Parsing (Ayrıştırma):** Ham JSON verisini parçalayarak `Message` objesine dönüştürür.
       *(Converts raw JSON data into a structured `Message` object.)*
       
    2. **Dispatching (Dağıtım):** Veriyi `on_message`, `@command` veya `@message` tetikleyicilerine gönderir.
       *(Routes data to `on_message`, `@command`, or `@message` triggers.)*
       
    3. **Filtering (Filtreleme):** Botun kendi mesajlarını veya istenmeyen içerikleri süzer.
       *(Filters out the bot's own messages or unwanted content.)*
       
    4. **Execution (Yürütme):** Komutları asenkron (asyncio) olarak, birbirini engellemeden çalıştırır.
       *(Executes commands asynchronously using asyncio without blocking the main loop.)*
    """
    @staticmethod
    async def HandleMessages(data:dict,bot:'KickBot'):
        """
        [TR] Gelen her mesajı analiz eden, raporlayan ve dağıtan ana motor.
        [EN] Main engine that analyzes, reports, and dispatches every incoming message.
        """
        ctx = Context(data, bot)
        if bot.display_live_chat:
            if not ctx.is_bot or bot.display_bot_messages:
                perms = " | ".join(ctx.badge_texts) if ctx.badge_texts else "Viewer"
                msg_log = f"{Fore.YELLOW}{ctx.author}{Fore.WHITE}: {ctx.content} {Fore.BLACK}({perms})"
                Zerror.log(level="message", msg_tr=msg_log, msg_en=msg_log)
        if not (bot.filter_bot_messages and ctx.is_bot):
            for watcher in bot._on_message_tasks:
                asyncio.create_task(Events.run_with_args(watcher, ctx, []))
        if ctx.author.lower() == bot.user_name.lower():
            return
        for trigger, configs in bot._message_handlers.items():
            for config in configs:
                if ctx.is_bot and not config.get("execute_bot", False):
                    continue
                is_lower = config.get("lower", True)
                msg_content = ctx.content.lower() if is_lower else ctx.content
                trig_content = trigger.lower() if is_lower else trigger
                is_triggered = False
                args = []
                if config.get("exact", True):
                    if msg_content == trig_content:
                        is_triggered = True
                        args = ctx.content.split()
                else:
                    if msg_content.startswith(trig_content):
                        is_triggered = True                          
                        trig_word_count = len(trig_content.split())
                        args = ctx.content.split()[trig_word_count:]
                if is_triggered:
                    asyncio.create_task(Events.run_with_args(config["func"], ctx, args))

        # --- 4. KOMUT TAKİBİ (command Kümesi) ---
        if ctx.content.startswith(bot.prefix):
            parts = ctx.content[len(bot.prefix):].split()
            if parts:
                cmd_raw = parts[0]
                cmd_lower = parts[0].lower()
                
                # Hem orijinal ismiyle hem küçük harf ismiyle kayıtlı komut ordusunu bul
                cmd_configs = bot._commands.get(cmd_raw, [])
                if cmd_lower != cmd_raw:
                    cmd_configs += bot._commands.get(cmd_lower, [])

                for cmd_info in cmd_configs:
                    # Bot izni ve kendi kendine komut tetikleme engeli
                    if ctx.is_bot and not cmd_info.get("execute_bot", False):
                        continue
                    
                    asyncio.create_task(Events.run_with_args(cmd_info["func"], ctx, parts[1:]))
    @staticmethod
    async def run_with_args(func, ctx, args):
        """
        ### 🇹🇷 [TR] Dinamik Fonksiyon Yürütücü
        Fonksiyonun beklediği parametre sayısını kontrol eder ve güvenle çalıştırır.
        - ctx: Bağlam (Context) objesi.
        - args: Mesajdan ayrıştırılan argüman listesi.

        ### 🇺🇸 [EN] Dynamic Function Executor
        Inspects the number of parameters the function expects and executes it safely.
        - ctx: The Context object.
        - args: List of arguments parsed from the message.
        """
        try:
            sig = inspect.signature(func)
            params_count = len(sig.parameters)
            
            if params_count == 2:
                await func(ctx, args)
            elif params_count == 1:
                await func(ctx)
            else:
                await func()
        except Exception as e:
            Zerror.log(level="error", msg_tr=f"{func.__name__} çalışırken hata oluştu: {e}", msg_en=f"Error while running {func.__name__}: {e}")
        
class Decorators:
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
            if CommandName not in KickBot._commands:
                KickBot._commands[CommandName] = []
            KickBot._commands[CommandName].append({"func": fx, "execute_bot": execute_bot})
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
            if content not in KickBot._message_handlers:
                KickBot._message_handlers[content] = []
            KickBot._message_handlers[content].append({
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
            KickBot._on_message_tasks.append(func)
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
            KickBot._on_ready_tasks.append(func)
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
                KickBot._timer_tasks.append({"func": fx, "interval": total_time})
            return fx
        return Decorator

class KickBot:
    _commands: Dict[str, list] = {}           # {} kalsın ama içi liste dolacak
    _message_handlers: Dict[str, list] = {}    # {} kalsın ama içi liste dolacak
    _timer_tasks: list = [] 
    _on_message_tasks: list = []               # _on_message_func yerine tasks yap
    _on_ready_tasks: list = []
    
    user_name: str = ""
    chat_id: int = 0
    bearer_token: str = ""
    app_key: str = ""
    cluster: str = "us2"
    prefix: str = "!"

    def __init__(self, user_name, app_key, chat_id, bearer_token, **kwargs):
        KickBot.user_name = user_name.lower()
        KickBot.app_key = app_key
        KickBot.chat_id = chat_id
        KickBot.bearer_token = bearer_token if bearer_token.startswith("Bearer ") else f"Bearer {bearer_token}"
        KickBot.prefix = kwargs.get("prefix", "!")
        KickBot.cluster = kwargs.get("cluster", "us2")
        
        self.display_live_chat = kwargs.get("display_live_chat", True)
        self.display_bot_messages = kwargs.get("display_bot_messages", True)
        self.filter_bot_messages = kwargs.get("filter_bot_messages", True)
        Zerror.lang = kwargs.get("framework_lang", "tr")

    # --- ⭐ SARI METODLAR (Yıldızlı Yetenekler) ---

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
        return Decorators.command(name, lower=lower, execute_bot=execute_bot)

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
        return Decorators.message(content, exact, lower, execute_bot)

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
        return Decorators.on_message()

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
        return Decorators.on_ready()

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
        return Decorators.timer_task(hours, minutes, seconds)
        

    @staticmethod
    async def send_message(content: str):
        """API üzerinden kanala mesaj gönderir."""
        url = f"https://kick.com/api/v2/messages/send/{KickBot.chat_id}"
        headers = {
            "Authorization": KickBot.bearer_token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {"content": str(content), "type": "message"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status not in [200, 201]:
                    Zerror.log(level="error", msg_tr=f"Mesaj gönderilemedi! Kick API Durumu: {resp.status}", msg_en=f"Failed to send message! Kick API Status: {resp.status}")
                return resp.status

    async def _run_timer_task(self, task):
        """Zamanlanmış görevleri arka planda koşturur."""
        while True:
            await asyncio.sleep(task["interval"])
            try:
                sig = inspect.signature(task["func"])
                # Eğer timer fonksiyonu 'ctx' bekliyorsa boş bir context göndeririz
                if len(sig.parameters) > 0:
                    fake_data = {"content": "Timer", "sender": {"username": "System"}}
                    await task["func"](Context(fake_data, self))
                else:
                    await task["func"]()
            except Exception as e:
                Zerror.log(level="warn", msg_tr=f"Timer Hatası ({task['func'].__name__}): {e}", msg_en=f"Timer Error ({task['func'].__name__}): {e}")
    async def start(self):
        """
        ### 🇹🇷 [TR] Motoru Ateşle
        Botu Kick sunucularına bağlar, tüm görev kümelerini (Ready & Timer) 
        asenkron olarak başlatır ve mesajları dinlemeye başlar.

        ### 🇺🇸 [EN] Fire Up the Engine
        Connects the bot to Kick servers, launches all task clusters (Ready & Timer) 
        asynchronously, and begins listening for messages.
        
        ---
        **Args:** (Yok / None)
        """
        uri = f"wss://ws-{KickBot.cluster}.pusher.com/app/{KickBot.app_key}?protocol=7&client=js&version=7.6.0"
        colorama.init(autoreset=True)
        Zerror.log(level="succ", msg_tr=f"KickZero Framework Aktif! (Kaptan: {KickBot.user_name})", msg_en=f"KickZero Framework Active! (Captain: {KickBot.user_name})")
        
        while True:
            try:
                async with websockets.connect(uri) as ws:
                    # 1. Kanala Abone Ol
                    await ws.send(json.dumps({
                        "event": "pusher:subscribe",
                        "data": {"channel": f"chatrooms.{KickBot.chat_id}.v2"}
                    }))
                    
                    # ⚓ 2. Bot Hazır Tetikleyicileri (Ordu Modu)
                    # Tek bir fonksiyon yerine listeye kayıtlı tüm samurayları göreve çağırıyoruz.
                    for ready_func in KickBot._on_ready_tasks:
                        asyncio.create_task(ready_func())
                    
                    # ⚓ 3. Zamanlanmış Görevleri Başlat
                    for task in KickBot._timer_tasks:
                        asyncio.create_task(self._run_timer_task(task))

                    # ⚓ 4. Ana Dinleme Döngüsü
                    while True:
                        raw = await ws.recv()
                        data = json.loads(raw)
                        
                        # Mesaj Geldiğinde
                        if data.get("event") == "App\\Events\\ChatMessageEvent":
                            inner_data = json.loads(data["data"])
                            # HandleMessages artık orduları kontrol eden merkezimiz.
                            asyncio.create_task(Events.HandleMessages(inner_data, self))
                        
                        # Sunucu Ping'ine Cevap Ver (Bağlantıyı canlı tutar)
                        elif data.get("event") == "pusher:ping":
                            await ws.send(json.dumps({"event": "pusher:pong"}))
                            
            except Exception as e:
                # 🛡️ Zırh: Bağlantı kopsa bile bot kapanmaz, 5 saniye bekleyip tekrar dener.
                Zerror.log(level="warn", msg_tr=f"Bağlantı koptu, 5sn sonra tekrar bağlanılıyor: {e}", msg_en=f"Connection lost, reconnecting in 5s: {e}")
                await asyncio.sleep(5)