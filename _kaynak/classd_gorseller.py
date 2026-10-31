# -*- coding: utf-8 -*-
"""Class D amplifikatör yazısının gövdesi ve çizimleri.
`python3 _kaynak/classd_gorseller.py` → _kaynak/yazilar/class-d.{tr,en}.html
Frekans cevabı ideal hesaptır (hoparlör saf direnç kabul edilir)."""
import os, math, cmath

L = 22e-6      # her çıkış hattındaki bobin
C = 220e-9     # filtrelenmiş çıkışlar arasındaki kondansatör
F0 = 1 / (2 * math.pi * math.sqrt(2 * L * C))  # diferansiyel: 2L ile C (≈ 51,2 kHz)


def h_db(f, r_load):
    """Diferansiyel LC'nin yarım devresi: L, 2C, R/2."""
    w = 2 * math.pi * f
    h = 1 / (1 - w * w * L * 2 * C + 1j * w * L / (r_load / 2))
    return 20 * math.log10(abs(h))


def q(r_load):
    return (r_load / 2) * math.sqrt(2 * C / L)


def num(x, lang, nd=1):
    s = f'{x:.{nd}f}'
    return s.replace('.', ',') if lang == 'tr' else s


def filter_svg(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    coil = lambda x, y: ''.join(f'<path d="M{x + i * 14} {y} a7 7 0 0 1 14 0" class="w"/>' for i in range(4))
    return f'''<svg class="cd-sch" viewBox="0 0 660 250" role="img" aria-label="{T('Diferansiyel LC çıkış filtresi şeması', 'Differential LC output filter schematic')}">
  <rect x="20" y="40" width="120" height="170" rx="10" class="ic"/><text x="80" y="118" text-anchor="middle" class="ict">MAX98357A</text><text x="80" y="138" text-anchor="middle" class="ics">Class D · BTL</text>
  <text x="150" y="70" class="pin">OUTP</text><text x="150" y="190" class="pin">OUTN</text>
  <path d="M140 80 H222" class="w"/>{coil(222, 80)}<path d="M278 80 H470" class="w"/>
  <path d="M140 200 H222" class="w"/>{coil(222, 200)}<path d="M278 200 H470" class="w"/>
  <text x="250" y="60" text-anchor="middle" class="lbl">L1 · 22 µH</text><text x="250" y="230" text-anchor="middle" class="lbl">L2 · 22 µH</text>
  <circle cx="360" cy="80" r="4" class="dot"/><circle cx="360" cy="200" r="4" class="dot"/>
  <path d="M360 80 V132 M342 132 H378 M342 146 H378 M360 146 V200" class="w"/>
  <text x="372" y="144" class="lbl">C4 · 220 nF</text>
  <rect x="470" y="98" width="34" height="84" rx="4" class="spk"/><path d="M504 98 L548 64 V216 L504 182 Z" class="spk"/>
  <path d="M470 80 V98 M470 200 V182" class="w"/>
  <text x="562" y="134" class="lbl">{T('Hoparlör', 'Speaker')}</text><text x="562" y="154" class="sub">J3</text>
  <text x="182" y="100" class="tp">TP4</text><text x="182" y="222" class="tp">TP5</text><text x="300" y="100" class="tp ok">TP6</text><text x="300" y="222" class="tp ok">TP7</text>
</svg>'''


def bode_svg(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    x0, x1, y0, y1 = 70, 610, 30, 250       # çizim alanı
    fmin, fmax, dbmin, dbmax = 1e3, 1e6, -60, 10
    X = lambda f: x0 + (math.log10(f) - math.log10(fmin)) / (math.log10(fmax) - math.log10(fmin)) * (x1 - x0)
    Y = lambda d: y0 + (dbmax - max(dbmin, min(dbmax, d))) / (dbmax - dbmin) * (y1 - y0)
    def curve(r):
        pts = []
        for i in range(0, 241):
            f = 10 ** (3 + 3 * i / 240)
            pts.append(f'{X(f):.1f},{Y(h_db(f, r)):.1f}')
        return 'M' + ' L'.join(pts)
    grid = ''
    for f in (1e3, 1e4, 1e5, 1e6):
        grid += f'<path d="M{X(f):.1f} {y0}V{y1}" class="g"/><text x="{X(f):.1f}" y="{y1 + 18}" text-anchor="middle" class="ax">{'1 MHz' if f >= 1e6 else str(int(f / 1000)) + ' kHz'}</text>'
    for d in (0, -20, -40, -60):
        grid += f'<path d="M{x0} {Y(d):.1f}H{x1}" class="g"/><text x="{x0 - 8}" y="{Y(d) + 4:.1f}" text-anchor="end" class="ax">{d} dB</text>'
    band = f'<rect x="{X(20):.1f}" y="{y0}" width="{X(20e3) - X(fmin):.1f}" height="{y1 - y0}" class="band"/>'
    band = f'<rect x="{x0}" y="{y0}" width="{X(20e3) - x0:.1f}" height="{y1 - y0}" class="band"/><text x="{(x0 + X(20e3)) / 2:.1f}" y="{y0 + 16}" text-anchor="middle" class="bt">{T("ses bandı", "audio band")}</text>'
    f0x = X(F0)
    return f'''<svg class="cd-bode" viewBox="0 0 640 290" role="img" aria-label="{T('LC filtrenin hesaplanan frekans cevabı, 8 ve 4 ohm yük', 'Calculated frequency response of the LC filter, 8 and 4 ohm loads')}">
  {band}{grid}
  <path d="M{f0x:.1f} {y0}V{y1}" class="f0"/><text x="{f0x + 6:.1f}" y="{y1 - 8}" class="f0t">f₀ ≈ {num(F0 / 1000, lang)} kHz</text>
  <path d="{curve(8)}" class="c8"/><path d="{curve(4)}" class="c4"/>
  <g class="leg"><path d="M430 52 H456" class="c8"/><text x="462" y="56">8 Ω {T('hoparlör', 'speaker')}</text><path d="M430 72 H456" class="c4"/><text x="462" y="76">4 Ω {T('hoparlör', 'speaker')}</text></g>
</svg>'''


def dv(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    return f'''  <div class="dv">
    <div class="dv-head">
      <div class="dv-title">{T('Class D amplifikatör kartı', 'Class D amplifier board')}</div>
      <div class="dv-tabs" role="tablist" aria-label="{T('Görünüm', 'View')}">
        <button class="dv-tab" role="tab" id="cd-t1" aria-controls="cd-p1" aria-selected="true">PCB</button>
        <button class="dv-tab" role="tab" id="cd-t2" aria-controls="cd-p2" aria-selected="false" tabindex="-1">3D</button>
      </div>
    </div>
    <div class="dv-panel" role="tabpanel" id="cd-p1" aria-labelledby="cd-t1">
      <img src="pcb-yerlesim.jpg" class="blog-img" alt="{T('KiCad PCB yerleşimi: MAX98357A, iki 22 µH bobin, test noktaları ve klemensler', 'KiCad PCB layout: MAX98357A, two 22 µH inductors, test points and terminal blocks')}" width="1400" height="1007" loading="eager" decoding="async">
      <figcaption>{T('İki katmanlı yerleşim: ortada MAX98357A, üstte ve altta 22 µH bobinler, sağda hoparlör (J3) ve 5 V (J1) klemensleri, solda I²S bağlantısı (J2)', 'Two-layer layout: MAX98357A in the middle, 22 µH inductors above and below, speaker (J3) and 5 V (J1) terminals on the right, I²S header (J2) on the left')}</figcaption>
    </div>
    <div class="dv-panel" role="tabpanel" id="cd-p2" aria-labelledby="cd-t2" hidden>
      <img src="3d-gorunum.jpg" class="blog-img" alt="{T('Kartın KiCad 3D görünümü', 'KiCad 3D view of the board')}" width="1200" height="1013" loading="lazy" decoding="async">
      <figcaption>{T('KiCad 3D görünümü: mavi test noktaları filtre öncesi ve sonrası sinyallere erişim sağlıyor', 'KiCad 3D view: the blue test points give access to the signals before and after the filter')}</figcaption>
    </div>
  </div>'''


def body(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    q8, q4 = q(8), q(4)
    d20_8, d20_4 = h_db(20e3, 8), h_db(20e3, 4)
    d500 = h_db(500e3, 8)
    li = 'https://www.linkedin.com/posts/ahmet-ulu-16099832b_pcbdesign-kicad-classdamplifier-ugcPost-7522386923663810562-1I9a/'
    return f'''  <div class="blog-tag">{T('PCB Tasarımı · Ses elektroniği', 'PCB Design · Audio electronics')}</div>
  <h1>{T('Class D Amplifikatörde EMI ve LC Çıkış Filtresi: MAX98357A ile PCB Tasarımım', 'EMI in Class D Amplifiers and an LC Output Filter: My MAX98357A PCB Design')}</h1>
  <div class="blog-meta">Ahmet Ulu · {T('Ekim 2026', 'October 2026')}</div>

  <p>{T('Class D ses amplifikatörleri çok verimli ama bu verimin bir bedeli var: çıkışta sesin yanında yüksek frekanslı anahtarlama bileşenleri de bulunuyor. Bu projede bu sorunu inceledim ve KiCad\'de, <strong>MAX98357A</strong> I²S Class D amplifikatör entegresini ve bir <strong>diferansiyel LC çıkış filtresini</strong> içeren 2 katmanlı bir PCB tasarladım.',
     'Class D audio amplifiers are very efficient, but that efficiency has a price: the output carries high-frequency switching components along with the audio. In this project I looked into that problem and designed a 2-layer PCB in KiCad with the <strong>MAX98357A</strong> I²S Class D amplifier IC and a <strong>differential LC output filter</strong>.')}</p>

{dv(lang)}

  <h3>{T('Problem: anahtarlama gürültüsü ve uzun kablolar', 'The problem: switching noise and long cables')}</h3>
  <p>{T('Class D amplifikatör, çıkış transistörlerini ses bandının çok üzerindeki bir frekansta açıp kapatır; ses bilgisi bu darbelerin genişliğinde taşınır. Hoparlör yüksek frekansları zaten duyurmaz, ama bu bileşenler <strong>hoparlör kablolarında</strong> dolaşmaya devam eder. Kablo uzadıkça bir anten gibi davranır ve yüksek frekanslı enerjiyi çevreye yayabilir; bu da yakındaki elektronik sistemlerde <strong>elektromanyetik girişime (EMI)</strong> yol açabilir.',
     'A Class D amplifier switches its output transistors on and off at a frequency far above the audio band; the audio is carried in the width of those pulses. The speaker does not reproduce the high frequencies anyway, but they keep travelling along the <strong>speaker cables</strong>. The longer the cable, the more it behaves like an antenna and radiates that energy, which can cause <strong>electromagnetic interference (EMI)</strong> in nearby electronics.')}</p>
  <p>{T('MAX98357A, kenar hızı kontrolü sayesinde kısa kablolarda filtresiz çalışacak şekilde tasarlanmış bir entegre. Benim merak ettiğim, kablo uzadığında bir çıkış filtresinin ne kadar fark yaratacağıydı. Bu yüzden kartı filtreli tasarladım ve filtrenin her iki tarafına ölçüm noktaları koydum.',
     'The MAX98357A is designed to run filterless with short cables, thanks to its edge-rate control. What I wanted to find out was how much difference an output filter makes once the cable gets longer. So I designed the board with a filter and put measurement points on both sides of it.')}</p>

  <h3>{T('Çözüm: diferansiyel LC filtre', 'The fix: a differential LC filter')}</h3>
  <p>{T('MAX98357A\'nın çıkışı <strong>BTL (köprü)</strong> yapısında: hoparlör iki çıkış arasına bağlanıyor, ikisi de anahtarlanıyor. Bu yüzden filtreyi de simetrik kurdum: her çıkış hattına bir <strong>22 µH</strong> bobin, filtrelenmiş iki çıkış arasına bir <strong>220 nF</strong> kondansatör.',
     'The MAX98357A output is <strong>BTL (bridge-tied load)</strong>: the speaker sits between two outputs and both of them switch. So I built the filter symmetrically too: a <strong>22 µH</strong> inductor in each output line and a <strong>220 nF</strong> capacitor between the two filtered outputs.')}</p>
  <figure class="stm-fig"><div class="wave-scroll">{filter_svg(lang)}</div><figcaption>{T('Filtre öncesi: TP4 (OUT_P) ve TP5 (OUT_N). Filtre sonrası, hoparlör tarafı: TP6 ve TP7.', 'Before the filter: TP4 (OUT_P) and TP5 (OUT_N). After the filter, speaker side: TP6 and TP7.')}</figcaption></figure>

  <h3>{T('Hesap: kesim frekansı', 'The maths: cut-off frequency')}</h3>
  <p>{T('Diferansiyel sinyal açısından akım iki bobinden de geçer, yani kondansatör toplam <strong>2 × 22 = 44 µH</strong> ile birlikte çalışır:',
     'For the differential signal the current flows through both inductors, so the capacitor works against a total of <strong>2 × 22 = 44 µH</strong>:')}</p>
  <div class="formula"><span>f₀ = 1 / (2π · √(L<sub>{T('toplam', 'total')}</sub> · C))</span><span>f₀ = 1 / (2π · √(44 µH · 220 nF)) ≈ <b>{num(F0 / 1000, lang)} kHz</b></span></div>
  <p>{T(f'Bu, 20 kHz\'lik ses bandının üzerinde, anahtarlama frekansının ise çok altında. İkinci dereceden bir filtre olduğu için f₀\'ın üzerinde zayıflatma <strong>on katta 40 dB</strong> artıyor: ideal hesapta 500 kHz\'de sinyal yaklaşık <strong>{num(d500, lang, 0)} dB</strong>, yani gerilim olarak yaklaşık 100\'de 1\'ine iniyor.',
     f'That is above the 20 kHz audio band and well below the switching frequency. Being a second-order filter, attenuation above f₀ grows by <strong>40 dB per decade</strong>: in the ideal calculation the signal at 500 kHz is about <strong>{num(d500, lang, 0)} dB</strong>, roughly 1/100 in voltage.')}</p>
  <figure class="stm-fig wide"><div class="wave-scroll">{bode_svg(lang)}</div><figcaption>{T('Hesaplanan frekans cevabı (hoparlör saf direnç kabul edildi). Mavi alan ses bandı, kesikli çizgi f₀.', 'Calculated frequency response (speaker treated as a pure resistor). The shaded area is the audio band, the dashed line is f₀.')}</figcaption></figure>
  <p>{T(f'Grafikte gözüme çarpan bir nokta oldu: filtrenin sönümü <strong>hoparlör empedansına</strong> bağlı. 8 Ω hoparlörde Q ≈ {num(q8, lang, 2)} ve 20 kHz\'deki düşüş yaklaşık {num(-d20_8, lang)} dB; 4 Ω hoparlörde ise Q ≈ {num(q4, lang, 2)} ve 20 kHz\'de yaklaşık {num(-d20_4, lang)} dB düşüş görünüyor. Gerçek bir hoparlörün empedansı frekansla değiştiği için bu hesabı LTspice\'ta ve ölçümle doğrulamak bir sonraki adımım.',
     f'One thing stood out in the plot: the damping of the filter depends on the <strong>speaker impedance</strong>. With an 8 Ω speaker Q ≈ {num(q8, lang, 2)} and the drop at 20 kHz is about {num(-d20_8, lang)} dB; with a 4 Ω speaker Q ≈ {num(q4, lang, 2)} and the drop at 20 kHz is about {num(-d20_4, lang)} dB. A real speaker\'s impedance changes with frequency, so checking this in LTspice and on the bench is my next step.')}</p>

  <h3>{T('PCB tasarımında EMI için yaptıklarım', 'What I did on the PCB for EMI')}</h3>
  <ul>
    <li>{T('<strong>Kısa yüksek akım yolları:</strong> bobinleri entegrenin çıkış pinlerine yakın yerleştirdim; anahtarlanan akımın dolaştığı alanı küçük tutmak yayılan gürültüyü azaltıyor.', '<strong>Short high-current paths:</strong> I placed the inductors close to the IC outputs; keeping the switched-current loop small reduces radiated noise.')}</li>
    <li>{T('<strong>GND düzlemleri ve stitching via\'lar:</strong> iki katmanda da toprak dökümü var; katmanları çok sayıda via ile birbirine bağlayarak dönüş akımları için kısa ve düşük empedanslı bir yol sağladım.', '<strong>GND planes and stitching vias:</strong> both layers carry a ground pour, tied together with many vias to give return currents a short, low-impedance path.')}</li>
    <li>{T('<strong>Dekuplaj:</strong> 100 nF ve 10 µF kondansatörler entegrenin besleme pinine yakın.', '<strong>Decoupling:</strong> the 100 nF and 10 µF capacitors sit right next to the IC supply pin.')}</li>
    <li>{T('<strong>Simetri:</strong> OUT_P ve OUT_N hatlarını ve iki bobini birbirine benzer şekilde yönlendirdim.', '<strong>Symmetry:</strong> I routed OUT_P and OUT_N and the two inductors as similarly as possible.')}</li>
    <li>{T('<strong>Ölçülebilirlik:</strong> filtre öncesi (TP4, TP5) ve sonrası (TP6, TP7) çıkışlar, 5 V (TP1), GND (TP2) ve SD_MODE (TP3) için test noktaları ekledim.', '<strong>Measurability:</strong> test points for the outputs before (TP4, TP5) and after (TP6, TP7) the filter, 5 V (TP1), GND (TP2) and SD_MODE (TP3).')}</li>
  </ul>
  <p>{T('Hazır bir amplifikatör modülü kullanmak yerine entegreyi doğrudan karta yerleştirdim; böylece filtrenin ve yerleşimin her detayını kendim seçebildim.', 'Instead of using a ready-made amplifier module, I put the IC directly on the board, so I could choose every detail of the filter and the layout myself.')}</p>

  <div class="tech-box">
    <h4>{T('Teknik detaylar', 'Technical details')}</h4>
    <div class="tech-row"><span class="comp">{T('Entegre', 'IC')}</span><span class="detail">MAX98357A · I²S Class D, 5 V {T('ile 4 Ω\'a 3,2 W\'a kadar', 'up to 3.2 W into 4 Ω')}</span></div>
    <div class="tech-row"><span class="comp">{T('Çıkış filtresi', 'Output filter')}</span><span class="detail">2 × 22 µH + 220 nF · f₀ ≈ {num(F0 / 1000, lang)} kHz</span></div>
    <div class="tech-row"><span class="comp">{T('Bağlantılar', 'Connectors')}</span><span class="detail">{T('J2: 7 pin I²S + SD_CTRL · J1: 5 V klemens · J3: hoparlör klemensi', 'J2: 7-pin I²S + SD_CTRL · J1: 5 V terminal · J3: speaker terminal')}</span></div>
    <div class="tech-row"><span class="comp">PCB</span><span class="detail">{T('2 katman, GND düzlemleri, 4 × M2 montaj deliği', '2 layers, GND planes, 4 × M2 mounting holes')}</span></div>
    <div class="tech-row"><span class="comp">{T('Araç', 'Tool')}</span><span class="detail">KiCad</span></div>
  </div>

  <h3>{T('Sonraki adım', 'Next step')}</h3>
  <p>{T('Tasarım aşaması tamamlandı. Sırada filtreyi <strong>LTspice</strong>\'ta farklı hoparlör yükleriyle simüle etmek, sonra kartı üretip osiloskopla filtre öncesi ve sonrası sinyalleri ölçmek var. Farklı kablo uzunluklarında filtreli ve filtresiz durumu karşılaştırıp sonuçları burada paylaşacağım.',
     'The design stage is done. Next I will simulate the filter in <strong>LTspice</strong> with different speaker loads, then build the board and measure the signals before and after the filter on an oscilloscope. I will compare the filtered and unfiltered cases with different cable lengths and share the results here.')}</p>
  <p>{T(f'Projeyi <a href="{li}" target="_blank" rel="noopener">LinkedIn\'de de paylaştım</a>. Benzer bir kart ya da özel bir PCB tasarımı için <a href="../../pcb-tasarim-hizmeti.html">PCB tasarım hizmeti</a> sayfama göz atabilirsin.',
     f'I also shared the project <a href="{li}" target="_blank" rel="noopener">on LinkedIn</a>. For a similar board or a custom PCB, have a look at my <a href="../pcb-design-service.html">PCB design service</a> page.')}</p>

  <h3>{T('Kaynaklar', 'References')}</h3>
  <ul>
    <li><a href="https://www.analog.com/en/products/max98357a.html" target="_blank" rel="noopener">Analog Devices — MAX98357A {T('ürün sayfası ve datasheet', 'product page and datasheet')}</a></li>
    <li><a href="https://www.ti.com/lit/pdf/sloa119" target="_blank" rel="noopener">Texas Instruments — SLOA119: Class-D LC Filter Design</a></li>
  </ul>'''


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    for lang in ('tr', 'en'):
        p = os.path.join(here, 'yazilar', f'class-d.{lang}.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(body(lang) + '\n')
        print('yazıldı:', p)
    print('f0', F0, 'Q8', q(8), 'Q4', q(4), '20k', h_db(20e3, 8), h_db(20e3, 4), '500k', h_db(500e3, 8))
