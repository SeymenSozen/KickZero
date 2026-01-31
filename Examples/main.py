import asyncio
import random
from KickZero import KickBot

# --- BOT AYARLARI ---
# Not: Bilgilerinizi buraya girmeyi unutmayın!
Zoro = KickBot(
    user_name="BOT_ADINIZ",
    app_key="PUSHER_KEY",
    cluster="us2",
    chat_id="KANAL_ID",
    bearer_token="Bearer TOKEN_BURAYA",
    prefix="!",
    live_chat=True
)

# --- 1. KOMUTLAR (@Zoro.command) ---
# Prefix ile tetiklenen fonksiyonlar (örn: !zar).

@Zoro.command(name="zar")
async def zar_at(ctx, args):
    """🎲 Rastgele sayı atar."""
    sayi = random.randint(1, 6)
    await ctx.reply(f"Zar atıldı: {sayi}")

@Zoro.command(name="say")
async def soyle(ctx, args):
    """🗣️ Yazdığınız kelimeleri bota söyletir."""
    mesaj = " ".join(args) if args else "Ne dememi istersin kaptan?"
    await ctx.reply(mesaj)

# --- 2. ÖZEL MESAJ TEPKİLERİ (@Zoro.message) ---
# Prefix olmadan belirli kelimelere tepki verir.

@Zoro.message(content="sa", exact=True)
async def selam(ctx):
    """Sadece 'sa' yazıldığında tetiklenir."""
    await ctx.reply("Aleykümselam hoş geldin!")

@Zoro.message(content="zoro", exact=False)
async def zoro_nida(ctx):
    """Cümle içinde 'zoro' geçtiği her an tetiklenir."""
    await ctx.reply("Biri kılıç ustasını mı çağırdı? ⚔️")

# --- 3. ZAMANLANMIŞ GÖREVLER (@Zoro.timer_task) ---
# v1.1 Yeni Özelliği: Belirli aralıklarla arka planda çalışır.

@Zoro.timer_task(minutes=5)
async def otomatik_duyuru(ctx):
    """Her 5 dakikada bir chate rastgele duyuru atar."""
    duyurular = [
        "⚓ Yayını beğenmeyi unutmayın!",
        "🏴‍☠️ Discord sunucumuza bekleriz!",
        "🍶 Zoro sake içmeye gitti, hemen gelecek."
    ]
    await ctx.send_message(random.choice(duyurular))

@Zoro.timer_task(hours=1)
async def saatlik_hatirlatici():
    """Parametresiz (ctx olmadan) kullanım örneği."""
    print("⏰ Bir saatlik yayın süresi doldu!")

# --- 4. ETKİNLİKLER (EVENTS) ---

@Zoro.on_ready()
async def hazirim():
    """Bot bağlandığında çalışır."""
    print(f"{Zoro.user_name} v1.1 limandan ayrılmaya hazır! ⚔️")

@Zoro.on_message()
async def log_kaydi(ctx):
    """Her mesajda terminale log basar."""
    if not ctx.author.lower() == Zoro.user_name:
        print(f"📁 Kayıt: {ctx.author} -> {ctx.content}")

# --- BAŞLATICI ---
if __name__ == "__main__":
    try:
        # v1.1 Başlatıcı: Pylance hatalarını önleyen en stabil yöntem
        asyncio.run(Zoro.start())
    except KeyboardInterrupt:
        print("\n⚔️ Zoro kınına geri dönüyor... (Bot kapatıldı)")