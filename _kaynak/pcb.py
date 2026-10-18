# -*- coding: utf-8 -*-
"""PCB tasarım hizmeti: 'PCB nedir?' anlatımı (ana sayfa bölümü + ayrı hizmet sayfası).
Metinleri burada değiştir; sayfayı build.py (build_pcb_service, pcb_explain) üretir."""


def illustration(lang):
    """Breadboard + kablo yumağı → düzenli PCB çizimi (satır içi SVG)."""
    tr = lang == 'tr'
    l1 = 'Prototip: breadboard ve kablolar' if tr else 'Prototype: breadboard and wires'
    l2 = 'PCB: tek, sağlam ve düzenli kart' if tr else 'PCB: one solid, tidy board'
    pins = ''.join(f'M{426 + i * 8} 92v-6M{426 + i * 8} 162v6' for i in range(8))
    pins += ''.join(f'M420 {98 + i * 8}h-6M490 {98 + i * 8}h6' for i in range(8))
    hdr = ''.join(f'<rect x="603" y="{126 + i * 15}" width="6" height="6" fill="#d9b45a"/>' for i in range(4))
    return f'''<svg class="pcb-illu" viewBox="0 0 640 270" role="img" aria-label="{l1} → {l2}">
  <defs><pattern id="bbh" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="1.6" fill="#b9b6a8"/></pattern>
  <radialGradient id="ledg"><stop offset="0" stop-color="#fca5a5"/><stop offset="1" stop-color="#ef4444" stop-opacity="0"/></radialGradient></defs>
  <rect x="14" y="30" width="272" height="190" rx="12" fill="#ecebe4" stroke="#cfcdc2"/>
  <rect x="24" y="42" width="252" height="166" fill="url(#bbh)"/>
  <rect x="14" y="120" width="272" height="9" fill="#dcdad0"/>
  <rect x="30" y="150" width="92" height="60" rx="5" fill="#1f6fb2"/><rect x="62" y="166" width="28" height="22" rx="2" fill="#0f2f4d"/>
  <rect x="150" y="104" width="46" height="36" rx="3" fill="#222"/>
  <rect x="216" y="56" width="50" height="40" rx="4" fill="#6b46c1"/><circle cx="241" cy="76" r="9" fill="#d6ccf5"/>
  <circle cx="92" cy="70" r="7" fill="#ef4444"/><rect x="112" y="66" width="22" height="8" rx="3" fill="#d6b98c"/>
  <g fill="none" stroke-width="3.4" stroke-linecap="round">
    <path d="M60 150C60 90 170 60 160 104" stroke="#ef4444"/>
    <path d="M80 150C100 40 240 20 236 56" stroke="#eab308"/>
    <path d="M100 150C140 215 232 200 252 96" stroke="#22c55e"/>
    <path d="M45 150C18 80 120 38 186 104" stroke="#3b82f6"/>
    <path d="M110 150C164 122 126 66 96 74" stroke="#f97316"/>
    <path d="M70 208C200 246 262 160 262 96" stroke="#9ca3af"/>
    <path d="M118 158C170 170 210 150 190 140" stroke="#ec4899"/>
  </g>
  <g class="pcb-arrow"><circle cx="319" cy="125" r="20"/><path d="M308 125h20m-7-7 7 7-7 7" fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>
  <rect x="352" y="30" width="276" height="190" rx="14" fill="#0e5a3a" stroke="#0a4029" stroke-width="2"/>
  <g fill="#0a4029" stroke="#c9a227" stroke-width="2"><circle cx="368" cy="46" r="6"/><circle cx="612" cy="46" r="6"/><circle cx="368" cy="204" r="6"/><circle cx="612" cy="204" r="6"/></g>
  <g fill="none" stroke="#d9b45a" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round">
    <path d="M384 74H402L412 84V102H414"/><path d="M384 96H398L408 106V118H414"/>
    <path d="M384 154H402L410 146V142H414"/><path d="M384 176H404L414 166V150H414"/>
    <path d="M496 102H522L534 90V66H556"/><path d="M496 126H548L560 138V146"/>
    <path d="M496 150H514L526 162V186H578"/><path d="M496 118H580L592 130H600"/>
  </g>
  <g fill="#d9b45a"><circle cx="556" cy="66" r="4"/><circle cx="560" cy="146" r="4"/><circle cx="578" cy="186" r="4"/></g>
  <rect x="356" y="60" width="28" height="50" rx="3" fill="#1f8f4e"/><circle cx="370" cy="74" r="5" fill="#a7f3c4"/><circle cx="370" cy="96" r="5" fill="#a7f3c4"/>
  <rect x="356" y="140" width="28" height="50" rx="3" fill="#1f8f4e"/><circle cx="370" cy="154" r="5" fill="#a7f3c4"/><circle cx="370" cy="176" r="5" fill="#a7f3c4"/>
  <path d="{pins}" stroke="#d9b45a" stroke-width="3"/>
  <rect x="420" y="92" width="70" height="70" rx="4" fill="#1a1a1a"/><circle cx="430" cy="102" r="2.5" fill="#555"/>
  <circle cx="566" cy="66" r="18" fill="url(#ledg)"/><circle cx="566" cy="66" r="7" fill="#ef4444"/>
  <circle cx="572" cy="160" r="11" fill="#2563eb" stroke="#93c5fd" stroke-width="1.5"/>
  <rect x="598" y="120" width="16" height="64" rx="2" fill="#111"/>{hdr}
  <text x="440" y="206" class="silk">AU-01  REV A</text>
  <text x="150" y="252" text-anchor="middle" class="lbl">{l1}</text>
  <text x="490" y="252" text-anchor="middle" class="lbl">{l2}</text>
</svg>'''


T = {
 'tr': dict(
  # ana sayfa bölümü
  home_k='PCB nedir?', home_h='Kablo yumağından tek bir karta',
  home_p='PCB (baskı devre kartı), elektronik cihazların içindeki o yeşil karttır. Parçaları kablolar yerine kartın üzerindeki ince bakır yollar birbirine bağlar. Böylece devreniz küçülür, sağlamlaşır ve aynısından istediğiniz kadar üretilebilir.',
  home_chips=['Arduino / ESP32 prototipini ürüne dönüştürmek', 'Okul ve bitirme projeleri', 'Röle, sensör ve motor kartları', 'Aynı karttan 10, 100 adet'],
  home_b1='PCB tasarımı hakkında →', home_b2='Bionluk\'tan teklif al',
  # hizmet sayfası
  title='PCB Tasarımı Yaptırma: Baskı Devre (PCB) Nedir? — Ahmet Ulu',
  desc='PCB (baskı devre) nedir, ne zaman gerekir? Arduino/ESP32 prototipinizi, okul projenizi ya da ürün fikrinizi KiCad ile üretime hazır bir PCB\'ye dönüştürüyorum. Örnek tasarımlar, süreç ve sık sorulanlar.',
  k='Freelance · KiCad', h='Fikrinizi üretilebilir bir karta dönüştürüyorum',
  lead='Elinizde kablolarla çalışan bir prototip, bir okul projesi ya da sadece bir fikir olabilir. Teknik bilgi gerekmiyor: ne yapmasını istediğinizi anlatın, şematiğini ve baskı devre kartını (PCB) ben tasarlayayım, üretime hazır dosyaları size teslim edeyim.',
  b1='Bionluk\'tan teklif al →', b2='Bana yaz',
  what_h='PCB (baskı devre) nedir?',
  what_p=['PCB, İngilizce <strong>Printed Circuit Board</strong> yani <strong>baskı devre kartı</strong> demek. Telefonunuzun, kombinizin, çamaşır makinenizin içinde gördüğünüz, üzerinde küçük parçalar dizili yeşil kart budur.',
          'Bir devreyi ilk denerken parçalar genelde breadboard denen delikli bir tahtaya takılır ve kablolarla birbirine bağlanır. Bu, denemek için harikadır ama kablolar kolayca çıkar, devre büyük ve dağınık olur. PCB\'de ise bağlantılar kartın üzerine basılmış bakır yollardır: kablo yoktur, parçalar karta lehimlenir ve kart bir kutuya rahatça sığar.'],
  when_h='Ne zaman PCB\'ye ihtiyacınız olur?',
  when=[('plug', 'Prototipiniz çalışıyor ama kablo yumağı', 'Breadboard\'da ya da kablolarla çalışan devrenizi, kutuya sığan ve titreşimde bozulmayan tek bir karta taşıyalım.'),
        ('layers', 'Aynı cihazdan birden çok yapacaksınız', '5, 50 ya da 500 adet üretecekseniz her birini elle kablolamak yerine fabrikada basılan, birbirinin aynısı kartlar kullanırsınız.'),
        ('cap', 'Okul ya da bitirme projesi', 'Jüriye sunacağınız projede düzenli ve profesyonel görünen bir kart büyük fark yaratır, arıza riskini de azaltır.'),
        ('bulb', 'Bir ürün fikriniz var', 'Satmayı düşündüğünüz bir cihaz için küçük, ucuz ve üretime uygun bir kart tasarlayalım.')],
  types_h='Örnek kart türleri',
  types=['Arduino / ESP32 / STM32 tabanlı kontrol kartları', 'Röle, MOSFET ve motor sürücü çıkışları', 'Sensör ve buton giriş kartları', 'Güç girişi ve regülatör devreleri', 'LED, gösterge ve trafik ışığı kartları', 'Mevcut modülleri tek karta toplayan kartlar'],
  steps_h='Süreç nasıl işliyor?',
  steps=[(None, 'Anlatın', 'Kart ne yapacak, neyle beslenecek, hangi sensör ve çıkışlar olacak? Varsa prototipinizin fotoğrafı ya da elle çizdiğiniz bir taslak yeterli.'),
         ('sema.jpg', 'Şematik', 'Devrenin çizimini hazırlıyorum: hangi parçanın nereye bağlandığını gösteren elektrik şeması.'),
         ('pcb.jpg', 'PCB yerleşimi', 'Parçaları karta yerleştirip bakır yolları çiziyorum. Güç hatları kalın, klemensler kenarda, kart kutuya uygun.'),
         ('3d.jpg', '3D önizleme ve teslim', 'Kartın 3D görüntüsünü birlikte kontrol ediyoruz, istediğiniz değişiklikleri yapıyorum ve üretime hazır dosyaları teslim ediyorum.')],
  work_h='Tasarladığım kartlardan örnekler',
  work=[('3d.jpg', 'Trafik sinyalizasyon kartı', 'NodeMCU tabanlı, trafik ışıklarını süren ve buton/sensör girişlerini okuyan kontrol kartı.'),
        ('peltier-3d.jpg', 'ESP32 Peltier kontrol kartı', 'Altı Peltier modülünü PWM ile süren; fanları, pompaları ve sensörleri de yöneten ESP32 tabanlı kart.')],
  work_more='Tasarımların ayrıntıları →',
  need_h='Sizden ne gerekiyor?',
  need=['Kartın ne yapmasını istediğiniz (birkaç cümle yeter)', 'Neyle beslenecek: pil, adaptör, 12 V, USB…', 'Bağlanacak sensörler, modüller, röleler, ekran vb.', 'Varsa boyut ya da kutu kısıtı', 'Varsa prototipinizin fotoğrafı, şeması ya da kodu'],
  faq_h='Sık sorulanlar',
  faq=[('PCB ile baskı devre aynı şey mi?', 'Evet. PCB, "Printed Circuit Board" kelimelerinin kısaltması; Türkçede baskı devre, baskılı devre kartı ya da kısaca devre kartı denir.'),
       ('Teknik bilgim yok, yine de yaptırabilir miyim?', 'Evet. Ne yapmasını istediğinizi kendi cümlelerinizle anlatmanız yeterli; teknik kısımları birlikte netleştiririz.'),
       ('Kartı siz mi üretiyorsunuz?', 'Ben tasarımı ve üretim dosyalarını hazırlıyorum. Kartın kendisi PCB üretim firmalarında basılıyor; dosyaları nasıl sipariş edeceğinizi de anlatırım.'),
       ('Ne kadar sürer, ücreti ne kadar?', 'Kartın büyüklüğüne ve karmaşıklığına göre değişiyor. Projenizi anlatın, size süre ve fiyat söyleyeyim.'),
       ('Hangi programı kullanıyorsunuz?', 'KiCad. Ücretsiz ve açık kaynaklı olduğu için dosyalarınızı ileride siz ya da başka biri de açıp düzenleyebilir.')],
  cta_h='Projenizi anlatın', cta_p='Kısa bir açıklama yeterli; size nasıl bir kart gerektiğini ve yaklaşık ücretini söyleyeyim.',
 ),
 'en': dict(
  home_k='What is a PCB?', home_h='From a tangle of wires to one board',
  home_p='A PCB (printed circuit board) is the green board inside electronic devices. Instead of wires, thin copper tracks on the board connect the parts. Your circuit gets smaller and sturdier, and you can make as many copies as you need.',
  home_chips=['Turning an Arduino / ESP32 prototype into a product', 'School and capstone projects', 'Relay, sensor and motor boards', '10 or 100 copies of the same board'],
  home_b1='About PCB design →', home_b2='Get a quote on Bionluk',
  title='PCB Design Service: What Is a PCB? — Ahmet Ulu',
  desc='What is a PCB and when do you need one? I turn your Arduino/ESP32 prototype, school project or product idea into a production-ready PCB in KiCad. Example designs, process and FAQ.',
  k='Freelance · KiCad', h='I turn your idea into a board you can manufacture',
  lead='You might have a prototype held together with wires, a school project or just an idea. No technical knowledge needed: tell me what it should do, and I will design the schematic and the printed circuit board (PCB) and hand you production-ready files.',
  b1='Get a quote on Bionluk →', b2='Contact me',
  what_h='What is a PCB?',
  what_p=['PCB stands for <strong>printed circuit board</strong>. It is the green board covered with small parts that you see inside your phone, boiler or washing machine.',
          'When you first try a circuit, the parts usually go on a breadboard and are connected with jumper wires. That is great for experimenting, but wires come loose and the circuit is big and messy. On a PCB the connections are copper tracks printed on the board: no wires, the parts are soldered on, and the board fits neatly in an enclosure.'],
  when_h='When do you need a PCB?',
  when=[('plug', 'Your prototype works, but it is a tangle of wires', 'Let us move the circuit from the breadboard to a single board that fits in a box and does not fall apart when it shakes.'),
        ('layers', 'You need more than one', 'If you are building 5, 50 or 500 of them, factory-made identical boards beat wiring each one by hand.'),
        ('cap', 'School or capstone project', 'A tidy, professional-looking board makes a big difference in front of a jury and lowers the risk of failure.'),
        ('bulb', 'You have a product idea', 'Let us design a small, low-cost board that is ready for production for the device you want to sell.')],
  types_h='Example board types',
  types=['Arduino / ESP32 / STM32 based control boards', 'Relay, MOSFET and motor driver outputs', 'Sensor and button input boards', 'Power input and regulator circuits', 'LED, display and traffic light boards', 'Boards that combine existing modules into one'],
  steps_h='How does it work?',
  steps=[(None, 'Tell me', 'What will the board do, how is it powered, which sensors and outputs does it need? A photo of your prototype or a hand-drawn sketch is enough.'),
         ('sema.jpg', 'Schematic', 'I draw the circuit: the electrical diagram that shows what connects where.'),
         ('pcb.jpg', 'PCB layout', 'I place the parts and route the copper tracks: thick power lines, terminals on the edge, a board that fits your enclosure.'),
         ('3d.jpg', '3D preview and delivery', 'We check the 3D view together, I make the changes you want and deliver production-ready files.')],
  work_h='Boards I have designed',
  work=[('3d.jpg', 'Traffic signal board', 'A NodeMCU-based control board that drives traffic lights and reads button/sensor inputs.'),
        ('peltier-3d.jpg', 'ESP32 Peltier control board', 'An ESP32-based board that drives six Peltier modules with PWM and also manages fans, pumps and sensors.')],
  work_more='Design details →',
  need_h='What I need from you',
  need=['What the board should do (a few sentences is enough)', 'How it is powered: battery, adapter, 12 V, USB…', 'Sensors, modules, relays, displays and so on to connect', 'Any size or enclosure limits', 'A photo, schematic or code of your prototype, if you have one'],
  faq_h='FAQ',
  faq=[('Is a PCB the same as a circuit board?', 'Yes. PCB stands for "printed circuit board"; people also just call it a circuit board.'),
       ('I have no technical background. Can I still order one?', 'Yes. Describe what it should do in your own words; we will work out the technical details together.'),
       ('Do you manufacture the board?', 'I prepare the design and the production files. The board itself is made by a PCB manufacturer, and I will explain how to order it.'),
       ('How long does it take and how much does it cost?', 'It depends on the size and complexity of the board. Tell me about your project and I will give you a time frame and a price.'),
       ('Which software do you use?', 'KiCad. It is free and open source, so you or anyone else can open and edit your files later.')],
  cta_h='Tell me about your project', cta_p='A short description is enough; I will tell you what kind of board you need and roughly what it costs.',
 ),
}

ICONS = {
 'plug': '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/>',
 'layers': '<path d="M12 3 3 8l9 5 9-5zM3 13l9 5 9-5M3 17l9 5 9-5"/>',
 'cap': '<path d="M2 9l10-5 10 5-10 5zM6 11v5c3 2 9 2 12 0v-5M22 9v6"/>',
 'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
 'chat': '<path d="M4 5h16v11H8l-4 4z"/>',
}
