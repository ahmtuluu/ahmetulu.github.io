# -*- coding: utf-8 -*-
"""STM32 serisi yazıları için ortak çizimler (SVG/HTML). Yazı gövdeleri bu dosyadaki
fonksiyonlarla üretilir: `python3 _kaynak/stm32_gorseller.py` → _kaynak/yazilar/stm32-01-buton.{tr,en}.html"""
import os

LED = {12: ('#22c55e', 'yeşil', 'green'), 13: ('#f59e0b', 'turuncu', 'orange'), 14: ('#ef4444', 'kırmızı', 'red'), 15: ('#3b82f6', 'mavi', 'blue')}
POS = {13: (150, 46), 12: (62, 124), 14: (238, 124), 15: (150, 202)}


def board_svg(active, lang, caption_id):
    """STM32F407 Discovery'deki 4 LED'in yerleşimi; `active` yanan pinler."""
    tr = lang == 'tr'
    leds = ''
    for pin, (x, y) in POS.items():
        col, ntr, nen = LED[pin]
        on = pin in active
        lab = f'PD{pin}'
        name = ntr if tr else nen
        tx = {12: (x - 30, y + 4, 'end'), 14: (x + 30, y + 4, 'start'), 13: (x + 24, y - 4, 'start'), 15: (x + 24, y + 12, 'start')}[pin]
        leds += (f'<g class="led{" on" if on else ""}" style="--c:{col}">'
                 f'<circle cx="{x}" cy="{y}" r="22" class="halo"/><rect x="{x - 11}" y="{y - 7}" width="22" height="14" rx="3" class="body"/>'
                 f'<text x="{tx[0]}" y="{tx[1]}" text-anchor="{tx[2]}" class="lbl"><tspan class="pin">{lab}</tspan> {name}</text></g>')
    return (f'<svg class="stm-board" viewBox="-40 0 380 250" role="img" aria-labelledby="{caption_id}">'
            f'<rect x="20" y="8" width="260" height="234" rx="16" class="pcb"/>'
            f'<rect x="112" y="88" width="76" height="72" rx="6" class="chip"/><text x="150" y="121" text-anchor="middle" class="chip-t">STM32</text>'
            f'<text x="150" y="137" text-anchor="middle" class="chip-s">F407VG</text>{leds}'
            f'<g class="btn-g"><circle cx="58" cy="210" r="14" class="btn"/><text x="58" y="240" text-anchor="middle" class="lbl">B1 · PA0</text></g></svg>')


def bounce_svg(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    real = 'M70 228 H230 V168 H238 V228 H246 V168 H260 V228 H266 V168 H284 V212 H290 V168 H620'
    grid = ''.join(f'<path d="M{x} 20V300" class="g"/>' for x in range(70, 621, 40))
    marks = ''.join(f'<circle cx="{x}" cy="262" r="5" class="bad"/>' for x in (230, 246, 266, 290))
    return f'''<svg class="stm-wave" viewBox="0 0 630 320" role="img" aria-label="{T('Butona basıldığında ideal ve gerçek sinyal; kontak sıçraması ve debounce bekleme süresi', 'Ideal and real signal when the button is pressed; contact bounce and the debounce wait')}">
  {grid}
  <rect x="230" y="150" width="62" height="92" rx="4" class="zone"/>
  <text x="261" y="142" text-anchor="middle" class="zt">{T('sıçrama', 'bounce')}</text>
  <text x="14" y="44" class="ch">{T('İdeal', 'Ideal')}</text><text x="14" y="62" class="sub">3,3 V / 0 V</text>
  <path d="M70 100 H230 V40 H620" class="ideal"/>
  <text x="14" y="184" class="ch">{T('Gerçek', 'Real')}</text><text x="14" y="202" class="sub">{T('PA0 pini', 'PA0 pin')}</text>
  <path d="{real}" class="real"/>
  <text x="14" y="266" class="ch">{T('Kod', 'Code')}</text>
  {marks}<text x="304" y="267" class="bad-t">{T('debounce olmadan: 4 basış sayılır', 'without debounce: 4 presses counted')}</text>
  <path d="M230 290 H420" class="win"/><path d="M230 284v12M420 284v12" class="win"/>
  <circle cx="230" cy="290" r="5" class="ok"/><circle cx="420" cy="290" r="7" class="ok"/>
  <text x="325" y="310" text-anchor="middle" class="ok-t">delay(DEBOUNCE)</text>
  <text x="434" y="295" class="ok-t">{T('hâlâ 1 → tek basış ✓', 'still 1 → one press ✓')}</text>
  <text x="240" y="66" class="sub">← {T('butona basıldı', 'button pressed')}</text>
</svg>'''


def moder_html(lang):
    tr = lang == 'tr'
    cells = ''
    for pin in (15, 14, 13, 12):
        col = LED[pin][0]
        cells += (f'<div class="rg-field" style="--c:{col}"><div class="rg-name">MODER{pin}</div>'
                  f'<div class="rg-bits"><span>0</span><span class="one">1</span></div><div class="rg-idx">{pin * 2 + 1}:{pin * 2}</div></div>')
    legend = ('<b>00</b> giriş · <b>01</b> çıkış · <b>10</b> alternatif fonksiyon · <b>11</b> analog' if tr
              else '<b>00</b> input · <b>01</b> output · <b>10</b> alternate function · <b>11</b> analog')
    return (f'<figure class="stm-fig"><div class="rg">{cells}<div class="rg-more">… MODER11 – MODER0</div></div>'
            f'<figcaption>{"GPIOD_MODER: her pin için 2 bit. PD12–15 için “01” = çıkış." if tr else "GPIOD_MODER: 2 bits per pin. “01” on PD12–15 = output."}<br>{legend}</figcaption></figure>')


def bsrr_html(lang):
    tr = lang == 'tr'
    def row(kind, active):
        cells = ''
        for b in range(15, -1, -1):
            pin = b
            act = pin in active
            st = f' style="--c:{LED[pin][0]}"' if act else ''
            num = b + 16 if kind == 'BR' else b
            cells += f'<span class="bs{" act" if act else ""}"{st} title="{kind}{b} (bit {num})">{b}</span>'
        name = ('BR — söndür (bit 31–16)' if tr else 'BR — reset (bits 31–16)') if kind == 'BR' else ('BS — yak (bit 15–0)' if tr else 'BS — set (bits 15–0)')
        return f'<div class="bs-row"><div class="bs-name">{name}</div><div class="bs-cells">{cells}</div></div>'
    cap = ('<code>GPIOD-&gt;BSRR = CROSS_B | (CROSS_A &lt;&lt; 16);</code> tek yazmada turuncu ve maviyi (BS13, BS15) yakar, yeşil ve kırmızıyı (BR12, BR14) söndürür. 0 yazılan bitler hiçbir pini değiştirmez.'
           if tr else '<code>GPIOD-&gt;BSRR = CROSS_B | (CROSS_A &lt;&lt; 16);</code> turns orange and blue on (BS13, BS15) and green and red off (BR12, BR14) in a single write. Bits written as 0 leave their pins alone.')
    return f'<figure class="stm-fig"><div class="bsrr">{row("BR", {12, 14})}{row("BS", {13, 15})}</div><figcaption>{cap}</figcaption></figure>'


def flow_html(lang):
    tr = lang == 'tr'
    steps = [('1', 'IDR & BTN', 'Pin 1 mi? Basılmış olabilir.', 'Is the pin 1? It might be a press.'),
             ('2', 'delay(DEBOUNCE)', 'Sıçramalar bitsin diye bekle.', 'Wait for the bouncing to end.'),
             ('3', 'IDR & BTN', 'Hâlâ 1 mi? → Gerçek basış: LED\'leri değiştir, count++', 'Still 1? → Real press: swap LEDs, count++'),
             ('4', 'while (IDR & BTN);', 'Buton bırakılana kadar bekle.', 'Wait until the button is released.'),
             ('5', 'delay(DEBOUNCE)', 'Bırakırken oluşan sıçramayı da atla.', 'Skip the bounce on release too.')]
    items = ''.join(f'<li><span class="fl-n">{n}</span><div><code>{c}</code><p>{t if tr else e}</p></div></li>' for n, c, t, e in steps)
    end = ('count == 3 olunca döngüden çıkar → 4 LED birlikte yanıp söner.' if tr else 'When count reaches 3 the loop ends → all 4 LEDs blink together.')
    return f'<figure class="stm-fig"><ol class="flow">{items}</ol><figcaption>{end}</figcaption></figure>'


def demo_html(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    return f'''<div class="stm-demo" data-lang="{lang}">
  <div class="sd-head"><div><div class="sd-k">{T('Kendin dene', 'Try it yourself')}</div><div class="sd-t">{T('Sanal kart: 3 geçerli basış', 'Virtual board: 3 valid presses')}</div></div>
    <label class="sd-sw"><input type="checkbox" checked data-sd-deb><span></span>Debounce</label></div>
  <div class="sd-body">
    {board_svg({13, 15}, lang, 'sdcap')}
    <div class="sd-side">
      <button type="button" class="sd-btn" data-sd-press>{T('Butona bas', 'Press the button')}</button>
      <div class="sd-count"><span data-sd-count>0</span> / 3 <small>{T('geçerli basış', 'valid presses')}</small></div>
      <div class="sd-log" data-sd-log aria-live="polite">{T('Debounce açıkken her basış bir kez sayılır. Kapatıp tekrar dene.', 'With debounce on, each press counts once. Turn it off and try again.')}</div>
      <button type="button" class="sd-reset" data-sd-reset>{T('Sıfırla', 'Reset')}</button>
    </div>
  </div>
  <p class="sd-cap" id="sdcap">{T('Simülasyon: debounce kapalıyken her basışta kontak 2–4 kez “sıçrar”.', 'Simulation: with debounce off, the contact “bounces” 2–4 times per press.')}</p>
</div>
<script>
(function () {{
  var d = document.querySelector('.stm-demo'); if (!d) return;
  var tr = d.getAttribute('data-lang') === 'tr', count = 0, blink = null, busy = false;
  var leds = {{}}; d.querySelectorAll('.stm-board .led').forEach(function (g, i) {{ leds[[13, 12, 14, 15][i]] = g; }});
  var show = function (pins) {{ Object.keys(leds).forEach(function (k) {{ leds[k].classList.toggle('on', pins.indexOf(+k) > -1); }}); }};
  var A = [12, 14], B = [13, 15], out = d.querySelector('[data-sd-count]'), log = d.querySelector('[data-sd-log]'), deb = d.querySelector('[data-sd-deb]');
  var say = function (s) {{ log.textContent = s; }};
  var finish = function () {{ var on = false; blink = setInterval(function () {{ on = !on; show(on ? [12, 13, 14, 15] : []); }}, 400);
    say(tr ? '3 basış tamam → 2. aşama: hepsi yanıp sönüyor.' : '3 presses done → stage 2: all blinking.'); }};
  var add = function () {{ if (count >= 3) return; count++; out.textContent = count; if (count >= 3) {{ finish(); }} }};
  d.querySelector('[data-sd-press]').addEventListener('click', function () {{
    if (busy || count >= 3) return; busy = true;
    if (deb.checked) {{
      show(A); add(); if (count < 3) say(tr ? 'Gerçek basış: 1 kez sayıldı ✓' : 'Real press: counted once ✓');
      setTimeout(function () {{ if (count < 3) show(B); busy = false; }}, 350);
    }} else {{
      var n = 2 + Math.floor(Math.random() * 3), k = 0, before = count;
      var t = setInterval(function () {{ show(k % 2 ? B : A); if (k % 2 === 0) add(); k++;
        if (k >= n * 2 || count >= 3) {{ clearInterval(t); if (count < 3) show(B); busy = false;
          var m = (tr ? 'Bir basış ' : 'One press was counted ') + (count - before) + (tr ? ' kez sayıldı ✗ (bouncing)' : ' times ✗ (bouncing)');
          if (count >= 3) m += tr ? ' → sayaç erken doldu, 2. aşama başladı.' : ' → the counter filled up early and stage 2 started.';
          say(m); }} }}, 70);
    }}
  }});
  d.querySelector('[data-sd-reset]').addEventListener('click', function () {{ clearInterval(blink); count = 0; out.textContent = 0; busy = false; show(B);
    say(tr ? 'Sıfırlandı. Başlangıç: turuncu + mavi.' : 'Reset. Start: orange + blue.'); }});
}})();
</script>'''


CODE = r'''#include "stm32f4xx.h"

#define BTN       (1U << 0)                     // PA0
#define CROSS_A   ((1U << 12) | (1U << 14))     // yesil + kirmizi
#define CROSS_B   ((1U << 13) | (1U << 15))     // turuncu + mavi
#define LED_ALL   (CROSS_A | CROSS_B)           // PD12-15
#define DEBOUNCE  30000U                        // fazla olursa kisa basislari kacirir
#define BLINK     300000U

void delay(volatile uint32_t n) { while (n--); }

int main(void)
{
    uint32_t i;
    uint32_t count = 0;                          // gecerli basis sayisi

    RCC->AHB1ENR |= (1U << 0) | (1U << 3);       // GPIOA + GPIOD saati
    GPIOA->MODER &= ~(3U << (0 * 2));            // PA0 giris
    GPIOA->PUPDR &= ~(3U << (0 * 2));            // PA0 pull yok (kartta pull-down var)
    for (i = 12; i < 16; i++) {
        GPIOD->MODER &= ~(3U << (i * 2));        // PD12-15 temizle
        GPIOD->MODER |=  (1U << (i * 2));        // PD12-15 cikis
    }

    GPIOD->BSRR = CROSS_B | (CROSS_A << 16);     // baslangic: buton birakili durumu

    while (count < 3U)
    {
        if (GPIOA->IDR & BTN) {                  // (1) basis olabilir
            delay(DEBOUNCE);                     // (2) sicramalar bitsin
            if (GPIOA->IDR & BTN) {              // (3) hala basili -> gercek basis
                GPIOD->BSRR = CROSS_A | (CROSS_B << 16);
                count++;
                while (GPIOA->IDR & BTN);        // (4) birakilana kadar bekle
                GPIOD->BSRR = CROSS_B | (CROSS_A << 16);
                delay(DEBOUNCE);                 // (5) birakma sicramasini atla
            }
        }
    }

    /* --- 2. asama: hepsi yanip sonsun --- */
    while (1)
    {
        GPIOD->BSRR = LED_ALL;                   // BS12-15 -> hepsi yanar
        delay(BLINK);
        GPIOD->BSRR = LED_ALL << 16;             // BR12-15 -> hepsi soner
        delay(BLINK);
    }
}'''


def code_block():
    import html
    return f'<pre class="code"><code>{html.escape(CODE)}</code></pre>'


def snippet(s):
    import html
    return f'<pre class="code"><code>{html.escape(s)}</code></pre>'


def body(lang):
    tr = lang == 'tr'
    T = (lambda a, b: a if tr else b)
    road = '../../stm32-yol-haritasi.html' if tr else '../stm32-roadmap.html'
    return f'''  <div class="blog-tag">{T('STM32 Yol Haritam · 1. Bölüm', 'My STM32 Roadmap · Part 1')}</div>
  <h1>{T('STM32F407 ile Buton Okuma ve Debounce: Register Seviyesinde İlk Adım', 'Reading a Button and Debouncing on the STM32F407: My First Register-Level Step')}</h1>
  <div class="blog-meta">Ahmet Ulu · {T('Ekim 2026', 'October 2026')}</div>

  <a class="series-box" href="{road}"><span class="series-k">{T('Seri', 'Series')}</span><span class="series-t">{T('STM32 Yol Haritam', 'My STM32 Roadmap')}</span><span class="series-s">{T('1. bölüm · Tüm bölümler →', 'Part 1 · All parts →')}</span></a>

  <p>{T('Gömülü sistemlerde bir sonraki adımım <strong>STM32</strong>: endüstride de öğrenci takımlarında da (kısa süre önce katıldığım AGÜ Roket Takımı dahil) en sık karşılaşılan mikrodenetleyici ailelerinden biri. Bu yüzden STM32\'yi temelden, gerçekten anlayarak öğrenmeye karar verdim ve öğrendiklerimi burada bölüm bölüm kaydediyorum.',
     'My next step in embedded systems is <strong>STM32</strong>: one of the most common microcontroller families both in industry and in student teams (including the AGÜ rocket team I recently joined). So I decided to learn STM32 from the ground up, really understanding it, and I am documenting it here part by part.')}</p>

  <p>{T('Arduino\'daki <code>digitalRead()</code> gibi hazır fonksiyonlar yerine <strong>register seviyesinde</strong> başlıyorum: hangi bit neyi yapıyor, referans kılavuzdan (RM0090) bakıp kendim yazıyorum. Kart <strong>STM32F407G-DISC1</strong>, geliştirme ortamı <strong>Keil µVision</strong>. İlk uygulama: kartın üzerindeki butonu okuyup LED\'leri sürmek.',
     'Instead of ready-made functions like Arduino\'s <code>digitalRead()</code>, I am starting at the <strong>register level</strong>: looking up what each bit does in the reference manual (RM0090) and writing it myself. The board is an <strong>STM32F407G-DISC1</strong> and the IDE is <strong>Keil µVision</strong>. First exercise: read the on-board button and drive the LEDs.')}</p>

  <h3>{T('Görev', 'The task')}</h3>
  <p>{T('Başlangıçta turuncu ve mavi LED yanar. Butona her basışta yeşil ve kırmızı yanar, bırakınca turuncu ve mavi geri döner. <strong>3 geçerli basıştan</strong> sonra program ikinci aşamaya geçer ve dört LED birlikte yanıp söner. Kulağa basit geliyor ama asıl ders, “geçerli basış” kelimesinde saklı.',
     'At the start the orange and blue LEDs are on. Each press turns on green and red, and releasing brings orange and blue back. After <strong>3 valid presses</strong> the program moves to stage two and all four LEDs blink together. Sounds simple, but the real lesson is hidden in the words “valid press”.')}</p>

  <div class="stm-two">
    <figure class="stm-fig">{board_svg({13, 15}, lang, 'cap1')}<figcaption id="cap1">{T('Buton bırakılı: <b>CROSS_B</b> — turuncu (PD13) + mavi (PD15)', 'Button released: <b>CROSS_B</b> — orange (PD13) + blue (PD15)')}</figcaption></figure>
    <figure class="stm-fig">{board_svg({12, 14}, lang, 'cap2')}<figcaption id="cap2">{T('Buton basılı: <b>CROSS_A</b> — yeşil (PD12) + kırmızı (PD14)', 'Button pressed: <b>CROSS_A</b> — green (PD12) + red (PD14)')}</figcaption></figure>
  </div>

  <h3>{T('Donanım: kartın üzerindeki buton ve LED\'ler', 'Hardware: the on-board button and LEDs')}</h3>
  <p>{T('Mavi <strong>USER</strong> butonu (B1) <strong>PA0</strong> pinine bağlı ve <strong>aktif-yüksek</strong>: basınca pin 1, bırakınca 0 okunuyor. Kartta harici bir pull-down direnci olduğu için PA0\'ın dahili pull-up/pull-down dirençlerini kapalı bıraktım. Dört LED ise <strong>PD12–PD15</strong> pinlerinde, kartın ortasında bir artı şeklinde diziliyor. Karşılıklı duran yeşil–kırmızı çiftine <code>CROSS_A</code>, turuncu–mavi çiftine <code>CROSS_B</code> adını verdim.',
     'The blue <strong>USER</strong> button (B1) is wired to <strong>PA0</strong> and is <strong>active-high</strong>: pressed reads 1, released reads 0. The board already has an external pull-down resistor, so I left PA0\'s internal pull-ups/pull-downs off. The four LEDs sit on <strong>PD12–PD15</strong>, arranged in a cross in the middle of the board. I named the opposite green–red pair <code>CROSS_A</code> and the orange–blue pair <code>CROSS_B</code>.')}</p>

  <h3>{T('Adım 1: Saatleri aç (RCC)', 'Step 1: Turn on the clocks (RCC)')}</h3>
  <p>{T('STM32\'de güç tasarrufu için çevre birimlerinin saati varsayılan olarak kapalıdır; GPIO portuna yazmadan önce saatini açmak gerekir. GPIOA ve GPIOD, <strong>AHB1</strong> veriyolunda. <code>RCC_AHB1ENR</code> register\'ında bit 0 GPIOA\'yı, bit 3 GPIOD\'yi açıyor.',
     'To save power, peripheral clocks on an STM32 are off by default; you must enable a GPIO port\'s clock before writing to it. GPIOA and GPIOD are on the <strong>AHB1</strong> bus. In <code>RCC_AHB1ENR</code>, bit 0 enables GPIOA and bit 3 enables GPIOD.')}</p>
  {snippet('RCC->AHB1ENR |= (1U << 0) | (1U << 3);   // GPIOA + GPIOD saati')}

  <h3>{T('Adım 2: Pin modlarını ayarla (MODER, PUPDR)', 'Step 2: Set the pin modes (MODER, PUPDR)')}</h3>
  <p>{T('<code>MODER</code> register\'ında her pine <strong>2 bit</strong> düşer. Önce iki biti <code>&= ~(3U &lt;&lt; (i*2))</code> ile temizleyip sonra <code>|= (1U &lt;&lt; (i*2))</code> ile “01” yazıyorum; temizlemeden yazarsam önceki değer karışabilir. PA0\'ın modu “00” (giriş) kalıyor.',
     'In <code>MODER</code> each pin gets <strong>2 bits</strong>. I first clear both bits with <code>&= ~(3U &lt;&lt; (i*2))</code>, then write “01” with <code>|= (1U &lt;&lt; (i*2))</code>; writing without clearing could mix with the previous value. PA0 stays at “00” (input).')}</p>
  {moder_html(lang)}

  <h3>{T('Adım 3: LED\'leri BSRR ile sür', 'Step 3: Drive the LEDs with BSRR')}</h3>
  <p>{T('LED\'leri <code>ODR</code> yerine <code>BSRR</code> (bit set/reset) register\'ıyla yakıp söndürüyorum. Alt 16 bit pini <strong>1 yapar</strong>, üst 16 bit <strong>0 yapar</strong>; 0 yazılan bitler hiçbir şeyi değiştirmez. Böylece tek bir yazmayla bazı LED\'leri yakıp bazılarını söndürebiliyorum ve oku-değiştir-yaz yapmama gerek kalmıyor; işlem <strong>atomik</strong>.',
     'I switch the LEDs with <code>BSRR</code> (bit set/reset) instead of <code>ODR</code>. The lower 16 bits <strong>set</strong> a pin to 1 and the upper 16 bits <strong>reset</strong> it to 0; bits written as 0 change nothing. So a single write can turn some LEDs on and others off without a read-modify-write, and the operation is <strong>atomic</strong>.')}</p>
  {bsrr_html(lang)}

  <h3>{T('Sorun: bir basış, birden fazla sayım (bouncing)', 'The problem: one press, many counts (bouncing)')}</h3>
  <p>{T('İlk denemede tek basışın birden fazla basış gibi algılandığını gördüm. İlk başta bunun buton kontakları arasında oluşan bir ark olduğunu düşünmüştüm; asıl sebep ise <strong>mekanik</strong>: butona bastığında içindeki metal kontaklar birbirine çarpar ve yerine oturmadan önce çok kısa bir süre <strong>sekerek</strong> birkaç kez açılıp kapanır. Buna <strong>kontak sıçraması (contact bounce)</strong> deniyor ve çoğu butonda birkaç milisaniye sürüyor.',
     'On my first try I saw a single press being detected as several. At first I thought it was arcing between the button contacts; the real cause is <strong>mechanical</strong>: when you press the button, the metal contacts hit each other and <strong>bounce</strong>, opening and closing a few times for a very short time before they settle. This is called <strong>contact bounce</strong> and on most buttons it lasts a few milliseconds.')}</p>
  <p>{T('İnsan için birkaç milisaniye hiçbir şey ama 16 MHz\'de çalışan bir işlemci bu sürede pini binlerce kez okuyabilir. Kodun gözünden her sıçrama ayrı bir basış: 3 basışlık hedef tek basışta dolabilir.',
     'A few milliseconds is nothing to a human, but a processor running at 16 MHz can read the pin thousands of times in that window. To the code, every bounce is a separate press: a 3-press target can be reached in a single press.')}</p>
  <figure class="stm-fig wide"><div class="wave-scroll">{bounce_svg(lang)}</div><figcaption>{T('Üstte ideal buton, ortada gerçek sinyal. Debounce olmadan kod her yükselen kenarı ayrı basış sayar (kırmızı); debounce ile ilk okumadan sonra bekleyip tekrar bakar ve tek basış sayar (yeşil).', 'Top: an ideal button; middle: the real signal. Without debounce the code counts every rising edge as a press (red); with debounce it waits after the first read, checks again and counts a single press (green).')}</figcaption></figure>

  <h3>{T('Çözüm: oku, bekle, tekrar oku', 'The fix: read, wait, read again')}</h3>
  <p>{T('Çözüm olarak <strong>yazılımsal debounce</strong> uyguladım: pin 1 okunduğunda hemen sayma, sıçramaların bitmesi için biraz bekle ve tekrar oku. Hâlâ 1 ise bu gerçek bir basıştır. Ardından buton bırakılana kadar bekleyip bırakırken oluşan sıçramayı da atlıyorum; yoksa bırakma anındaki sıçrama yeni bir basış gibi görünebiliyor.',
     'I implemented a <strong>software debounce</strong>: when the pin reads 1, don\'t count it yet; wait for the bouncing to settle and read again. If it is still 1, it is a real press. Then I wait for the release and skip the bounce on release as well; otherwise the release bounce can look like a new press.')}</p>
  {flow_html(lang)}
  {snippet("""while (count < 3U) {
    if (GPIOA->IDR & BTN) {                 // (1) basis olabilir
        delay(DEBOUNCE);                    // (2) sicramalar bitsin
        if (GPIOA->IDR & BTN) {             // (3) hala basili -> gercek basis
            GPIOD->BSRR = CROSS_A | (CROSS_B << 16);
            count++;
            while (GPIOA->IDR & BTN);       // (4) birakilana kadar bekle
            GPIOD->BSRR = CROSS_B | (CROSS_A << 16);
            delay(DEBOUNCE);                // (5) birakma sicramasini atla
        }
    }
}""")}

  {demo_html(lang)}

  <h3>{T('Neden delay ve sınırları', 'Why a delay, and its limits')}</h3>
  <p>{T('Bekleme için şimdilik basit bir sayaç döngüsü kullandım: <code>void delay(volatile uint32_t n) { while (n--); }</code>. <code>volatile</code>, derleyicinin bu “hiçbir şey yapmayan” döngüyü optimizasyonla silmesini engelliyor. <code>DEBOUNCE</code> değerini deneyerek ayarladım: çok küçük olursa sıçramalar geçmeden tekrar okunuyor, çok büyük olursa kısa ve hızlı basışlar kaçırılıyor.',
     'For the wait I used a simple counting loop for now: <code>void delay(volatile uint32_t n) { while (n--); }</code>. <code>volatile</code> stops the compiler from optimising this “do-nothing” loop away. I tuned <code>DEBOUNCE</code> by trial: too small and the pin is read again before the bouncing ends; too large and short, quick presses are missed.')}</p>
  <p>{T('Bu yöntemin iki zayıf yanı var: süre, işlemci frekansına ve derleyici ayarlarına göre değişiyor, yani milisaniye cinsinden kesin değil; ve beklerken işlemci başka hiçbir iş yapamıyor. Aynı anda sensör okuyan ya da haberleşme yapan bir projede, butonu beklemek için işlemciyi kilitlemek kabul edilemez. Bunun daha iyi yolları var: <strong>SysTick</strong> ile gerçek milisaniye zamanlaması ve butonu <strong>EXTI kesmesiyle</strong> okumak.',
     'This approach has two weak points: the delay depends on the CPU frequency and compiler settings, so it is not an exact number of milliseconds; and the CPU can do nothing else while waiting. In a project that also reads sensors or communicates, locking up the CPU to wait for a button is not acceptable. There are better ways: real millisecond timing with <strong>SysTick</strong> and reading the button with an <strong>EXTI interrupt</strong>.')}</p>

  <figure class="blog-figure"><img src="kod-1.png" class="blog-img" alt="{T('Keil µVision: tanımlar ve GPIO ayarları', 'Keil µVision: definitions and GPIO setup')}" width="1600" height="607" loading="lazy" decoding="async"><figcaption>{T('Keil µVision\'da kodun ilk kısmı: tanımlar, saatler ve pin ayarları', 'The first part of the code in Keil µVision: definitions, clocks and pin setup')}</figcaption></figure>
  <figure class="blog-figure"><img src="kod-2.png" class="blog-img" alt="{T('Debounce döngüsü ve yanıp sönme aşaması', 'Debounce loop and blinking stage')}" width="1300" height="637" loading="lazy" decoding="async"><figcaption>{T('Debounce döngüsü ve ikinci aşama', 'The debounce loop and stage two')}</figcaption></figure>

  <details class="code-full"><summary>{T('Kodun tamamı', 'Full code')}</summary>{code_block()}</details>

  <div class="tech-box">
    <h4>{T('Teknik detaylar', 'Technical details')}</h4>
    <ul>
      <li>{T('Kart', 'Board')}: STM32F407G-DISC1 (STM32F407VG, Cortex-M4)</li>
      <li>{T('Geliştirme ortamı', 'IDE')}: Keil µVision · {T('Dil', 'Language')}: C, {T('register seviyesi (CMSIS başlığı', 'register level (CMSIS header')} <code>stm32f4xx.h</code>)</li>
      <li>{T('Kullanılan register\'lar', 'Registers used')}: <code>RCC_AHB1ENR</code>, <code>GPIOx_MODER</code>, <code>GPIOx_PUPDR</code>, <code>GPIOx_IDR</code>, <code>GPIOx_BSRR</code></li>
      <li>{T('Pinler', 'Pins')}: PA0 ({T('USER butonu, aktif-yüksek', 'USER button, active-high')}), PD12–PD15 (LED)</li>
      <li>{T('Kendi devrende LED kullanacaksan seri direnci <a href="../../araclar/led-direnci.html">LED direnci hesaplama</a> aracıyla bulabilirsin.', 'If you use LEDs in your own circuit, find the series resistor with the <a href="../tools/led-resistor.html">LED resistor calculator</a>.')}</li>
    </ul>
  </div>

  <h3>{T('Bu bölümden aklımda kalanlar', 'What I took away from this part')}</h3>
  <ul>
    <li>{T('Bir çevre birimini kullanmadan önce saatini açmak gerekiyor.', 'A peripheral\'s clock must be enabled before using it.')}</li>
    <li>{T('MODER gibi çok bitli alanlara yazmadan önce ilgili bitleri temizlemek gerekiyor.', 'Multi-bit fields like MODER need to be cleared before writing.')}</li>
    <li>{T('BSRR ile pinleri tek yazmada ve güvenle değiştirmek mümkün.', 'BSRR changes pins safely in a single write.')}</li>
    <li>{T('Mekanik butonlar “temiz” sinyal vermez; debounce her zaman gerekir.', 'Mechanical buttons never give a “clean” signal; you always need debounce.')}</li>
  </ul>

  <a class="series-box next" href="{road}"><span class="series-k">{T('Seri', 'Series')}</span><span class="series-t">{T('STM32 Yol Haritam', 'My STM32 Roadmap')}</span><span class="series-s">{T('Yeni bölümler yayımlandıkça burada · Tüm bölümler →', 'New parts appear here as they are published · All parts →')}</span></a>

  <h3>{T('Kaynaklar', 'References')}</h3>
  <ul>
    <li><a href="https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf" target="_blank" rel="noopener">RM0090 — STM32F405/415, STM32F407/417… Reference manual (STMicroelectronics)</a></li>
    <li><a href="https://www.st.com/resource/en/user_manual/um1472-discovery-kit-with-stm32f407vg-mcu-stmicroelectronics.pdf" target="_blank" rel="noopener">UM1472 — Discovery kit with STM32F407VG MCU (STMicroelectronics)</a></li>
    <li><a href="https://www.ganssle.com/debouncing.htm" target="_blank" rel="noopener">Jack Ganssle — A Guide to Debouncing</a></li>
  </ul>'''


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    for lang in ('tr', 'en'):
        p = os.path.join(here, 'yazilar', f'stm32-01-buton.{lang}.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(body(lang) + '\n')
        print('yazıldı:', p)
