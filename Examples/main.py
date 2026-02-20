import asyncio
from colorama import Fore
from KickZero import KickBot, Context # Framework dosyanızın adı KickZero.py olmalı

# 1. Amiral Gemisini Hazırla
Zoro = KickBot(
    user_name="",
    app_key="",
    chat_id=0,
    bearer_token="Bearer id|token",
    prefix="!",
    framework_lang="tr"
)

# --- [ ORDU TESTİ 1: Çoklu on_ready ] ---
@Zoro.on_ready()
async def sistem_selami():
    print(f"{Fore.GREEN}⚔️ [SİSTEM] Zoro birinci kılıcını çekti!")

@Zoro.on_ready()
async def veritabani_selami():
    print(f"{Fore.CYAN}⚔️ [SİSTEM] Zoro ikinci kılıcını çekti! (Paralel Başlatma Başarılı)")

# --- [ ORDU TESTİ 2: Çoklu on_message ] ---
@Zoro.on_message()
async def radar_izleyici(ctx: Context):
    if not ctx.is_bot:
        print(f"{Fore.YELLOW}[RADAR]: {ctx.author} tarafından bir mesaj algılandı.")

@Zoro.on_message()
async def log_izleyici(ctx: Context):
    if not ctx.is_bot:
        print(f"{Fore.MAGENTA}[LOG]: '{ctx.content}' mesajı kayıt altına alındı.")

# --- [ ORDU TESTİ 3: Çoklu Komut Tetikleme ] ---
@Zoro.command(name="ping")
async def ping_savunma(ctx: Context):
    await ctx.reply("Pong! (Savunma Hattı Aktif) 🏓")

@Zoro.command(name="ping")
async def ping_arka_plan(ctx: Context):
    print(f"{Fore.RED}>> Arka Planda !ping istatistiği işleniyor...")

# --- [ ORDU TESTİ 4: Çoklu Kelime Takibi ] ---
@Zoro.message("sa", exact=True)
async def selam_karsilama(ctx: Context):
    await ctx.reply("Aleykümselam tayfaya hoş geldin! ⚔️")

@Zoro.message("sa", exact=True)
async def selam_kayit(ctx: Context):
    print(f"{Fore.BLUE}>> {ctx.author} için selamlama görevi tamamlandı.")

# --- [ TEST 5: Esnek Takip ve Argümanlar ] ---
@Zoro.command(name="DUEL", lower=False)
async def buyuk_duel(ctx: Context, args):
    hedef = " ".join(args) if args else "herkes"
    await ctx.reply(f"KAPTAN BAĞIRARAK DÜELLO İSTEDİ! Hedef: {hedef} ⚔️🔥")

@Zoro.message("nasılsın", exact=False)
async def hal_hatir(ctx: Context, args):
    hitap = " ".join(args) if args else "dostum"
    await ctx.reply(f"Bir samuray her zaman tetiktedir, sen nasılsın {hitap}?")

# --- [ TEST 6: Zamanlanmış Görev Ordusu ] ---
@Zoro.timer_task(seconds=30)
async def kisa_devriye():
    print(f"{Fore.YELLOW}>> [TIMER] 30 saniyelik çevre kontrolü yapıldı.")

@Zoro.timer_task(minutes=2)
async def uzun_devriye():
    await Zoro.send_message("Zoro 2 dakikadır nöbette, ufukta düşman görünmüyor... 🏯")

# 2. Yelkenler Fora!
if __name__ == "__main__":
    try:
        asyncio.run(Zoro.__start())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🛑 Zoro kılıcını kınına soktu, limana dönüyor. (CTRL+C)")