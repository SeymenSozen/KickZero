import asyncio
import random
from kickzero import kickbot, message_context, points_context

# --- ⚓ AMİRAL GEMİSİ AYARLARI ---
Zoro = kickbot(
    user_name="BOT_NAME",
    bearer_token="TOKEN_BURAYA",
    app_key='APP_KEY_BURAYA',
    prefix="!",
    framework_lang="tr" # Hata ve loglar Türkçe gelsin
)

# --- 📡 ÇOKLU KANAL DESTEĞİ ---
# Botu aynı anda birden fazla gemiye (kanala) radar olarak ekleyebilirsin
Zoro.add_channel(name="ana_kanal", channel_id="111111", chat_id="222222")
Zoro.add_channel(name="ikinci_kanal", channel_id="333333", chat_id="444444")

# --- 🛡️ YETKİ KONTROLÜ ÖRNEĞİ ---
@Zoro.command(name="ban")
async def ban_komutu(ctx: message_context, args):
    # Sadece yayıncı ve moderatörler bu komutu kullanabilsin
    if not (ctx.is_broadcaster or ctx.is_mod):
        await ctx.reply("❌ Bu komutu kullanmak için yetkin yok, tayfaya geri dön!")
        return

    if args:
        target = args[0]
        await ctx.send(f"⚔️ {target} kaptanın emriyle gemiden atıldı (Banlandı)!")
        #V3.2 ile gelicek 
    else:
        await ctx.reply("❓ Kimi banlayacağımı söylemedin kaptan!")

# --- 💎 KANAL PUANI (REWARD) YAKALAYICI ---
# Kick panelinde belirlediğin ödül ismiyle birebir aynı olmalı
@Zoro.on_rewards_redemption(title="Işıkları Kapat")
async def isik_odulu(rctx: points_context):
    print(f"🔥 Ödül Tetiklendi: {rctx.username} ışıkları kapattı!")
    # r_ctx üzerinden kanala özel mesaj gönderebilirsin
    await rctx.send(f"💡 @{rctx.username} ödülü kullandı, ortalık karardı!")

@Zoro.on_rewards_redemption(title="Şarkı İste")
async def sarki_istegi(rctx: points_context):
    if rctx.input:
        await rctx.reply(f"🎶 İstediğin '{rctx.input}' şarkısı listeye eklendi!")
    else:
        await rctx.reply("⚠️ Şarkı ismi yazmayı unuttun!")

# --- 🔄 GENEL MESAJ İZLEYİCİ (LOGLAMA) ---
@Zoro.on_message()
async def mesaj_kaydedici(ctx: message_context):
    # Botun kendi mesajlarını kaydetme (sonsuz döngü olmasın)
    if ctx.is_bot:
        return
    
    # Tüm chat trafiğini arkada bir dosyaya yazabilirsin
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"[{ctx.channel.name}] {ctx.author}: {ctx.content}\n")

# --- ⏱️ GELİŞMİŞ ZAMANLAYICI (DATABASE UPDATE SİMÜLASYONU) ---
@Zoro.timer_task(hours=1)
async def veritabani_yedekle():
    # Bu görev parametre (ctx) almaz, sistem görevidir
    print("💾 Veritabanı yedeği alınıyor...")
    await asyncio.sleep(2)
    print("✅ Yedekleme tamamlandı.")

# --- ⚓ HAZIR OLDUĞUNDA ÇALIŞACAK GÖREVLER ---
@Zoro.on_ready()
async def bot_basladi():
    print("🚢 Zoro okyanusa açıldı, radar aktif!")
    # Belirli bir kanala bot açıldı mesajı atalım
    ana_gemi = Zoro.find_channel("ana_kanal")
    if ana_gemi:
        await ana_gemi.send("⚓ Zoro Bot v1.3.1 artık görevinin başında!")

if __name__ == "__main__":
    Zoro.run()