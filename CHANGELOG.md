# ⚔️ Kick Zero Seyir Defteri (Changelog)

Tüm önemli değişiklikler bu dosya altında kronolojik olarak listelenmektedir.

---

## [1.1.0] - 2026-01-31
### 🚀 v1.1 - The Great Timer Update |

Bu sürümle birlikte framework, statik bir bot yapısından dinamik görev yönetimine geçiş yapmıştır.

### ✨ Yeni Özellikler
* **`timer_task` Dekoratörü**: Arka planda belirli zaman aralıklarıyla (saat, dakika, saniye) çalışan fonksiyonlar tanımlama yeteneği eklendi.
* **Akıllı Fonksiyon İmzası**: Fonksiyonların `ctx` (Context) parametresi alıp almadığı `inspect` kütüphanesi ile otomatik analiz edilir hale getirildi.
* **Özel Tip Belirlemeleri**: `MesajFonksiyonu` gibi tip takma adları (Type Aliases) kullanılarak geliştirici deneyimi ve VS Code IntelliSense desteği artırıldı.

### 🛠️ İyileştirmeler & Düzeltmeler
* **Mimaride Mantık Güncellemesi**: Zamanlayıcıların her mesajda tekrar başlamasına neden olan döngü hatası giderildi; artık bot başlatıldığında (`start`) bir kez kurulur.
* **Güvenlik Kontrolleri**: Toplam süresi 0 olan görevlerin başlatılması engellendi ve terminale uyarı (Warning) logları eklendi.
* **Kod Temizliği**: `message` argümanı dekoratörden kaldırıldı; artık mesaj gönderme işlemi tamamen fonksiyonun içindeki mantığa (ctx.send_message) bırakıldı.
* **Async Kararlılığı**: Başlatıcı (main) bloğunda karşılaşılan `asyncio` hataları için dökümantasyon ve `asyncio.run()` standardı getirildi.

---

## [1.0.0] - 2026-01-17
### ⚓ İlk Yelken Açılışı (Initial Release)
* Temel `KickBot` sınıfı oluşturuldu.
* `@command` ve `@message` dekoratörleri ile temel komut yapısı kuruldu.
* Pusher üzerinden Kick.com canlı sohbet bağlantısı sağlandı.