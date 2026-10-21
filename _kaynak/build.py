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
import os, sys, html, hashlib, json, datetime
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import araclar
import pcb

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
CV = {'tr': 'assets/ahmet-ulu-cv-tr.pdf', 'en': 'assets/ahmet-ulu-cv.pdf'}   # telefonsuz web sürümleri; telefonlu başvuru sürümleri repo dışında (ahmetulu_website\\cv-basvuru)
GSC_VERIFICATION = "kDmbOcP_ZD3wqx9IxPQzHMZo0sCyWcbTu7h1BzVJdyA"   # Google Search Console 'HTML etiketi' doğrulama kodu (content="..." içindeki değer)
GOATCOUNTER = None    # ör. 'ahmetulu' (goatcounter.com hesabındaki kod)

# ---------------------------------------------------------------- ikonlar
ICON = {
 'github': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>',
 'linkedin': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>',
 'search': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 'leaf': '<svg viewBox="0 0 24 24" width="46" height="46" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
 'download': '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11m0 0-4.5-4.5M12 15l4.5-4.5M5 20h14"/></svg>',
 'doc': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg>',
 'chip': '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
}

# ---------------------------------------------------------------- arayüz metinleri
S = {
 'tr': dict(
   nav=[('home', None), ('about', 'Hakkımda'), ('education', 'Eğitim'), ('projects', 'Projeler'), ('blog', 'Yazılar'), ('tools', 'Araçlar'), ('contact', 'İletişim')],
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
   nav=[('home', None), ('about', 'About'), ('education', 'Education'), ('projects', 'Projects'), ('blog', 'Blog'), ('tools', 'Tools'), ('contact', 'Contact')],
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
 'tools': ('araclar.html', 'en/tools.html'),
 'pcb': ('pcb-tasarim-hizmeti.html', 'en/pcb-design-service.html'),
 'contact': ('iletisim.html', 'en/contact.html'),
}
MONTHS = {'tr': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}

# ---------------------------------------------------------------- içerik
GROUPS = [  # yazılar sayfasındaki gruplar (sıra önemli)
 dict(key='web', tr=('Web Projeleri', 'Tasarlayıp kodladığım siteler'), en=('Web Projects', 'Websites I designed and built')),
 dict(key='pcb', tr=('PCB Tasarımları', 'Bionluk üzerinden müşteriler için yaptığım tasarımlar'), en=('PCB Designs', 'Designs I made for clients through Bionluk')),
 dict(key='tarim', tr=('Akıllı Tarım Sistemi', 'Projenin adım adım gelişimi'), en=('Smart Agriculture System', 'Step-by-step development of the project')),
 dict(key='ev', tr=('Elektrik Şarj İstasyonu Optimizasyonu', 'Projenin adım adım gelişimi'), en=('EV Charging Station Optimization', 'Step-by-step development of the project')),
 dict(key='pratik', tr=('Pratik Projeler', 'Öğrenmek için yapılan küçük denemeler'), en=('Practical Projects', 'Small experiments built to learn')),
]

POSTS = [  # en yeni en üstte
 dict(slug='mustech-web', group='web', date=(2026, 10),
      tr_url='yazilar/mustech-web/mustech-agro-web-sitesi.html', en_url='en/blog/mustech-agro-website.html',
      img_dir='yazilar/mustech-web/', thumb='assets/img/kapak/mustech-web.jpg',
      keywords={'tr': ['MUSTECH', 'Mustech Agro', 'akıllı tarım web sitesi', 'HTML CSS JavaScript', 'FAO-56 sulama hesabı'],
                'en': ['MUSTECH', 'Mustech Agro', 'smart agriculture website', 'HTML CSS JavaScript', 'FAO-56 irrigation calculator']},
      tr=dict(kicker='Web Tasarımı · MUSTECH', title='MUSTECH Agro Web Sitesi', page_title='MUSTECH Agro Web Sitesi: HTML, CSS ve JavaScript ile Akıllı Tarım Sitesi',
              desc='MUSTECH Agro için tasarlayıp kodladığım web sitesi: iki dil, açık/koyu tema, buğday tarlası animasyonu, hava durumuna dayalı tarla araçları, FAO-56 sulama hesaplayıcı ve sohbet asistanı.'),
      en=dict(kicker='Web Design · MUSTECH', title='The MUSTECH Agro Website', page_title='The MUSTECH Agro Website: A Smart Agriculture Site in HTML, CSS and JavaScript',
              desc='The website I designed and built for MUSTECH Agro: two languages, light/dark themes, a wheat field animation, weather-based field tools, an FAO-56 irrigation calculator and a chat assistant.')),
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
 dict(kind='main', year='2026', cover='assets/img/kapak/planner.jpg', posts=[],
      links=[('Canlı demoyu dene ↗', 'Try the live demo ↗', 'https://ahmtuluu.github.io/planner/demo.html'),
             ('Tanıtım sayfası ↗', 'Product page ↗', 'https://ahmtuluu.github.io/planner/')],
      tags=['Uygulama', 'JavaScript', 'PWA', 'Google Apps Script', 'Gemini API', 'Telegram Bot'],
      tr=dict(title='Planner — Akıllı Ajanda Uygulaması', desc='Kendi ihtiyacım için yaptığım ajanda: Telegram\'dan sabah brifingi ve hatırlatmalar, Gemini ile gün planı ve alt adımlar, mesajla görev ekleme, alışkanlık serileri. Telefonda uygulama gibi kurulur, bilgisayarda tarayıcıda çalışır.'),
      en=dict(title='Planner — Smart Planner App', desc='A planner I built for myself: morning briefings and reminders on Telegram, day plans and subtasks with Gemini, adding tasks by message and habit streaks. Installs like an app on the phone and runs in the browser on a computer.')),
 dict(kind='main', year='2026', cover='assets/img/kapak/mustech-web.jpg', posts=['mustech-web'], url='https://mustechagro.com.tr/',
      tags=['Web Tasarımı', 'HTML/CSS', 'JavaScript', 'MUSTECH'],
      tr=dict(title='MUSTECH Agro Web Sitesi', desc='Çalıştığım akıllı tarım şirketinin sitesi: iki dil, açık/koyu tema, hava durumuna dayalı tarla araçları, FAO-56 sulama hesaplayıcı ve sohbet asistanı. Düz HTML, CSS ve JavaScript.'),
      en=dict(title='MUSTECH Agro Website', desc='The site of the smart agriculture company I work at: two languages, light/dark themes, weather-based field tools, an FAO-56 irrigation calculator and a chat assistant. Plain HTML, CSS and JavaScript.')),
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
FEATURED = [0, 3, 4]  # ana sayfadaki projeler (PROJECTS indeksleri)

TAG_EN = {'Uygulama': 'App', 'Web Tasarımı': 'Web Design', 'PCB Tasarımı': 'PCB Design', 'Sensör': 'Sensors', 'Enerji': 'Energy', 'Otomasyon': 'Automation', 'Güç Elektroniği': 'Power Electronics',
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
    if path in ('index.html', 'en/index.html'):
        gsc += ''.join(f'<link rel="me" href="{u}">\n' for u in [GITHUB, LINKEDIN] + ([BIONLUK] if BIONLUK else []))
    ldjson = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld or []))
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<meta name="author" content="Ahmet Ulu">
<meta name="theme-color" content="#0a0f1c">
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

# ---------------------------------------------------------------- CV seçici (TR / EN)
CV_META = {
    'tr': dict(name='Türkçe', code='TR', file='Ahmet_Ulu_CV_TR.pdf', img='assets/img/cv/cv-tr.jpg'),
    'en': dict(name='English', code='EN', file='Ahmet_Ulu_CV_EN.pdf', img='assets/img/cv/cv-en.jpg'),
}
CV_UPDATED = {'tr': 'Ekim 2026', 'en': 'October 2026'}

def cv_options(lang, rel):
    """İki dilli CV kartları (pencerede ve Hakkımda sayfasında ortak)."""
    tr = lang == 'tr'
    order = ['tr', 'en'] if tr else ['en', 'tr']
    cards = []
    for i, k in enumerate(order):
        m = CV_META[k]
        kb = max(1, round(os.path.getsize(os.path.join(ROOT, CV[k])) / 1024))
        meta = (f'1 sayfa · PDF · {kb} KB' if tr else f'1 page · PDF · {kb} KB')
        rec = (f'<span class="cv-rec">{"Bu sayfanın dili" if tr else "This page"}</span>' if i == 0 else '')
        sub = {('tr', 'tr'): 'Türk firmaları için', ('tr', 'en'): 'Uluslararası başvurular için',
               ('en', 'en'): 'For international applications', ('en', 'tr'): 'For companies in Türkiye'}[(lang, k)]
        cards.append(
            f'<div class="cv-opt{" is-first" if i == 0 else ""}">'
            f'<a class="cv-prev" href="{rel}{CV[k]}" target="_blank" rel="noopener" hreflang="{k}" aria-label="{m["name"]} CV — {"önizle" if tr else "preview"}">'
            f'<img src="{rel}{m["img"]}" alt="" width="520" height="322" loading="lazy" decoding="async"><span class="cv-code">{m["code"]}</span></a>'
            f'<div class="cv-opt-body"><div class="cv-opt-head"><span class="cv-lang">{m["name"]}</span>{rec}</div>'
            f'<div class="cv-sub">{sub}</div><div class="cv-meta">{meta}</div>'
            f'<div class="cv-actions"><a class="btn {"btn-primary" if i == 0 else "btn-ghost"} cv-dl" href="{rel}{CV[k]}" download="{m["file"]}" hreflang="{k}">'
            f'{ICON["download"]}{"İndir" if tr else "Download"}</a>'
            f'<a class="cv-view" href="{rel}{CV[k]}" target="_blank" rel="noopener" hreflang="{k}">{"Önizle" if tr else "Preview"} ↗</a></div></div></div>')
    return f'<div class="cv-opts">{"".join(cards)}</div>'

def cv_note(lang):
    return ('Telefon numaram gizlilik için web sürümünde yok; ihtiyacınız olursa e-postayla isteyebilirsiniz.' if lang == 'tr'
            else 'My phone number is left out of the web version for privacy; feel free to ask for it by email.')

def cv_dialog(lang, rel):
    tr = lang == 'tr'
    return (f'<dialog class="cv-dialog" id="cvDialog" aria-labelledby="cvDlgTitle">\n'
            f'  <div class="cv-dlg-inner">\n'
            f'    <div class="cv-dlg-head"><div><h2 id="cvDlgTitle">{"CV\'mi indir" if tr else "Download my CV"}</h2>'
            f'<p>{"Hangi dilde istersin? İkisi de tek sayfa ve güncel" if tr else "Which language do you need? Both are one page and up to date"} ({CV_UPDATED[lang]}).</p></div>'
            f'<button type="button" class="cv-close" data-cv-close aria-label="{"Kapat" if tr else "Close"}">×</button></div>\n'
            f'    {cv_options(lang, rel)}\n'
            f'    <p class="cv-note">{cv_note(lang)}</p>\n'
            f'  </div>\n'
            f'</dialog>\n')

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
{cv_dialog(lang, rel) if CV else ''}<script src="{rel}assets/js/main.js?v={asset_ver('assets/js/main.js')}" defer></script>
</body>
</html>
'''

def asset_ver(path):
    # Dosya içeriğinden kısa sürüm kodu: CSS/JS değişince tarayıcı eski önbelleği kullanmaz
    with open(os.path.join(ROOT, path), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def person_ld(lang):
    return {
        '@type': 'Person', '@id': f'{SITE}/#ahmet-ulu', 'name': 'Ahmet Ulu', 'alternateName': ['Ahmet ULU', 'ahmtuluu'],
        'givenName': 'Ahmet', 'familyName': 'Ulu', 'url': f'{SITE}/',
        'description': ("Abdullah Gül Üniversitesi'nde elektrik-elektronik mühendisliği öğrencisi; MUSTECH'te gömülü sistemler geliştiricisi ve freelance PCB tasarımcısı."
                        if lang == 'tr' else 'Electrical and electronics engineering student at Abdullah Gül University, embedded systems developer at MUSTECH and freelance PCB designer.'),
        'worksFor': {'@type': 'Organization', 'name': 'MUSTECH', 'url': 'https://mustechagro.com.tr/'},
        'knowsLanguage': ['tr', 'en'],
        'image': f'{SITE}/assets/img/og.jpg', 'email': f'mailto:{EMAIL}',
        'jobTitle': 'Elektrik-Elektronik Mühendisliği Öğrencisi, Gömülü Sistemler Geliştiricisi' if lang == 'tr' else 'Electrical & Electronics Engineering Student, Embedded Systems Developer',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Kayseri', 'addressCountry': 'TR'},
        'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Abdullah Gül Üniversitesi', 'url': 'https://www.agu.edu.tr/'},
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
def reading_time(p, lang):
    import re as _re
    path = os.path.join(HERE, 'yazilar', f'{p["slug"]}.{lang}.html')
    txt = _re.sub(r'<[^>]+>', ' ', open(path, encoding='utf-8').read())
    words = len(txt.split())
    mins = max(1, round(words / 190))
    return f'{mins} dk okuma' if lang == 'tr' else f'{mins} min read'

def post_item(p, lang, rel, kicker=True):
    t = p[lang]
    k = f'<div class="post-kicker">{t["kicker"]}</div>' if kicker else ''
    g = next(x for x in GROUPS if x['key'] == p['group'])[lang][0]
    return f'''<a href="{rel}{post_url(p, lang)}" class="post-item" data-filter-item data-tags="{esc(g)}">
  <img class="post-thumb" src="{rel}{p["thumb"]}" alt="" width="96" height="72" loading="lazy" decoding="async">
  <div class="post-info">{k}<div class="post-title">{t["title"]}</div><div class="post-date">{date_str(p, lang)} · {reading_time(p, lang)}</div></div>
  <span class="post-arrow" aria-hidden="true">→</span>
</a>'''

def post_card(p, lang, rel):
    t = p[lang]
    return f'''<a href="{rel}{post_url(p, lang)}" class="post-card">
  <div class="post-card-media"><img src="{rel}{p["thumb"]}" alt="" width="800" height="500" loading="lazy" decoding="async"></div>
  <div class="post-card-body">
    <div class="post-kicker">{t["kicker"]}</div>
    <h3 class="post-card-title">{t["title"]}</h3>
    <p class="post-card-desc">{t["desc"]}</p>
    <div class="post-date">{date_str(p, lang)} · {reading_time(p, lang)}</div>
  </div>
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
    if pr.get('url'):
        visit = 'Siteyi ziyaret et ↗' if lang == 'tr' else 'Visit the site ↗'
        links += f'<a class="card-link" href="{pr["url"]}" target="_blank" rel="noopener">{visit}</a>'
    if pr.get('links'):
        links = ''.join(f'<a class="card-link{" card-stretch" if i == 0 and not pr["posts"] else ""}" href="{u}" target="_blank" rel="noopener">{ltr if lang == "tr" else len_}</a>'
                        for i, (ltr, len_, u) in enumerate(pr['links'])) + (links if pr['posts'] else '')
        count = count if pr['posts'] else f'<span class="badge">{"Canlı demo" if lang == "tr" else "Live demo"}</span>'
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
    return f'''      <section class="section">
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
    return f'''      <section class="section">
        <div class="section-head"><h2 class="section-title">{s["reviews"]}</h2>{more}</div>
        <div class="review-grid">
{items}
        </div>
      </section>
'''

# ---------------------------------------------------------------- sayfalar
# ---------------------------------------------------------------- PCB tasarım hizmeti
def pcb_svg_icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{pcb.ICONS[name]}</svg>'

def pcb_explain(lang, rel, P):
    """Ana sayfadaki kısa 'PCB nedir?' bölümü."""
    t = pcb.T[lang]
    chips = ''.join(f'<li>{esc(c)}</li>' for c in t['home_chips'])
    b2 = f'<a class="btn btn-ghost" href="{BIONLUK}" target="_blank" rel="noopener">{t["home_b2"]}</a>' if BIONLUK else ''
    return (f'    <section class="section" id="pcb-nedir" data-reveal="0">\n'
            f'      <div class="pcb-explain">\n'
            f'        <div class="pcb-explain-text">\n'
            f'          <span class="tool-kicker">{t["home_k"]}</span>\n'
            f'          <h2 class="section-title">{t["home_h"]}</h2>\n'
            f'          <p>{t["home_p"]}</p>\n'
            f'          <ul class="pcb-uses">{chips}</ul>\n'
            f'          <div class="cta-actions"><a class="btn btn-primary" href="{P("pcb")}">{t["home_b1"]}</a>{b2}</div>\n'
            f'        </div>\n'
            f'        <div class="pcb-explain-art">{pcb.illustration(lang)}</div>\n'
            f'      </div>\n'
            f'    </section>\n')

def build_pcb_service(lang):
    tr = lang == 'tr'
    t = pcb.T[lang]
    path = PAGES['pcb'][0 if tr else 1]
    rel = rel_of(path)
    P = lambda k: rel + PAGES[k][0 if tr else 1]
    img = lambda f: f'{rel}assets/img/pcb/{f}'
    bion = f'<a class="btn btn-primary" href="{BIONLUK}" target="_blank" rel="noopener">{t["b1"]}</a>' if BIONLUK else ''
    actions = f'<div class="cta-actions">{bion}<a class="btn btn-ghost" href="{P("contact")}">{t["b2"]}</a></div>'
    when = '\n'.join(f'        <div class="tile pcb-when"><span class="tool-ico">{pcb_svg_icon(ic)}</span>'
                     f'<div class="tile-title">{esc(h)}</div><p class="tile-sub">{esc(d)}</p></div>' for ic, h, d in t['when'])
    types = ''.join(f'<li>{esc(x)}</li>' for x in t['types'])
    steps = []
    for i, (im, h, d) in enumerate(t['steps'], 1):
        media = (f'<div class="pcb-step-media"><img src="{img(im)}" alt="{esc(h)}" width="720" height="540" loading="lazy" decoding="async"></div>' if im
                 else f'<div class="pcb-step-media pcb-step-chat">{pcb_svg_icon("chat")}</div>')
        steps.append(f'        <li class="pcb-step">{media}<div class="pcb-step-body"><span class="pcb-step-n">{i}</span>'
                     f'<div class="tile-title">{esc(h)}</div><p class="tile-sub">{esc(d)}</p></div></li>')
    post = POST.get('pcb-tasarim')
    post_href = rel + post_url(post, lang) if post else P('projects')
    work = '\n'.join(f'        <a class="tile tile-img pcb-work" href="{post_href}"><img src="{img(im)}" alt="{esc(h)}" width="720" height="540" loading="lazy" decoding="async">'
                     f'<div class="tile-over"><div class="tile-title">{esc(h)}</div><div class="tile-sub">{esc(d)}</div></div></a>' for im, h, d in t['work'])
    need = ''.join(f'<li>{esc(x)}</li>' for x in t['need'])
    faq = '\n'.join(f'        <details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in t['faq'])
    body = f'''  <div class="wrap inner fade-in pcb-page">
    <nav class="crumbs" aria-label="{'Konum' if tr else 'Breadcrumb'}"><a href="{P('home')}">{'Ana sayfa' if tr else 'Home'}</a><span aria-hidden="true">/</span><span>{'PCB tasarımı' if tr else 'PCB design'}</span></nav>
    <header class="pcb-hero">
      <div class="tool-head"><span class="tool-kicker">{t['k']}</span><h1>{t['h']}</h1><p>{t['lead']}</p>
        {actions}
      </div>
      {stats_html(lang)}
    </header>

    <section class="pcb-sec pcb-what">
      <div class="pcb-what-text"><h2 class="section-title">{t['what_h']}</h2>{''.join(f'<p>{x}</p>' for x in t['what_p'])}</div>
      <div class="pcb-explain-art">{pcb.illustration(lang)}</div>
    </section>

    <section class="pcb-sec">
      <h2 class="section-title">{t['when_h']}</h2>
      <div class="pcb-when-grid">
{when}
      </div>
      <h3 class="pcb-sub">{t['types_h']}</h3>
      <ul class="pcb-uses">{types}</ul>
    </section>

    <section class="pcb-sec">
      <h2 class="section-title">{t['steps_h']}</h2>
      <ol class="pcb-steps">
{chr(10).join(steps)}
      </ol>
    </section>

    <section class="pcb-sec">
      <div class="section-head"><div><h2 class="section-title">{t['work_h']}</h2></div><a class="section-link" href="{post_href}">{t['work_more']}</a></div>
      <div class="pcb-work-grid">
{work}
      </div>
    </section>

    <section class="pcb-sec pcb-two">
      <div class="pcb-need"><h2 class="section-title">{t['need_h']}</h2><ul class="pcb-check">{need}</ul></div>
      <div class="pcb-faq"><h2 class="section-title">{t['faq_h']}</h2>
{faq}
      </div>
    </section>
{reviews_block(lang)}
    <section class="section">
      <div class="cta-band">
        <div><h2 class="section-title">{t['cta_h']}</h2><p>{t['cta_p']}</p></div>
        {actions}
      </div>
    </section>
  </div>'''
    ld = [{'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', 'name': 'PCB tasarımı' if tr else 'PCB design', 'serviceType': 'PCB design',
         'description': t['desc'], 'url': f'{SITE}/{path}', 'areaServed': 'TR', 'inLanguage': lang,
         'provider': {'@id': f'{SITE}/#ahmet-ulu'}},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ahmet Ulu', 'item': f'{SITE}/' + ('' if tr else 'en/')},
            {'@type': 'ListItem', 'position': 2, 'name': 'PCB tasarımı' if tr else 'PCB design', 'item': f'{SITE}/{path}'}]}]}]
    page(lang, 'pcb', t['title'], t['desc'], body, ld=ld)

# ---------------------------------------------------------------- Planner (uygulama tanıtımı)
PLANNER = dict(
    site='https://ahmtuluu.github.io/planner/', demo='https://ahmtuluu.github.io/planner/demo.html',
    tr=dict(k='Yeni · Kendi yaptığım uygulama', h='Planner', tag='Günün, cebinde.',
            p='Kendi ihtiyacım için yaptığım akıllı ajanda. Sabahları Telegram\'dan günün özetini gönderiyor, Gemini ile günümü saat saat planlıyor, yaklaşan teslimleri hatırlatıyor. Telefona uygulama olarak kuruluyor, bilgisayarda tarayıcıda çalışıyor.',
            feats=[('☀️', 'Telegram\'dan sabah brifingi'), ('✨', 'Gemini ile gün planı'), ('🧩', 'Görevi alt adımlara bölme'),
                   ('💬', '"yarın 14:00 #iş" gibi hızlı ekleme'), ('🔥', 'Alışkanlık serileri'), ('📱', 'Telefon + bilgisayar')],
            b1='Canlı demoyu dene ↗', b2='Tanıtım sayfası ↗',
            note='Sunucusuz: Google Apps Script + Google Sheets · Telegram Bot API · Gemini API',
            alts=['Planner takvim ekranı', 'Planner bugün ekranı', 'Planner istatistik ekranı, koyu tema']),
    en=dict(k='New · An app I built', h='Planner', tag='Your day, in your pocket.',
            p='A smart planner I built for myself. Every morning it sends a summary of the day on Telegram, plans my day hour by hour with Gemini and reminds me of upcoming deadlines. It installs as an app on the phone and runs in the browser on a computer.',
            feats=[('☀️', 'Morning briefing on Telegram'), ('✨', 'Day plan with Gemini'), ('🧩', 'Break tasks into steps'),
                   ('💬', 'Quick add: "tomorrow 14:00 #work"'), ('🔥', 'Habit streaks'), ('📱', 'Phone + desktop')],
            b1='Try the live demo ↗', b2='Product page ↗',
            note='Serverless: Google Apps Script + Google Sheets · Telegram Bot API · Gemini API',
            alts=['Planner calendar screen', 'Planner today screen', 'Planner statistics screen, dark theme']),
)

def home_planner(lang, rel):
    t = PLANNER[lang]
    feats = ''.join(f'<li><span aria-hidden="true">{e}</span>{esc(x)}</li>' for e, x in t['feats'])
    imgs = ''.join(f'<img class="pl-phone pl-{i}" src="{rel}assets/img/planner/{f}.jpg" alt="{esc(a)}" width="600" height="1298" loading="lazy" decoding="async">'
                   for i, (f, a) in enumerate(zip(['takvim', 'bugun', 'istatistik'], t['alts'])))
    return (f'    <section class="section" id="planner" data-reveal="0">\n'
            f'      <div class="planner-band">\n'
            f'        <div class="planner-text">\n'
            f'          <span class="pl-kicker">{t["k"]}</span>\n'
            f'          <div class="pl-title"><img src="{rel}assets/img/planner/icon.png" alt="" width="56" height="56"><div><h2>{t["h"]}</h2><p class="pl-tag">{t["tag"]}</p></div></div>\n'
            f'          <p>{t["p"]}</p>\n'
            f'          <ul class="pl-feats">{feats}</ul>\n'
            f'          <div class="cta-actions"><a class="btn pl-btn" href="{PLANNER["demo"]}" target="_blank" rel="noopener">{t["b1"]}</a>'
            f'<a class="btn btn-ghost" href="{PLANNER["site"]}" target="_blank" rel="noopener">{t["b2"]}</a></div>\n'
            f'          <p class="pl-note">{t["note"]}</p>\n'
            f'        </div>\n'
            f'        <div class="planner-art" aria-hidden="false">{imgs}</div>\n'
            f'      </div>\n'
            f'    </section>\n')

HOME_TOOLS = ['led', 'regulator', 'color', 'trace']
def home_tools(lang, rel, P):
    tr = lang == 'tr'
    h = 'Elektronik hesap araçları' if tr else 'Electronics calculators'
    sub = (f'LED direncinden LM2596 ayarına, {len(araclar.TOOLS)} ücretsiz araç. Formülleri ve kaynaklarıyla.' if tr
           else f'From LED resistors to LM2596 settings: {len(araclar.TOOLS)} free tools, with formulas and sources.')
    cards = '\n'.join(tool_card(araclar.TOOL[i], lang, rel, tags=False) for i in HOME_TOOLS)
    return (f'    <section class="section" data-reveal="0">\n'
            f'      <div class="section-head"><div><h2 class="section-title">{h}</h2><p class="section-sub">{sub}</p></div><a class="section-link" href="{P("tools")}">{S[lang]["see_all"]}</a></div>\n'
            f'      <div class="tool-grid home-tools">\n{cards}\n      </div>\n    </section>')

def build_home(lang):
    s = S[lang]
    rel = rel_of(PAGES['home'][0 if lang == 'tr' else 1])
    P = lambda k: rel + PAGES[k][0 if lang == 'tr' else 1]
    tr = lang == 'tr'
    pcb_proj = PROJECTS[FEATURED[0]]
    small1, small2 = PROJECTS[FEATURED[1]], PROJECTS[FEATURED[2]]
    feat_posts = set(pcb_proj['posts'])
    latest = next((p for p in POSTS if p['slug'] not in feat_posts), POSTS[0])

    def proj_link(pr):
        return rel + post_url(POST[pr['posts'][0]], lang) if pr['posts'] else P('projects')

    if tr:
        title = 'Ahmet Ulu — Elektrik-Elektronik, Gömülü Sistemler ve IoT'
        desc = "Ahmet Ulu — Kayseri'den elektrik-elektronik mühendisliği öğrencisi. Gömülü sistemler, IoT ve PCB tasarımı projeleri, yazılar ve deneyimler."
        l1, l2 = 'Merhaba, ben', 'Ahmet Ulu.'
        role = 'Gömülü Sistemler · IoT · PCB Tasarımı'
        intro = 'Elektrik-elektronik öğrencisiyim. Asıl öğrendiklerimin çoğu ders dışında, bir şeyler yaparken ortaya çıktı: sensörlerden PCB\'lere, Raspberry Pi\'den mobil uygulamalara.'
        b1, b2 = 'Projelerime bak', 'İletişime geç'
        avail = 'Freelance PCB işlerine açığım'
        uni, uni2 = 'Abdullah Gül Üniversitesi', 'Elektrik-Elektronik Müh.'
        st_h, st_sub, st_link = 'Bionluk puanı', '8 tamamlanan sipariş · 6/6 beş yıldız', 'Profilim →'
        stack_h = 'Kullandıklarım'
        now_h, now_1, now_2 = 'Şu an', 'MUSTECH\'te gömülü sistemler geliştiricisi', 'Bionluk\'ta freelance PCB tasarımı'
        feat_k = 'Öne çıkan'
        soc_h = 'Bağlantılar'
        last_k = 'Son yazı'
        cv_h, cv_t = 'CV', 'Türkçe · English'
        blog_h, blog_sub = 'Son yazılar', 'Projelerin adım adım hikâyesi, hatalar ve öğrendiklerim.'
        cta_h, cta_t = 'Bir projen mi var?', 'PCB tasarımı, gömülü sistem ya da IoT fikrin varsa konuşalım. Genellikle 1–2 gün içinde dönüş yaparım.'
        cta_b1, cta_b2 = 'Bana yaz →', 'Bionluk profilim'
    else:
        title = 'Ahmet Ulu — Electrical & Electronics, Embedded Systems and IoT'
        desc = 'Ahmet Ulu — an electrical and electronics engineering student from Kayseri, Türkiye. Embedded systems, IoT and PCB design projects, posts and experiences.'
        l1, l2 = "Hi, I'm", 'Ahmet Ulu.'
        role = 'Embedded Systems · IoT · PCB Design'
        intro = "I'm an electrical and electronics engineering student. Most of what I've really learned came from outside the classroom, while building things: from sensors to PCBs, from Raspberry Pi to mobile apps."
        b1, b2 = 'See my projects', 'Get in touch'
        avail = 'Open to freelance PCB work'
        uni, uni2 = 'Abdullah Gül University', 'Electrical & Electronics Eng.'
        st_h, st_sub, st_link = 'Bionluk rating', '8 completed orders · 6/6 five-star', 'My profile →'
        stack_h = 'My toolkit'
        now_h, now_1, now_2 = 'Now', 'Embedded systems developer at MUSTECH', 'Freelance PCB design on Bionluk'
        feat_k = 'Featured'
        soc_h = 'Elsewhere'
        last_k = 'Latest post'
        cv_h, cv_t = 'CV', 'English · Türkçe'
        blog_h, blog_sub = 'Latest posts', 'Step-by-step project stories, mistakes and lessons learned.'
        cta_h, cta_t = 'Got a project in mind?', "If you have a PCB, embedded or IoT idea, let's talk. I usually reply within 1–2 days."
        cta_b1, cta_b2 = 'Write to me →', 'My Bionluk profile'

    stack = ['ESP32', 'STM32', 'Raspberry Pi', 'Arduino', 'KiCad', 'Python', 'C / C++', 'MATLAB']
    stack_html = ''.join(f'<span class="chip-sm">{x}</span>' for x in stack)
    rating = STATS[1][0] if len(STATS) > 1 else '5.0'
    cv_tile = ''
    if CV:
        cv_tile = f'''      <a class="tile t-cv" href="{rel}{CV[lang]}" target="_blank" rel="noopener" data-cv-open aria-haspopup="dialog" data-reveal="6">
        <div class="tile-k">{cv_h}</div>
        <div class="cv-icon" aria-hidden="true">{ICON['doc']}</div>
        <div class="tile-sub">{cv_t} ↓</div>
      </a>'''
    bion_soc = f'<a href="{BIONLUK}" target="_blank" rel="noopener" class="soc">{ICON["chip"]}<span>Bionluk</span></a>' if BIONLUK else ''

    def small_tile(pr, cls, d):
        t = pr[lang]
        return f'''      <a class="tile tile-img {cls}" href="{proj_link(pr)}" data-reveal="{d}">
        <img src="{rel}{pr['cover']}" alt="" width="800" height="500" loading="lazy" decoding="async">
        <div class="tile-over"><div class="tile-k">{pr['year']}</div><div class="tile-title">{t['title']}</div></div>
      </a>'''

    posts = '\n'.join(post_card(p, lang, rel) for p in [x for x in POSTS if x is not latest][:3])
    body = f'''  <div class="wrap">
    <section class="bento" aria-label="{'Tanıtım' if tr else 'Introduction'}">
      <div class="tile t-intro" data-reveal="0">
        <a class="avail" href="{P('pcb')}"><span class="dot" aria-hidden="true"></span>{avail}</a>
        <h1 class="home-title" id="homeTitle"><span class="tline">{l1}</span><em class="tline">{l2}</em></h1>
        <div class="role">{role}</div>
        <p class="home-desc">{intro}</p>
        <div class="home-cta">
          <a class="btn btn-primary" href="{P('projects')}">{b1}</a>
          <a class="btn btn-ghost" href="{P('contact')}">{b2}</a>
        </div>
      </div>
      <div class="tile t-mono" data-reveal="1">
        <div class="mono" aria-hidden="true"><span>AU</span></div>
        <div class="tile-title">{uni}</div>
        <div class="tile-sub">{uni2} · Kayseri</div>
      </div>
      <a class="tile t-stat" href="{BIONLUK or P('contact')}" target="_blank" rel="noopener" data-reveal="2">
        <div class="tile-k">{st_h}</div>
        <div class="big-num">★ {rating}</div>
        <div class="tile-sub">{st_sub}</div>
        <div class="tile-link">{st_link}</div>
      </a>
      <div class="tile t-stack" data-reveal="3">
        <div class="tile-k">{stack_h}</div>
        <div class="chips-sm">{stack_html}</div>
      </div>
      <a class="tile tile-img t-feat" href="{proj_link(pcb_proj)}" data-reveal="1">
        <img src="{rel}{pcb_proj['cover']}" alt="" width="800" height="500" loading="lazy" decoding="async">
        <div class="tile-over">
          <div class="tile-k">{feat_k} · {pcb_proj['year']}</div>
          <div class="tile-title lg">{pcb_proj[lang]['title']}</div>
          <div class="tile-sub">{pcb_proj[lang]['desc']}</div>
        </div>
      </a>
{small_tile(small1, 't-p1', 2)}
{small_tile(small2, 't-p2', 3)}
      <div class="tile t-now" data-reveal="4">
        <div class="tile-k">{now_h}</div>
        <ul class="now-list"><li>{now_1}</li><li>{now_2}</li></ul>
      </div>
      <div class="tile t-soc" data-reveal="5">
        <div class="tile-k">{soc_h}</div>
        <div class="socs">
          <a href="{GITHUB}" target="_blank" rel="noopener" class="soc">{ICON['github']}<span>GitHub</span></a>
          <a href="{LINKEDIN}" target="_blank" rel="noopener" class="soc">{ICON['linkedin']}<span>LinkedIn</span></a>
          {bion_soc}
          <a href="mailto:{EMAIL}" class="soc">{ICON['mail']}<span>{'E-posta' if tr else 'Email'}</span></a>
        </div>
      </div>
      <a class="tile t-last" href="{rel}{post_url(latest, lang)}" data-reveal="5">
        <img src="{rel}{latest['thumb']}" alt="" width="800" height="500" loading="lazy" decoding="async">
        <div>
          <div class="tile-k">{last_k} · {date_str(latest, lang)}</div>
          <div class="tile-title">{latest[lang]['title']}</div>
          <div class="tile-sub">{reading_time(latest, lang)}</div>
        </div>
        <span class="tile-arrow" aria-hidden="true">→</span>
      </a>
{cv_tile}
    </section>
{home_planner(lang, rel)}{pcb_explain(lang, rel, P)}
    <section class="section" data-reveal="0">
      <div class="section-head"><div><h2 class="section-title">{blog_h}</h2><p class="section-sub">{blog_sub}</p></div><a class="section-link" href="{P('blog')}">{s['see_all']}</a></div>
      <div class="post-cards">
{posts}
      </div>
    </section>
{reviews_block(lang)}
{home_tools(lang, rel, P)}
    <section class="section">
      <div class="cta-band" data-reveal="0">
        <div><h2 class="section-title">{cta_h}</h2><p>{cta_t}</p></div>
        <div class="cta-actions"><a class="btn btn-primary" href="{P('contact')}">{cta_b1}</a>{f'<a class="btn btn-ghost" href="{BIONLUK}" target="_blank" rel="noopener">{cta_b2}</a>' if BIONLUK else ''}</div>
      </div>
    </section>
  </div>'''
    ld = [{'@context': 'https://schema.org', '@graph': [person_ld(lang),
          {'@type': 'WebSite', '@id': f'{SITE}/#site', 'url': f'{SITE}/', 'name': 'Ahmet Ulu', 'alternateName': ['ahmetulu.com.tr', 'Ahmet Ulu — Kişisel Site'], 'inLanguage': lang, 'publisher': {'@id': f'{SITE}/#ahmet-ulu'}}]}]
    page(lang, 'home', title, desc, body, ld=ld)

ABOUT = {
 'tr': dict(title='Ahmet Ulu Kimdir? — Hakkımda', h='Ahmet Ulu hakkında', sub='Kim olduğum, ne ile ilgilendiğim.',
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
 'en': dict(title='About Ahmet Ulu — Electronics Engineering Student', h='About Ahmet Ulu', sub='Who I am and what I work on.',
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
        h = 'CV\'mi indir' if lang == 'tr' else 'Download my CV'
        cv = (f'\n    <section class="cv-inline" id="cv"><h2 class="sub-title">{h}</h2>{cv_options(lang, rel)}'
              f'<p class="cv-note">{cv_note(lang)}</p></section>')
    body = (f'  <div class="wrap-narrow inner fade-in">\n'
            f'    <div class="page-header"><h1>{a["h"]}</h1><p>{a["sub"]}</p></div>\n'
            f'{paras}{cv}\n'
            f'    <h2 class="sub-title">{a["exp_h"]}</h2>\n'
            f'    <div class="edu-list">\n{exp}    </div>\n'
            f'    <h2 class="sub-title">{a["skills_h"]}</h2>\n'
            f'    <div class="skills-grid">\n{skills}\n    </div>\n'
            '  </div>')
    ld = [{'@context': 'https://schema.org', '@type': 'ProfilePage', 'url': f'{SITE}/{PAGES["about"][0 if lang == "tr" else 1]}',
           'inLanguage': lang, 'dateModified': datetime.date.today().isoformat(), 'mainEntity': person_ld(lang)}]
    page(lang, 'about', a['title'], a['desc'], body, ld=ld)

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
        cvlab = 'Türkçe · English (PDF)' if lang == 'tr' else 'English · Türkçe (PDF)'
        crel = rel_of(PAGES["contact"][0 if lang == "tr" else 1])
        bion += f'\n      <a href="{crel}{CV[lang]}" target="_blank" rel="noopener" class="contact-row" data-cv-open aria-haspopup="dialog"><span class="contact-icon">{ICON["doc"]}</span><span class="contact-label">CV</span><span class="contact-value">{cvlab}</span></a>'
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
    import re as _re, urllib.parse as _up
    path = post_url(p, lang)
    alt = post_url(p, 'en' if lang == 'tr' else 'tr')
    rel = rel_of(path)
    s = S[lang]
    tr = lang == 'tr'
    body = open(os.path.join(HERE, 'yazilar', f'{p["slug"]}.{lang}.html'), encoding='utf-8').read().rstrip()
    if lang == 'en':  # görseller Türkçe yazının klasöründe duruyor
        body = body.replace('<img src="', f'<img src="{rel}{p["img_dir"]}')
    # okuma süresi
    rt = reading_time(p, lang)
    body = _re.sub(r'(<div class="blog-meta">)(.*?)(</div>)', lambda m: f'{m.group(1)}{m.group(2)} · {rt}{m.group(3)}', body, count=1)
    # başlıklara id + içindekiler
    heads = []
    def add_id(m):
        txt = _re.sub(r'<[^>]+>', '', m.group(1))
        slug = _re.sub(r'[^a-z0-9]+', '-', txt.lower().translate(str.maketrans('çğıöşüâî', 'cgiosuai'))).strip('-')[:60] or f'b{len(heads)}'
        heads.append((slug, txt))
        return f'<h3 id="{slug}">{m.group(1)}</h3>'
    body = _re.sub(r'<h3>(.*?)</h3>', add_id, body)
    if len(heads) >= 3:
        items = ''.join(f'<li><a href="#{a}">{esc(t)}</a></li>' for a, t in heads)
        toc = f'''
  <details class="toc">
    <summary>{'İçindekiler' if tr else 'Contents'}</summary>
    <ol>{items}</ol>
  </details>'''
        body = _re.sub(r'(<div class="blog-meta">.*?</div>)', lambda m: m.group(1) + toc, body, count=1)
    # paylaş + yazar kutusu
    url = f'{SITE}/{path}'
    qt = _up.quote(p[lang]['title']); qu = _up.quote(url)
    share = f'''
  <div class="share">
    <span class="share-label">{'Paylaş' if tr else 'Share'}</span>
    <a class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={qu}" target="_blank" rel="noopener">LinkedIn</a>
    <a class="share-btn" href="https://twitter.com/intent/tweet?url={qu}&amp;text={qt}" target="_blank" rel="noopener">X</a>
    <a class="share-btn" href="https://wa.me/?text={qt}%20{qu}" target="_blank" rel="noopener">WhatsApp</a>
    <button class="share-btn" type="button" data-copy="{url}" data-copied="{'Kopyalandı ✓' if tr else 'Copied ✓'}">{'Linki kopyala' if tr else 'Copy link'}</button>
  </div>'''
    about = rel + PAGES['about'][0 if tr else 1]
    bio = ("Abdullah Gül Üniversitesi'nde elektrik-elektronik mühendisliği öğrencisi; MUSTECH'te gömülü sistemler geliştiricisi ve freelance PCB tasarımcısı."
           if tr else 'Electrical and electronics engineering student at Abdullah Gül University; embedded systems developer at MUSTECH and freelance PCB designer.')
    author = f'''
  <aside class="author">
    <div class="mono sm" aria-hidden="true"><span>AU</span></div>
    <div>
      <div class="author-name">Ahmet Ulu</div>
      <p>{bio}</p>
      <div class="author-links"><a href="{about}">{'Hakkımda' if tr else 'About me'} →</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a></div>
    </div>
  </aside>'''
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
    out += f'''<div class="read-progress" aria-hidden="true"><span></span></div>
<main id="icerik">
<article class="wrap-narrow article">
  <a href="{blog}" class="back-link">{s['all_posts']}</a>
{body}
{share}
{author}

  <nav class="post-nav" aria-label="{s['more_posts']}">
    <div class="post-nav-title">{s['more_posts']}</div>
{others}
  </nav>
</article>
</main>
'''
    out += footer(lang, path)
    write(path, out)

# ---------------------------------------------------------------- hesap araçları
def tool_url(t, lang):
    return f'araclar/{t["slugs"][0]}.html' if lang == 'tr' else f'en/tools/{t["slugs"][1]}.html'

def tool_icon(t):
    return f'<span class="tool-ico" aria-hidden="true"><svg viewBox="0 0 24 24">{araclar.ICONS[t["id"]]}</svg></span>'

def tool_card(t, lang, rel, tags=True):
    c = t[lang]
    cat = next(x for x in araclar.CATS if x[0] == t['cat'])
    data = f' data-filter-item data-tags="{esc(cat[1] if lang == "tr" else cat[2])}"' if tags else ''
    go = 'Aç →' if lang == 'tr' else 'Open →'
    return (f'        <a class="tile tool-card" href="{rel}{tool_url(t, lang)}"{data}>{tool_icon(t)}'
            f'<span class="tool-txt"><span class="tile-title">{esc(c["short"])}</span><span class="tile-sub">{esc(c["card"])}</span></span>'
            f'<span class="tile-link">{go}</span></a>')

def build_tools_hub(lang):
    tr = lang == 'tr'
    path = PAGES['tools'][0 if tr else 1]
    rel = rel_of(path)
    if tr:
        title = 'Elektronik Hesap Araçları — Ahmet Ulu'
        desc = 'Ücretsiz elektronik hesap araçları: Ohm kanunu, LED direnci, gerilim bölücü, direnç renk kodu, SMD kod, LM2596/LM317 regülatör, buck, PCB iz genişliği, AWG, RC ve 555.'
        k, h = 'Ücretsiz · Kayıt yok', 'Elektronik hesap araçları'
        sub = 'Devre tasarlarken en sık ihtiyaç duyduğum hesapları tek yerde topladım. Hesaplar tarayıcında yapılır, hiçbir veri gönderilmez; her sayfanın altında formülü ve kaynağı var.'
        n1, n2, ph = 'araç', 'kategori', 'Araçlarda ara… (ör. LED, LM2596, 555)'
    else:
        title = 'Electronics Calculators — Ahmet Ulu'
        desc = "Free electronics calculators: Ohm's law, LED resistor, voltage divider, resistor color code, SMD codes, LM2596/LM317 regulators, buck, PCB trace width, AWG, RC and 555."
        k, h = 'Free · No sign-up', 'Electronics calculators'
        sub = 'The calculations I need most often when designing circuits, in one place. Everything runs in your browser and nothing is sent anywhere; each page explains its formula and source.'
        n1, n2, ph = 'tools', 'categories', 'Search tools… (e.g. LED, LM2596, 555)'
    secs = []
    for cid, ctr, cen, dtr, den in araclar.CATS:
        cards = '\n'.join(tool_card(t, lang, rel) for t in araclar.TOOLS if t['cat'] == cid)
        secs.append('    <section class="tool-section" data-filter-section>\n'
                    f'      <div class="tool-section-title"><h2>{ctr if tr else cen}</h2><span>{dtr if tr else den}</span></div>\n'
                    f'      <div class="tool-grid">\n{cards}\n      </div>\n    </section>')
    tags = [c[1] if tr else c[2] for c in araclar.CATS]
    body = (f'  <div class="wrap inner fade-in tools-page" data-filter>\n'
            f'    <div class="tools-hero">\n'
            f'      <div class="tool-head"><span class="tool-kicker">{k}</span><h1>{h}</h1><p>{sub}</p></div>\n'
            f'      <div class="tools-count"><div><b>{len(araclar.TOOLS)}</b><span>{n1}</span></div><div><b>{len(araclar.CATS)}</b><span>{n2}</span></div></div>\n'
            f'    </div>\n'
            f'{filter_bar(lang, ph, tags)}\n'
            + '\n'.join(secs) +
            f'\n    <p class="filter-empty" data-filter-empty hidden>{S[lang]["no_result"]}</p>\n'
            f'  </div>')
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': h, 'description': desc, 'url': f'{SITE}/{path}', 'inLanguage': lang,
           'hasPart': [{'@type': 'WebApplication', 'name': t[lang]['title'], 'url': f'{SITE}/{tool_url(t, lang)}'} for t in araclar.TOOLS]}]
    page(lang, 'tools', title, desc, body, ld=ld)

def build_tool(t, lang):
    tr = lang == 'tr'
    path = tool_url(t, lang)
    alt = tool_url(t, 'en' if tr else 'tr')
    rel = rel_of(path)
    c = t[lang]
    cat = next(x for x in araclar.CATS if x[0] == t['cat'])
    hub = rel + PAGES['tools'][0 if tr else 1]
    home = rel + PAGES['home'][0 if tr else 1]
    doc = c['doc']() if callable(c['doc']) else c['doc']
    srcs = '\n'.join(f'        <li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in (araclar.SRC[k] for k in t['src']))
    rel_cards = '\n'.join(tool_card(araclar.TOOL[r], lang, rel, tags=False) for r in t['related'])
    post = ''
    if t.get('post'):
        p = POST[t['post']]
        lab = 'Bu hesabı kullandığım proje' if tr else 'A project where I used this'
        post = f'\n      <p class="tool-post">{lab}: <a href="{rel}{post_url(p, lang)}">{esc(p[lang]["title"])}</a></p>'
    noscript = 'Bu hesaplayıcı JavaScript ile çalışır. Formüller aşağıda.' if tr else 'This calculator needs JavaScript. The formulas are below.'
    L = (lambda a, b: a if tr else b)
    body = (f'  <div class="wrap inner fade-in tools-page">\n'
            f'    <nav class="crumbs" aria-label="{L("Konum", "Breadcrumb")}"><a href="{home}">{L("Ana sayfa", "Home")}</a><span aria-hidden="true">/</span>'
            f'<a href="{hub}">{L("Araçlar", "Tools")}</a><span aria-hidden="true">/</span><span>{esc(c["short"])}</span></nav>\n'
            f'    <div class="tool-head"><span class="tool-kicker">{cat[1] if tr else cat[2]}</span><h1>{esc(c["title"])}</h1><p>{esc(c["lead"])}</p></div>\n'
            f'    <div class="calc" data-tool="{t["id"]}"><noscript><p class="calc-note warn">{noscript}</p></noscript></div>\n'
            f'    <section class="tool-doc" id="{L("nasil-hesaplanir", "how-it-works")}">\n'
            f'      <h2>{L("Nasıl hesaplanır?", "How is it calculated?")}</h2>\n'
            f'{doc}{post}\n'
            f'      <h3>{L("Kaynaklar", "Sources")}</h3>\n'
            f'      <ul class="sources">\n{srcs}\n      </ul>\n'
            f'    </section>\n'
            f'    <section class="tool-related">\n'
            f'      <div class="tool-section-title"><h2>{L("Diğer araçlar", "More tools")}</h2><a class="inline-link" href="{hub}">{S[lang]["see_all"]}</a></div>\n'
            f'      <div class="tool-grid">\n{rel_cards}\n      </div>\n'
            f'    </section>\n'
            f'  </div>')
    ld = [{'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebApplication', 'name': c['title'], 'description': c['desc'], 'url': f'{SITE}/{path}', 'inLanguage': lang,
         'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'Any', 'isAccessibleForFree': True,
         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'TRY'},
         'author': {'@type': 'Person', 'name': 'Ahmet Ulu', 'url': f'{SITE}/'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ahmet Ulu', 'item': f'{SITE}/' + ('' if tr else 'en/')},
            {'@type': 'ListItem', 'position': 2, 'name': L('Araçlar', 'Tools'), 'item': f'{SITE}/{PAGES["tools"][0 if tr else 1]}'},
            {'@type': 'ListItem', 'position': 3, 'name': c['short'], 'item': f'{SITE}/{path}'}]}]}]
    out = head(lang, path, f'{c["title"]} — Ahmet Ulu', c['desc'], alt, ld=ld)
    out += nav(lang, path, 'tools', alt)
    out += f'<main id="icerik">\n{body}\n</main>\n' + footer(lang, path)
    out = out.replace('</body>', f'<script src="{rel}assets/js/tools.js?v={asset_ver("assets/js/tools.js")}" defer></script>\n</body>')
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
    for t in araclar.TOOLS:
        urls += [(tool_url(t, 'tr'), today), (tool_url(t, 'en'), today)]
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
        build_tools_hub(lang)
        build_pcb_service(lang)
        for t in araclar.TOOLS:
            build_tool(t, lang)
    build_404(); build_sitemap()
    print('Tamam.')
