# _kaynak — sitenin kaynağı

> `_` ile başlayan klasörler GitHub Pages'te yayınlanmaz. Bu klasör sadece siteyi üretmek için.

Sitedeki tüm sayfalar (Türkçe + İngilizce) `build.py` ile üretilir:

```
python3 _kaynak/build.py
```

**HTML dosyalarını elle düzenleme**, çünkü bir sonraki üretimde üzerine yazılır. Değişiklikleri buradan yap.

## Neler nerede

| Ne | Nerede |
|---|---|
| Projeler, yazı listesi, gruplar, etiketlerin İngilizcesi | `build.py` → `PROJECTS`, `POSTS`, `GROUPS`, `TAG_EN` |
| Ana sayfadaki projeler | `build.py` → `FEATURED` |
| Hakkımda / Eğitim / İletişim metinleri | `build.py` → `ABOUT`, `build_education`, `build_contact` |
| Yazıların gövdesi | `yazilar/<slug>.tr.html` ve `yazilar/<slug>.en.html` |
| Bionluk linki, rakamlar, yorumlar, CV, ziyaretçi sayacı | `build.py` en üstte: `BIONLUK`, `STATS`, `REVIEWS`, `CV`, `GOATCOUNTER` |
| Ortak stil / script | `assets/css/style.css`, `assets/js/main.js` (bunlar elle düzenlenir) |

## Yeni yazı ekleme (Claude için kontrol listesi)

1. Ahmet fotoğrafları `yazilar/<proje-klasoru>/` içine koyar. Orijinalleri repo dışındaki `orijinal-fotograflar/` klasörüne yedekle.
2. Fotoğrafları küçült: en uzun kenar 1200 px, JPEG kalite ~74, progresif. Ekran görüntüleri ve şemalar için PNG kalabilir (yazılar okunur kalsın).
3. Kapak görseli üret: `assets/img/kapak/<slug>.jpg` (800×500).
4. `yazilar/<slug>.tr.html` ve `<slug>.en.html` dosyalarını yaz. `_ornek.tr.html` dosyasını kopyalayarak başla. `<img>` etiketlerinde sadece dosya adını yaz (ör. `src="foto1.jpg"`); İngilizce sürüm görselleri Türkçe klasörden otomatik alır. `width` ve `height` değerlerini gerçek piksel boyutuyla yaz.
5. `build.py` → `POSTS` listesinin başına yazıyı ekle (`tr_url`, `en_url`, `img_dir`, `thumb`, `group`, `date`, tr/en `kicker`, `title`, `page_title`, `desc`). Gerekirse `GROUPS`'a yeni grup, `PROJECTS`'e yeni proje ekle ya da var olan projenin `posts` listesine slug ekle.
6. `python3 _kaynak/build.py` çalıştır.
7. Telefon (390 px) ve masaüstü (1280 px) görünümünü test et: kırık link, sayfa taşması, konsol hatası olmasın.
8. Değişen ve yeni dosyaları Ahmet'in klasörüne yaz. Ahmet GitHub Desktop'ta **Commit → Push** yapar.

## Yazı içinde kullanılabilen bileşenler

- Fotoğraf: `<figure class="blog-figure"><img class="blog-img" ...><figcaption>…</figcaption></figure>`. Tıklanınca galeri açılır, ileri/geri gidilebilir, telefonda kaydırılabilir.
- Teknik detay kutusu: `<div class="tech-box">…</div>`
- Şematik / PCB / 3D sekmeli görüntüleyici: `_ornek.tr.html` içindeki `<div class="dv">` bloğu. Sekme ve panel `id`'leri sayfa içinde benzersiz olmalı.

## Hesap araçları

- Hesap kodu ve arayüz: `assets/js/tools.js` (her araç `TOOLS.<id>`; alanlar, modlar, `calc` fonksiyonu).
- Sayfa içeriği (başlık, açıklama, formüller, kaynaklar, ilgili araçlar): `_kaynak/araclar.py` → `TOOLS` listesi.
- Sayfalar: `araclar.html` + `araclar/<slug>.html` (TR), `en/tools.html` + `en/tools/<slug>.html` (EN). Ana sayfada `HOME_TOOLS` listesindeki 4 araç gösterilir.
- Yeni araç: `tools.js`'e `TOOLS.<id>` ekle → `araclar.py`'ye kayıt + `ICONS[<id>]` ekle → build → her iki dilde hesapları test et.
- Değerler adres çubuğuna yazılır (`?Vs=12&If=20`), yani hesap linki paylaşılabilir.
