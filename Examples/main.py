import asyncio
from KickZero import KickBot  # Hazırladığımız modülü içe aktarıyoruz

# --- AYARLAR ---
# GitHub'a yüklerken buraları boş bırakmayı unutma!
USER_NAME = "BOT_KULLANICI_ADI"
APP_KEY = "KICK_APP_KEY" # Pusher App Key
CLUSTER = "Cluster Seçimi"          # Genelde us2 olur
CHAT_ID = "KANAL ID NUMARAN"     # Kanal ID numaran
TOKEN = "BEARER_TOKEN"   # Edge'den aldığın token (Bearer yazmana gerek yok, modül ekliyor)

# Botu oluşturuyoruz
bot = KickBot(
    user_name=USER_NAME,
    app_key=APP_KEY,
    cluster=CLUSTER,
    chat_id=CHAT_ID,
    bearer_token=TOKEN,
    prefix="!",
    live_chat=True # Konsolda mesajları görmek için True kalsın
)

# --- KOMUTLAR ---

@bot.command(name="selam")
async def selamla(ctx, args):
    """Basit bir selamlaşma komutu"""
    await ctx.reply("Aleykümselam! Zoro nöbette! ⚔️")

@bot.command(name="zar")
async def zar_at(ctx, args):
    """1-6 arası rastgele sayı atar"""
    import random
    sayi = random.randint(1, 6)
    await ctx.reply(f"🎲 {sayi} attın!")

# --- ETKİNLİKLER (EVENTS) ---

@bot.on_message()
async def her_mesaj(ctx):
    """Gelen her mesajı yakalar (Botun kendi mesajları hariç)"""
    if "zoro" in ctx.content.lower():
        print(f"🔔 Birisi Zoro'dan bahsetti: {ctx.author}")

# --- BAŞLATICI ---
if __name__ == "__main__":
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n⚔️ Zoro kınına geri dönüyor... (Bot kapatıldı)")