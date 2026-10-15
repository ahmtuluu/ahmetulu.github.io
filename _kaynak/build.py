#!/usr/bin/env python3
"""
ahmetulu.com.tr site üreticisi (TR + EN)
========================================
Bu klasör (_kaynak) sitede yayınlanmaz. Sayfaların hepsi buradaki verilerden üretilir:

    python3 _kaynak/build.py

- Proje / yazı bilgileri: aşağıdaki PROJECTS, POSTS, GROUPS listeleri
- Yazı gövdeleri: _kaynak/yazilar/<slug>.tr.html ve <slug>.en.html
- Opsiyonel bölümler (doldurulunca görünür): BIONLUK, STATS, REVIEWS, CV, GOATCOUNTER
Elle düzenlenen HTML dosyaları bir sonraki çalıştırmada üzerine yazılır; değişiklikleri buradan yap.
"""
import os, html, hashlib, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://ahmetulu.com.tr'
YEAR = '2026'
EMAIL = 'ahulu2006@gmail.com'
GITHUB = 'https://github.com/ahmtuluu'
LINKEDIN = 'https://www.linkedin.com/in/ahmet-ulu-16099832b/'
FORMSPREE = 'https://formspree.io/f/mvzwyvky'

# ---------------------------------------------------------------- opsiyonel
BIONLUK = 'https://bionluk.com/ahmetuluu'
# Bionluk rakamları (Ekim 2026 itibarıyla) — profil güncellendikçe burayı da güncelle
STATS = [('8', 'tamamlanan sipariş', 'completed orders'),
         ('5.0', 'Bionluk puanı', 'Bionluk rating'),
         ('6/6', 'beş yıldızlı yorum', 'five-star reviews')]
# Gerçek Bionluk yorumları; Türkçesi kelimesi kelimesine, alıcı adları gizli
REVIEWS = [
 dict(tr='Ahmet Bey, aklımdaki projeyi anlatmam sonucu tam olarak ihtiyacım olan pcb tasarımını çok kısa bir sürede geliştirdi. Kendisine çok teşekkür ediyorum. Güvenle çalışabilirsiniz.',
      en='After I described the project I had in mind, Ahmet developed exactly the PCB design I needed in a very short time. Many thanks to him. You can work with him with confidence.'),
 dict(tr='İhtiyaçlarım doğrultusundaki PCB yi tasarladı ve detaylarını hiç sıkılmadan anlattı teşekkürler',
      en='He designed the PCB according to my needs and explained the details patiently. Thanks.'),
 dict(tr='Ahmet bey, tam istediğim gibi yaptı. İsteklerimi dinledi istişarede bulunduk, hep yardımcı oldu, kısa sürede teslim etti. Bu ilk işimizdi bundan sonrada beraber çalışacağız bionluk üzerinden çok teşekkürler ellerinize sağlık. Başarılarınızın devamını dilerim. Kolay gelsin',
      en="Ahmet did it exactly the way I wanted. He listened to my requests, we discussed it together, he was always helpful and delivered quickly. This was our first job; from now on we'll keep working together through Bionluk. Thank you very much, great work. I wish you continued success."),
]
CV = 'assets/ahmet-ulu-cv.pdf'   # İngilizce CV, telefon numarası çıkarılmış sürüm
GSC_VERIFICATION = "kDmbOcP_ZD3wqx9IxPQzHMZo0sCyWcbTu7h1BzVJdyA"   # Google Search Console 'HTML etiketi' doğrulama kodu (content="..." içindeki değer)
GOATCOUNTER = None    # ör. 'ahmetulu' (goatcounter.com hesabındaki kod)

# ---------------------------------------------------------------- ikonlar
ICON = {
 'github': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>',
 'linkedin': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>',
 'search': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 'leaf': '<svg viewBox="0 0 24 24" width="46" height="46" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
 'doc': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>',
 'chip': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
}

# ---------------------------------------------------------------- arayüz metinleri
S = {
 'tr': dict(
   nav=[('home', None), ('about', 'Hakkımda'), ('education', 'Eğitim'), ('projects', 'Projeler'), ('blog', 'Yazılar'), ('contact', 'İletişim')],
   skip='İçeriğe geç', menu='Menüyü aç/kapat', other_lang='EN', other_lang_label='English',
   all_posts='← Tüm yazılar', more_posts='Diğer yazılar', all_='Tümü', see_all='Tümü →',
   featured='Öne çıkan projeler', latest='Son yazılar', scroll='Öne çıkanlar',
   n_posts='{} yazı', read='Yazıyı oku →', soon='Ayrıntılar yakında', step_sep=' — ',
   search_projects='Projelerde ara…', search_posts='Yazılarda ara…', no_result='Sonuç bulunamadı. Başka bir kelime ya da etiket dene.',
   tags_label='Etiketler', small_projects='Pratik projeler', small_projects_desc='Öğrenmek için yapılan küçük denemeler.',
   reviews='Müşteri yorumları', reviews_all='Bionluk\'taki tüm yorumlar →', on_bionluk='Bionluk',
   cv='CV indir (PDF)', locale='tr_TR',
 ),
 'en': dict(
   nav=[('home', None), ('about', 'About'), ('education', 'Education'), ('projects', 'Projects'), ('blog', 'Blog'), ('contact', 'Contact')],
   skip='Skip to content', menu='Toggle menu', other_lang='TR', other_lang_label='Türkçe',
   all_posts='← All posts', more_posts='More posts', all_='All', see_all='See all →',
   featured='Featured projects', latest='Latest posts', scroll='Highlights',
   n_posts='{} post', read='Read the post →', soon='Details coming soon', step_sep=' — ',
   search_projects='Search projects…', search_posts='Search posts…', no_result='No results. Try another word or tag.',
   tags_label='Tags', small_projects='Practical projects', small_projects_desc='Small experiments built to learn.',
   reviews='Client reviews', reviews_all='All reviews on Bionluk →', on_bionluk='Bionluk',
   cv='Download CV (PDF)', locale='en_US',
 ),
}
PAGES = {  # anahtar: (tr yolu, en yolu)
 'home': ('index.html', 'en/index.html'),
 'about': ('hakkimda.html', 'en/about.html'),
 'education': ('egitim.html', 'en/education.html'),
 'projects': ('projeler.html', 'en/projects.html'),
 'blog': ('yazilar.html', 'en/blog.html'),
 'contact': ('iletisim.html', 'en/contact.html'),
}
MONTHS = {'tr': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}

# ---------------------------------------------------------------- içerik
GROUPS = [  # yazılar sayfasındaki gruplar (sıra önemli)
 dict(key='pcb', tr=('PCB Tasarımları', 'Bionluk üzerinden müşteriler için yaptığım tasarımlar'), en=('PCB Designs', 'Designs I made for clients through Bionluk')),
 dict(key='tarim', tr=('Akıllı Tarım Sistemi', 'Projenin adım adım gelişimi'), en=('Smart Agriculture System', 'Step-by-step development of the project')),
 dict(key='ev', tr=('Elektrik Şarj İstasyonu Optimizasyonu', 'Projenin adım adım gelişimi'), en=('EV Charging Station Optimization', 'Step-by-step development of the project')),
 dict(key='pratik', tr=('Pratik Projeler', 'Öğrenmek için yapılan küçük denemeler'), en=('Practical Projects', 'Small experiments built to learn')),
]

POSTS = [  # en yeni en üstte
 dict(slug='pcb-tasarim', group='pcb', date=(2026, 10),
      tr_url='yazilar/pcb-tasarim/kicad-pcb-tasarimlari.html', en_url='en/blog/kicad-pcb-design.html',
      img_dir='yazilar/pcb-tasarim/', thumb='assets/img/kapak/pcb-tasarim.jpg',
      tr=dict(kicker='PCB Tasarımı · Freelance', title='KiCad ile PCB Tasarımı: Bionluk\'ta Müşteriler İçin Tasarladığım Kartlar', page_title='KiCad ile PCB Tasarımı: ESP32 Peltier ve Trafik Sinyalizasyon Kartları',
              desc='Bionluk üzerinden müşteriler için KiCad ile tasarladığım kartlar: trafik sinyalizasyon kontrol kartı ve ESP32 tabanlı Peltier kontrol kartı; şematik, PCB ve 3D görünümler.'),
      en=dict(kicker='PCB Design · Freelance', title='PCB Design with KiCad: Boards I Designed for Clients', page_title='PCB Design with KiCad: ESP32 Peltier and Traffic Signal Boards',
              desc='Boards I designed in KiCad for clients on Bionluk: a traffic signal control board and an ESP32-based Peltier control board, with schematic, PCB and 3D views.')),
 dict(slug='guc-kaynagi', group='pratik', date=(2026, 4),
      tr_url='yazilar/pratik-projeler/guc-kaynagi/guc-kaynagi.html', en_url='en/blog/adjustable-power-supply.html',
      img_dir='yazilar/pratik-projeler/guc-kaynagi/', thumb='assets/img/kapak/guc-kaynagi.jpg',
      tr=dict(kicker='Pratik Proje', title='12V DC Ayarlı Güç Kaynağı — LM2596 Modifikasyonu', page_title='LM2596 ile 12V Ayarlı Güç Kaynağı Yapımı',
              desc='LM2596 tabanlı ayarlanabilir DC güç kaynağı: trimpot yerine 10 tur hassas potansiyometre, sorunlar ve çözümleri.'),
      en=dict(kicker='Practical Project', title='12V DC Adjustable Power Supply — LM2596 Mod', page_title='Building a 12V Adjustable Power Supply with the LM2596',
              desc='An adjustable DC power supply based on the LM2596: a 10-turn precision potentiometer instead of the trimpot, problems and fixes.')),
 dict(slug='ev-sarj-altyapi', group='ev', date=(2026, 4),
      tr_url='yazilar/ev-sarj/ev-sarj-altyapi.html', en_url='en/blog/ev-charging-data-infrastructure.html',
      img_dir='yazilar/ev-sarj/', thumb='assets/img/kapak/ev-sarj.jpg', step=1,
      tr=dict(kicker='EV Şarj · 1. Adım', title='Raspberry Pi ve Veri Altyapısı', page_title='Elektrikli Araç Şarj İstasyonu: Raspberry Pi ile Veri Altyapısı',
              desc='Elektrikli araç (EV) şarj istasyonu projesi: Raspberry Pi üzerinde PostgreSQL, Arduino ile sensör verisi, kamera ile plaka tanıma ve Flask REST API.'),
      en=dict(kicker='EV Charging · Step 1', title='Raspberry Pi and the Data Infrastructure', page_title='EV Charging Station Data Infrastructure with Raspberry Pi',
              desc='An electric vehicle (EV) charging station project: PostgreSQL on a Raspberry Pi, sensor data from an Arduino, license plate recognition and a Flask REST API.')),
 dict(slug='su-analizi', group='tarim', date=(2026, 3),
      tr_url='yazilar/akilli-tarim/su-analizi.html', en_url='en/blog/water-analysis-system.html',
      img_dir='yazilar/akilli-tarim/', thumb='assets/img/kapak/akilli-tarim.jpg', step=1,
      tr=dict(kicker='Akıllı Tarım · 1. Adım', title='Su Analiz Sistemi', page_title='Güneş Enerjili Su Analiz Sistemi: ESP32 ile pH, TDS ve Sıcaklık Ölçümü',
              desc='Güneş enerjili, off-grid su analiz sistemi: pH, TDS ve sıcaklık ölçümü, PCB, mobil uygulama ve sensör gürültüsü.'),
      en=dict(kicker='Smart Agriculture · Step 1', title='Water Analysis System', page_title='Solar-Powered Water Analysis System with ESP32: pH, TDS and Temperature',
              desc='A solar-powered, off-grid water analysis system: pH, TDS and temperature sensing, a PCB, a mobile app and sensor noise.')),
]
POST = {p['slug']: p for p in POSTS}

PROJECTS = [
 dict(kind='main', year='2025–2026', cover='assets/img/kapak/pcb-tasarim.jpg', posts=['pcb-tasarim'],
      tags=['PCB Tasarımı', 'KiCad', 'ESP32', 'Freelance'],
      tr=dict(title='Freelance PCB Tasarımı', desc='Bionluk üzerinden müşterilere özel şematik ve PCB tasarımı: ihtiyacı dinlemekten üretime hazır dosyalara kadar. 8 sipariş, 5.0 puan.'),
      en=dict(title='Freelance PCB Design', desc='Custom schematic and PCB design for clients on Bionluk, from understanding the need to production-ready files. 8 orders, 5.0 rating.')),
 dict(kind='main', year='2025', cover='assets/img/kapak/akilli-tarim.jpg', posts=['su-analizi'],
      tags=['ESP32', 'Python', 'IoT', 'Sensör'],
      tr=dict(title='Akıllı Tarım Sistemi', desc='Toprak nemi, sıcaklık ve ışık sensörleriyle otomatik sulama ve izleme yapan IoT tabanlı proje.'),
      en=dict(title='Smart Agriculture System', desc='An IoT project that automates irrigation and monitoring with soil moisture, temperature and light sensors.')),
 dict(kind='main', year='2024', cover='assets/img/kapak/ev-sarj.jpg', posts=['ev-sarj-altyapi'],
      tags=['Python', 'Raspberry Pi', 'Machine Learning', 'Enerji'],
      tr=dict(title='Elektrik Şarj İstasyonu Optimizasyonu', desc='Birden fazla EV şarj noktasının yük dengelemesini ve enerji dağıtımını optimize eden yazılım.'),
      en=dict(title='EV Charging Station Optimization', desc='Software that optimizes load balancing and energy distribution across multiple EV charging points.')),
 dict(kind='main', year='2025', cover=None, icon='leaf', posts=[],
      tags=['Raspberry Pi', 'Python', 'C++', 'Otomasyon'],
      tr=dict(title='Topraksız Tarım Projesi', desc='Hidroponik yöntemle bitki yetiştirmeyi otomatikleştiren sistem. pH ve EC değerlerini ölçerek dozaj pompalarını kontrol eder.'),
      en=dict(title='Hydroponics Project', desc='A system that automates growing plants hydroponically. It measures pH and EC values and controls the dosing pumps.')),
 dict(kind='small', year='2026', cover='assets/img/kapak/guc-kaynagi.jpg', posts=['guc-kaynagi'],
      tags=['LM2596', 'Güç Elektroniği', 'Lehim'],
      tr=dict(title='12V DC Ayarlı Güç Kaynağı', desc='LM2596 buck modülünün trimpotu yerine dışarıdan çevrilebilen 10 tur hassas potansiyometre ve dijital voltmetre.'),
      en=dict(title='12V DC Adjustable Power Supply', desc='An LM2596 buck module with an external 10-turn precision potentiometer instead of the trimpot, plus a digital voltmeter.')),
]
FEATURED = [0, 1, 2]  # ana sayfadaki projeler (PROJECTS indeksleri)

TAG_EN = {'PCB Tasarımı': 'PCB Design', 'Sensör': 'Sensors', 'Enerji': 'Energy', 'Otomasyon': 'Automation', 'Güç Elektroniği': 'Power Electronics',
          'Lehim': 'Soldering', 'PCB Tasarımı': 'PCB Design'}

# ---------------------------------------------------------------- yardımcılar
def esc(s):
    return html.escape(s, quote=True)

def rel_of(path):
    return '../' * path.count('/')

def date_str(p, lang):
    y, m = p['date']
    return f'{MONTHS[lang][m - 1]} {y}'

def tag_name(t, lang):
    return TAG_EN.get(t, t) if lang == 'en' else t

def post_url(p, lang):
    return p['tr_url'] if lang == 'tr' else p['en_url']

def head(lang, path, title, desc, alt_path, og_image='assets/img/og.jpg', og_type='website', noindex=False, ld=None):
    rel = rel_of(path)
    canon = f'{SITE}/{path}'.replace('/index.html', '/')
    tr_p, en_p = (path, alt_path) if lang == 'tr' else (alt_path, path)
    alt = ''
    if alt_path:
        tr_u = f'{SITE}/{tr_p}'.replace('/index.html', '/')
        en_u = f'{SITE}/{en_p}'.replace('/index.html', '/')
        alt = (f'<link rel="alternate" hreflang="tr" href="{tr_u}">\n<link rel="alternate" hreflang="en" href="{en_u}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{tr_u}">\n')
    gc = ''
    if GOATCOUNTER:
        gc = f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    gsc = f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">\n' if GSC_VERIFICATION and path == 'index.html' else ''
    ldjson = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<meta name="author" content="Ahmet Ulu">
<meta name="theme-color" content="#111110">
<link rel="canonical" href="{canon}">
{alt}<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{S[lang]['locale']}">
<meta property="og:site_name" content="Ahmet Ulu">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/style.css?v={asset_ver('assets/css/style.css')}">
<script>document.documentElement.classList.add('js')</script>
{gc}{gsc}{ldjson}</head>
'''

def nav(lang, path, active, alt_path):
    rel = rel_of(path)
    s = S[lang]
    items = []
    for key, label in s['nav']:
        if label is None:
            continue
        href = rel + PAGES[key][0 if lang == 'tr' else 1]
        cur = ' aria-current="page"' if key == active else ''
        items.append(f'    <li><a href="{href}"{cur}>{label}</a></li>')
    other = 'en' if lang == 'tr' else 'tr'
    if alt_path:
        items.append(f'    <li class="nav-lang"><a href="{rel}{alt_path}" hreflang="{other}" lang="{other}" aria-label="{s["other_lang_label"]}">{s["other_lang"]}</a></li>')
    home = rel + PAGES['home'][0 if lang == 'tr' else 1]
    items = '\n'.join(items)
    return f'''<body>
<a class="skip-link" href="#icerik">{s['skip']}</a>
<header class="site-nav">
  <a href="{home}" class="nav-logo"><span class="nav-logo-mark" aria-hidden="true">A</span>Ahmet Ulu</a>
  <button class="nav-toggle" aria-label="{s['menu']}" aria-expanded="false" aria-controls="menu"><span></span></button>
  <ul class="nav-links" id="menu">
{items}
  </ul>
</header>
'''

def footer(lang, path):
    rel = rel_of(path)
    bion = f'\n      <a href="{BIONLUK}" target="_blank" rel="noopener">Bionluk</a>' if BIONLUK else ''
    mail = 'E-posta' if lang == 'tr' else 'Email'
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-copy">© {YEAR} Ahmet Ulu · Kayseri</div>
    <div class="footer-social">
      <a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>{bion}
      <a href="mailto:{EMAIL}">{mail}</a>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/main.js?v={asset_ver('assets/js/main.js')}" defer></script>
</body>
</html>
'''

def asset_ver(path):
    # Dosya içeriğinden kısa sürüm kodu: CSS/JS değişince tarayıcı eski önbelleği kullanmaz
    with open(os.path.join(ROOT, path), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def person_ld(lang):
    return {
        '@type': 'Person', '@id': f'{SITE}/#ahmet-ulu', 'name': 'Ahmet Ulu', 'url': f'{SITE}/',
        'image': f'{SITE}/assets/img/og.jpg', 'email': f'mailto:{EMAIL}',
        'jobTitle': 'Elektrik-Elektronik Mühendisliği Öğrencisi, Gömülü Sistemler Geliştiricisi' if lang == 'tr' else 'Electrical & Electronics Engineering Student, Embedded Systems Developer',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Kayseri', 'addressCountry': 'TR'},
        'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Abdullah Gül Üniversitesi'},
        'knowsAbout': ['Gömülü Sistemler', 'IoT', 'PCB Tasarımı', 'KiCad', 'ESP32', 'STM32', 'Raspberry Pi', 'Elektrikli Araç Şarj Sistemleri'],
        'sameAs': [GITHUB, LINKEDIN] + ([BIONLUK] if BIONLUK else []),
    }

CANVAS = '<canvas id="circuit-canvas" aria-hidden="true"></canvas>\n'

def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('  ', path)

def page(lang, key, title, desc, body, canvas=None, ld=None):
    if canvas is None:
        canvas = (key == 'home')  # arka plan animasyonu sadece ana sayfada
    path = PAGES[key][0 if lang == 'tr' else 1]
    alt = PAGES[key][1 if lang == 'tr' else 0]
    out = head(lang, path, title, desc, alt, ld=ld) + nav(lang, path, key, alt) + (CANVAS if canvas else '')
    out += f'<main id="icerik">\n{body}\n</main>\n' + footer(lang, path)
    write(path, out)

# ---------------------------------------------------------------- bileşenler
def post_item(p, lang, rel, kicker=True):
    t = p[lang]
    k = f'<div class="post-kicker">{t["kicker"]}</div>' if kicker else ''
    g = next(x for x in GROUPS if x['key'] == p['group'])[lang][0]
    return f'''<a href="{rel}{post_url(p, lang)}" class="post-item" data-filter-item data-tags="{esc(g)}">
  <img class="post-thumb" src="{rel}{p["thumb"]}" alt="" width="72" height="72" loading="lazy" decoding="async">
  <div class="post-info">{k}<div class="post-title">{t["title"]}</div><div class="post-date">{date_str(p, lang)}</div></div>
  <span class="post-arrow" aria-hidden="true">→</span>
</a>'''

def link_text(p, lang):
    k = p[lang]['kicker']
    if ' · ' in k and ('Adım' in k or 'Step' in k):
        return f"{k.split(' · ')[-1]}{S[lang]['step_sep']}{p[lang]['title']} →"
    return S[lang]['read']

def project_card(pr, lang, rel):
    t = pr[lang]
    s = S[lang]
    if pr['cover']:
        media = f'<div class="card-media"><img src="{rel}{pr["cover"]}" alt="{esc(t["title"])}" width="800" height="500" loading="lazy" decoding="async"></div>'
    else:
        media = f'<div class="card-media placeholder">{ICON[pr.get("icon", "chip")]}</div>'
    proj_page = rel + PAGES['projects'][0 if lang == 'tr' else 1]
    tags = ''.join(f'<a class="tag" href="{proj_page}?tag={esc(tag_name(x, lang))}">{tag_name(x, lang)}</a>' for x in pr['tags'])
    if pr['posts']:
        links = ''.join(
            f'<a class="card-link{" card-stretch" if i == 0 else ""}" href="{rel}{post_url(POST[sl], lang)}">{link_text(POST[sl], lang)}</a>'
            for i, sl in enumerate(pr['posts']))
        count = f'<span class="badge neutral">{s["n_posts"].format(len(pr["posts"]))}{"s" if lang == "en" and len(pr["posts"]) > 1 else ""}</span>'
    else:
        links = f'<span class="card-link muted">{s["soon"]}</span>'
        count = ''
    data_tags = '|'.join(tag_name(x, lang) for x in pr['tags'])
    return f'''<article class="card" data-filter-item data-tags="{esc(data_tags)}">
  {media}
  <div class="card-body">
    <div class="card-meta"><span>{pr["year"]}</span>{count}</div>
    <h3 class="card-title">{t["title"]}</h3>
    <p class="card-desc">{t["desc"]}</p>
    <div class="tags">{tags}</div>
    <div class="card-links">{links}</div>
  </div>
</article>'''

def filter_bar(lang, placeholder, tags):
    s = S[lang]
    chips = [f'<button type="button" class="chip" data-filter-tag="" aria-pressed="true">{s["all_"]}</button>']
    chips += [f'<button type="button" class="chip" data-filter-tag="{esc(t)}" aria-pressed="false">{t}</button>' for t in tags]
    return f'''    <div class="filter-bar">
      <label class="search-box">{ICON["search"]}<input type="search" placeholder="{placeholder}" aria-label="{placeholder}" data-filter-search autocomplete="off"></label>
      <div class="chips" role="group" aria-label="{s["tags_label"]}">{"".join(chips)}</div>
    </div>'''

def social_links(lang):
    return f'''<div class="social-links reveal">
      <a href="{GITHUB}" target="_blank" rel="noopener" class="social-link" aria-label="GitHub">{ICON["github"]}</a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener" class="social-link" aria-label="LinkedIn">{ICON["linkedin"]}</a>
      <a href="mailto:{EMAIL}" class="social-link" aria-label="{"E-posta" if lang == "tr" else "Email"}">{ICON["mail"]}</a>
    </div>'''

def stats_html(lang):
    items = ''.join(f'<div class="stat"><div class="stat-num">{n}</div><div class="stat-label">{tr if lang == "tr" else en}</div></div>' for n, tr, en in STATS)
    return f'<div class="stats">{items}</div>' if STATS else ''

def service_block(lang):
    if not BIONLUK:
        return ''
    pcb = POST.get('pcb-tasarim')
    rel = rel_of(PAGES['home'][0 if lang == 'tr' else 1])
    if lang == 'tr':
        kicker, h = 'Freelance', 'PCB tasarımı yaptırmak mı istiyorsun?'
        txt = 'Bionluk üzerinden KiCad ile şematik ve PCB tasarımı yapıyorum: projeni dinliyorum, ihtiyacına göre tasarlıyorum ve üretime hazır dosyaları teslim ediyorum.'
        b1, b2 = 'Bionluk profilim →', 'Örnek tasarımlarım'
    else:
        kicker, h = 'Freelance', 'Need a PCB designed?'
        txt = 'I design schematics and PCBs in KiCad through Bionluk: I listen to your project, design to your needs and deliver production-ready files.'
        b1, b2 = 'My Bionluk profile →', 'See example designs'
    b2_html = f'<a class="btn btn-ghost" href="{rel}{post_url(pcb, lang)}">{b2}</a>' if pcb else ''
    return f'''      <section class="section" data-tone="dark">
        <div class="service">
          <div class="service-text">
            <div class="post-kicker">{kicker}</div>
            <h2 class="section-title">{h}</h2>
            <p>{txt}</p>
            <div class="cta-actions"><a class="btn btn-primary" href="{BIONLUK}" target="_blank" rel="noopener">{b1}</a>{b2_html}</div>
          </div>
          {stats_html(lang)}
        </div>
      </section>
'''

def reviews_block(lang):
    if not REVIEWS:
        return ''
    s = S[lang]
    who = 'Bionluk alıcısı' if lang == 'tr' else 'Bionluk client'
    note = '' if lang == 'tr' else ' · translated from Turkish'
    items = '\n'.join(f'''        <figure class="review">
          <div class="review-stars" aria-label="5/5">★★★★★</div>
          <blockquote>“{esc(r[lang])}”</blockquote>
          <figcaption>{who}{note}</figcaption>
        </figure>''' for r in REVIEWS)
    more = f'<a class="section-link" href="{BIONLUK}" target="_blank" rel="noopener">{s["reviews_all"]}</a>' if BIONLUK else ''
    return f'''      <section class="section" data-tone="light">
        <div class="section-head"><h2 class="section-title">{s["reviews"]}</h2>{more}</div>
        <div class="review-grid">
{items}
        </div>
      </section>
'''

# ---------------------------------------------------------------- sayfalar
def build_home(lang):
    s = S[lang]
    rel = rel_of(PAGES['home'][0 if lang == 'tr' else 1])
    cards = '\n'.join(project_card(PROJECTS[i], lang, rel) for i in FEATURED)
    posts = '\n'.join(post_item(p, lang, rel) for p in POSTS[:3])
    P = lambda k: rel + PAGES[k][0 if lang == 'tr' else 1]
    if lang == 'tr':
        title = 'Ahmet Ulu — Elektrik-Elektronik, Gömülü Sistemler ve IoT'
        desc = "Ahmet Ulu — Kayseri'den elektrik-elektronik mühendisliği öğrencisi. Gömülü sistemler, IoT ve otomasyon projeleri, yazılar ve deneyimler."
        l1, l2 = 'Merhaba, ben', 'Ahmet Ulu.'
        intro = 'Elektrik-elektronik öğrencisiyim. Ama asıl öğrendiğim şeylerin çoğu ders dışında, bir şeyler yaparken ortaya çıktı. Çoğuna meraktan başladım ve bilmediğim şeyleri öğrenmekten de hiç çekinmedim.'
        b1, b2 = 'Projelerime bak', 'Hakkımda'
    else:
        title = 'Ahmet Ulu — Electrical & Electronics, Embedded Systems and IoT'
        desc = 'Ahmet Ulu — an electrical and electronics engineering student from Kayseri, Türkiye. Embedded systems, IoT and automation projects, posts and experiences.'
        l1, l2 = "Hi, I'm", 'Ahmet Ulu.'
        intro = "I'm an electrical and electronics engineering student. But most of what I've really learned came from outside the classroom, while building things. I started most of them out of curiosity, and I've never been afraid of learning what I don't know."
        b1, b2 = 'See my projects', 'About me'
    body = f'''  <div class="wrap">
    <section class="hero" data-tone="dark">
      <div class="home-label reveal">Kayseri, Türkiye</div>
      <h1 class="home-title" id="homeTitle"><span class="tline">{l1}</span><em class="tline">{l2}</em></h1>
      <p class="home-desc reveal">{intro}</p>
      <div class="home-cta reveal">
        <a class="btn btn-primary" href="{P('projects')}">{b1}</a>
        <a class="btn btn-ghost" href="{P('about')}">{b2}</a>
      </div>
      {social_links(lang)}
      <a class="scroll-hint reveal" href="#one-cikanlar">{s['scroll']} <span aria-hidden="true">↓</span></a>
    </section>

    <div class="home-sections">
      <section class="section" id="one-cikanlar" data-tone="light">
        <div class="section-head"><h2 class="section-title">{s['featured']}</h2><a class="section-link" href="{P('projects')}">{s['see_all']}</a></div>
        <div class="card-grid">
{cards}
        </div>
      </section>
{service_block(lang)}{reviews_block(lang)}
      <section class="section" data-tone="light">
        <div class="section-head"><h2 class="section-title">{s['latest']}</h2><a class="section-link" href="{P('blog')}">{s['see_all']}</a></div>
{posts}
      </section>
    </div>
  </div>'''
    ld = [{'@context': 'https://schema.org', '@graph': [person_ld(lang),
          {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Ahmet Ulu', 'inLanguage': lang, 'publisher': {'@id': f'{SITE}/#ahmet-ulu'}}]}]
    page(lang, 'home', title, desc, body, ld=ld)

ABOUT = {
 'tr': dict(title='Hakkımda — Ahmet Ulu', h='Hakkımda', sub='Kim olduğum, ne ile ilgilendiğim.',
   desc="Ahmet Ulu kimdir? Gömülü sistemler, IoT ve PCB tasarımı üzerine çalışan elektrik-elektronik mühendisliği öğrencisi; MUSTECH'te gömülü sistemler geliştiricisi, Bionluk'ta freelance PCB tasarımcısı.",
   paras=["Merhaba, ben <strong>Ahmet Ulu</strong>. Kayseri'den bir yazılım ve donanım geliştiricisiyim. Gömülü sistemler, IoT projeleri ve otomasyon üzerine çalışıyorum. Makine öğrenmesini gerçek dünya problemlerine uygulamak hem hedefim hem de tutkum.",
          "<strong>Python, C ve C++</strong> ile yazılım geliştirirken; <strong>Raspberry Pi, STM32 ve ESP32</strong> gibi kartlarla donanım projelerini hayata geçiriyorum. Kodu sadece ekranda değil, gerçek bir sistemin içinde çalışırken görmek başka bir his.",
          "Bu site; projelerimi, deneyimlerimi ve öğrendiklerimi bir arada tuttuğum dijital evim."],
   exp_h='Deneyim',
   exp=[('Gömülü Sistemler Geliştiricisi', 'MUSTECH · Kayseri', 'Şubat 2026 — Devam ediyor',
         'IoT tabanlı çevresel izleme sistemleri için gömülü yazılım ve donanım arayüzleri; düşük gürültülü sensör arayüz devreleri ve sensör düğümlerinden bulut veritabanına uzanan veri hatları.', None),
        ('Freelance PCB Tasarımcısı', 'Bionluk · Uzaktan', '2025 — Devam ediyor',
         'Müşterilere özel şematik ve PCB tasarımı; ihtiyacı anlamaktan üretime hazır dosyalara kadar tüm süreç. 8 tamamlanan sipariş, 5.0 puan.', 'pcb-tasarim')],
   read_more='Örnek tasarımlar →',
   skills_h='Yetenekler',
   skills=[('Yazılım', ['Python', 'C', 'C++']), ('Donanım ve Kartlar', ['ESP32', 'STM32', 'Arduino', 'Raspberry Pi']),
           ('PCB ve Araçlar', ['KiCad', 'MATLAB & Simulink', 'Git', 'Linux']), ('Haberleşme', ['UART', 'SPI', 'I²C', 'LoRa']),
           ('Uzmanlık Alanları', ['Gömülü Sistemler', 'IoT', 'Otomasyon']), ('İlgi Alanları', ['Machine Learning', 'Sinyal İşleme', 'Kontrol Sistemleri'])]),
 'en': dict(title='About — Ahmet Ulu', h='About', sub='Who I am and what I work on.',
   desc='Who is Ahmet Ulu? An electrical and electronics engineering student working on embedded systems, IoT and PCB design; embedded systems developer at MUSTECH and freelance PCB designer on Bionluk.',
   paras=["Hi, I'm <strong>Ahmet Ulu</strong>, a software and hardware developer from Kayseri, Türkiye. I work on embedded systems, IoT projects and automation. Applying machine learning to real-world problems is both my goal and my passion.",
          "I write software in <strong>Python, C and C++</strong>, and bring hardware projects to life with boards like the <strong>Raspberry Pi, STM32 and ESP32</strong>. Seeing code run not just on a screen but inside a real system is a different feeling.",
          "This site is my digital home, where I keep my projects, experiences and what I've learned in one place."],
   exp_h='Experience',
   exp=[('Embedded Systems Developer', 'MUSTECH · Kayseri', 'February 2026 — Present',
         'Embedded firmware and hardware interfaces for IoT-based environmental monitoring systems; low-noise sensor interface circuits and data pipelines from sensor nodes to cloud databases.', None),
        ('Freelance PCB Designer', 'Bionluk · Remote', '2025 — Present',
         'Custom schematic and PCB design for clients, covering the whole process from understanding the need to production-ready files. 8 completed orders, 5.0 rating.', 'pcb-tasarim')],
   read_more='Example designs →',
   skills_h='Skills',
   skills=[('Software', ['Python', 'C', 'C++']), ('Hardware & Boards', ['ESP32', 'STM32', 'Arduino', 'Raspberry Pi']),
           ('PCB & Tools', ['KiCad', 'MATLAB & Simulink', 'Git', 'Linux']), ('Communication', ['UART', 'SPI', 'I²C', 'LoRa']),
           ('Focus Areas', ['Embedded Systems', 'IoT', 'Automation']), ('Interests', ['Machine Learning', 'Signal Processing', 'Control Systems'])]),
}

def build_about(lang):
    a = ABOUT[lang]
    rel = rel_of(PAGES['about'][0 if lang == 'tr' else 1])
    paras = '\n'.join(f'    <p class="about-text">{p}</p>' for p in a['paras'])
    skills = '\n'.join('      <div class="skill-group"><div class="skill-group-label">' + g + '</div><div class="skill-tags">'
                       + ''.join(f'<span class="stag">{x}</span>' for x in xs) + '</div></div>' for g, xs in a['skills'])
    exp = ''
    for t, org, d, desc, slug in a['exp']:
        more = f' <a class="inline-link" href="{rel}{post_url(POST[slug], lang)}">{a["read_more"]}</a>' if slug in POST else ''
        icon = '💼' if slug is None else '🛠️'
        exp += ('      <div class="edu-item">\n'
                f'        <div class="edu-icon" aria-hidden="true">{icon}</div>\n'
                f'        <div><div class="edu-title">{t}</div><div class="edu-sub">{org}</div><div class="edu-date">{d}</div><p class="edu-desc">{desc}{more}</p></div>\n'
                '      </div>\n')
    cv = ''
    if CV:
        lab = 'CV indir (İngilizce, PDF)' if lang == 'tr' else 'Download CV (PDF)'
        cv = f'\n    <div class="home-cta" style="margin-top:28px"><a class="btn btn-primary" href="{rel}{CV}" target="_blank" rel="noopener">{lab}</a></div>'
    body = (f'  <div class="wrap-narrow inner fade-in">\n'
            f'    <div class="page-header"><h1>{a["h"]}</h1><p>{a["sub"]}</p></div>\n'
            f'{paras}{cv}\n'
            f'    <h2 class="sub-title">{a["exp_h"]}</h2>\n'
            f'    <div class="edu-list">\n{exp}    </div>\n'
            f'    <h2 class="sub-title">{a["skills_h"]}</h2>\n'
            f'    <div class="skills-grid">\n{skills}\n    </div>\n'
            '  </div>')
    page(lang, 'about', a['title'], a['desc'], body)

def build_education(lang):
    if lang == 'tr':
        title, h, sub = 'Eğitim — Ahmet Ulu', 'Eğitim', 'Akademik geçmişim ve sertifikalarım.'
        desc = "Ahmet Ulu'nun akademik geçmişi ve sertifikaları: Abdullah Gül Üniversitesi Elektrik Elektronik Mühendisliği, English Path Dubai, Coursera ve MathWorks sertifikaları."
        items = [('🎓', 'Elektrik Elektronik Mühendisliği', 'Abdullah Gül Üniversitesi · Kayseri', '2024 — 2029 (beklenen)', 'Lisans'),
                 ('🌐', 'Yoğun İngilizce Dil Programı', 'English Path · Dubai, BAE', 'Haziran — Ağustos 2025', 'B2 · Upper Intermediate')]
        cert_h, view = 'Sertifikalar', 'Görüntüle'
        certs = [('From Schematic to PCB: Layout Fundamentals', 'Coursera · Mayıs 2026', None),
                 ('Introduction to the Internet of Things and Embedded Systems', 'Coursera', None),
                 ('MATLAB Onramp', 'MathWorks', 'assets/img/sertifika/matlab-onramp.jpg'),
                 ('LIFT UP — Sanayi Odaklı Lisans Bitirme Projeleri Konferansı', None, None),
                 ('English Language School Program (B2)', 'English Path Dubai · Ağustos 2025', None)]
    else:
        title, h, sub = 'Education — Ahmet Ulu', 'Education', 'My academic background and certificates.'
        desc = "Ahmet Ulu's academic background and certificates: Electrical and Electronics Engineering at Abdullah Gül University, English Path Dubai, Coursera and MathWorks certificates."
        items = [('🎓', 'Electrical and Electronics Engineering', 'Abdullah Gül University · Kayseri', '2024 — 2029 (expected)', "Bachelor's"),
                 ('🌐', 'Intensive English Language Program', 'English Path · Dubai, UAE', 'June — August 2025', 'B2 · Upper Intermediate')]
        cert_h, view = 'Certificates', 'View'
        certs = [('From Schematic to PCB: Layout Fundamentals', 'Coursera · May 2026', None),
                 ('Introduction to the Internet of Things and Embedded Systems', 'Coursera', None),
                 ('MATLAB Onramp', 'MathWorks', 'assets/img/sertifika/matlab-onramp.jpg'),
                 ('LIFT UP — Industry-Focused Undergraduate Capstone Projects Conference', None, None),
                 ('English Language School Program (B2)', 'English Path Dubai · August 2025', None)]
    rel = rel_of(PAGES['education'][0 if lang == 'tr' else 1])
    rows = '\n'.join('      <div class="edu-item">\n'
                     f'        <div class="edu-icon" aria-hidden="true">{i}</div>\n'
                     f'        <div><div class="edu-title">{t}</div><div class="edu-sub">{sb}</div><div class="edu-date">{d}</div><span class="badge">{b}</span></div>\n'
                     '      </div>' for i, t, sb, d, b in items)
    cl = []
    for t, o, img in certs:
        org = f'<span class="cert-org">{o}</span>' if o else ''
        link = f' <a class="inline-link" href="{rel}{img}" target="_blank" rel="noopener">{view} →</a>' if img else ''
        cl.append(f'      <li class="cert"><span class="cert-title">{t}</span>{org}{link}</li>')
    body = (f'  <div class="wrap-narrow inner fade-in">\n'
            f'    <div class="page-header"><h1>{h}</h1><p>{sub}</p></div>\n'
            f'    <div class="edu-list">\n{rows}\n    </div>\n'
            f'    <h2 class="sub-title">{cert_h}</h2>\n'
            f'    <ul class="cert-list">\n' + '\n'.join(cl) + '\n    </ul>\n'
            '  </div>')
    page(lang, 'education', title, desc, body)

def build_projects(lang):
    s = S[lang]
    rel = rel_of(PAGES['projects'][0 if lang == 'tr' else 1])
    counts = {}
    for p in PROJECTS:
        for t in p['tags']:
            counts[tag_name(t, lang)] = counts.get(tag_name(t, lang), 0) + 1
    tags = sorted(counts, key=lambda t: (-counts[t], t.lower()))
    main = '\n'.join(project_card(p, lang, rel) for p in PROJECTS if p['kind'] == 'main')
    small = '\n'.join(project_card(p, lang, rel) for p in PROJECTS if p['kind'] == 'small')
    if lang == 'tr':
        title, h, sub = 'Projeler — Ahmet Ulu', 'Projeler', 'Geliştirdiğim projeler ve çalışmalarım.'
        desc = "Ahmet Ulu'nun projeleri: akıllı tarım sistemi, EV şarj istasyonu optimizasyonu, topraksız tarım ve pratik elektronik projeler."
    else:
        title, h, sub = 'Projects — Ahmet Ulu', 'Projects', "Projects I've built and worked on."
        desc = "Ahmet Ulu's projects: a smart agriculture system, EV charging station optimization, hydroponics and practical electronics projects."
    body = f'''  <div class="wrap inner fade-in" data-filter>
    <div class="page-header"><h1>{h}</h1><p>{sub}</p></div>
{filter_bar(lang, s['search_projects'], tags)}
    <section data-filter-section>
      <div class="card-grid">
{main}
      </div>
    </section>
    <section class="section" data-filter-section>
      <div class="section-head"><h2 class="section-title">{s['small_projects']}</h2></div>
      <p class="section-desc">{s['small_projects_desc']}</p>
      <div class="card-grid">
{small}
      </div>
    </section>
    <p class="filter-empty" data-filter-empty hidden>{s['no_result']}</p>
  </div>'''
    page(lang, 'projects', title, desc, body)

def build_blog(lang):
    s = S[lang]
    rel = rel_of(PAGES['blog'][0 if lang == 'tr' else 1])
    groups = ''
    names = []
    for g in GROUPS:
        ps = [p for p in POSTS if p['group'] == g['key']]
        if not ps:
            continue
        name, gdesc = g[lang]
        names.append(name)
        items = '\n'.join(post_item(p, lang, rel, kicker=False) for p in ps)
        groups += f'''    <section class="post-group" data-filter-section>
      <h2 class="post-group-title">{name}</h2>
      <p class="post-group-desc">{gdesc}</p>
{items}
    </section>
'''
    if lang == 'tr':
        title, h, sub = 'Yazılar — Ahmet Ulu', 'Yazılar', 'Deneyimlerimi, öğrendiklerimi ve düşüncelerimi paylaştığım yer.'
        desc = 'Projelerin adım adım gelişimi, deneyimler ve öğrenilenler: su analiz sistemi, EV şarj veri altyapısı, LM2596 güç kaynağı.'
    else:
        title, h, sub = 'Blog — Ahmet Ulu', 'Blog', 'Where I share my experiences, what I learn and what I think.'
        desc = 'Step-by-step project write-ups, experiences and lessons learned: a water analysis system, EV charging data infrastructure, an LM2596 power supply.'
    body = f'''  <div class="wrap-narrow inner fade-in" data-filter>
    <div class="page-header"><h1>{h}</h1><p>{sub}</p></div>
{filter_bar(lang, s['search_posts'], names)}
{groups}    <p class="filter-empty" data-filter-empty hidden>{s['no_result']}</p>
  </div>'''
    page(lang, 'blog', title, desc, body)

def build_contact(lang):
    if lang == 'tr':
        t = dict(title='İletişim — Ahmet Ulu', h='İletişim', sub='Bir proje fikrin mi var? Yazışalım.',
                 desc='Ahmet Ulu ile iletişime geç: iş birliği, proje fikri veya sadece merhaba demek için e-posta, GitHub, LinkedIn ya da iletişim formu.',
                 intro='İş birliği, proje fikri veya sadece merhaba demek için ulaşabilirsin. Genellikle 1–2 gün içinde dönüş yaparım.',
                 mail='E-posta', name='Ad Soyad', name_ph='Adın ne?', email='E-posta', msg='Mesaj', msg_ph='Ne düşünüyorsun?',
                 send='Gönder →', sending='Gönderiliyor…', err='Mesaj gönderilemedi. Lütfen tekrar dene ya da doğrudan e-posta at.',
                 ok='✓ Mesajın alındı! En kısa sürede dönüş yapacağım.', bion='PCB tasarımı için Bionluk')
    else:
        t = dict(title='Contact — Ahmet Ulu', h='Contact', sub="Got a project idea? Let's talk.",
                 desc='Get in touch with Ahmet Ulu for collaborations, project ideas or just to say hello — by email, GitHub, LinkedIn or the contact form.',
                 intro='Reach out for a collaboration, a project idea or just to say hello. I usually reply within 1–2 days.',
                 mail='Email', name='Name', name_ph="What's your name?", email='Email', msg='Message', msg_ph="What's on your mind?",
                 send='Send →', sending='Sending…', err="The message couldn't be sent. Please try again or email me directly.",
                 ok="✓ Got your message! I'll get back to you soon.", bion='PCB design on Bionluk')
    bion = ''
    if CV:
        cvlab = 'CV (İngilizce, PDF)' if lang == 'tr' else 'CV (PDF)'
        bion += f'\n      <a href="{rel_of(PAGES["contact"][0 if lang == "tr" else 1])}{CV}" target="_blank" rel="noopener" class="contact-row"><span class="contact-icon">{ICON["doc"]}</span><span class="contact-label">CV</span><span class="contact-value">{cvlab}</span></a>'
    if BIONLUK:
        bion = f'\n      <a href="{BIONLUK}" target="_blank" rel="noopener" class="contact-row"><span class="contact-icon">{ICON["chip"]}</span><span class="contact-label">Bionluk</span><span class="contact-value">{t["bion"]}</span></a>' + bion
    body = f'''  <div class="wrap-narrow inner fade-in">
    <div class="page-header"><h1>{t['h']}</h1><p>{t['sub']}</p></div>
    <p class="contact-intro">{t['intro']}</p>
    <div class="contact-links">
      <a href="mailto:{EMAIL}" class="contact-row"><span class="contact-icon">{ICON["mail"]}</span><span class="contact-label">{t['mail']}</span><span class="contact-value">{EMAIL}</span></a>
      <a href="{GITHUB}" target="_blank" rel="noopener" class="contact-row"><span class="contact-icon">{ICON["github"]}</span><span class="contact-label">GitHub</span><span class="contact-value">github.com/ahmtuluu</span></a>
      <a href="{LINKEDIN}" target="_blank" rel="noopener" class="contact-row"><span class="contact-icon">{ICON["linkedin"]}</span><span class="contact-label">LinkedIn</span><span class="contact-value">linkedin.com/in/ahmet-ulu</span></a>{bion}
    </div>
    <form action="{FORMSPREE}" method="POST" id="contactForm" class="contact-form" data-sending="{t['sending']}">
      <div class="form-row">
        <div class="form-group"><label for="f-name">{t['name']}</label><input id="f-name" type="text" name="name" placeholder="{t['name_ph']}" autocomplete="name" required></div>
        <div class="form-group"><label for="f-mail">{t['email']}</label><input id="f-mail" type="email" name="email" placeholder="mail@example.com" autocomplete="email" inputmode="email" required></div>
      </div>
      <div class="form-group"><label for="f-msg">{t['msg']}</label><textarea id="f-msg" name="message" rows="5" placeholder="{t['msg_ph']}" required></textarea></div>
      <button type="submit" class="btn btn-primary" style="width:fit-content;margin-top:4px;">{t['send']}</button>
      <div class="form-msg err" id="formError" role="alert">{t['err']}</div>
    </form>
    <div class="form-msg ok" id="formSuccess" role="status">{t['ok']}</div>
  </div>'''
    page(lang, 'contact', t['title'], t['desc'], body)

def build_404():
    out = head('tr', '404.html', 'Sayfa bulunamadı — Ahmet Ulu', 'Aradığın sayfa bulunamadı.', None, noindex=True)
    out = out.replace('href="assets/', 'href="/assets/')
    out += nav('tr', '404.html', None, None).replace('href="', 'href="/').replace('href="/#', 'href="#')
    out += '''<main id="icerik">
  <div class="wrap-narrow notfound">
    <div class="code">404</div>
    <div class="page-header" style="margin:18px 0 28px"><h1>Bu sayfa bulunamadı</h1><p>Link değişmiş ya da sayfa kaldırılmış olabilir. · <span lang="en">This page could not be found.</span></p></div>
    <div class="home-cta" style="margin-top:0"><a class="btn btn-primary" href="/">Ana sayfa</a><a class="btn btn-ghost" href="/yazilar.html">Yazılar</a><a class="btn btn-ghost" href="/en/" lang="en">English</a></div>
  </div>
</main>
'''
    out += footer('tr', '404.html').replace('src="assets/', 'src="/assets/')
    write('404.html', out)

def build_post(p, lang):
    path = post_url(p, lang)
    alt = post_url(p, 'en' if lang == 'tr' else 'tr')
    rel = rel_of(path)
    s = S[lang]
    body = open(os.path.join(HERE, 'yazilar', f'{p["slug"]}.{lang}.html'), encoding='utf-8').read().rstrip()
    if lang == 'en':  # görseller Türkçe yazının klasöründe duruyor
        body = body.replace('<img src="', f'<img src="{rel}{p["img_dir"]}')
    others = '\n'.join(post_item(o, lang, rel) for o in POSTS if o is not p)
    blog = rel + PAGES['blog'][0 if lang == 'tr' else 1]
    y, m = p['date']
    blog_name = 'Yazılar' if lang == 'tr' else 'Blog'
    ld = [{'@context': 'https://schema.org', '@graph': [
        {'@type': 'BlogPosting', 'headline': p[lang]['title'], 'description': p[lang]['desc'],
         'image': f'{SITE}/{p["thumb"]}', 'datePublished': f'{y}-{m:02d}-01', 'dateModified': p.get('modified', f'{y}-{m:02d}-01'),
         'inLanguage': lang, 'mainEntityOfPage': f'{SITE}/{path}', 'author': {'@type': 'Person', 'name': 'Ahmet Ulu', 'url': f'{SITE}/'},
         'keywords': ', '.join(p.get('keywords', {}).get(lang, []))},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ahmet Ulu', 'item': f'{SITE}/' + ('' if lang == 'tr' else 'en/')},
            {'@type': 'ListItem', 'position': 2, 'name': blog_name, 'item': f'{SITE}/{PAGES["blog"][0 if lang == "tr" else 1]}'},
            {'@type': 'ListItem', 'position': 3, 'name': p[lang]['title'], 'item': f'{SITE}/{path}'}]}]}]
    out = head(lang, path, f'{p[lang]["page_title"]} — Ahmet Ulu', p[lang]['desc'], alt, og_image=p['thumb'], og_type='article', ld=ld)
    out += nav(lang, path, 'blog', alt)
    out += f'''<main id="icerik">
<article class="wrap-narrow article">
  <a href="{blog}" class="back-link">{s['all_posts']}</a>
{body}

  <nav class="post-nav" aria-label="{s['more_posts']}">
    <div class="post-nav-title">{s['more_posts']}</div>
{others}
  </nav>
</article>
</main>
'''
    out += footer(lang, path)
    write(path, out)

def build_sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for k, (tr, en) in PAGES.items():
        urls += [(tr, today), (en, today)]
    for p in POSTS:
        y, m = p['date']
        mod = p.get('modified', f'{y}-{m:02d}-01')
        urls += [(p['tr_url'], mod), (p['en_url'], mod)]
    body = '\n'.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>{d}</lastmod></url>'.replace('/index.html<', '/<') for u, d in urls)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')

if __name__ == '__main__':
    print('Sayfalar üretiliyor:')
    for lang in ('tr', 'en'):
        build_home(lang); build_about(lang); build_education(lang)
        build_projects(lang); build_blog(lang); build_contact(lang)
        for p in POSTS:
            build_post(p, lang)
    build_404(); build_sitemap()
    print('Tamam.')
