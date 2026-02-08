Kaptan, seyir defterini tam istediğin gibi, GitHub ve diğer Markdown okuyucularında kusursuz görünecek şekilde hazırladım. Dosyanın adını CHANGELOG.md olarak kaydedebilirsin. ⚔️

Markdown

# ⚔️ KickZero Seyir Defteri (Changelog)

Tüm önemli değişiklikler bu dosya altında kronolojik olarak listelenmektedir.

---

## 🚀 [1.2.0] - 2026-02-08
### ⚔️ **v1.2 - The Great Army Update | Ordu Düzeni**

Bu sürümle birlikte **KickZero**, "tekil fonksiyon" yapısını tamamen terk ederek, her bir olaya (Event) birden fazla bağımsız görevin atanabildiği **Kümeleme (Clustering)** mimarisine geçiş yapmıştır.

### ✨ **Yeni Özellikler**
* ⭐ **Çoklu Fonksiyon Desteği (Event Clustering):** Aynı komut (`!ping`), aynı hazır olma anı (`on_ready`) veya aynı kelime tetikleyicisi (`sa`) için sınırsız sayıda fonksiyon tanımlama yeteneği eklendi. Tüm fonksiyonlar **paralel ve asenkron** olarak çalışır.
* ⭐ **Ordu Mimarisi (Append Logic):** Dekoratörler artık kayıtlı fonksiyonların üzerine yazmak yerine, onları ilgili olay listesine (`append`) ekler.
* ⭐ **Gelişmiş Context (Bağlam) Objesi:** Mesajın kimden geldiği, yetkileri (`mod`, `vip`, `staff`) ve botun kendisi tarafından atılıp atılmadığını (`is_bot`) anında analiz eden merkezi `Context` yapısı modernize edildi.

### 🛠️ **İyileştirmeler & Düzeltmeler**
* ✅ **Dinamik Import Esnekliği:** Framework artık hem `KickZero` hem de `kickzero` (küçük harf duyarsız) isimleriyle sorunsuz bir şekilde projeye dahil edilebiliyor.
* ✅ **Akıllı Motor (start) Güncellemesi:** Bot başlatıldığında listelenmiş tüm `on_ready` görevlerini aynı anda ateşleyen asenkron döngü hattı kuruldu.
* ✅ **Radar (HandleMessages) Optimizasyonu:** Gelen her mesaj; genel izleyiciler, kelime takipçileri ve prefix komutları arasında hatasız bir hiyerarşiyle dağıtılır hale getirildi.
* ✅ **Sonsuz Döngü Koruması:** Botun kendi yazdığı mesajları tetikleyip sonsuz döngüye girmesini engelleyen merkezi **author-check** sistemi eklendi.
* ✅ **Dökümantasyon & IntelliSense:** Tüm metodlar için Türkçe/İngilizce **Docstrings** eklenerek VS Code üzerinde "Sarı İkon" rehberliği sağlandı.

---

## 🕒 [1.1.0] - 2026-01-31
### 🚀 **v1.1 - The Great Timer Update | Zamanın Efendisi**

* ✨ **`timer_task` Dekoratörü:** Arka planda belirli zaman aralıklarıyla (saat, dakika, saniye) çalışan fonksiyonlar tanımlama yeteneği eklendi.
* ✨ **Akıllı Fonksiyon İmzası:** Fonksiyonların `ctx` parametresi alıp almadığı `inspect` ile otomatik analiz edilir hale getirildi.
* 🛠️ **Async Kararlılığı:** `asyncio.run()` standardı ve başlatıcı blok iyileştirmeleri yapıldı.

---

## ⚓ [1.0.0] - 2026-01-17
### 🚀 **İlk Yelken Açılışı (Initial Release)**

* 📍 Temel `KickBot` sınıfı oluşturuldu.
* 📍 `@command` ve `@message` dekoratörleri ile temel komut yapısı kuruldu.
* 📍 Pusher üzerinden Kick.com canlı sohbet bağlantısı sağlandı.