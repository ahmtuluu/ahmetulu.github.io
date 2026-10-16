# -*- coding: utf-8 -*-
"""Hesap araçlarının içerik verisi (TR/EN).
Hesap kodu: assets/js/tools.js  ·  Sayfaları üreten: build.py (build_tools_hub, build_tool)
Yeni araç eklemek için: tools.js içine TOOLS.<id> tanımı + aşağıya bir kayıt.
"""

CATS = [
    ('basic', 'Temel hesaplar', 'Basics', 'Her projede lazım olanlar', 'What every project needs'),
    ('parts', 'Bileşenler', 'Components', 'Direnç, LED ve SMD kodları', 'Resistors, LEDs and SMD codes'),
    ('power', 'Güç', 'Power', 'Regülatör, buck ve pil', 'Regulators, buck converters and batteries'),
    ('pcb', 'PCB ve kablo', 'PCB & wiring', 'İz genişliği ve kablo kesiti', 'Trace width and wire gauge'),
    ('timing', 'Zamanlama ve filtre', 'Timing & filters', 'RC devreleri ve 555', 'RC circuits and the 555'),
]

ICONS = {
    'ohm': '<path d="M5 19h4v-2.6A6.6 6.6 0 1 1 15 16.4V19h4"/>',
    'series': '<path d="M3 8h4m10 0h4M7 6h10v4H7zM3 16h4m10 0h4M7 14h10v4H7zM3 8v8M21 8v8"/>',
    'divider': '<path d="M12 2v3M10 5h4v5h-4zM12 10v4M10 14h4v5h-4zM12 19v3M12 12h8"/><circle cx="12" cy="12" r="1.2"/>',
    'db': '<path d="M3 18l5-6 4 3 8-9M15 6h5v5"/>',
    'led': '<path d="M3 12h5M16 12h5M8 7v10l8-5zM16 7v10M14 5l2.5-2.5M17 7l2.5-2.5"/>',
    'color': '<path d="M2 12h3M19 12h3M5 8h14v8H5zM9 8v8M12 8v8M15 8v8"/>',
    'smd': '<path d="M4 8h16v8H4zM4 8h3v8H4zM17 8h3v8h-3zM10 12h4"/>',
    'regulator': '<path d="M4 6h10v10H4zM14 9h6M14 13h6M9 16v5M7 11h4"/>',
    'buck': '<path d="M2 15h3a2.4 2.4 0 0 1 4.8 0 2.4 2.4 0 0 1 4.8 0 2.4 2.4 0 0 1 4.8 0H22M4 7h6M7 4v6M15 7h5"/>',
    'battery': '<path d="M3 8h15v8H3zM18 10.5h3v3h-3M6.5 11v2M9.5 11v2M12.5 11v2"/>',
    'trace': '<path d="M3 6h6l4 4h8M3 18h8l3-3h7M3 12h18"/><circle cx="21" cy="10" r="1.2"/><circle cx="21" cy="15" r="1.2"/>',
    'awg': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/>',
    'rc': '<path d="M3 4v16h18M3 19c5 0 6-13 18-13"/>',
    't555': '<path d="M2 16h4V8h5v8h4V8h5v8h2"/>',
}

def F(*lines, note=None):
    """Formül kutusu."""
    body = ''.join(f'<span>{l}</span>' for l in lines)
    if note:
        body += f'<small>{note}</small>'
    return f'<div class="formula">{body}</div>'

SRC = {
    'lm2596': ('Texas Instruments — LM2596 datasheet', 'https://www.ti.com/lit/ds/symlink/lm2596.pdf'),
    'lm317': ('Texas Instruments — LM317 datasheet', 'https://www.ti.com/lit/ds/symlink/lm317.pdf'),
    'ne555': ('Texas Instruments — NE555 datasheet', 'https://www.ti.com/lit/ds/symlink/ne555.pdf'),
    'slva477': ('Texas Instruments — SLVA477B: Basic Calculation of a Buck Converter\'s Power Stage', 'https://www.ti.com/lit/an/slva477b/slva477b.pdf'),
    'mp1584': ('Monolithic Power Systems — MP1584 datasheet', 'https://www.monolithicpower.com/pub/media/document/MP1584_r1.1.pdf'),
    'xl4015': ('XLSEMI — XL4015 datasheet', 'https://www.radiolocman.com/datasheet/data.html?di=685191'),
    'ams1117': ('Advanced Monolithic Systems — AMS1117 datasheet', 'http://www.advanced-monolithic.com/pdf/ds1117.pdf'),
    'ipc2221': ('IPC-2221 — Generic Standard on Printed Board Design', 'https://shop.ipc.org/ipc-2221/ipc-2221-standard-only'),
    'iec60062': ('IEC 60062 — Marking codes for resistors and capacitors', 'https://webstore.iec.ch/en/publication/65655'),
    'astm258': ('ASTM B258 — AWG sizes of solid round wires', 'https://store.astm.org/standards/b258'),
    'esp32': ('Espressif — ESP32 datasheet (güç tüketimi tabloları)', 'https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf'),
    'w_ohm': ('Wikipedia — Ohm\'s law', 'https://en.wikipedia.org/wiki/Ohm%27s_law'),
    'w_sp': ('Wikipedia — Series and parallel circuits', 'https://en.wikipedia.org/wiki/Series_and_parallel_circuits'),
    'w_div': ('Wikipedia — Voltage divider', 'https://en.wikipedia.org/wiki/Voltage_divider'),
    'w_db': ('Wikipedia — Decibel', 'https://en.wikipedia.org/wiki/Decibel'),
    'w_dbm': ('Wikipedia — dBm', 'https://en.wikipedia.org/wiki/DBm'),
    'w_eser': ('Wikipedia — E series of preferred numbers (IEC 60063)', 'https://en.wikipedia.org/wiki/E_series_of_preferred_numbers'),
    'w_led': ('Wikipedia — Light-emitting diode', 'https://en.wikipedia.org/wiki/Light-emitting_diode'),
    'w_color': ('Wikipedia — Electronic color code', 'https://en.wikipedia.org/wiki/Electronic_color_code'),
    'w_awg': ('Wikipedia — American wire gauge', 'https://en.wikipedia.org/wiki/American_wire_gauge'),
    'w_rc': ('Wikipedia — RC circuit', 'https://en.wikipedia.org/wiki/RC_circuit'),
}

# Renk kodu tablosu (IEC 60062:2016)
COLOR_TABLE = [
    ('#1a1a1a', 'Siyah', 'Black', '0', '×1', '—', '250'),
    ('#7c4a1e', 'Kahverengi', 'Brown', '1', '×10', '±1 %', '100'),
    ('#dc2626', 'Kırmızı', 'Red', '2', '×100', '±2 %', '50'),
    ('#f97316', 'Turuncu', 'Orange', '3', '×1 k', '±0,05 %', '15'),
    ('#facc15', 'Sarı', 'Yellow', '4', '×10 k', '±0,02 %', '25'),
    ('#16a34a', 'Yeşil', 'Green', '5', '×100 k', '±0,5 %', '20'),
    ('#2563eb', 'Mavi', 'Blue', '6', '×1 M', '±0,25 %', '10'),
    ('#7c3aed', 'Mor', 'Violet', '7', '×10 M', '±0,1 %', '5'),
    ('#9ca3af', 'Gri', 'Grey', '8', '×100 M', '±0,01 %', '1'),
    ('#f8fafc', 'Beyaz', 'White', '9', '×1 G', '—', '—'),
    ('#c9a227', 'Altın', 'Gold', '—', '×0,1', '±5 %', '—'),
    ('#c0c4cc', 'Gümüş', 'Silver', '—', '×0,01', '±10 %', '—'),
]

def color_table(lang):
    tr = lang == 'tr'
    h = ('Renk', 'Hane', 'Çarpan', 'Tolerans', 'ppm/K') if tr else ('Colour', 'Digit', 'Multiplier', 'Tolerance', 'ppm/K')
    rows = ''
    for c, ntr, nen, d, m, t, tc in COLOR_TABLE:
        if t.endswith(' %'):
            t = '±%' + t[1:-2] if tr else t[:-2] + '%'
        if not tr:
            m, t = m.replace(',', '.'), t.replace(',', '.')
        rows += (f'<tr><td><span class="cdot" style="background:{c}"></span>{ntr if tr else nen}</td>'
                 f'<td>{d}</td><td>{m}</td><td>{t}</td><td>{tc}</td></tr>')
    head = ''.join(f'<th>{x}</th>' for x in h)
    return f'<div class="table-wrap"><table class="calc-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


TOOLS = [
# ------------------------------------------------------------------ TEMEL
dict(id='ohm', cat='basic', slugs=('ohm-kanunu', 'ohms-law'), src=['w_ohm'], related=['series', 'divider', 'led'],
 tr=dict(title='Ohm Kanunu Hesaplama', short='Ohm kanunu', card='Gerilim, akım, direnç ve güçten ikisini gir; diğer ikisini bul.',
   lead='V, I, R ve P\'den bildiğin iki tanesini gir; diğer ikisi anında hesaplansın. Birimleri (mA, kΩ, mW…) yanındaki kutudan seçebilirsin.',
   desc='Ohm kanunu hesaplayıcı: gerilim, akım, direnç ve güçten ikisini gir, diğerlerini anında bul. V = I·R ve P = V·I formülleri, birim seçimi ve açıklamalı.',
   doc=f'''<p>Ohm kanunu bir direnç üzerindeki <strong>gerilim (V)</strong>, <strong>akım (I)</strong> ve <strong>direnç (R)</strong> arasındaki ilişkidir. Güç formülüyle birleşince dört büyüklükten herhangi ikisini bilmek diğer ikisini bulmaya yeter.</p>
{F('V = I · R', 'P = V · I = I² · R = V² / R')}
<p>Araç, seçtiğin iki değere göre bu denklemleri çözer. Örneğin P ve R biliniyorsa önce <strong>V = √(P·R)</strong>, sonra <strong>I = √(P/R)</strong> bulunur.</p>
<h3>Pratikte dikkat</h3>
<ul><li>Direnç seçerken güç değeri, hesaplanan gücün <strong>en az iki katı</strong> olsun (0,2 W harcıyorsa 1/2 W direnç).</li>
<li>Ohm kanunu doğrusal (omik) elemanlar içindir. LED ve diyot gibi elemanlarda doğrudan kullanılmaz; onlar için LED direnci aracını kullan.</li></ul>'''),
 en=dict(title='Ohm\'s Law Calculator', short='Ohm\'s law', card='Enter two of voltage, current, resistance and power; get the other two.',
   lead='Enter any two of V, I, R and P and the other two are calculated instantly. Pick units (mA, kΩ, mW…) from the box next to each field.',
   desc='Ohm\'s law calculator: enter two of voltage, current, resistance and power and get the rest instantly. V = I·R and P = V·I explained, with unit selection.',
   doc=f'''<p>Ohm\'s law links the <strong>voltage (V)</strong>, <strong>current (I)</strong> and <strong>resistance (R)</strong> of a resistor. Combined with the power formula, knowing any two of the four quantities is enough to find the others.</p>
{F('V = I · R', 'P = V · I = I² · R = V² / R')}
<p>The tool solves these equations for the pair you pick. For example, with P and R known it first finds <strong>V = √(P·R)</strong>, then <strong>I = √(P/R)</strong>.</p>
<h3>In practice</h3>
<ul><li>Pick a resistor rated for <strong>at least twice</strong> the calculated power (0.2 W dissipated → 1/2 W resistor).</li>
<li>Ohm\'s law applies to linear (ohmic) parts. It does not apply directly to LEDs or diodes; use the LED resistor tool for those.</li></ul>''')),

dict(id='series', cat='basic', slugs=('seri-paralel', 'series-parallel'), src=['w_sp'], related=['ohm', 'divider', 'rc'],
 tr=dict(title='Seri ve Paralel Direnç / Kondansatör / Bobin Hesaplama', short='Seri / paralel', card='Direnç, kondansatör veya bobinlerin seri ve paralel eşdeğerini bul.',
   lead='Elindeki değerleri gir; seri ve paralel bağlandığında toplamın ne olacağını birlikte gör. Elinde olmayan bir değeri iki parçayla elde etmek için ideal.',
   desc='Seri ve paralel direnç, kondansatör ve bobin hesaplayıcı. 10 değere kadar ekle, eşdeğer değeri anında gör. Formüller ve açıklamalar.',
   doc=f'''<p>Dirençler ve bobinler aynı kuralla toplanır; kondansatörlerde kural <strong>tersine döner</strong>.</p>
{F('Direnç / bobin, seri:   R = R1 + R2 + …', 'Direnç / bobin, paralel:   1/R = 1/R1 + 1/R2 + …', 'Kondansatör, paralel:   C = C1 + C2 + …', 'Kondansatör, seri:   1/C = 1/C1 + 1/C2 + …', note='Bobin hesabında bobinler arasındaki manyetik kuplaj ihmal edilir.')}
<p>İki eşit direnç paralel bağlanınca değer yarıya iner (2 × 10 kΩ → 5 kΩ). Paralel bağlantının sonucu her zaman <strong>en küçük değerden de küçüktür</strong>; bu, sonucu kontrol etmenin hızlı bir yoludur.</p>'''),
 en=dict(title='Series and Parallel Resistor / Capacitor / Inductor Calculator', short='Series / parallel', card='Find the series and parallel equivalent of resistors, capacitors or inductors.',
   lead='Enter your values and see the total for both series and parallel connection. Handy for building a value you do not have from two parts.',
   desc='Series and parallel resistor, capacitor and inductor calculator. Add up to 10 values and see the equivalent instantly. Formulas explained.',
   doc=f'''<p>Resistors and inductors add up the same way; for capacitors the rule is <strong>reversed</strong>.</p>
{F('Resistor / inductor, series:   R = R1 + R2 + …', 'Resistor / inductor, parallel:   1/R = 1/R1 + 1/R2 + …', 'Capacitor, parallel:   C = C1 + C2 + …', 'Capacitor, series:   1/C = 1/C1 + 1/C2 + …', note='Magnetic coupling between inductors is ignored.')}
<p>Two equal resistors in parallel give half the value (2 × 10 kΩ → 5 kΩ). A parallel result is always <strong>smaller than the smallest part</strong>, which is a quick way to sanity-check it.</p>''')),

dict(id='divider', cat='basic', slugs=('gerilim-bolucu', 'voltage-divider'), src=['w_div', 'w_eser'], related=['regulator', 'ohm', 'series'],
 tr=dict(title='Gerilim Bölücü Hesaplama', short='Gerilim bölücü', card='Vout\'u bul ya da istenen gerilim için alt direnci seç; yük etkisiyle birlikte.',
   lead='İki dirençle gerilimi düşür: çıkış gerilimini hesapla ya da hedef gerilim için gereken direnci bul. İstersen yük direncini ekle, gerçek çıkışı gör.',
   desc='Gerilim bölücü hesaplayıcı: Vout = Vin·R2/(R1+R2). Hedef gerilim için R2 bul, E24/E96 standart değer öner, yük direnci etkisini gör.',
   doc=f'''<p>İki direnç seri bağlanıp ortadan çıkış alındığında, giriş gerilimi dirençlerin oranında bölünür.</p>
{F('Vout = Vin · R2 / (R1 + R2)', 'Yük varsa:   R2\' = R2 · RL / (R2 + RL)', 'R2 = R1 · Vout / (Vin − Vout)', 'Bölücü akımı:   I = Vin / (R1 + R2)')}
<p>“Alt direnci bul” modunda R2 hesaplandıktan sonra <strong>E24 (±%5)</strong> ve <strong>E96 (±%1)</strong> serilerindeki en yakın standart değer önerilir ve o değerle elde edilecek gerçek Vout gösterilir.</p>
<h3>Pratikte dikkat</h3>
<ul><li>Gerilim bölücü bir güç kaynağı değildir: çıkışa yük bağlandığında gerilim düşer. Yük direnci alanı bu düşüşü gösterir.</li>
<li>ADC ile pil gerilimi ölçerken toplam direnç 10–100 kΩ arası iyi bir başlangıçtır; MΩ seviyesi gürültü ve ölçüm hatası getirebilir.</li></ul>'''),
 en=dict(title='Voltage Divider Calculator', short='Voltage divider', card='Find Vout or pick the bottom resistor for a target voltage, including load.',
   lead='Drop a voltage with two resistors: calculate the output, or find the resistor needed for a target voltage. Add a load resistance to see the real output.',
   desc='Voltage divider calculator: Vout = Vin·R2/(R1+R2). Find R2 for a target voltage, get E24/E96 standard values and see the effect of a load.',
   doc=f'''<p>When two resistors are in series and the output is taken from the middle, the input voltage is divided in the ratio of the resistors.</p>
{F('Vout = Vin · R2 / (R1 + R2)', 'With a load:   R2\' = R2 · RL / (R2 + RL)', 'R2 = R1 · Vout / (Vin − Vout)', 'Divider current:   I = Vin / (R1 + R2)')}
<p>In “find bottom resistor” mode R2 is calculated, then the nearest standard values in the <strong>E24 (±5%)</strong> and <strong>E96 (±1%)</strong> series are suggested together with the real Vout you would get.</p>
<h3>In practice</h3>
<ul><li>A divider is not a power supply: its output drops under load. The load field shows how much.</li>
<li>For measuring a battery with an ADC, a total of 10–100 kΩ is a good start; MΩ values can add noise and error.</li></ul>''')),

dict(id='db', cat='basic', slugs=('desibel', 'decibel'), src=['w_db', 'w_dbm'], related=['rc', 'divider', 'ohm'],
 tr=dict(title='Desibel (dB) ve dBm Hesaplama', short='Desibel (dB)', card='Gerilim/güç oranını dB\'ye çevir, dB\'yi orana çevir, dBm ↔ W.',
   lead='Kazanç ve zayıflamayı desibel ile ifade et: gerilim ya da güç oranından dB, dB\'den oran ve dBm\'den watt.',
   desc='Desibel hesaplayıcı: gerilim oranı (20·log), güç oranı (10·log), dB → oran ve dBm ↔ watt dönüşümü. Formüller açıklamalı.',
   doc=f'''<p>Desibel, iki büyüklüğün oranını logaritmik olarak ifade eder. Güç gerilimin karesiyle orantılı olduğundan (aynı empedansta) gerilim için katsayı 20, güç için 10\'dur.</p>
{F('Gerilim:   dB = 20 · log₁₀(V2 / V1)', 'Güç:   dB = 10 · log₁₀(P2 / P1)', 'Ters:   V oranı = 10^(dB/20),   P oranı = 10^(dB/10)', 'dBm:   P(W) = 10^(dBm/10) / 1000,   V(50 Ω) = √(P · 50)')}
<p>Akılda tutulacaklar: +6 dB ≈ gerilim ×2, +3 dB ≈ güç ×2, +20 dB = gerilim ×10. 0 dBm = 1 mW, 20 dBm = 100 mW (Wi-Fi modüllerinde sık görülür).</p>'''),
 en=dict(title='Decibel (dB) and dBm Calculator', short='Decibel (dB)', card='Convert voltage/power ratios to dB, dB to ratios, and dBm ↔ W.',
   lead='Express gain and attenuation in decibels: dB from a voltage or power ratio, a ratio from dB, and watts from dBm.',
   desc='Decibel calculator: voltage ratio (20·log), power ratio (10·log), dB to ratio and dBm ↔ watt conversion. Formulas explained.',
   doc=f'''<p>A decibel expresses the ratio of two quantities on a log scale. Because power is proportional to voltage squared (at the same impedance), the factor is 20 for voltage and 10 for power.</p>
{F('Voltage:   dB = 20 · log₁₀(V2 / V1)', 'Power:   dB = 10 · log₁₀(P2 / P1)', 'Inverse:   V ratio = 10^(dB/20),   P ratio = 10^(dB/10)', 'dBm:   P(W) = 10^(dBm/10) / 1000,   V(50 Ω) = √(P · 50)')}
<p>Worth remembering: +6 dB ≈ voltage ×2, +3 dB ≈ power ×2, +20 dB = voltage ×10. 0 dBm = 1 mW and 20 dBm = 100 mW (common for Wi-Fi modules).</p>''')),

# ------------------------------------------------------------------ BİLEŞENLER
dict(id='led', cat='parts', slugs=('led-direnci', 'led-resistor'), src=['w_led', 'w_eser'], related=['ohm', 'color', 'smd'],
 tr=dict(title='LED Direnci Hesaplama', short='LED direnci', card='LED için seri direnci, standart değeri ve direnç gücünü bul.',
   lead='LED rengini seç, besleme gerilimini ve akımı gir: gereken direnç, satın alabileceğin standart değer ve direncin güç değeri hazır.',
   desc='LED direnci hesaplayıcı: R = (Vs − Vf)/I. LED rengine göre ileri gerilim, seri LED sayısı, E24 standart direnç önerisi ve güç hesabı.',
   doc=f'''<p>LED üzerindeki gerilim akımla neredeyse sabit kalır (ileri gerilim, Vf). Bu yüzden akımı sınırlamak için seri bir direnç gerekir; direncin üzerine kalan gerilim düşer.</p>
{F('R = (Vs − n · Vf) / I', 'Gerçek akım:   I = (Vs − n · Vf) / R(E24)', 'Direnç gücü:   P = (Vs − n · Vf) · I', note='n: seri bağlı LED sayısı')}
<p>Hesaplanan direnç genelde standart bir değer değildir. Araç, <strong>E24 serisinde bir üst değeri</strong> önerir; böylece LED akımı hedeflediğin değeri hiçbir zaman aşmaz. Direncin güç değeri için hesaplanan gücün en az iki katı önerilir.</p>
<h3>Renklere göre tipik Vf</h3>
<ul><li>Kırmızı ≈ 2,0 V · turuncu / sarı ≈ 2,1 V · IR ≈ 1,3 V</li><li>Yeşil, mavi, beyaz (InGaN) ≈ 3,0–3,2 V</li></ul>
<p>Bunlar tipik değerlerdir; kesin değer LED\'in datasheet\'inde yazar ve akıma, sıcaklığa göre değişir.</p>'''),
 en=dict(title='LED Resistor Calculator', short='LED resistor', card='Find the series resistor, a standard value and its power rating for an LED.',
   lead='Pick the LED colour, enter the supply voltage and current: you get the required resistor, a standard value you can buy and its power rating.',
   desc='LED resistor calculator: R = (Vs − Vf)/I. Forward voltage by colour, LEDs in series, E24 standard resistor suggestion and power rating.',
   doc=f'''<p>The voltage across an LED stays almost constant with current (the forward voltage, Vf). So a series resistor is needed to limit the current; the rest of the supply voltage drops across it.</p>
{F('R = (Vs − n · Vf) / I', 'Actual current:   I = (Vs − n · Vf) / R(E24)', 'Resistor power:   P = (Vs − n · Vf) · I', note='n: number of LEDs in series')}
<p>The calculated resistor is rarely a standard value. The tool suggests the <strong>next value up in the E24 series</strong>, so the LED current never exceeds your target. A power rating of at least twice the calculated power is recommended.</p>
<h3>Typical Vf by colour</h3>
<ul><li>Red ≈ 2.0 V · orange / yellow ≈ 2.1 V · IR ≈ 1.3 V</li><li>Green, blue, white (InGaN) ≈ 3.0–3.2 V</li></ul>
<p>These are typical values; the exact figure is in the LED datasheet and changes with current and temperature.</p>''')),

dict(id='color', cat='parts', slugs=('direnc-renk-kodu', 'resistor-color-code'), src=['iec60062', 'w_color'], related=['smd', 'led', 'series'],
 tr=dict(title='Direnç Renk Kodu Hesaplama (4, 5, 6 Bant)', short='Direnç renk kodu', card='Renklere tıkla, değeri gör; ya da değeri yaz, renkleri bul.',
   lead='4, 5 ve 6 bantlı dirençlerin renk kodunu çöz: renkleri seç, değeri ve toleransı gör. Ters yönde de çalışır: değeri yaz, hangi renkler olduğunu öğren.',
   desc='Direnç renk kodu hesaplayıcı: 4, 5 ve 6 bant. Renklerden değer ve tolerans, değerden renkler. IEC 60062 renk tablosu ile.',
   doc=lambda: f'''<p>Renk bantları soldan sağa okunur. Tolerans bandı genelde diğerlerinden biraz ayrıktır ve sağ tarafta kalır.</p>
{F('4 bant:   [hane][hane] × [çarpan]   [tolerans]', '5 bant:   [hane][hane][hane] × [çarpan]   [tolerans]', '6 bant:   5 bant + [sıcaklık katsayısı]', note='Örnek: sarı-mor-kırmızı-altın = 47 × 100 = 4,7 kΩ ±%5')}
<p>“Değerden renk bul” alanı, yazdığın değeri 4 bantta 2, 5–6 bantta 3 anlamlı haneye yuvarlar ve çarpanı seçer.</p>
<h3>Renk tablosu (IEC 60062)</h3>
{color_table('tr')}'''),
 en=dict(title='Resistor Color Code Calculator (4, 5, 6 Band)', short='Resistor color code', card='Click the colours to see the value, or type a value to get the colours.',
   lead='Decode 4, 5 and 6-band resistor colour codes: pick the colours and see the value and tolerance. It also works backwards: type a value, get the colours.',
   desc='Resistor color code calculator for 4, 5 and 6 bands. Value and tolerance from colours, colours from a value. With the IEC 60062 colour table.',
   doc=lambda: f'''<p>Bands are read from left to right. The tolerance band is usually set slightly apart, on the right.</p>
{F('4 bands:   [digit][digit] × [multiplier]   [tolerance]', '5 bands:   [digit][digit][digit] × [multiplier]   [tolerance]', '6 bands:   5 bands + [temperature coefficient]', note='Example: yellow-violet-red-gold = 47 × 100 = 4.7 kΩ ±5%')}
<p>The “find colours from value” field rounds your value to 2 significant digits (4 bands) or 3 (5–6 bands) and picks the multiplier.</p>
<h3>Colour table (IEC 60062)</h3>
{color_table('en')}''')),

dict(id='smd', cat='parts', slugs=('smd-kod-cozucu', 'smd-code'), src=['iec60062', 'w_eser'], related=['color', 'led', 'series'],
 tr=dict(title='SMD Direnç ve Kondansatör Kodu Çözücü', short='SMD kod çözücü', card='103, 4702, 4R7, 01C, 104J gibi kodları değere çevir.',
   lead='SMD direnç ve seramik kondansatörlerin üzerindeki kodu yaz; değerini anında gör. 3 haneli, 4 haneli, R\'li ve EIA-96 kodlarını tanır.',
   desc='SMD direnç kodu ve kondansatör kodu çözücü: 3 hane (103), 4 hane (1002), R (4R7), EIA-96 (01C) ve kondansatör kodları (104, 473J).',
   doc=f'''<h3>SMD direnç</h3>
{F('3 hane:   AB C  →  AB × 10^C          103 = 10 × 10³ = 10 kΩ', '4 hane:   ABC D →  ABC × 10^D        1002 = 100 × 10² = 10 kΩ', 'R ondalık:   4R7 = 4,7 Ω,   R10 = 0,1 Ω', 'EIA-96:   01C = 100 × 100 = 10 kΩ')}
<p><strong>EIA-96</strong> kodunda iki rakam, E96 serisindeki değerin sıra numarasıdır (01 = 100, 02 = 102 … 96 = 976). Harf çarpanı verir: Z = 0,001 · Y/R = 0,01 · X/S = 0,1 · A = 1 · B/H = 10 · C = 100 · D = 1 k · E = 10 k · F = 100 k.</p>
<h3>Seramik kondansatör</h3>
{F('AB C  →  AB × 10^C pF          104 = 10 × 10⁴ pF = 100 nF', 'C = 8 → ×0,01,   C = 9 → ×0,1', note='Sondaki harf toleranstır: B ±0,1 pF · C ±0,25 pF · D ±0,5 pF · F ±%1 · G ±%2 · J ±%5 · K ±%10 · M ±%20 · Z +%80/−%20')}'''),
 en=dict(title='SMD Resistor and Capacitor Code Decoder', short='SMD code decoder', card='Turn codes like 103, 4702, 4R7, 01C, 104J into values.',
   lead='Type the code printed on an SMD resistor or ceramic capacitor and see the value instantly. Understands 3-digit, 4-digit, R-notation and EIA-96 codes.',
   desc='SMD resistor code and capacitor code decoder: 3-digit (103), 4-digit (1002), R notation (4R7), EIA-96 (01C) and capacitor codes (104, 473J).',
   doc=f'''<h3>SMD resistors</h3>
{F('3 digits:   AB C  →  AB × 10^C          103 = 10 × 10³ = 10 kΩ', '4 digits:   ABC D →  ABC × 10^D        1002 = 100 × 10² = 10 kΩ', 'R as decimal point:   4R7 = 4.7 Ω,   R10 = 0.1 Ω', 'EIA-96:   01C = 100 × 100 = 10 kΩ')}
<p>In an <strong>EIA-96</strong> code the two digits are the index of the value in the E96 series (01 = 100, 02 = 102 … 96 = 976). The letter is the multiplier: Z = 0.001 · Y/R = 0.01 · X/S = 0.1 · A = 1 · B/H = 10 · C = 100 · D = 1 k · E = 10 k · F = 100 k.</p>
<h3>Ceramic capacitors</h3>
{F('AB C  →  AB × 10^C pF          104 = 10 × 10⁴ pF = 100 nF', 'C = 8 → ×0.01,   C = 9 → ×0.1', note='A trailing letter is the tolerance: B ±0.1 pF · C ±0.25 pF · D ±0.5 pF · F ±1% · G ±2% · J ±5% · K ±10% · M ±20% · Z +80/−20%')}''')),

# ------------------------------------------------------------------ GÜÇ
dict(id='regulator', cat='power', slugs=('ayarli-regulator', 'adjustable-regulator'), src=['lm2596', 'xl4015', 'mp1584', 'lm317', 'ams1117', 'w_eser'],
 related=['buck', 'divider', 'battery'], post='guc-kaynagi',
 tr=dict(title='Ayarlı Regülatör Direnç Hesaplama (LM2596, LM317, MP1584…)', short='Ayarlı regülatör', card='LM2596, XL4015, MP1584, LM317, AMS1117 için geri besleme dirençleri.',
   lead='Entegreyi seç: dirençlerden çıkış gerilimini hesapla ya da istediğin gerilim için gereken direnci ve en yakın standart değeri bul.',
   desc='LM2596, XL4015, MP1584, LM317 ve AMS1117 ayarlı regülatör hesaplayıcı: geri besleme dirençlerinden Vout, hedef gerilim için direnç ve E24/E96 önerisi.',
   doc=f'''<p>Ayarlı regülatörler çıkışı bir direnç bölücüyle izler ve FB/ADJ pinindeki gerilimi iç referansa (Vref) eşitler. İki farklı bağlantı tipi vardır.</p>
<h3>FB tipi: LM2596, XL4015, MP1584</h3>
{F('Vout = Vref · (1 + Rüst / Ralt)', 'Rüst = Ralt · (Vout / Vref − 1)', note='Rüst: Vout → FB,  Ralt: FB → GND.  Vref: LM2596 = 1,23 V · XL4015 = 1,25 V · MP1584 = 0,8 V')}
<h3>ADJ tipi: LM317, AMS1117</h3>
{F('Vout = Vref · (1 + R2 / R1) + Iadj · R2', 'R2 = (Vout − Vref) / (Vref / R1 + Iadj)', note='R1: OUT → ADJ,  R2: ADJ → GND.  Vref = 1,25 V,  Iadj ≈ 50 µA')}
<p>Hedef gerilim modunda hesaplanan direnç için <strong>E24</strong> ve <strong>E96</strong> serilerinden en yakın değerler önerilir ve o değerle elde edilecek gerçek çıkış gösterilir.</p>
<h3>Datasheet uyarıları</h3>
<ul><li><strong>LM2596:</strong> FB → GND direnci için 240 Ω – 1,5 kΩ aralığı önerilir. Araç bu aralığın dışında uyarı verir.</li>
<li><strong>MP1584:</strong> alt direncin 40 kΩ\'un altında tutulması önerilir.</li>
<li>Vref\'in kendisi de ±%2–3 toleranslıdır; hassas bir gerilim gerekiyorsa çıkışı ölçüp ince ayar yap.</li></ul>'''),
 en=dict(title='Adjustable Regulator Resistor Calculator (LM2596, LM317, MP1584…)', short='Adjustable regulator', card='Feedback resistors for the LM2596, XL4015, MP1584, LM317 and AMS1117.',
   lead='Pick the chip: calculate the output voltage from the resistors, or find the resistor and nearest standard value for the voltage you want.',
   desc='Adjustable regulator calculator for the LM2596, XL4015, MP1584, LM317 and AMS1117: Vout from feedback resistors, resistor for a target voltage, E24/E96 values.',
   doc=f'''<p>Adjustable regulators sense the output through a resistor divider and hold the FB/ADJ pin at an internal reference (Vref). There are two wiring styles.</p>
<h3>FB type: LM2596, XL4015, MP1584</h3>
{F('Vout = Vref · (1 + Rtop / Rbot)', 'Rtop = Rbot · (Vout / Vref − 1)', note='Rtop: Vout → FB,  Rbot: FB → GND.  Vref: LM2596 = 1.23 V · XL4015 = 1.25 V · MP1584 = 0.8 V')}
<h3>ADJ type: LM317, AMS1117</h3>
{F('Vout = Vref · (1 + R2 / R1) + Iadj · R2', 'R2 = (Vout − Vref) / (Vref / R1 + Iadj)', note='R1: OUT → ADJ,  R2: ADJ → GND.  Vref = 1.25 V,  Iadj ≈ 50 µA')}
<p>In target-voltage mode the nearest values in the <strong>E24</strong> and <strong>E96</strong> series are suggested together with the real output they give.</p>
<h3>Datasheet notes</h3>
<ul><li><strong>LM2596:</strong> 240 Ω – 1.5 kΩ is recommended for the FB → GND resistor. The tool warns outside this range.</li>
<li><strong>MP1584:</strong> keep the bottom resistor below 40 kΩ.</li>
<li>Vref itself has about ±2–3% tolerance; if you need a precise voltage, measure the output and trim.</li></ul>''')),

dict(id='buck', cat='power', slugs=('buck-donusturucu', 'buck-converter'), src=['slva477', 'lm2596', 'xl4015'], related=['regulator', 'battery', 'trace'],
 tr=dict(title='Buck Dönüştürücü Bobin ve Kondansatör Hesaplama', short='Buck dönüştürücü', card='Bobin, çıkış kondansatörü, görev oranı ve tepe akımını hesapla.',
   lead='Giriş/çıkış gerilimini ve akımı gir; buck devren için gereken en küçük bobini, çıkış kondansatörünü, görev oranını ve tepe akımını gör.',
   desc='Buck dönüştürücü hesaplayıcı: bobin değeri, çıkış kondansatörü, görev oranı, dalgalanma ve tepe akım. TI SLVA477 uygulama notundaki formüllerle.',
   doc=f'''<p>Hesaplar Texas Instruments\'ın <strong>SLVA477</strong> uygulama notundaki temel buck denklemlerine dayanır ve sürekli iletim modunu (CCM) varsayar.</p>
{F('D = Vout / (Vin · η)', 'ΔIL = (0,2 … 0,4) · Iout', 'L = Vout · (Vin − Vout) / (ΔIL · fs · Vin)', 'Itepe = Iout + ΔIL / 2', 'Cout = ΔIL / (8 · fs · ΔVout)', 'ΔVout(ESR) = ESR · ΔIL', note='η: verim · fs: anahtarlama frekansı · ΔIL: bobin dalgalanma akımı · ΔVout: izin verilen çıkış dalgalanması')}
<p>Bobin değeri için <strong>en yüksek giriş gerilimi</strong> kullanılır, çünkü dalgalanma akımı orada en büyüktür. Araç hesaplanan değerin bir üstündeki E12 bobin değerini de önerir.</p>
<h3>Pratikte dikkat</h3>
<ul><li>Bobinin doyma akımı, hesaplanan tepe akımdan büyük olmalı.</li>
<li>Çıkış dalgalanmasında çoğu zaman kapasiteden çok <strong>ESR</strong> belirleyicidir; ESR alanını doldurursan araç bunu da kontrol eder.</li>
<li>Datasheet belirli bir bobin ve kondansatör öneriyorsa önce onu kullan; bu hesap başlangıç noktası içindir.</li></ul>'''),
 en=dict(title='Buck Converter Inductor and Capacitor Calculator', short='Buck converter', card='Calculate the inductor, output capacitor, duty cycle and peak current.',
   lead='Enter input/output voltage and current to get the minimum inductor, output capacitor, duty cycle and peak current for your buck circuit.',
   desc='Buck converter calculator: inductor value, output capacitor, duty cycle, ripple and peak current, using the formulas in TI application note SLVA477.',
   doc=f'''<p>The calculations follow the basic buck equations in Texas Instruments application note <strong>SLVA477</strong> and assume continuous conduction mode (CCM).</p>
{F('D = Vout / (Vin · η)', 'ΔIL = (0.2 … 0.4) · Iout', 'L = Vout · (Vin − Vout) / (ΔIL · fs · Vin)', 'Ipeak = Iout + ΔIL / 2', 'Cout = ΔIL / (8 · fs · ΔVout)', 'ΔVout(ESR) = ESR · ΔIL', note='η: efficiency · fs: switching frequency · ΔIL: inductor ripple current · ΔVout: allowed output ripple')}
<p>The <strong>maximum input voltage</strong> is used for the inductor, because ripple current is largest there. The tool also suggests the next E12 inductor value up.</p>
<h3>In practice</h3>
<ul><li>The inductor saturation current must be above the calculated peak current.</li>
<li>Output ripple is often set more by <strong>ESR</strong> than by capacitance; fill the ESR field and the tool checks it too.</li>
<li>If the datasheet recommends a specific inductor and capacitor, use those first; this calculation is a starting point.</li></ul>''')),

dict(id='battery', cat='power', slugs=('pil-omru', 'battery-life'), src=['esp32'], related=['regulator', 'buck', 'ohm'],
 tr=dict(title='Pil Ömrü Hesaplama (Uyku Modlu)', short='Pil ömrü', card='Aktif ve uyku akımlarıyla ortalama akımı ve pil ömrünü tahmin et.',
   lead='Cihazın ne kadar süre çalışıp ne kadar uyuduğunu gir; ortalama akımı ve pilin kaç gün dayanacağını gör. ESP32 gibi uyku modlu projeler için.',
   desc='Pil ömrü hesaplayıcı: aktif ve uyku akımına göre ortalama akım ve tahmini çalışma süresi. ESP32 deep sleep projeleri için.',
   doc=f'''<p>Uyku modlu bir cihaz zamanının çoğunu çok düşük akımla geçirir. Pil ömrünü belirleyen, bir döngü boyunca çekilen <strong>ortalama akımdır</strong>.</p>
{F('Iort = (Iaktif · taktif + Iuyku · tuyku) / (taktif + tuyku)', 'Süre (saat) = Kapasite (Ah) · k / Iort', note='k: kullanılabilir kapasite oranı (kesme gerilimi, sıcaklık, kendi kendine deşarj payı)')}
<p>Örnek: 5 s boyunca 80 mA, 10 s uyku 20 µA → ortalama ≈ 26,7 mA. Uyku süresini 10 dakikaya çıkarırsan ortalama ≈ 0,68 mA\'e düşer ve 2000 mAh pil aylarca dayanır.</p>
<h3>Pratikte dikkat</h3>
<ul><li>Geliştirme kartlarında regülatör, USB-seri çip ve LED\'ler uykuda bile mA seviyesinde akım çekebilir; ölçerek kontrol et.</li>
<li>Yüksek akımda ve soğukta pilin verebildiği kapasite düşer.</li></ul>'''),
 en=dict(title='Battery Life Calculator (with Sleep Mode)', short='Battery life', card='Estimate average current and battery life from active and sleep currents.',
   lead='Enter how long your device is awake and how long it sleeps; see the average current and how many days the battery lasts. For ESP32-style sleep projects.',
   desc='Battery life calculator: average current and estimated run time from active and sleep current. Made for ESP32 deep sleep projects.',
   doc=f'''<p>A device with a sleep mode spends most of its time at a very low current. What sets battery life is the <strong>average current</strong> over one cycle.</p>
{F('Iavg = (Iactive · tactive + Isleep · tsleep) / (tactive + tsleep)', 'Life (hours) = Capacity (Ah) · k / Iavg', note='k: usable capacity ratio (margin for cut-off voltage, temperature and self-discharge)')}
<p>Example: 80 mA for 5 s, then 20 µA sleep for 10 s → average ≈ 26.7 mA. Stretch the sleep to 10 minutes and the average drops to ≈ 0.68 mA, so a 2000 mAh battery lasts for months.</p>
<h3>In practice</h3>
<ul><li>On development boards the regulator, USB-serial chip and LEDs can draw mA even in sleep; measure to be sure.</li>
<li>Usable capacity drops at high current and low temperature.</li></ul>''')),

# ------------------------------------------------------------------ PCB
dict(id='trace', cat='pcb', slugs=('pcb-iz-genisligi', 'pcb-trace-width'), src=['ipc2221'], related=['awg', 'buck', 'ohm'], post='pcb-tasarim',
 tr=dict(title='PCB İz Genişliği Hesaplama (IPC-2221)', short='PCB iz genişliği', card='Akıma ve bakır kalınlığına göre en az iz genişliği, direnç ve düşüm.',
   lead='Akımı, bakır kalınlığını ve izin verdiğin sıcaklık artışını gir; PCB izinin en az ne kadar geniş olması gerektiğini ve iz üzerindeki kaybı gör.',
   desc='PCB iz genişliği hesaplayıcı (IPC-2221): akım, bakır kalınlığı (oz) ve sıcaklık artışına göre iz genişliği, iz direnci, gerilim düşümü ve güç kaybı.',
   doc=f'''<p>Hesap, <strong>IPC-2221</strong> standardındaki akım–sıcaklık artışı eğrilerinin denklemine dayanır.</p>
{F('I = k · ΔT^0,44 · A^0,725', 'A = (I / (k · ΔT^0,44))^(1/0,725)   [mil²]', 'W = A / (t · 1,378)   [mil],   W(mm) = W(mil) · 0,0254', note='k = 0,048 dış katman, 0,024 iç katman · t: bakır kalınlığı (oz) · 1 oz = 1,378 mil = 35 µm')}
<p>İz uzunluğunu girersen iz direnci de hesaplanır. Bakırın özdirenci sıcaklıkla arttığı için hesapta ortam + sıcaklık artışı kullanılır:</p>
{F('R = ρ · L / (W · t)', 'ρ = 1,72·10⁻⁸ Ω·m · (1 + 0,00393 · (T − 20 °C))')}
<h3>Pratikte dikkat</h3>
<ul><li>İç katmanlar ısıyı daha zor attığı için aynı akımda yaklaşık iki kat daha geniş iz ister.</li>
<li>IPC-2221 eğrileri temkinlidir ve 35 A\'e kadar geçerlidir. Daha ayrıntılı analiz için yeni standart IPC-2152 kullanılır.</li></ul>'''),
 en=dict(title='PCB Trace Width Calculator (IPC-2221)', short='PCB trace width', card='Minimum trace width, resistance and drop from current and copper weight.',
   lead='Enter the current, copper weight and allowed temperature rise to see the minimum PCB trace width and the loss along the trace.',
   desc='PCB trace width calculator (IPC-2221): trace width from current, copper weight (oz) and temperature rise, plus trace resistance, voltage drop and power loss.',
   doc=f'''<p>The calculation is based on the equation fitted to the current vs. temperature-rise curves in <strong>IPC-2221</strong>.</p>
{F('I = k · ΔT^0.44 · A^0.725', 'A = (I / (k · ΔT^0.44))^(1/0.725)   [mil²]', 'W = A / (t · 1.378)   [mil],   W(mm) = W(mil) · 0.0254', note='k = 0.048 external, 0.024 internal · t: copper weight (oz) · 1 oz = 1.378 mil = 35 µm')}
<p>Enter the trace length to get its resistance too. Copper resistivity rises with temperature, so ambient + temperature rise is used:</p>
{F('R = ρ · L / (W · t)', 'ρ = 1.72·10⁻⁸ Ω·m · (1 + 0.00393 · (T − 20 °C))')}
<h3>In practice</h3>
<ul><li>Inner layers shed heat less easily, so they need roughly twice the width for the same current.</li>
<li>IPC-2221 curves are conservative and valid up to 35 A. The newer IPC-2152 is used for more detailed analysis.</li></ul>''')),

dict(id='awg', cat='pcb', slugs=('awg-kablo', 'awg-wire'), src=['astm258', 'w_awg'], related=['trace', 'ohm', 'battery'],
 tr=dict(title='AWG ↔ mm² Kablo Kesiti Hesaplama', short='AWG ↔ mm²', card='AWG\'yi mm²\'ye çevir; çap ve metre başına direnç.',
   lead='AWG numarasını mm² kesite çevir ya da elindeki mm² için karşılık gelen AWG\'yi bul. Çap ve bakır direnci de hesaplanır.',
   desc='AWG mm² dönüştürücü: AWG\'den kesit alanı, çap ve metre başına direnç; mm²\'den en yakın AWG. ASTM B258 formülüyle.',
   doc=f'''<p>AWG (American Wire Gauge) logaritmik bir ölçektir: numara büyüdükçe kablo incelir ve her 6 numarada çap yaklaşık yarıya iner.</p>
{F('d (mm) = 0,127 · 92^((36 − n) / 39)', 'A = π · d² / 4', 'R / m = ρ / A,   ρ(Cu, 20 °C) = 1,7241·10⁻⁸ Ω·m', note='00 → n = −1,  000 → n = −2,  0000 → n = −3')}
<p>“mm² → AWG” modunda, girdiğin kesit alanına <strong>eşit ya da daha büyük</strong> olan en ince AWG önerilir; yani daha ince bir kabloya düşmezsin.</p>
<p>Kablonun taşıyabileceği akım tek bir sayı değildir: yalıtım malzemesine, kabloların demet halinde olup olmamasına ve ortam sıcaklığına göre değişir.</p>'''),
 en=dict(title='AWG ↔ mm² Wire Gauge Calculator', short='AWG ↔ mm²', card='Convert AWG to mm²; diameter and resistance per metre.',
   lead='Convert an AWG number to a mm² cross-section, or find the AWG for the mm² you have. Diameter and copper resistance are calculated too.',
   desc='AWG to mm² converter: cross-section, diameter and resistance per metre from AWG; nearest AWG from mm². Uses the ASTM B258 formula.',
   doc=f'''<p>AWG (American Wire Gauge) is a log scale: a higher number means a thinner wire, and every 6 gauges the diameter roughly halves.</p>
{F('d (mm) = 0.127 · 92^((36 − n) / 39)', 'A = π · d² / 4', 'R / m = ρ / A,   ρ(Cu, 20 °C) = 1.7241·10⁻⁸ Ω·m', note='00 → n = −1,  000 → n = −2,  0000 → n = −3')}
<p>In “mm² → AWG” mode the thinnest AWG whose area is <strong>equal or larger</strong> than your value is suggested, so you never end up with a thinner wire.</p>
<p>Current capacity is not a single number: it depends on the insulation, whether wires are bundled and the ambient temperature.</p>''')),

# ------------------------------------------------------------------ ZAMANLAMA
dict(id='rc', cat='timing', slugs=('rc-filtre', 'rc-filter'), src=['w_rc'], related=['t555', 'db', 'series'],
 tr=dict(title='RC Filtre ve Zaman Sabiti Hesaplama', short='RC filtre / τ', card='Kesim frekansı, zaman sabiti ve hedef yüzdeye şarj süresi.',
   lead='R ve C değerini gir: RC filtrenin kesim frekansını, zaman sabitini (τ) ve kondansatörün istediğin yüzdeye ne kadar sürede dolduğunu gör.',
   desc='RC filtre hesaplayıcı: kesim frekansı fc = 1/(2πRC), zaman sabiti τ = RC ve kondansatör şarj süresi. Alçak/yüksek geçiren filtre ve gecikme devreleri için.',
   doc=f'''<p>Bir direnç ve bir kondansatör hem basit bir filtre hem de bir gecikme devresi oluşturur. İkisini de aynı çarpım belirler: <strong>τ = R·C</strong>.</p>
{F('τ = R · C', 'fc = 1 / (2π · R · C)', 'Vc(t) = V · (1 − e^(−t/τ))   →   t = −τ · ln(1 − p)', note='p: hedef şarj oranı (0,9 = %90)')}
<p>1τ\'da kondansatör %63,2\'ye, 5τ\'da %99,3\'e dolar; pratikte 5τ “tam dolu” kabul edilir. Kesim frekansı, sinyalin gücünün yarıya (−3 dB) indiği noktadır ve alçak geçiren ile yüksek geçiren RC filtre için aynıdır.</p>
<p>Not: Çıkışa bağlanan yük filtreyi değiştirir. Yük direnci R\'den en az 10 kat büyük olmalıdır.</p>'''),
 en=dict(title='RC Filter and Time Constant Calculator', short='RC filter / τ', card='Cut-off frequency, time constant and time to reach a target charge.',
   lead='Enter R and C to see the RC filter cut-off frequency, the time constant (τ) and how long the capacitor takes to charge to the level you want.',
   desc='RC filter calculator: cut-off frequency fc = 1/(2πRC), time constant τ = RC and capacitor charge time. For low/high-pass filters and delay circuits.',
   doc=f'''<p>A resistor and a capacitor form both a simple filter and a delay circuit. The same product sets both: <strong>τ = R·C</strong>.</p>
{F('τ = R · C', 'fc = 1 / (2π · R · C)', 'Vc(t) = V · (1 − e^(−t/τ))   →   t = −τ · ln(1 − p)', note='p: target charge ratio (0.9 = 90%)')}
<p>After 1τ the capacitor is at 63.2%, after 5τ at 99.3%; in practice 5τ counts as fully charged. The cut-off frequency is where signal power halves (−3 dB) and is the same for RC low-pass and high-pass filters.</p>
<p>Note: a load on the output changes the filter. Keep the load at least 10× larger than R.</p>''')),

dict(id='t555', cat='timing', slugs=('555-zamanlayici', '555-timer'), src=['ne555'], related=['rc', 'led', 'series'],
 tr=dict(title='555 Zamanlayıcı Hesaplama (Astable / Monostable)', short='555 zamanlayıcı', card='Astable frekans ve görev oranı, monostable darbe süresi.',
   lead='555 entegresiyle osilatör ya da tek darbe devresi kur: R1, R2 ve C\'ye göre frekansı, görev oranını ve darbe süresini hesapla.',
   desc='555 zamanlayıcı hesaplayıcı: astable modda frekans, görev oranı, yüksek/düşük süre; monostable modda darbe süresi. NE555 datasheet formülleriyle.',
   doc=f'''<p>Formüller Texas Instruments <strong>NE555 datasheet</strong>\'indeki denklemlerdir. Kondansatör, besleme geriliminin 1/3\'ü ile 2/3\'ü arasında dolup boşalır; 0,693 bu aralığın karşılığı olan ln 2\'dir.</p>
<h3>Astable (osilatör)</h3>
{F('tH = 0,693 · (R1 + R2) · C', 'tL = 0,693 · R2 · C', 'f = 1,44 / ((R1 + 2·R2) · C)', 'Görev oranı = (R1 + R2) / (R1 + 2·R2)')}
<h3>Monostable (tek darbe)</h3>
{F('t = 1,1 · R1 · C')}
<h3>Pratikte dikkat</h3>
<ul><li>Bu bağlantıda görev oranı her zaman %50\'nin üstündedir. Daha düşük görev oranı için R2\'ye paralel bir diyot eklenir.</li>
<li>R1 çok küçük olursa deşarj pini fazla akım çeker; birkaç kΩ ve üstü uygundur.</li>
<li>Elektrolitik kondansatörlerin toleransı geniştir (±%20); hassas zamanlama için film kondansatör tercih et.</li></ul>'''),
 en=dict(title='555 Timer Calculator (Astable / Monostable)', short='555 timer', card='Astable frequency and duty cycle, monostable pulse width.',
   lead='Build an oscillator or one-shot with the 555: calculate frequency, duty cycle and pulse width from R1, R2 and C.',
   desc='555 timer calculator: frequency, duty cycle and high/low time in astable mode; pulse width in monostable mode. Uses the NE555 datasheet formulas.',
   doc=f'''<p>The formulas are the equations in the Texas Instruments <strong>NE555 datasheet</strong>. The capacitor charges and discharges between 1/3 and 2/3 of the supply; 0.693 is ln 2, which corresponds to that range.</p>
<h3>Astable (oscillator)</h3>
{F('tH = 0.693 · (R1 + R2) · C', 'tL = 0.693 · R2 · C', 'f = 1.44 / ((R1 + 2·R2) · C)', 'Duty cycle = (R1 + R2) / (R1 + 2·R2)')}
<h3>Monostable (one-shot)</h3>
{F('t = 1.1 · R1 · C')}
<h3>In practice</h3>
<ul><li>With this wiring the duty cycle is always above 50%. Add a diode across R2 for lower duty cycles.</li>
<li>A very small R1 makes the discharge pin sink too much current; a few kΩ or more is fine.</li>
<li>Electrolytic capacitors have wide tolerance (±20%); use a film capacitor for accurate timing.</li></ul>''')),
]
TOOL = {t['id']: t for t in TOOLS}
