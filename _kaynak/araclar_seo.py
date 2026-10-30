# -*- coding: utf-8 -*-
"""Hesap araçları için arama motoru içeriği: sayfa başlıkları (<title>), açıklamalar,
hesaplanmış tablolar (sık kullanılan değerler) ve sık sorulan sorular.
Tablolar kodla hesaplanır; elle değer yazılmaz. build.py → build_tool() kullanır."""
import math
from araclar import COLOR_TABLE

# ---------------------------------------------------------------- yardımcılar
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def e24_all(lo=1, hi=1e7):
    out = []
    for d in range(0, 8):
        for v in E24:
            x = round(v * 10 ** d, 6)
            if lo <= x <= hi:
                out.append(x)
    return out


def e24_up(x):
    return min(v for v in e24_all() if v >= x - 1e-9)


def num(x, lang, nd=2):
    s = f'{x:.{nd}f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',') if lang == 'tr' else s


def ohm(x, lang):
    for f, u in ((1e6, 'MΩ'), (1e3, 'kΩ')):
        if x >= f:
            return f'{num(x / f, lang)} {u}'
    return f'{num(x, lang)} Ω'


def farad(pf, lang):
    for f, u in ((1e6, 'µF'), (1e3, 'nF')):
        if pf >= f:
            return f'{num(pf / f, lang)} {u}'
    return f'{num(pf, lang)} pF'


def table(head, rows, cls=''):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="table-wrap"><table class="calc-table{(" " + cls) if cls else ""}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


# ---------------------------------------------------------------- direnç renk kodu
CT = {i: row for i, row in enumerate(COLOR_TABLE[:10])}  # 0..9 renkleri
GOLD, SILVER = COLOR_TABLE[10], COLOR_TABLE[11]


def bands(value, n):
    """Değer → renk satırları listesi (n=4: 2 hane, n=5: 3 hane). Tolerans hariç."""
    digits = 2 if n == 4 else 3
    exp = math.floor(math.log10(value)) - (digits - 1)
    sig = round(value / 10 ** exp)
    ds = [int(c) for c in str(sig).zfill(digits)]
    mult = {-1: GOLD, -2: SILVER}.get(exp) or CT[exp]
    return [CT[d] for d in ds] + [mult]


def color_name(row, lang):
    return row[1] if lang == 'tr' else row[2]


def swatch(rows, lang):
    dots = ''.join(f'<span class="cdot" style="background:{r[0]}" title="{color_name(r, lang)}"></span>' for r in rows)
    names = '-'.join(color_name(r, lang).lower() for r in rows)
    return f'<span class="cband">{dots}</span><span class="cnames">{names}</span>'


COMMON_R = [10, 22, 47, 100, 150, 220, 330, 470, 680, 1e3, 2.2e3, 3.3e3, 4.7e3, 10e3, 22e3, 47e3, 100e3, 220e3, 470e3, 1e6]


def color_words(value, n, lang):
    tol = GOLD if n == 4 else CT[1]
    return '-'.join(color_name(r, lang).lower() for r in bands(value, n) + [tol])


def color_common(lang):
    tr = lang == 'tr'
    rows = []
    for v in COMMON_R:
        rows.append([f'<b>{ohm(v, lang)}</b>', swatch(bands(v, 4) + [GOLD], lang), swatch(bands(v, 5) + [CT[1]], lang)])
    head = ('Değer', '4 bant (±%5)', '5 bant (±%1)') if tr else ('Value', '4 bands (±5%)', '5 bands (±1%)')
    return table(head, rows, 'ctab')


def color_extra(lang):
    tr = lang == 'tr'
    if tr:
        return f'''<h3>Direnç renk kodu nasıl okunur? (4 adım)</h3>
<ol class="steps-ol"><li><strong>Yönü bul:</strong> altın ya da gümüş bant varsa onu sağa al. Bantlar bir uca daha yakınsa okumaya o uçtan başla.</li>
<li><strong>Haneleri yaz:</strong> 4 bantlı dirençte ilk iki, 5 bantlıda ilk üç bant rakamdır (siyah 0 … beyaz 9).</li>
<li><strong>Çarpanı uygula:</strong> sonraki bant kaç sıfır ekleneceğini söyler (kırmızı ×100, turuncu ×1 k, altın ×0,1).</li>
<li><strong>Toleransı oku:</strong> son bant hassasiyettir: altın ±%5, gümüş ±%10, kahverengi ±%1.</li></ol>
<p><strong>Örnek:</strong> kahverengi-siyah-turuncu-altın → 1, 0, ×1000 → <strong>10 kΩ ±%5</strong>. Aynı direnç 5 bantlı olarak kahverengi-siyah-siyah-kırmızı-kahverengi yazılır.</p>
<h3>Sık kullanılan direnç değerlerinin renk kodları</h3>
<p>Arduino, LED ve sensör devrelerinde en çok karşılaşılan değerler. Renklerin yanında yazılı adları da var; tabloyu telefonundan açıp dirence bakarak karşılaştırabilirsin.</p>
{color_common('tr')}'''
    return f'''<h3>How to read a resistor colour code (4 steps)</h3>
<ol class="steps-ol"><li><strong>Find the direction:</strong> put the gold or silver band on the right. If the bands sit closer to one end, start reading from that end.</li>
<li><strong>Write down the digits:</strong> the first two bands (4-band) or three bands (5-band) are digits (black 0 … white 9).</li>
<li><strong>Apply the multiplier:</strong> the next band tells you how many zeros to add (red ×100, orange ×1 k, gold ×0.1).</li>
<li><strong>Read the tolerance:</strong> the last band is the precision: gold ±5%, silver ±10%, brown ±1%.</li></ol>
<p><strong>Example:</strong> brown-black-orange-gold → 1, 0, ×1000 → <strong>10 kΩ ±5%</strong>. The same resistor with 5 bands is brown-black-black-red-brown.</p>
<h3>Colour codes of common resistor values</h3>
<p>The values you meet most in Arduino, LED and sensor circuits, with the colour names written out.</p>
{color_common('en')}'''


def color_faq(lang):
    tr = lang == 'tr'
    W = lambda v, n: color_words(v, n, lang)
    if tr:
        return [
            ('Direnç renk kodu hangi taraftan okunur?', 'Altın veya gümüş tolerans bandı sağda kalacak şekilde soldan sağa okunur. Tolerans bandı çoğu zaman diğerlerinden biraz ayrıktır; bantlar bir uca daha yakınsa okuma o uçtan başlar. Emin olamıyorsan multimetreyle ölçmek en kesin yoldur.'),
            ('10k direncin renk kodu nedir?', f'4 bantlı 10 kΩ direnç: {W(10e3, 4)}. 5 bantlı (±%1) 10 kΩ direnç: {W(10e3, 5)}.'),
            ('220 ohm direncin renkleri nelerdir?', f'4 bant: {W(220, 4)}. 5 bant: {W(220, 5)}. LED devrelerinde 5 V ile en sık kullanılan değerlerden biridir.'),
            ('1k (1 kΩ) direnç renk kodu nedir?', f'4 bant: {W(1e3, 4)}. 5 bant: {W(1e3, 5)}.'),
            ('4,7k direncin renkleri nelerdir?', f'4 bant: {W(4.7e3, 4)}. 5 bant: {W(4.7e3, 5)}. I²C hatlarında pull-up olarak sık kullanılır.'),
            ('Altın ve gümüş bant ne anlama gelir?', 'Son bantta altın ±%5, gümüş ±%10 tolerans demektir. Çarpan bandında ise altın ×0,1, gümüş ×0,01 anlamına gelir ve düşük değerli dirençlerde görülür: 4,7 Ω = sarı-mor-altın-altın.'),
            ('4 bantlı ve 5 bantlı direnç arasındaki fark nedir?', '4 bantlı dirençte 2 rakam, 5 bantlıda 3 rakam vardır; 5 bantlılar genellikle ±%1 metal film dirençlerdir ve daha hassastır. 6. bant varsa sıcaklık katsayısını (ppm/K) gösterir.'),
        ]
    return [
        ('Which side do you read a resistor colour code from?', 'Read from left to right with the gold or silver tolerance band on the right. The tolerance band is often set slightly apart; if the bands sit closer to one end, start from that end. When in doubt, a multimeter is the surest check.'),
        ('What is the colour code of a 10k resistor?', f'4-band 10 kΩ: {W(10e3, 4)}. 5-band (±1%) 10 kΩ: {W(10e3, 5)}.'),
        ('What are the colours of a 220 ohm resistor?', f'4 bands: {W(220, 4)}. 5 bands: {W(220, 5)}.'),
        ('What is the colour code of a 1k resistor?', f'4 bands: {W(1e3, 4)}. 5 bands: {W(1e3, 5)}.'),
        ('What do gold and silver bands mean?', 'As the last band, gold means ±5% and silver ±10% tolerance. As a multiplier, gold is ×0.1 and silver ×0.01, used on low values: 4.7 Ω = yellow-violet-gold-gold.'),
        ('What is the difference between 4-band and 5-band resistors?', 'A 4-band resistor has 2 digits, a 5-band resistor has 3; 5-band parts are usually ±1% metal film resistors. A 6th band shows the temperature coefficient (ppm/K).'),
    ]


# ---------------------------------------------------------------- LED direnci
LED_VF = [('Kırmızı', 'Red', 2.0), ('Sarı / turuncu', 'Yellow / orange', 2.1), ('Yeşil / mavi / beyaz', 'Green / blue / white', 3.1)]
LED_VS = [3.3, 5, 9, 12]


def led_r(vs, vf, i=0.02):
    return e24_up((vs - vf) / i)


def led_extra(lang):
    tr = lang == 'tr'
    rows = []
    for ntr, nen, vf in LED_VF:
        cells = [f'<b>{ntr if tr else nen}</b> <small>({num(vf, lang)} V)</small>']
        for vs in LED_VS:
            if vs - vf < 0.5:
                cells.append('—')
            else:
                cells.append(ohm(led_r(vs, vf), lang))
        rows.append(cells)
    head = ['LED' if not tr else 'LED rengi'] + [f'{num(v, lang)} V' for v in LED_VS]
    if tr:
        return f'''<h3>Hazır tablo: 20 mA için LED direnci</h3>
<p>Tek LED, 20 mA akım ve E24 serisinde bir üst standart değer. Daha az parlaklık yeterliyse (gösterge LED'i) akımı 5–10 mA'e düşürüp direnci büyütebilirsin; LED daha uzun ömürlü olur.</p>
{table(head, rows)}
<p class="tool-note">“—”: besleme gerilimi LED'in ileri gerilimine çok yakın; direnç akımı güvenle sınırlayamaz. 3,3 V ile mavi/beyaz LED için direnç yerine daha yüksek besleme ya da sabit akım sürücüsü düşün.</p>'''
    return f'''<h3>Quick table: LED resistor for 20 mA</h3>
<p>One LED, 20 mA and the next standard value up in the E24 series. For an indicator LED, 5–10 mA is often bright enough and the LED lasts longer.</p>
{table(head, rows)}
<p class="tool-note">“—”: the supply is too close to the LED forward voltage for a resistor to limit the current safely.</p>'''


def led_faq(lang):
    tr = lang == 'tr'
    if tr:
        return [
            ('5V ile LED için kaç ohm direnç gerekir?', f'20 mA için kırmızı LED (≈2,0 V) ile {ohm(led_r(5, 2.0), "tr")}, beyaz/mavi LED (≈3,1 V) ile {ohm(led_r(5, 3.1), "tr")} direnç yeterlidir. Arduino projelerinde sık görülen 220 Ω, akımı biraz düşürerek güvenli tarafta kalır.'),
            ('12V ile LED için hangi direnç kullanılır?', f'20 mA için kırmızı LED ile {ohm(led_r(12, 2.0), "tr")}, beyaz LED ile {ohm(led_r(12, 3.1), "tr")}. Direncin harcadığı güç yaklaşık 0,2 W olduğu için 1/2 W direnç seçmek daha güvenlidir.'),
            ('LED direnci hangi bacağa takılır?', 'Seri bağlandığı sürece anot (+, uzun bacak) ya da katot (−) tarafına takılabilir; akım aynıdır.'),
            ('Birden fazla LED tek dirençle sürülebilir mi?', 'Seri bağlı LED\'ler tek dirençle sürülebilir (besleme yeterliyse). Paralel bağlı LED\'lerin her birine ayrı direnç koymak gerekir; yoksa akım eşit paylaşılmaz.'),
        ]
    return [
        ('What resistor do I need for an LED on 5V?', f'For 20 mA, a red LED (≈2.0 V) needs {ohm(led_r(5, 2.0), "en")} and a white/blue LED (≈3.1 V) needs {ohm(led_r(5, 3.1), "en")}. The common 220 Ω runs it a little below 20 mA, which is safe.'),
        ('What resistor do I need for an LED on 12V?', f'For 20 mA: {ohm(led_r(12, 2.0), "en")} with a red LED, {ohm(led_r(12, 3.1), "en")} with a white LED. It dissipates about 0.2 W, so a 1/2 W resistor is safer.'),
        ('Which leg does the LED resistor go on?', 'As long as it is in series, it can go on the anode (+, long leg) or the cathode (−) side; the current is the same.'),
        ('Can several LEDs share one resistor?', 'LEDs in series can (if the supply is high enough). LEDs in parallel each need their own resistor, or the current will not share evenly.'),
    ]


# ---------------------------------------------------------------- SMD kod
SMD_R = ['100', '101', '221', '331', '471', '102', '222', '472', '103', '473', '104', '105', '4R7', '1001', '1002', '4701']
SMD_C = ['101', '221', '102', '222', '103', '473', '104', '105', '106']


def smd_r_val(code):
    if 'R' in code:
        return float(code.replace('R', '.'))
    return int(code[:-1]) * 10 ** int(code[-1])


def smd_extra(lang):
    tr = lang == 'tr'
    rr = [[f'<code>{c}</code>', ohm(smd_r_val(c), lang)] for c in SMD_R]
    cc = [[f'<code>{c}</code>', farad(int(c[:2]) * 10 ** int(c[2]), lang)] for c in SMD_C]
    half = (len(rr) + 1) // 2
    if tr:
        return f'''<h3>Sık görülen SMD direnç kodları</h3>
<div class="two-tables">{table(('Kod', 'Değer'), rr[:half])}{table(('Kod', 'Değer'), rr[half:])}</div>
<h3>Sık görülen seramik kondansatör kodları</h3>
{table(('Kod', 'Değer'), cc)}
<p><code>000</code> ya da <code>0</code> yazan SMD parça 0 Ω'luk köprüdür (jumper).</p>'''
    return f'''<h3>Common SMD resistor codes</h3>
<div class="two-tables">{table(('Code', 'Value'), rr[:half])}{table(('Code', 'Value'), rr[half:])}</div>
<h3>Common ceramic capacitor codes</h3>
{table(('Code', 'Value'), cc)}
<p>A part marked <code>000</code> or <code>0</code> is a 0 Ω jumper.</p>'''


def smd_faq(lang):
    if lang == 'tr':
        return [
            ('SMD dirençte 103 ne demek?', '103 = 10 × 10³ = 10 kΩ. İlk iki rakam değer, üçüncü rakam eklenecek sıfır sayısıdır.'),
            ('104 kondansatör kaç nF?', '104 = 10 × 10⁴ pF = 100 000 pF = 100 nF (0,1 µF). Dekuplaj kondansatörü olarak en sık kullanılan değerdir.'),
            ('4R7 ne anlama gelir?', 'R ondalık virgülün yerini tutar: 4R7 = 4,7 Ω, R10 = 0,1 Ω.'),
            ('01C gibi harfli kodlar nedir?', 'Bunlar ±%1 dirençlerde kullanılan EIA-96 kodlarıdır. 01 E96 serisindeki 100 değerini, C ise ×100 çarpanını gösterir: 01C = 10 kΩ.'),
        ]
    return [
        ('What does 103 mean on an SMD resistor?', '103 = 10 × 10³ = 10 kΩ. The first two digits are the value and the third is the number of zeros.'),
        ('How many nF is a 104 capacitor?', '104 = 10 × 10⁴ pF = 100,000 pF = 100 nF (0.1 µF), the most common decoupling value.'),
        ('What does 4R7 mean?', 'R marks the decimal point: 4R7 = 4.7 Ω, R10 = 0.1 Ω.'),
        ('What are codes like 01C?', 'These are EIA-96 codes for ±1% resistors. 01 is the value 100 in the E96 series and C is the ×100 multiplier: 01C = 10 kΩ.'),
    ]


# ---------------------------------------------------------------- gerilim bölücü
DIV_CASES = [(5, 3.3), (12, 5), (12, 3.3), (24, 5), (9, 5), (4.2, 3.3)]


def div_pair(vin, vout, r2=10e3):
    best = min(e24_all(100, 1e6), key=lambda r1: abs(vin * r2 / (r1 + r2) - vout))
    return best, vin * r2 / (best + r2)


def div_extra(lang):
    tr = lang == 'tr'
    rows = []
    for vin, vout in DIV_CASES:
        r1, real = div_pair(vin, vout)
        rows.append([f'{num(vin, lang)} V → {num(vout, lang)} V', ohm(r1, lang), ohm(10e3, lang), f'{num(real, lang)} V'])
    head = ('Dönüşüm', 'R1 (üst)', 'R2 (alt)', 'Gerçek Vout') if tr else ('Conversion', 'R1 (top)', 'R2 (bottom)', 'Actual Vout')
    if tr:
        return f'''<h3>Hazır tablo: sık kullanılan gerilim bölücüler</h3>
<p>R2 = 10 kΩ sabit, R1 E24 serisinden en yakın değer. Yüksüz çıkış gösterilir; ADC girişi gibi yüksek empedanslı yükler için uygundur.</p>
{table(head, rows)}'''
    return f'''<h3>Quick table: common voltage dividers</h3>
<p>R2 fixed at 10 kΩ, R1 is the closest E24 value. Unloaded output; fine for high-impedance loads such as an ADC input.</p>
{table(head, rows)}'''


def div_faq(lang):
    r1, real = div_pair(5, 3.3)
    if lang == 'tr':
        return [
            ('5V\'u 3,3V\'a gerilim bölücüyle nasıl düşürürüm?', f'R1 = {ohm(r1, "tr")} (üst) ve R2 = 10 kΩ (alt) ile çıkış ≈ {num(real, "tr")} V olur. Bu yöntem sinyal seviyesi düşürmek (ör. 5 V UART → 3,3 V) için uygundur; bir devreyi beslemek için değil.'),
            ('Gerilim bölücü ile bir modül beslenir mi?', 'Hayır. Çıkış, çekilen akıma göre değişir. Besleme için regülatör (LDO ya da buck) kullanılmalı.'),
            ('Gerilim bölücüde hangi direnç değerleri seçilmeli?', 'Toplam 10–100 kΩ çoğu ADC ve sinyal uygulaması için iyi bir başlangıçtır: düşük değerler gereksiz akım çeker, çok yüksek değerler gürültü ve ölçüm hatası getirir.'),
        ]
    return [
        ('How do I drop 5V to 3.3V with a voltage divider?', f'R1 = {ohm(r1, "en")} (top) and R2 = 10 kΩ (bottom) give ≈ {num(real, "en")} V. Good for shifting a signal level (e.g. 5 V UART → 3.3 V), not for powering a circuit.'),
        ('Can a voltage divider power a module?', 'No. The output changes with the load current. Use a regulator (LDO or buck) for power.'),
        ('What resistor values should a divider use?', 'A total of 10–100 kΩ is a good start for most ADC and signal uses: low values waste current, very high values add noise and error.'),
    ]


# ---------------------------------------------------------------- ohm kanunu
def ohm_extra(lang):
    tr = lang == 'tr'
    i_220 = (5 - 0) / 220 * 1000
    p_max = math.sqrt(0.25 / 1000) * 1000
    if tr:
        return f'''<h3>Çözümlü örnekler</h3>
<ul><li><strong>Akım bul:</strong> 5 V, 220 Ω dirence uygulanırsa I = 5 / 220 = <strong>{num(i_220, "tr", 1)} mA</strong>.</li>
<li><strong>Direnç bul:</strong> 12 V ile 2 A çeken bir yükün direnci R = 12 / 2 = <strong>6 Ω</strong>, gücü P = 12 × 2 = <strong>24 W</strong>.</li>
<li><strong>Güç sınırı:</strong> 1/4 W\'lık 1 kΩ dirençten en fazla I = √(P / R) = √(0,25 / 1000) ≈ <strong>{num(p_max, "tr", 1)} mA</strong> geçebilir.</li></ul>
<p>Formülü hatırlamanın kolay yolu <strong>V-I-R üçgeni</strong>: aradığın büyüklüğü kapat; kalan ikisi yan yanaysa çarp (V = I·R), üst üsteyse böl (I = V/R, R = V/I).</p>'''
    return f'''<h3>Worked examples</h3>
<ul><li><strong>Find the current:</strong> 5 V across 220 Ω gives I = 5 / 220 = <strong>{num(i_220, "en", 1)} mA</strong>.</li>
<li><strong>Find the resistance:</strong> a load drawing 2 A from 12 V is R = 12 / 2 = <strong>6 Ω</strong> and uses P = 12 × 2 = <strong>24 W</strong>.</li>
<li><strong>Power limit:</strong> a 1/4 W, 1 kΩ resistor can carry at most I = √(P / R) = √(0.25 / 1000) ≈ <strong>{num(p_max, "en", 1)} mA</strong>.</li></ul>
<p>An easy way to remember it is the <strong>V-I-R triangle</strong>: cover the quantity you want; if the other two sit side by side multiply (V = I·R), if one is above the other divide (I = V/R, R = V/I).</p>'''


def ohm_faq(lang):
    if lang == 'tr':
        return [
            ('Ohm kanunu formülü nedir?', 'V = I × R. Gerilim (volt) = akım (amper) × direnç (ohm). Buradan I = V / R ve R = V / I elde edilir; güç için P = V × I kullanılır.'),
            ('Ohm kanununda birimler nelerdir?', 'Gerilim volt (V), akım amper (A), direnç ohm (Ω), güç watt (W). mA ve kΩ kullanırken birimleri aynı ölçeğe çevirmeyi unutma: 5 V / 1 kΩ = 5 mA.'),
            ('Ohm kanunu LED\'e uygulanır mı?', 'Doğrudan uygulanmaz; LED\'in gerilimi akımla doğrusal değişmez. LED için seri direnci hesaplamak gerekir; bunun için LED direnci aracını kullanabilirsin.'),
        ]
    return [
        ('What is the Ohm\'s law formula?', 'V = I × R. Voltage (volts) = current (amps) × resistance (ohms). From it, I = V / R and R = V / I; for power use P = V × I.'),
        ('What units does Ohm\'s law use?', 'Volts (V), amps (A), ohms (Ω) and watts (W). When using mA and kΩ, keep the units consistent: 5 V / 1 kΩ = 5 mA.'),
        ('Does Ohm\'s law apply to an LED?', 'Not directly; an LED\'s voltage does not change linearly with current. Calculate a series resistor instead with the LED resistor tool.'),
    ]


# ---------------------------------------------------------------- AWG
def awg_d(n):
    return 0.127 * 92 ** ((36 - n) / 39)


def awg_extra(lang):
    tr = lang == 'tr'
    rows = []
    for n in range(10, 31, 2):
        d = awg_d(n)
        a = math.pi / 4 * d * d
        r = 0.01724 / a  # bakır, 20 °C, Ω/m (ρ = 0,01724 Ω·mm²/m)
        rows.append([f'<b>{n} AWG</b>', f'{num(a, lang, 3)} mm²', f'{num(d, lang, 3)} mm', f'{num(r * 1000, lang, 1)} mΩ/m'])
    head = ('AWG', 'Kesit', 'Çap', 'Direnç (bakır)') if tr else ('AWG', 'Area', 'Diameter', 'Resistance (copper)')
    return (f'<h3>{"AWG – mm² dönüşüm tablosu" if tr else "AWG to mm² conversion table"}</h3>'
            f'<p>{"ASTM B258 formülüyle hesaplanmış tek damarlı bakır tel değerleri (20 °C)." if tr else "Solid copper wire values calculated with the ASTM B258 formula (20 °C)."}</p>'
            + table(head, rows))


def awg_faq(lang):
    a18 = math.pi / 4 * awg_d(18) ** 2
    a22 = math.pi / 4 * awg_d(22) ** 2
    if lang == 'tr':
        return [
            ('18 AWG kaç mm²?', f'18 AWG ≈ {num(a18, "tr", 2)} mm² (çap ≈ {num(awg_d(18), "tr", 2)} mm). Avrupa\'daki en yakın standart kesit 0,75 mm²\'dir.'),
            ('22 AWG kaç mm²?', f'22 AWG ≈ {num(a22, "tr", 2)} mm². Breadboard jumper kabloları genelde 22–24 AWG\'dir.'),
            ('AWG numarası büyüdükçe kablo kalınlaşır mı?', 'Hayır, tersine incelir. Her 6 AWG adımda çap yaklaşık yarıya, her 3 adımda kesit yaklaşık yarıya iner.'),
        ]
    return [
        ('How many mm² is 18 AWG?', f'18 AWG ≈ {num(a18, "en", 2)} mm² (diameter ≈ {num(awg_d(18), "en", 2)} mm). The nearest European size is 0.75 mm².'),
        ('How many mm² is 22 AWG?', f'22 AWG ≈ {num(a22, "en", 2)} mm². Breadboard jumper wires are usually 22–24 AWG.'),
        ('Does a bigger AWG number mean a thicker wire?', 'No, a thinner one. Every 6 AWG steps the diameter roughly halves; every 3 steps the area roughly halves.'),
    ]


# ---------------------------------------------------------------- PCB iz genişliği
def trace_w(i, dt=10, oz=1, k=0.048):
    area = (i / (k * dt ** 0.44)) ** (1 / 0.725)  # mil²
    return area / (1.378 * oz) * 0.0254  # mm


def trace_extra(lang):
    tr = lang == 'tr'
    rows = [[f'<b>{num(i, lang, 1)} A</b>', f'{num(trace_w(i), lang, 2)} mm', f'{num(trace_w(i, oz=2), lang, 2)} mm', f'{num(trace_w(i, k=0.024), lang, 2)} mm']
            for i in (0.5, 1, 2, 3, 5)]
    head = ('Akım', 'Dış katman, 1 oz', 'Dış katman, 2 oz', 'İç katman, 1 oz') if tr else ('Current', 'Outer layer, 1 oz', 'Outer layer, 2 oz', 'Inner layer, 1 oz')
    note = ('IPC-2221, 10 °C sıcaklık artışı için en küçük iz genişliği. Üretimde bir miktar pay bırak.' if tr
            else 'IPC-2221 minimum trace width for a 10 °C temperature rise. Leave some margin for production.')
    return f'<h3>{"Hazır tablo: akıma göre PCB yol genişliği" if tr else "Quick table: PCB trace width by current"}</h3><p>{note}</p>' + table(head, rows)


def trace_faq(lang):
    if lang == 'tr':
        return [
            ('1 amper için PCB yol genişliği kaç mm olmalı?', f'IPC-2221\'e göre dış katmanda 1 oz (35 µm) bakır ve 10 °C artış için en az ≈ {num(trace_w(1), "tr", 2)} mm. Pratikte 0,5 mm ve üstü rahat bir seçimdir.'),
            ('İç katmanlar neden daha geniş yol ister?', 'İç katmandaki iz ısısını havaya veremez; IPC-2221 bu yüzden iç katmanlar için katsayıyı yarıya indirir ve aynı akım için yaklaşık 2,6 kat daha geniş iz çıkar.'),
            ('Yol uzunluğu genişliği etkiler mi?', 'Isınma hesabını değil, gerilim düşümünü etkiler. Uzun güç yollarında düşümü de kontrol et; araç milivolt cinsinden gösterir.'),
        ]
    return [
        ('How wide should a PCB trace be for 1 amp?', f'Per IPC-2221, on an outer layer with 1 oz (35 µm) copper and a 10 °C rise, at least ≈ {num(trace_w(1), "en", 2)} mm. In practice 0.5 mm or more is comfortable.'),
        ('Why do inner layers need wider traces?', 'An inner trace cannot shed heat to the air, so IPC-2221 halves the constant for inner layers, giving roughly 2.6 times the width for the same current.'),
        ('Does trace length affect the width?', 'Not the heating calculation, but the voltage drop. Check the drop on long power traces; the tool shows it in millivolts.'),
    ]


# ---------------------------------------------------------------- kısa SSS'ler
def short_faq(tid, lang):
    tr = lang == 'tr'
    lm317_5 = 1.25 * (1 + 750 / 240) + 50e-6 * 750
    F = {
     'series': [('Paralel direnç nasıl hesaplanır?', '1/R = 1/R1 + 1/R2 + … İki direnç için kısa yol: R = (R1 × R2) / (R1 + R2). 10 kΩ ∥ 10 kΩ = 5 kΩ.'),
                ('Kondansatörler seri bağlanınca ne olur?', 'Toplam kapasite küçülür: 1/C = 1/C1 + 1/C2. Paralel bağlanınca ise toplanır.')],
     'db': [('3 dB ne demek?', 'Gücün yaklaşık iki katı (+3 dB) ya da yarısı (−3 dB). Gerilimde aynı oran 6 dB\'dir.'),
            ('0 dBm kaç watt?', '0 dBm = 1 mW. 10 dBm = 10 mW, 20 dBm = 100 mW, 30 dBm = 1 W.')],
     'regulator': [('LM2596 çıkış gerilimi nasıl hesaplanır?', 'Vout = 1,23 × (1 + R2 / R1). R1 FB ile GND arasına, R2 çıkış ile FB arasına bağlanır; R1 için 240 Ω – 1,5 kΩ önerilir.'),
                   ('LM317 ile 5 V için hangi dirençler kullanılır?', f'R1 = 240 Ω ve R2 = 750 Ω (E24) ile Vout ≈ {num(lm317_5, "tr")} V olur. Daha hassas sonuç için R2\'yi E96\'dan (ör. 715 Ω) seçebilirsin.')],
     'buck': [('Buck dönüştürücüde bobin nasıl seçilir?', 'Bobin dalgalanma akımına göre seçilir; genelde çıkış akımının %20–40\'ı hedeflenir. Bobinin doyma akımı, hesaplanan tepe akımından büyük olmalı.'),
              ('Görev oranı (duty cycle) nedir?', 'Anahtarın açık kaldığı sürenin periyoda oranı: ideal durumda D = Vout / Vin. 12 V → 5 V için ≈ %42.')],
     'battery': [('2000 mAh pil kaç saat dayanır?', 'Ortalama akıma bölünür: 2000 mAh / 20 mA = 100 saat. Pratikte regülatör kaybı ve sıcaklık yüzünden %20–30 pay bırakmak gerekir.'),
                 ('Uyku modu pil ömrünü nasıl uzatır?', 'Ortalama akım, aktif ve uyku akımlarının süreye göre ağırlıklı ortalamasıdır. Cihaz zamanın çoğunu µA seviyesinde uykuda geçirirse pil aylarca dayanabilir.')],
     'rc': [('RC filtre kesim frekansı formülü nedir?', 'fc = 1 / (2π·R·C). 10 kΩ ve 100 nF ile fc ≈ 159 Hz.'),
            ('Zaman sabiti (τ) nedir?', 'τ = R·C. Kondansatör 1τ\'da %63, 5τ\'da yaklaşık %99 dolar.')],
     't555': [('555 astable frekans formülü nedir?', 'f = 1,44 / ((R1 + 2·R2) · C). Görev oranı = (R1 + R2) / (R1 + 2·R2), bu yüzden standart devrede her zaman %50\'nin üstündedir.'),
              ('555 monostable süresi nasıl hesaplanır?', 't = 1,1 · R · C. 100 kΩ ve 10 µF ile yaklaşık 1,1 saniye.')],
    }
    E = {
     'series': [('How do you calculate parallel resistors?', '1/R = 1/R1 + 1/R2 + … For two resistors: R = (R1 × R2) / (R1 + R2). 10 kΩ ∥ 10 kΩ = 5 kΩ.'),
                ('What happens to capacitors in series?', 'The total gets smaller: 1/C = 1/C1 + 1/C2. In parallel they add up.')],
     'db': [('What does 3 dB mean?', 'About double (+3 dB) or half (−3 dB) the power. For voltage the same ratio is 6 dB.'),
            ('How many watts is 0 dBm?', '0 dBm = 1 mW. 10 dBm = 10 mW, 20 dBm = 100 mW, 30 dBm = 1 W.')],
     'regulator': [('How do you calculate the LM2596 output voltage?', 'Vout = 1.23 × (1 + R2 / R1). R1 goes from FB to GND, R2 from the output to FB; 240 Ω – 1.5 kΩ is recommended for R1.'),
                   ('Which resistors give 5 V with an LM317?', f'R1 = 240 Ω and R2 = 750 Ω (E24) give Vout ≈ {num(lm317_5, "en")} V. For a closer result pick R2 from E96 (e.g. 715 Ω).')],
     'buck': [('How do you choose the inductor for a buck converter?', 'By ripple current; 20–40% of the output current is a common target. Its saturation current must exceed the calculated peak current.'),
              ('What is the duty cycle?', 'The fraction of each period the switch is on: ideally D = Vout / Vin. For 12 V → 5 V, ≈ 42%.')],
     'battery': [('How long does a 2000 mAh battery last?', 'Divide by the average current: 2000 mAh / 20 mA = 100 hours. Leave 20–30% margin for regulator losses and temperature.'),
                 ('How does sleep mode extend battery life?', 'The average current is the time-weighted mix of active and sleep current. If the device sleeps at µA levels most of the time, the battery can last months.')],
     'rc': [('What is the RC filter cut-off formula?', 'fc = 1 / (2π·R·C). With 10 kΩ and 100 nF, fc ≈ 159 Hz.'),
            ('What is the time constant (τ)?', 'τ = R·C. A capacitor charges to 63% in 1τ and about 99% in 5τ.')],
     't555': [('What is the 555 astable frequency formula?', 'f = 1.44 / ((R1 + 2·R2) · C). Duty cycle = (R1 + R2) / (R1 + 2·R2), so in the standard circuit it is always above 50%.'),
              ('How do you calculate the 555 monostable time?', 't = 1.1 · R · C. With 100 kΩ and 10 µF, about 1.1 seconds.')],
    }
    return (F if tr else E).get(tid, [])


# ---------------------------------------------------------------- başlıklar ve açıklamalar
SEO = {
 'color': dict(tr=('Direnç Renk Kodu Hesaplama ve Tablosu (4, 5, 6 Bant)',
                   'Direnç renk kodu hesaplama: renkleri seç, değeri gör ya da değeri yaz, renkleri bul. 4, 5, 6 bant, renk tablosu ve 10k, 220 Ω, 1k, 4,7k gibi sık değerlerin renkleri.'),
               en=('Resistor Color Code Calculator and Chart (4, 5, 6 Band)',
                   'Resistor color code calculator: pick colours to get the value or type a value to get the colours. 4, 5 and 6 bands, colour chart and colours of common values like 10k, 220 Ω and 1k.')),
 'led': dict(tr=('LED Direnci Hesaplama (5V, 12V, 3,3V) — Hangi Direnç?',
                 'LED direnci hesaplama: besleme gerilimi ve LED rengine göre gereken direnç, standart değer ve güç. 5 V, 12 V ve 3,3 V için hazır tablo.'),
             en=('LED Resistor Calculator (5V, 12V, 3.3V) — Which Resistor?',
                 'LED resistor calculator: the resistor you need from the supply voltage and LED colour, with a standard value and power rating. Ready table for 5 V, 12 V and 3.3 V.')),
 'ohm': dict(tr=('Ohm Kanunu Hesaplama: Gerilim, Akım, Direnç ve Güç',
                 'Ohm kanunu hesaplama: V = I·R. Gerilim, akım, direnç ve güçten ikisini gir, diğerlerini bul. Çözümlü örnekler ve formüller.'),
             en=('Ohm\'s Law Calculator: Voltage, Current, Resistance and Power', None)),
 'smd': dict(tr=('SMD Direnç Kodu ve Kondansatör Kodu Çözücü (103, 104, 4R7)',
                 'SMD direnç kodu çözücü: 103, 472, 1002, 4R7, 01C gibi kodları değere çevir. 104 kondansatör kaç nF? Sık kodlar tablosu.'),
             en=('SMD Resistor Code and Capacitor Code Calculator (103, 104, 4R7)', None)),
 'divider': dict(tr=('Gerilim Bölücü Hesaplama: 5V → 3,3V, 12V → 5V Direnç Seçimi',
                     'Gerilim bölücü hesaplama: Vout = Vin·R2/(R1+R2). Hedef gerilim için direnç bul, E24/E96 standart değer öner. 5 V → 3,3 V ve 12 V → 5 V için hazır tablo.'),
                 en=('Voltage Divider Calculator: 5V to 3.3V, 12V to 5V Resistors', None)),
 'series': dict(tr=('Seri ve Paralel Direnç Hesaplama (Kondansatör, Bobin)', None),
                en=('Series and Parallel Resistor Calculator (Capacitor, Inductor)', None)),
 'trace': dict(tr=('PCB Yol (İz) Genişliği Hesaplama — IPC-2221 Tablosu',
                   'PCB yol genişliği hesaplama: akıma ve bakır kalınlığına göre en küçük iz genişliği, direnç ve gerilim düşümü. IPC-2221 formülü ve 0,5–5 A için hazır tablo.'),
               en=('PCB Trace Width Calculator — IPC-2221 Table', None)),
 'awg': dict(tr=('AWG mm² Dönüşüm Tablosu ve Kablo Kesiti Hesaplama',
                 'AWG mm² çevirme: 10–30 AWG kesit, çap ve metre başına direnç tablosu. 18 AWG kaç mm²? Hesaplayıcı ve ASTM B258 formülü.'),
             en=('AWG to mm² Conversion Chart and Wire Gauge Calculator', None)),
 'regulator': dict(tr=('LM2596 / LM317 Çıkış Gerilimi ve Direnç Hesaplama', None),
                   en=('LM2596 / LM317 Output Voltage and Resistor Calculator', None)),
 'buck': dict(tr=('Buck Dönüştürücü Hesaplama: Bobin ve Kondansatör Seçimi', None),
              en=('Buck Converter Calculator: Inductor and Capacitor Selection', None)),
 'battery': dict(tr=('Pil Ömrü Hesaplama (mAh, Uyku Modu, ESP32)', None),
                 en=('Battery Life Calculator (mAh, Sleep Mode, ESP32)', None)),
 'rc': dict(tr=('RC Filtre Kesim Frekansı ve Zaman Sabiti Hesaplama', None),
            en=('RC Filter Cut-off Frequency and Time Constant Calculator', None)),
 't555': dict(tr=('555 Zamanlayıcı Hesaplama: Astable Frekans ve Monostable Süre', None),
              en=('555 Timer Calculator: Astable Frequency and Monostable Time', None)),
 'db': dict(tr=('Desibel Hesaplama: dB, dBm ↔ Watt Dönüşümü', None),
            en=('Decibel Calculator: dB and dBm to Watt Conversion', None)),
}

EXTRA = {'color': color_extra, 'led': led_extra, 'smd': smd_extra, 'divider': div_extra, 'ohm': ohm_extra, 'awg': awg_extra, 'trace': trace_extra}
FAQ = {'color': color_faq, 'led': led_faq, 'smd': smd_faq, 'divider': div_faq, 'ohm': ohm_faq, 'awg': awg_faq, 'trace': trace_faq}


def page_title(tid, lang, fallback):
    t = SEO.get(tid, {}).get(lang, (None, None))[0] or fallback
    return t if len(t) > 50 else f'{t} — Ahmet Ulu'


def page_desc(tid, lang, fallback):
    return SEO.get(tid, {}).get(lang, (None, None))[1] or fallback


def extra(tid, lang):
    f = EXTRA.get(tid)
    return f(lang) if f else ''


def faq(tid, lang):
    f = FAQ.get(tid)
    return f(lang) if f else short_faq(tid, lang)


if __name__ == '__main__':  # hızlı kontrol
    for v in (10, 220, 1e3, 4.7e3, 10e3, 1e6):
        print(ohm(v, 'tr'), color_words(v, 4, 'tr'), '|', color_words(v, 5, 'tr'))
    for vs in LED_VS:
        print(vs, [ohm(led_r(vs, vf), 'tr') for _, _, vf in LED_VF])
    print([div_pair(a, b) for a, b in DIV_CASES])
    print('1A', trace_w(1), 'awg18', math.pi / 4 * awg_d(18) ** 2)
    for t in SEO:
        for l in ('tr', 'en'):
            print(len(page_title(t, l, 'x')), page_title(t, l, 'x'))
