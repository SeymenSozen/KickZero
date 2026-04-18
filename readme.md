# 🏴‍☠️ KickZero Framework (v1.3.1)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Proprietary-red)
![Maintainer](https://img.shields.io/badge/maintainer-Seymen%20S%C3%B6zen-orange)

**KickZero**, Kick.com platformu için geliştirilmiş, modüler ve tamamen asenkron bir chatbot framework'üdür. Geliştiricilere karmaşık WebSocket trafiğiyle uğraşmadan, hızlı ve güçlü botlar üretme imkanı sağlar.

---

## 🚀 Özellikler / Features

- **Asynchronous Engine:** `asyncio` ve `aiohttp` tabanlı, donma yapmayan hızlı yapı.
- **Multi-Channel Support:** Aynı anda birden fazla kanalı tek bir botla yönetme.
- **Easy Decoration:** `@bot.command`, `@bot.message` ve `@bot.timer_task` dekoratörleri ile kolay geliştirme.
- **Smart Context:** Mesajın yetki, renk ve içerik bilgilerine tek noktadan (`ctx`) erişim.
- **Reward Integration:** Kanal puanı (Reward) kullanımlarını anında yakalama.

---

## 📦 Kurulum / Installation

Terminalinize şu komutu yazarak okyanusa açılabilirsiniz:

```bash
pip install kickzero