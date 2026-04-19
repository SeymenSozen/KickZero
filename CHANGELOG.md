# 📜 Değişim Günlüğü (Change Log)

Tüm önemli değişiklikler bu dosyada belgelenecektir.

---

## [1.3.2] - 2026-04-19 🏴‍☠️

### ⚓ Bağlantı ve Stabilite (Kritik Güncelleme)
- **Handshake Çözümü:** WebSocket bağlantısı sırasında yaşanan `timed out during opening handshake` hatası, `connect` fonksiyonu asenkron hale getirilerek ve `open_timeout` süresi 30 saniyeye çıkarılarak çözüldü.
- **Dinamik Yeniden Bağlanma:** Bağlantı koptuğunda veya zaman aşımına uğradığında botun çökmesini engelleyen `try-except` döngüsü eklendi. Bot artık 5 saniye bekleyip otomatik olarak tekrar deniyor.
- **Modern Asenkron Yapı:** Ana döngüdeki bağlantı yönetimi `async with await` protokolüne geçirilerek daha stabil ve sızıntısız (leak-proof) bir yapıya kavuşturuldu.


