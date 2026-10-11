# Siteye yeni proje / yazı ekleme rehberi

> `_sablon` klasörü sitede yayınlanmaz (GitHub Pages `_` ile başlayan klasörleri atlar).
> Bu dosya hem Ahmet hem de Claude için bir hatırlatma notudur.

## Ahmet'in yapacakları

1. Fotoğrafları yazının klasörüne koy:
   `yazilar/<proje-klasoru>/` — örnek: `yazilar/akilli-tarim/`, `yazilar/pratik-projeler/<yeni-proje>/`
   - Fotoğrafları telefondan çıktığı gibi atabilirsin, Claude küçültür.
   - Dosya adlarında Türkçe karakter ve boşluk kullanma (`devre-1.jpg` gibi).
2. Claude'a şunları söyle:
   - Proje adı, yeni proje mi yoksa var olan bir projenin yeni adımı mı
   - Tarih (ay/yıl)
   - Metin (kabaca yazman yeterli, istersen Claude düzenler)
   - Hangi fotoğraf nerede ve altında ne yazsın
   - Kullanılan bileşenler (Teknik Detaylar kutusu için)
3. Claude bitirince GitHub Desktop'ta değişikliklere bak, **Commit to main → Push origin**.

## Claude'un kontrol listesi

- [ ] Fotoğrafları küçült: en uzun kenar 1200 px, JPEG kalite ~74, progresif. Orijinalleri repo dışındaki `orijinal-fotograflar/` klasörüne yedekle.
- [ ] Kapak görseli üret: `assets/img/kapak/<proje>.jpg` (800×500, kırpılmış).
- [ ] Yazıyı `_sablon/yazi-sablonu.html` kopyalayarak oluştur. Yol derinliğine göre `../` sayısını ayarla
      (`yazilar/x/y.html` → `../../`, `yazilar/x/y/z.html` → `../../../`). `<img>` etiketlerine gerçek `width`/`height` yaz.
- [ ] `<head>`: title, description, canonical, og:url, og:image (kapak) güncelle.
- [ ] `yazilar.html`: ilgili gruba `post-item` ekle (yeni proje ise yeni `post-group`).
- [ ] `projeler.html`: yeni proje ise kart ekle; var olan projeyse kartın `card-links` kısmına yeni adımı ekle, "N yazı" rozetini güncelle.
- [ ] `index.html`: "Son yazılar" listesini en yeni 3 yazı olacak şekilde güncelle; gerekirse "Öne çıkan projeler".
- [ ] Diğer yazıların altındaki "Diğer yazılar" listesine yeni yazıyı ekle.
- [ ] `sitemap.xml`'e yeni URL'yi ekle.
- [ ] Telefon (390 px) ve masaüstü (1280 px) görünümünü kontrol et, kırık link olmadığını doğrula.

## Yapı

```
index.html, hakkimda.html, egitim.html, projeler.html, yazilar.html, iletisim.html, 404.html
assets/css/style.css   → tüm sayfaların ortak stili (renkler en üstte :root içinde)
assets/js/main.js      → mobil menü, yazı makinesi, devre animasyonu, form, fotoğraf büyütme
assets/img/kapak/      → proje kapak görselleri
assets/img/og.jpg      → link paylaşım önizleme görseli
yazilar/<proje>/...    → yazılar ve fotoğrafları
sitemap.xml, robots.txt, CNAME
```
