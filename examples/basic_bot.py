import asyncio
import random
from kickzero import kickbot, message_context

# --- ⚓ KAPTANIN KONTROL PANELİ ---
# NOT: Kendi bilgilerinizi girmeyi unutmayın!
Zoro = kickbot(
    user_name="BOT_ADINIZ",
    bearer_token="TOKEN_BURAYA",
    app_key='APP_KEY_BURAYA',
    prefix="!",
    framework_lang="tr"
)

# Sosyal Medya Linkleri
SOCIAL_LINKS = {
    "twitch": "https://www.twitch.tv/",
    "kick": "https://kick.com/",
    "youtube": "https://www.youtube.com/",
    "donate": "https://donate.bynogame.com/",
    "instagram": "https://www.instagram.com/",
    "tiktok": "https://www.tiktok.com/"
}

# --- 📡 KANAL AYARLARI ---
# Botun dinleyeceği kanalı ekliyoruz
Zoro.add_channel(name="", channel_id="", chat_id="")

# --- 💬 MESAJ TETİKLEYİCİLERİ ---

@Zoro.message(content="sa")
async def ase(ctx: message_context):
    await ctx.reply("As helelelelele")

@Zoro.message(content="helelele", exact=False)
async def hele(ctx: message_context):
    await ctx.reply("helelelele")

# --- ⚔️ KOMUTLAR ---

@Zoro.command(name="donate")
async def donate(ctx: message_context):
    await ctx.reply(f"Bağış Linki ==> {SOCIAL_LINKS['donate']}")

@Zoro.command(name="twitch")
async def twitch(ctx: message_context):
    await ctx.reply(f"Twitch Linki ==> {SOCIAL_LINKS['twitch']}")

@Zoro.command(name="kick")
async def kick(ctx: message_context):
    await ctx.reply(f"Kick Linki ==> {SOCIAL_LINKS['kick']}")

@Zoro.command(name="youtube")
async def youtube(ctx: message_context):
    await ctx.reply(f"YouTube Linki ==> {SOCIAL_LINKS['youtube']}")

@Zoro.command(name="instagram")
async def instagram(ctx: message_context):
    await ctx.reply(f"Instagram Linki ==> {SOCIAL_LINKS['instagram']}")

# --- ⏱️ ZAMANLANMIŞ GÖREVLER (TIMERS) ---

@Zoro.timer_task(minutes=10)
async def tanitim(ctx: message_context):
    await ctx.send(f"Şu anda her yerde yayındayız! Takip etmeyi unutma! | !twitch ve !youtube yazarak linklere ulaşabilirsin!")

@Zoro.timer_task(minutes=15)
async def eglenme(ctx: message_context):
    mesajlar = [
        "Beleş izleme, bir donate at helelelele!",
        "Mega kutu açmamız lazım helelelele!"
    ]
    await ctx.send(random.choice(mesajlar))

# --- 🚀 GEMİYİ ATEŞLE ---
if __name__ == "__main__":
    Zoro.run()