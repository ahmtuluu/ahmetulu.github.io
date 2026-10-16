/* =========================================================
   ahmetulu.com.tr — Elektronik hesap araçları
   Her araç TOOLS içinde tanımlı; arayüzü bu dosya çizer.
   Hesaplar canlı yapılır, değerler adres çubuğuna yazılır (paylaşılabilir link).
   ========================================================= */
(function () {
  'use strict';
  var root = document.querySelector('.calc[data-tool]');
  if (!root) return;
  var LANG = document.documentElement.lang === 'en' ? 'en' : 'tr';
  var L = function (o) { return o == null ? '' : (typeof o === 'string' ? o : (o[LANG] || o.tr)); };
  var NF = function (x, d) {
    return new Intl.NumberFormat(LANG === 'tr' ? 'tr-TR' : 'en-US', { maximumSignificantDigits: d || 4 }).format(x);
  };
  var NFfix = function (x, d) {
    return new Intl.NumberFormat(LANG === 'tr' ? 'tr-TR' : 'en-US', { minimumFractionDigits: 0, maximumFractionDigits: d }).format(x);
  };

  /* ---------- Birimler ve sayı biçimleri ---------- */
  var PFX = [['p', 1e-12], ['n', 1e-9], ['µ', 1e-6], ['m', 1e-3], ['', 1], ['k', 1e3], ['M', 1e6], ['G', 1e9]];
  var UNITS = {
    V: [['mV', 1e-3], ['V', 1], ['kV', 1e3]],
    A: [['µA', 1e-6], ['mA', 1e-3], ['A', 1]],
    'Ω': [['mΩ', 1e-3], ['Ω', 1], ['kΩ', 1e3], ['MΩ', 1e6]],
    F: [['pF', 1e-12], ['nF', 1e-9], ['µF', 1e-6], ['mF', 1e-3]],
    H: [['nH', 1e-9], ['µH', 1e-6], ['mH', 1e-3], ['H', 1]],
    Hz: [['Hz', 1], ['kHz', 1e3], ['MHz', 1e6]],
    s: [['µs', 1e-6], ['ms', 1e-3], ['s', 1], ['dk', 60, 'min'], ['sa', 3600, 'h']],
    W: [['mW', 1e-3], ['W', 1], ['kW', 1e3]]
  };
  var SIN = { p: 1e-12, n: 1e-9, u: 1e-6, 'µ': 1e-6, m: 1e-3, k: 1e3, K: 1e3, M: 1e6, G: 1e9 };
  // "4,7" "4.7" "4k7" "4.7k" "470R" hepsini anlar
  var parseNum = function (str) {
    if (str == null) return NaN;
    var s = String(str).trim().replace(/\s/g, '').replace(',', '.');
    if (!s) return NaN;
    var m = s.match(/^(-?\d*)([pnuµmkKMGR])(\d+)$/);
    if (m && m[1] !== '' && m[1] !== '-') return parseFloat(m[1] + '.' + m[3]) * (m[2] === 'R' ? 1 : SIN[m[2]]);
    m = s.match(/^(-?\d*\.?\d+(?:e-?\d+)?)([pnuµmkKMGR]?)$/i);
    if (!m) return NaN;
    var v = parseFloat(m[1]);
    var suf = m[2];
    if (suf && suf !== 'R' && suf !== 'r') v *= SIN[suf] || (suf === 'K' ? 1e3 : 1);
    return v;
  };
  var fmtSI = function (x, unit, digits) {
    if (!isFinite(x)) return '—';
    if (x === 0) return '0 ' + unit;
    var a = Math.abs(x), best = PFX[4];
    for (var i = 0; i < PFX.length; i++) if (a >= PFX[i][1] * 0.9995) best = PFX[i];
    if (unit === 'Ω' && best[1] < 1e-3) best = ['m', 1e-3];
    return NF(x / best[1], digits || 4) + ' ' + best[0] + unit;
  };
  var pct = function (txt) { return LANG === 'tr' ? '%' + txt : txt + '%'; };
  var fmtTime = function (sec) {
    if (!isFinite(sec)) return '—';
    if (sec < 60) return fmtSI(sec, 's');
    var u = LANG === 'tr' ? { m: 'dk', h: 'saat', d: 'gün', y: 'yıl' } : { m: 'min', h: 'h', d: 'days', y: 'years' };
    if (sec < 3600) return NF(sec / 60, 3) + ' ' + u.m;
    if (sec < 86400 * 2) return NF(sec / 3600, 3) + ' ' + u.h;
    if (sec < 86400 * 730) return NF(sec / 86400, 3) + ' ' + u.d;
    return NF(sec / (86400 * 365), 3) + ' ' + u.y;
  };

  /* ---------- Standart değer serileri ---------- */
  var E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2];
  var E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1];
  var E96 = []; for (var e = 0; e < 96; e++) E96.push(Math.round(Math.pow(10, e / 96) * 100) / 100);
  var SERIES = { E12: E12, E24: E24, E96: E96 };
  var candidates = function (x, list) {
    var dec = Math.pow(10, Math.floor(Math.log10(x)));
    var out = [];
    [dec / 10, dec, dec * 10].forEach(function (d) { list.forEach(function (v) { out.push(Math.round(v * d * 1e6) / 1e6); }); });
    return out;
  };
  var nearest = function (x, name) {
    if (!(x > 0)) return NaN;
    var c = candidates(x, SERIES[name]), b = c[0];
    c.forEach(function (v) { if (Math.abs(Math.log(v / x)) < Math.abs(Math.log(b / x))) b = v; });
    return b;
  };
  var nextUp = function (x, name) {
    if (!(x > 0)) return NaN;
    var c = candidates(x, SERIES[name]).filter(function (v) { return v >= x * 0.9999; });
    return Math.min.apply(null, c);
  };
  var nextDown = function (x, name) {
    if (!(x > 0)) return NaN;
    var c = candidates(x, SERIES[name]).filter(function (v) { return v <= x * 1.0001; });
    return Math.max.apply(null, c);
  };
  var POWER_RATINGS = [0.125, 0.25, 0.5, 1, 2, 3, 5];
  var ratingFor = function (p) { for (var i = 0; i < POWER_RATINGS.length; i++) if (POWER_RATINGS[i] >= p * 2) return POWER_RATINGS[i]; return NaN; };
  var ratingTxt = function (r) {
    return { 0.125: '1/8 W', 0.25: '1/4 W', 0.5: '1/2 W' }[r] || (isFinite(r) ? r + ' W' : (LANG === 'tr' ? '5 W üzeri' : 'over 5 W'));
  };

  /* ---------- Ortak metinler ---------- */
  var TX = {
    tr: { results: 'Sonuçlar', copy: 'Linki kopyala', copied: 'Kopyalandı ✓', reset: 'Sıfırla', fill: 'Değerleri girince sonuçlar burada görünür.',
          nearest: 'En yakın', safer: 'Önerilen (bir üst)', optional: 'isteğe bağlı', mode: 'Ne hesaplanacak?' },
    en: { results: 'Results', copy: 'Copy link', copied: 'Copied ✓', reset: 'Reset', fill: 'Results appear here once you enter values.',
          nearest: 'Nearest', safer: 'Recommended (next up)', optional: 'optional', mode: 'What to calculate?' }
  }[LANG];

  /* =========================================================
     ARAÇ TANIMLARI
     ========================================================= */
  var TOOLS = {};

  /* ---------- Ohm kanunu ---------- */
  TOOLS.ohm = {
    modes: [
      { id: 'VI', label: 'V, I', show: ['V', 'I'] }, { id: 'VR', label: 'V, R', show: ['V', 'R'] },
      { id: 'IR', label: 'I, R', show: ['I', 'R'] }, { id: 'PV', label: 'P, V', show: ['P', 'V'] },
      { id: 'PI', label: 'P, I', show: ['P', 'I'] }, { id: 'PR', label: 'P, R', show: ['P', 'R'] }
    ],
    modeLabel: { tr: 'Bildiğin iki değer', en: 'The two values you know' },
    fields: [
      { id: 'V', label: { tr: 'Gerilim (V)', en: 'Voltage (V)' }, q: 'V', def: '12', du: 1 },
      { id: 'I', label: { tr: 'Akım (I)', en: 'Current (I)' }, q: 'A', def: '20', du: 1 },
      { id: 'R', label: { tr: 'Direnç (R)', en: 'Resistance (R)' }, q: 'Ω', def: '470', du: 1 },
      { id: 'P', label: { tr: 'Güç (P)', en: 'Power (P)' }, q: 'W', def: '1', du: 1 }
    ],
    calc: function (v, m) {
      var V = v.V, I = v.I, R = v.R, P = v.P;
      if (m === 'VI') { R = V / I; P = V * I; }
      if (m === 'VR') { I = V / R; P = V * V / R; }
      if (m === 'IR') { V = I * R; P = I * I * R; }
      if (m === 'PV') { I = P / V; R = V * V / P; }
      if (m === 'PI') { V = P / I; R = P / (I * I); }
      if (m === 'PR') { V = Math.sqrt(P * R); I = Math.sqrt(P / R); }
      var known = m.split('');
      var r = [];
      [['V', V, 'V', { tr: 'Gerilim', en: 'Voltage' }], ['I', I, 'A', { tr: 'Akım', en: 'Current' }],
       ['R', R, 'Ω', { tr: 'Direnç', en: 'Resistance' }], ['P', P, 'W', { tr: 'Güç', en: 'Power' }]].forEach(function (q) {
        if (known.indexOf(q[0]) < 0) r.push({ label: q[3], value: fmtSI(q[1], q[2]), primary: r.length === 0 });
      });
      return { results: r };
    }
  };

  /* ---------- Seri / paralel ---------- */
  TOOLS.series = {
    listDefs: { R: ['1k', '2.2k', '4.7k'], C: ['100n', '47n', '10n'], L: ['10u', '22u', '47u'] },
    fields: [
      { id: 'kind', type: 'seg', label: { tr: 'Bileşen', en: 'Component' }, def: 'R',
        options: [['R', { tr: 'Direnç', en: 'Resistor' }], ['C', { tr: 'Kondansatör', en: 'Capacitor' }], ['L', { tr: 'Bobin', en: 'Inductor' }]] },
      { id: 'list', type: 'list', label: { tr: 'Değerler', en: 'Values' }, q: function (s) { return { R: 'Ω', C: 'F', L: 'H' }[s.kind]; },
        def: ['1k', '2.2k', '4.7k'], hint: { tr: 'Önek kullanabilirsin: 4k7, 100n, 10u (µ), 2.2M', en: 'You can use prefixes: 4k7, 100n, 10u (µ), 2.2M' } }
    ],
    calc: function (v, m, s) {
      var xs = v.list.filter(function (x) { return x > 0; });
      if (xs.length < 2) return { info: [{ tr: 'En az iki değer gir.', en: 'Enter at least two values.' }] };
      var sum = xs.reduce(function (a, b) { return a + b; }, 0);
      var inv = 1 / xs.reduce(function (a, b) { return a + 1 / b; }, 0);
      var u = { R: 'Ω', C: 'F', L: 'H' }[s.kind];
      var ser = s.kind === 'C' ? inv : sum, par = s.kind === 'C' ? sum : inv;
      return { results: [
        { label: { tr: 'Seri bağlı toplam', en: 'Series total' }, value: fmtSI(ser, u), primary: true },
        { label: { tr: 'Paralel bağlı toplam', en: 'Parallel total' }, value: fmtSI(par, u), primary: true }
      ] };
    }
  };

  /* ---------- Gerilim bölücü ---------- */
  TOOLS.divider = {
    modes: [{ id: 'vout', label: { tr: 'Çıkış gerilimi', en: 'Output voltage' }, show: ['Vin', 'R1', 'R2', 'RL'] },
            { id: 'r2', label: { tr: 'Alt direnci bul', en: 'Find bottom resistor' }, show: ['Vin', 'Vout', 'R1'] }],
    diagram: 'divider',
    fields: [
      { id: 'Vin', label: { tr: 'Giriş gerilimi (Vin)', en: 'Input voltage (Vin)' }, q: 'V', def: '12', du: 1 },
      { id: 'Vout', label: { tr: 'İstenen çıkış (Vout)', en: 'Target output (Vout)' }, q: 'V', def: '3.3', du: 1 },
      { id: 'R1', label: { tr: 'Üst direnç R1 (Vin → Vout)', en: 'Top resistor R1 (Vin → Vout)' }, q: 'Ω', def: '10', du: 2 },
      { id: 'R2', label: { tr: 'Alt direnç R2 (Vout → GND)', en: 'Bottom resistor R2 (Vout → GND)' }, q: 'Ω', def: '3.3', du: 2 },
      { id: 'RL', label: { tr: 'Yük direnci RL', en: 'Load resistance RL' }, q: 'Ω', def: '', du: 2, optional: true }
    ],
    calc: function (v, m) {
      var res = [], warn = [];
      if (m === 'vout') {
        var R2e = isFinite(v.RL) && v.RL > 0 ? (v.R2 * v.RL) / (v.R2 + v.RL) : v.R2;
        var Vo = v.Vin * R2e / (v.R1 + R2e), I = v.Vin / (v.R1 + R2e);
        res.push({ label: 'Vout', value: fmtSI(Vo, 'V'), primary: true });
        if (R2e !== v.R2) res.push({ label: { tr: 'Yüksüz Vout', en: 'Unloaded Vout' }, value: fmtSI(v.Vin * v.R2 / (v.R1 + v.R2), 'V') });
        res.push({ label: { tr: 'Oran (Vout / Vin)', en: 'Ratio (Vout / Vin)' }, value: NF(Vo / v.Vin, 4) });
        res.push({ label: { tr: 'Bölücü akımı', en: 'Divider current' }, value: fmtSI(I, 'A') });
        res.push({ label: { tr: 'R1 / R2 gücü', en: 'R1 / R2 power' }, value: fmtSI(I * I * v.R1, 'W') + ' · ' + fmtSI(Math.pow(Vo, 2) / v.R2, 'W') });
      } else {
        if (!(v.Vout < v.Vin)) return { warn: [{ tr: 'Vout, Vin\'den küçük olmalı.', en: 'Vout must be lower than Vin.' }] };
        var R2 = v.R1 * v.Vout / (v.Vin - v.Vout);
        res.push({ label: 'R2', value: fmtSI(R2, 'Ω'), primary: true });
        ['E24', 'E96'].forEach(function (sname) {
          var n = nearest(R2, sname);
          res.push({ label: TX.nearest + ' ' + sname, value: fmtSI(n, 'Ω'),
            sub: '→ Vout = ' + fmtSI(v.Vin * n / (v.R1 + n), 'V') });
        });
      }
      return { results: res, warn: warn };
    }
  };

  /* ---------- Desibel ---------- */
  TOOLS.db = {
    modes: [
      { id: 'v2db', label: { tr: 'Gerilim oranı → dB', en: 'Voltage ratio → dB' }, show: ['a', 'b'] },
      { id: 'p2db', label: { tr: 'Güç oranı → dB', en: 'Power ratio → dB' }, show: ['pa', 'pb'] },
      { id: 'db2r', label: { tr: 'dB → oran', en: 'dB → ratio' }, show: ['dB'] },
      { id: 'dbm', label: 'dBm ↔ W', show: ['dBm'] }
    ],
    fields: [
      { id: 'a', label: { tr: 'Çıkış gerilimi', en: 'Output voltage' }, q: 'V', def: '10', du: 1 },
      { id: 'b', label: { tr: 'Giriş gerilimi', en: 'Input voltage' }, q: 'V', def: '1', du: 1 },
      { id: 'pa', label: { tr: 'Çıkış gücü', en: 'Output power' }, q: 'W', def: '10', du: 1 },
      { id: 'pb', label: { tr: 'Giriş gücü', en: 'Input power' }, q: 'W', def: '1', du: 1 },
      { id: 'dB', label: 'dB', unit: 'dB', def: '20' },
      { id: 'dBm', label: 'dBm', unit: 'dBm', def: '20' }
    ],
    calc: function (v, m) {
      if (m === 'v2db') return { results: [{ label: { tr: 'Kazanç', en: 'Gain' }, value: NF(20 * Math.log10(v.a / v.b), 4) + ' dB', primary: true }] };
      if (m === 'p2db') return { results: [{ label: { tr: 'Kazanç', en: 'Gain' }, value: NF(10 * Math.log10(v.pa / v.pb), 4) + ' dB', primary: true }] };
      if (m === 'db2r') return { results: [
        { label: { tr: 'Gerilim oranı', en: 'Voltage ratio' }, value: '× ' + NF(Math.pow(10, v.dB / 20), 4), primary: true },
        { label: { tr: 'Güç oranı', en: 'Power ratio' }, value: '× ' + NF(Math.pow(10, v.dB / 10), 4), primary: true }] };
      var P = Math.pow(10, v.dBm / 10) / 1000;
      return { results: [
        { label: { tr: 'Güç', en: 'Power' }, value: fmtSI(P, 'W'), primary: true },
        { label: { tr: '50 Ω yükte gerilim (RMS)', en: 'Voltage into 50 Ω (RMS)' }, value: fmtSI(Math.sqrt(P * 50), 'V') }] };
    }
  };

  /* ---------- LED direnci ---------- */
  TOOLS.led = {
    presets: { id: 'color', label: { tr: 'LED rengi', en: 'LED colour' }, set: 'Vf', options: [
      ['red', { tr: 'Kırmızı', en: 'Red' }, '2.0', '#ef4444'], ['orange', { tr: 'Turuncu', en: 'Orange' }, '2.1', '#f97316'],
      ['yellow', { tr: 'Sarı', en: 'Yellow' }, '2.1', '#eab308'], ['green', { tr: 'Yeşil', en: 'Green' }, '3.1', '#22c55e'],
      ['blue', { tr: 'Mavi', en: 'Blue' }, '3.1', '#3b82f6'], ['white', { tr: 'Beyaz', en: 'White' }, '3.1', '#f8fafc'],
      ['ir', 'IR', '1.3', '#7f1d1d']] },
    diagram: 'led',
    fields: [
      { id: 'Vs', label: { tr: 'Besleme gerilimi', en: 'Supply voltage' }, q: 'V', def: '5', du: 1 },
      { id: 'Vf', label: { tr: 'LED ileri gerilimi (Vf)', en: 'LED forward voltage (Vf)' }, q: 'V', def: '2.0', du: 1,
        hint: { tr: 'Kesin değer LED\'in datasheet\'inde yazar.', en: 'Check the LED datasheet for the exact value.' } },
      { id: 'If', label: { tr: 'LED akımı', en: 'LED current' }, q: 'A', def: '10', du: 1,
        hint: { tr: 'Gösterge LED\'leri için 5–10 mA çoğu zaman yeterli.', en: '5–10 mA is usually enough for indicator LEDs.' } },
      { id: 'n', label: { tr: 'Seri LED sayısı', en: 'LEDs in series' }, unit: { tr: 'adet', en: 'pcs' }, def: '1' }
    ],
    calc: function (v) {
      var n = Math.max(1, Math.round(v.n || 1)), drop = v.Vs - n * v.Vf;
      if (!(drop > 0)) return { warn: [{ tr: 'Besleme gerilimi LED\'lerin toplam ileri geriliminden büyük olmalı.', en: 'Supply voltage must exceed the total LED forward voltage.' }] };
      var R = drop / v.If, Rs = nextUp(R, 'E24'), Ia = drop / Rs, P = drop * Ia;
      return { results: [
        { label: { tr: 'Gereken direnç', en: 'Required resistor' }, value: fmtSI(R, 'Ω'), primary: true },
        { label: TX.safer + ' E24', value: fmtSI(Rs, 'Ω'), sub: (LANG === 'tr' ? 'gerçek akım ' : 'actual current ') + fmtSI(Ia, 'A'), accent: true },
        { label: { tr: 'Dirençte harcanan güç', en: 'Resistor power' }, value: fmtSI(P, 'W'),
          sub: (LANG === 'tr' ? 'en az ' : 'use at least ') + ratingTxt(ratingFor(P)) },
        { label: { tr: 'LED başına güç', en: 'Power per LED' }, value: fmtSI(v.Vf * Ia, 'W') }
      ], info: n > 1 ? [{ tr: n + ' LED seri bağlı: hepsinden aynı akım geçer.', en: n + ' LEDs in series: the same current flows through all of them.' }] : [] };
    }
  };

  /* ---------- Ayarlı regülatör ---------- */
  var REGS = {
    lm2596: { name: 'LM2596-ADJ', vref: 1.23, type: 'fb', iadj: 0, rlow: [240, 1500], d: ['3.3', 2, '1', 2] },
    xl4015: { name: 'XL4015', vref: 1.25, type: 'fb', iadj: 0, d: ['3.3', 2, '1', 2] },
    mp1584: { name: 'MP1584', vref: 0.8, type: 'fb', iadj: 0, rlowMax: 40e3, d: ['52.3', 2, '10', 2] },
    lm317: { name: 'LM317', vref: 1.25, type: 'adj', iadj: 50e-6, d: ['240', 1, '720', 1] },
    ams1117: { name: 'AMS1117-ADJ', vref: 1.25, type: 'adj', iadj: 50e-6, d: ['240', 1, '720', 1] },
    custom: { name: { tr: 'Özel (Vref gir)', en: 'Custom (enter Vref)' }, vref: null, type: 'fb', iadj: 0 }
  };
  var regLabel = function (s, pos) {
    var t = REGS[s.chip].type;
    if (pos === 'up') return t === 'fb' ? { tr: 'Üst direnç (Vout → FB)', en: 'Top resistor (Vout → FB)' } : { tr: 'Üst direnç (OUT → ADJ)', en: 'Top resistor (OUT → ADJ)' };
    return t === 'fb' ? { tr: 'Alt direnç (FB → GND)', en: 'Bottom resistor (FB → GND)' } : { tr: 'Alt direnç (ADJ → GND)', en: 'Bottom resistor (ADJ → GND)' };
  };
  TOOLS.regulator = {
    presets: { id: 'chip', label: { tr: 'Entegre', en: 'Chip' }, options: Object.keys(REGS).map(function (k) { return [k, REGS[k].name]; }) },
    onPreset: function (k, set) { var d = REGS[k].d; if (d) { set('Rup', d[0], d[1]); set('Rlow', d[2], d[3]); } },
    modes: [{ id: 'vout', label: { tr: 'Dirençlerden Vout', en: 'Vout from resistors' }, show: ['Rup', 'Rlow', 'Vref'] },
            { id: 'find', label: { tr: 'Vout için direnç bul', en: 'Find resistor for Vout' }, show: ['Vout', 'Rup', 'Rlow', 'Vref'] }],
    diagram: 'reg',
    fields: [
      { id: 'Vout', label: { tr: 'İstenen çıkış gerilimi', en: 'Target output voltage' }, q: 'V', def: '5', du: 1 },
      { id: 'Rup', label: function (s) { return regLabel(s, 'up'); }, q: 'Ω', def: '3.3', du: 2,
        hidden: function (s, m) { return m === 'find' && REGS[s.chip].type === 'fb'; } },
      { id: 'Rlow', label: function (s) { return regLabel(s, 'low'); }, q: 'Ω', def: '1', du: 2,
        hidden: function (s, m) { return m === 'find' && REGS[s.chip].type === 'adj'; } },
      { id: 'Vref', label: { tr: 'Referans gerilimi (Vref)', en: 'Reference voltage (Vref)' }, q: 'V', def: '1.25', du: 1,
        hidden: function (s) { return s.chip !== 'custom'; } }
    ],
    calc: function (v, m, s) {
      var c = REGS[s.chip], Vref = c.vref || v.Vref, res = [], warn = [], info = [];
      var vout = function (up, low) { return c.type === 'fb' ? Vref * (1 + up / low) : Vref * (1 + low / up) + c.iadj * low; };
      if (m === 'vout') {
        res.push({ label: 'Vout', value: fmtSI(vout(v.Rup, v.Rlow), 'V'), primary: true });
        res.push({ label: { tr: 'Bölücü akımı', en: 'Divider current' }, value: fmtSI(Vref / (c.type === 'fb' ? v.Rlow : v.Rup), 'A') });
      } else {
        if (!(v.Vout > Vref)) return { warn: [{ tr: 'Çıkış gerilimi Vref\'ten (' + NF(Vref) + ' V) büyük olmalı.', en: 'Output must be above Vref (' + NF(Vref) + ' V).' }] };
        var need = c.type === 'fb' ? v.Rlow * (v.Vout / Vref - 1) : (v.Vout - Vref) / (Vref / v.Rup + c.iadj);
        var lab = c.type === 'fb' ? regLabel(s, 'up') : regLabel(s, 'low');
        res.push({ label: lab, value: fmtSI(need, 'Ω'), primary: true });
        ['E24', 'E96'].forEach(function (sn) {
          var n = nearest(need, sn);
          var vo = c.type === 'fb' ? vout(n, v.Rlow) : vout(v.Rup, n);
          res.push({ label: TX.nearest + ' ' + sn, value: fmtSI(n, 'Ω'), sub: '→ Vout = ' + fmtSI(vo, 'V') });
        });
      }
      if (c.rlow && (v.Rlow < c.rlow[0] || v.Rlow > c.rlow[1]))
        warn.push({ tr: 'LM2596 datasheet\'i alt direnç (FB → GND) için 240 Ω – 1,5 kΩ arası öneriyor.', en: 'The LM2596 datasheet recommends 240 Ω – 1.5 kΩ for the bottom resistor (FB → GND).' });
      if (c.rlowMax && v.Rlow > c.rlowMax)
        warn.push({ tr: 'MP1584 datasheet\'i alt direncin 40 kΩ\'un altında olmasını öneriyor.', en: 'The MP1584 datasheet recommends keeping the bottom resistor under 40 kΩ.' });
      if (c.iadj) info.push({ tr: 'ADJ pininden akan ~50 µA akım hesaba katıldı.', en: 'The ~50 µA ADJ pin current is included.' });
      info.push({ tr: 'Vref ±%2–3 tolerans taşır; gerçek çıkış biraz farklı olabilir.', en: 'Vref has about ±2–3% tolerance, so the real output may differ slightly.' });
      return { results: res, warn: warn, info: info };
    }
  };

  /* ---------- Buck dönüştürücü ---------- */
  TOOLS.buck = {
    presets: { id: 'chip', label: { tr: 'Entegre', en: 'Chip' }, set: 'fs', options: [
      ['lm2596', 'LM2596 (150 kHz)', '150'], ['xl4015', 'XL4015 (180 kHz)', '180'], ['custom', { tr: 'Özel frekans', en: 'Custom frequency' }, null]] },
    fields: [
      { id: 'Vin', label: { tr: 'Giriş gerilimi (en yüksek)', en: 'Input voltage (maximum)' }, q: 'V', def: '12', du: 1 },
      { id: 'Vout', label: { tr: 'Çıkış gerilimi', en: 'Output voltage' }, q: 'V', def: '5', du: 1 },
      { id: 'Iout', label: { tr: 'Çıkış akımı (en yüksek)', en: 'Output current (maximum)' }, q: 'A', def: '2', du: 2 },
      { id: 'fs', label: { tr: 'Anahtarlama frekansı', en: 'Switching frequency' }, q: 'Hz', def: '150', du: 1 },
      { id: 'r', label: { tr: 'Bobin dalgalanma oranı', en: 'Inductor ripple ratio' }, unit: '%', def: '30',
        hint: { tr: 'TI önerisi: çıkış akımının %20–40\'ı.', en: 'TI suggests 20–40% of output current.' } },
      { id: 'eff', label: { tr: 'Tahmini verim', en: 'Estimated efficiency' }, unit: '%', def: '85' },
      { id: 'dV', label: { tr: 'İzin verilen çıkış dalgalanması', en: 'Allowed output ripple' }, q: 'V', def: '50', du: 0 },
      { id: 'esr', label: { tr: 'Çıkış kondansatörü ESR', en: 'Output capacitor ESR' }, q: 'Ω', def: '', du: 0, optional: true }
    ],
    calc: function (v) {
      if (!(v.Vout < v.Vin)) return { warn: [{ tr: 'Çıkış, girişten düşük olmalı (buck = düşürücü).', en: 'Output must be lower than input (buck = step-down).' }] };
      var eta = v.eff / 100, D = v.Vout / (v.Vin * eta), dI = v.r / 100 * v.Iout;
      var L = v.Vout * (v.Vin - v.Vout) / (dI * v.Vin * v.fs), Ipk = v.Iout + dI / 2, C = dI / (8 * v.dV * v.fs);
      var res = [
        { label: { tr: 'Bobin (en az)', en: 'Inductor (minimum)' }, value: fmtSI(L, 'H'), sub: TX.safer + ': ' + fmtSI(nextUp(L, 'E12'), 'H'), primary: true },
        { label: { tr: 'Çıkış kondansatörü (en az)', en: 'Output capacitor (minimum)' }, value: fmtSI(C, 'F'), primary: true },
        { label: { tr: 'Görev oranı (D)', en: 'Duty cycle (D)' }, value: pct(NFfix(D * 100, 1)) },
        { label: { tr: 'Bobin dalgalanma akımı', en: 'Inductor ripple current' }, value: fmtSI(dI, 'A') },
        { label: { tr: 'Tepe akım (bobin, diyot, anahtar)', en: 'Peak current (inductor, diode, switch)' }, value: fmtSI(Ipk, 'A') }
      ];
      var warn = [];
      if (isFinite(v.esr) && v.esr > 0) {
        var dvE = v.esr * dI;
        res.push({ label: { tr: 'ESR kaynaklı dalgalanma', en: 'Ripple from ESR' }, value: fmtSI(dvE, 'V') });
        if (dvE > v.dV) warn.push({ tr: 'Bu ESR ile dalgalanma hedefini aşıyorsun; daha düşük ESR\'li (ör. polimer/seramik) kondansatör seç.', en: 'This ESR alone exceeds your ripple target; pick a lower-ESR (e.g. polymer/ceramic) capacitor.' });
      }
      if (D > 0.95) warn.push({ tr: 'Görev oranı çok yüksek; giriş ile çıkış arasındaki fark yetersiz olabilir.', en: 'Duty cycle is very high; the input–output headroom may be too small.' });
      return { results: res, warn: warn, info: [{ tr: 'Datasheet belirli bir bobin öneriyorsa önce onu kullan.', en: 'If the datasheet recommends a specific inductor, use that first.' }] };
    }
  };

  /* ---------- Pil ömrü ---------- */
  TOOLS.battery = {
    fields: [
      { id: 'cap', label: { tr: 'Pil kapasitesi', en: 'Battery capacity' }, unit: 'mAh', def: '2000' },
      { id: 'Ia', label: { tr: 'Aktif akım', en: 'Active current' }, q: 'A', def: '80', du: 1, hint: { tr: 'ESP32 Wi-Fi açıkken tipik 80–240 mA çeker.', en: 'An ESP32 with Wi-Fi on typically draws 80–240 mA.' } },
      { id: 'ta', label: { tr: 'Aktif süre (her döngüde)', en: 'Active time (per cycle)' }, q: 's', def: '5', du: 2 },
      { id: 'Is', label: { tr: 'Uyku akımı', en: 'Sleep current' }, q: 'A', def: '20', du: 0 },
      { id: 'ts', label: { tr: 'Uyku süresi (her döngüde)', en: 'Sleep time (per cycle)' }, q: 's', def: '10', du: 3 },
      { id: 'k', label: { tr: 'Kullanılabilir kapasite', en: 'Usable capacity' }, unit: '%', def: '80',
        hint: { tr: 'Kesme gerilimi, sıcaklık ve kendi kendine deşarj için pay.', en: 'Margin for cut-off voltage, temperature and self-discharge.' } }
    ],
    calc: function (v) {
      var Iavg = (v.Ia * v.ta + v.Is * v.ts) / (v.ta + v.ts);
      var hours = (v.cap / 1000) * (v.k / 100) / Iavg;
      return { results: [
        { label: { tr: 'Tahmini pil ömrü', en: 'Estimated battery life' }, value: fmtTime(hours * 3600), primary: true },
        { label: { tr: 'Ortalama akım', en: 'Average current' }, value: fmtSI(Iavg, 'A') },
        { label: { tr: 'Aktif kalma oranı', en: 'Active ratio' }, value: pct(NFfix(100 * v.ta / (v.ta + v.ts), 2)) },
        { label: { tr: 'Döngü süresi', en: 'Cycle time' }, value: fmtTime(v.ta + v.ts) }
      ] };
    }
  };

  /* ---------- PCB iz genişliği (IPC-2221) ---------- */
  TOOLS.trace = {
    fields: [
      { id: 'I', label: { tr: 'Akım', en: 'Current' }, q: 'A', def: '2', du: 2 },
      { id: 'oz', type: 'select', label: { tr: 'Bakır kalınlığı', en: 'Copper thickness' }, def: '1',
        options: [['0.5', '0,5 oz (17,5 µm)'], ['1', '1 oz (35 µm)'], ['2', '2 oz (70 µm)'], ['3', '3 oz (105 µm)']] },
      { id: 'layer', type: 'seg', label: { tr: 'Katman', en: 'Layer' }, def: 'ext',
        options: [['ext', { tr: 'Dış katman', en: 'External' }], ['int', { tr: 'İç katman', en: 'Internal' }]] },
      { id: 'dT', label: { tr: 'İzin verilen sıcaklık artışı', en: 'Allowed temperature rise' }, unit: '°C', def: '10' },
      { id: 'len', label: { tr: 'İz uzunluğu', en: 'Trace length' }, unit: 'mm', def: '50', optional: true },
      { id: 'Ta', label: { tr: 'Ortam sıcaklığı', en: 'Ambient temperature' }, unit: '°C', def: '25' }
    ],
    calc: function (v, m, s) {
      var k = s.layer === 'int' ? 0.024 : 0.048;
      var A = Math.pow(v.I / (k * Math.pow(v.dT, 0.44)), 1 / 0.725); // mil²
      var tmil = parseFloat(s.oz) * 1.378, wmil = A / tmil, wmm = wmil * 0.0254;
      var res = [
        { label: { tr: 'En az iz genişliği', en: 'Minimum trace width' }, value: NF(wmm, 3) + ' mm', sub: NF(wmil, 4) + ' mil', primary: true },
        { label: { tr: 'Kesit alanı', en: 'Cross-section' }, value: NF(A, 4) + ' mil²', sub: NF(A * 0.00064516, 3) + ' mm²' }
      ];
      if (isFinite(v.len) && v.len > 0) {
        var rho = 1.72e-8 * (1 + 0.00393 * (v.Ta + v.dT - 20));
        var R = rho * (v.len / 1000) / (wmm / 1000 * tmil * 25.4e-6);
        res.push({ label: { tr: 'İz direnci', en: 'Trace resistance' }, value: fmtSI(R, 'Ω') });
        res.push({ label: { tr: 'Gerilim düşümü', en: 'Voltage drop' }, value: fmtSI(R * v.I, 'V') });
        res.push({ label: { tr: 'Güç kaybı', en: 'Power loss' }, value: fmtSI(R * v.I * v.I, 'W') });
      }
      var warn = [];
      if (v.I > 35 || v.dT > 100) warn.push({ tr: 'IPC-2221 eğrileri 35 A ve 100 °C artışa kadar geçerli.', en: 'IPC-2221 curves are valid up to 35 A and a 100 °C rise.' });
      return { results: res, warn: warn };
    }
  };

  /* ---------- AWG ---------- */
  var awgLabel = function (n) { return n === 0 ? '0' : n < 0 ? (1 - n) + '/0' : String(n); };
  var awgOpts = []; for (var g = -3; g <= 40; g++) awgOpts.push([String(g), 'AWG ' + awgLabel(g)]);
  var awgD = function (n) { return 0.127 * Math.pow(92, (36 - n) / 39); };
  TOOLS.awg = {
    modes: [{ id: 'awg', label: { tr: 'AWG → mm²', en: 'AWG → mm²' }, show: ['awg'] }, { id: 'mm2', label: { tr: 'mm² → AWG', en: 'mm² → AWG' }, show: ['mm2'] }],
    fields: [
      { id: 'awg', type: 'select', label: { tr: 'Kablo kalınlığı', en: 'Wire gauge' }, def: '22', options: awgOpts },
      { id: 'mm2', label: { tr: 'Kesit alanı', en: 'Cross-section' }, unit: 'mm²', def: '1.5' }
    ],
    calc: function (v, m, s) {
      var n = m === 'awg' ? parseInt(s.awg, 10) : null;
      if (m === 'mm2') { n = 40; for (var i = 40; i >= -3; i--) { if (Math.PI * Math.pow(awgD(i) / 2, 2) >= v.mm2 * 0.999) { n = i; break; } } }
      var d = awgD(n), A = Math.PI * d * d / 4, Rkm = 1.7241e-8 / (A * 1e-6) * 1000;
      var res = [];
      if (m === 'mm2') res.push({ label: { tr: 'Karşılayan en ince AWG', en: 'Thinnest AWG that fits' }, value: 'AWG ' + awgLabel(n), primary: true });
      res.push({ label: { tr: 'Kesit alanı', en: 'Cross-section' }, value: NF(A, 4) + ' mm²', primary: m === 'awg' });
      res.push({ label: { tr: 'Çap', en: 'Diameter' }, value: NF(d, 4) + ' mm' });
      res.push({ label: { tr: 'Direnç (bakır, 20 °C)', en: 'Resistance (copper, 20 °C)' }, value: NF(Rkm, 4) + ' Ω/km', sub: fmtSI(Rkm / 1000, 'Ω') + ' / m' });
      return { results: res, info: [{ tr: 'Taşıyabileceği akım; yalıtıma, demet halinde olup olmamasına ve ortama göre değişir.', en: 'Current capacity depends on insulation, bundling and environment.' }] };
    }
  };

  /* ---------- RC ---------- */
  TOOLS.rc = {
    diagram: 'rc',
    fields: [
      { id: 'R', label: { tr: 'Direnç (R)', en: 'Resistance (R)' }, q: 'Ω', def: '10', du: 2 },
      { id: 'C', label: { tr: 'Kondansatör (C)', en: 'Capacitance (C)' }, q: 'F', def: '100', du: 1 },
      { id: 'p', label: { tr: 'Hedef şarj yüzdesi', en: 'Target charge level' }, unit: '%', def: '90' }
    ],
    calc: function (v) {
      var tau = v.R * v.C, p = Math.min(99.999, Math.max(0.001, v.p)) / 100;
      return { results: [
        { label: { tr: 'Kesim frekansı (−3 dB)', en: 'Cut-off frequency (−3 dB)' }, value: fmtSI(1 / (2 * Math.PI * tau), 'Hz'), primary: true },
        { label: { tr: 'Zaman sabiti τ = RC', en: 'Time constant τ = RC' }, value: fmtSI(tau, 's'), primary: true },
        { label: (LANG === 'tr' ? '%' + NF(v.p) + '\'e şarj süresi' : 'Time to ' + NF(v.p) + '%'), value: fmtSI(-tau * Math.log(1 - p), 's') },
        { label: { tr: '5τ (≈ %99,3 şarj)', en: '5τ (≈ 99.3% charged)' }, value: fmtSI(5 * tau, 's') }
      ] };
    }
  };

  /* ---------- 555 ---------- */
  TOOLS.t555 = {
    modes: [{ id: 'ast', label: { tr: 'Astable (osilatör)', en: 'Astable (oscillator)' }, show: ['Ra', 'Rb', 'C'] },
            { id: 'mono', label: { tr: 'Monostable (tek darbe)', en: 'Monostable (one-shot)' }, show: ['Ra', 'C'] }],
    diagram: '555',
    fields: [
      { id: 'Ra', label: 'R1 (RA)', q: 'Ω', def: '1', du: 2 },
      { id: 'Rb', label: 'R2 (RB)', q: 'Ω', def: '10', du: 2 },
      { id: 'C', label: 'C', q: 'F', def: '10', du: 2 }
    ],
    calc: function (v, m) {
      if (m === 'mono') return { results: [{ label: { tr: 'Darbe süresi', en: 'Pulse width' }, value: fmtSI(1.1 * v.Ra * v.C, 's'), primary: true }] };
      var th = 0.693 * (v.Ra + v.Rb) * v.C, tl = 0.693 * v.Rb * v.C;
      return { results: [
        { label: { tr: 'Frekans', en: 'Frequency' }, value: fmtSI(1.44 / ((v.Ra + 2 * v.Rb) * v.C), 'Hz'), primary: true },
        { label: { tr: 'Görev oranı (yüksek)', en: 'Duty cycle (high)' }, value: pct(NFfix(100 * th / (th + tl), 1)), primary: true },
        { label: { tr: 'Yüksek süre', en: 'High time' }, value: fmtSI(th, 's') },
        { label: { tr: 'Düşük süre', en: 'Low time' }, value: fmtSI(tl, 's') },
        { label: { tr: 'Periyot', en: 'Period' }, value: fmtSI(th + tl, 's') }
      ], info: [{ tr: 'Bu bağlantıda görev oranı her zaman %50\'nin üstündedir.', en: 'With this wiring the duty cycle is always above 50%.' }] };
    }
  };

  /* ---------- Direnç renk kodu (özel arayüz) ---------- */
  var COLORS = [
    ['black', { tr: 'Siyah', en: 'Black' }, '#1a1a1a', 0, 1, null, 250], ['brown', { tr: 'Kahverengi', en: 'Brown' }, '#7c4a1e', 1, 10, 1, 100],
    ['red', { tr: 'Kırmızı', en: 'Red' }, '#dc2626', 2, 100, 2, 50], ['orange', { tr: 'Turuncu', en: 'Orange' }, '#f97316', 3, 1e3, 0.05, 15],
    ['yellow', { tr: 'Sarı', en: 'Yellow' }, '#facc15', 4, 1e4, 0.02, 25], ['green', { tr: 'Yeşil', en: 'Green' }, '#16a34a', 5, 1e5, 0.5, 20],
    ['blue', { tr: 'Mavi', en: 'Blue' }, '#2563eb', 6, 1e6, 0.25, 10], ['violet', { tr: 'Mor', en: 'Violet' }, '#7c3aed', 7, 1e7, 0.1, 5],
    ['grey', { tr: 'Gri', en: 'Grey' }, '#9ca3af', 8, 1e8, 0.01, 1], ['white', { tr: 'Beyaz', en: 'White' }, '#f8fafc', 9, 1e9, null, null],
    ['gold', { tr: 'Altın', en: 'Gold' }, '#c9a227', null, 0.1, 5, null], ['silver', { tr: 'Gümüş', en: 'Silver' }, '#c0c4cc', null, 0.01, 10, null]
  ];
  var CI = {}; COLORS.forEach(function (c, i) { CI[c[0]] = c; });
  TOOLS.color = { custom: true };

  /* ---------- SMD / kondansatör kodu (özel arayüz) ---------- */
  var EIA96_MULT = { Z: 0.001, Y: 0.01, R: 0.01, X: 0.1, S: 0.1, A: 1, B: 10, H: 10, C: 100, D: 1e3, E: 1e4, F: 1e5 };
  var CAP_TOL = { B: '±0,1 pF', C: '±0,25 pF', D: '±0,5 pF', F: '±%1', G: '±%2', J: '±%5', K: '±%10', M: '±%20', Z: '+%80 / −%20' };
  TOOLS.smd = { custom: true };

  /* =========================================================
     ARAYÜZ
     ========================================================= */
  var id = root.getAttribute('data-tool');
  var T = TOOLS[id];
  if (!T) return;
  var params = new URLSearchParams(location.search);
  var state = {};

  var el = function (tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var saveURL = function () {
    try { var u = new URL(location.href); u.search = ''; Object.keys(state).forEach(function (k) { if (state[k] !== '' && state[k] != null) u.searchParams.set(k, Array.isArray(state[k]) ? state[k].join(';') : state[k]); }); history.replaceState(null, '', u); } catch (e) {}
  };
  var actions = function () {
    var a = el('div', 'calc-actions');
    var cp = el('button', 'calc-btn', TX.copy); cp.type = 'button';
    cp.addEventListener('click', function () {
      var done = function () { cp.textContent = TX.copied; setTimeout(function () { cp.textContent = TX.copy; }, 1600); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
    });
    var rs = el('button', 'calc-btn ghost', TX.reset); rs.type = 'button';
    rs.addEventListener('click', function () { location.href = location.pathname; });
    a.appendChild(cp); a.appendChild(rs);
    return a;
  };

  /* ---------- Devre çizimleri (küçük, açıklayıcı) ---------- */
  var DIAG = {
    divider: '<svg viewBox="0 0 160 150" aria-hidden="true"><path d="M20 15h40M60 15v15m0 30v25m0 30v25M60 75h70M60 140H20" class="w"/><rect x="50" y="30" width="20" height="30" rx="3" class="r"/><rect x="50" y="85" width="20" height="30" rx="3" class="r"/><text x="78" y="49">R1</text><text x="78" y="104">R2</text><text x="6" y="19">Vin</text><text x="133" y="79">Vout</text><text x="2" y="144">GND</text></svg>',
    led: '<svg viewBox="0 0 200 90" aria-hidden="true"><path d="M10 45h30m40 0h30m30 0h50" class="w"/><rect x="40" y="35" width="40" height="20" rx="3" class="r"/><path d="M110 30v30l30-15z" class="d"/><path d="M140 30v30" class="w"/><path d="M128 22l8-8m-2 0h2v2M138 26l8-8m-2 0h2v2" class="w thin"/><text x="52" y="28">R</text><text x="112" y="80">LED</text><text x="0" y="40">+V</text></svg>',
    reg: '<svg viewBox="0 0 230 140" aria-hidden="true"><rect x="20" y="20" width="70" height="44" rx="6" class="r"/><text x="38" y="46">REG</text><path d="M90 32H210M150 32v8m0 28v18m0 28v14M150 78H55V64M125 128h50" class="w"/><circle cx="150" cy="32" r="3" class="n"/><circle cx="150" cy="78" r="3" class="n"/><rect x="140" y="40" width="20" height="28" rx="3" class="r"/><rect x="140" y="86" width="20" height="28" rx="3" class="r"/><text x="168" y="58" id="dg-up">Üst</text><text x="168" y="104" id="dg-low">Alt</text><text x="180" y="25">Vout</text><text x="62" y="94">FB/ADJ</text><text x="182" y="132">GND</text></svg>',
    rc: '<svg viewBox="0 0 200 110" aria-hidden="true"><path d="M10 30h30m40 0h70M120 30v25m0 10v30M10 95h160" class="w"/><rect x="40" y="20" width="40" height="20" rx="3" class="r"/><path d="M105 55h30M105 65h30" class="w"/><text x="54" y="14">R</text><text x="142" y="64">C</text><text x="0" y="24">in</text><text x="155" y="24">out</text></svg>',
    '555': '<svg viewBox="0 0 230 150" aria-hidden="true"><path d="M32 12h148M40 12v16m0 26v16m0 0v6m0 26v10m0 0v6m0 6v16M20 140h160M40 70h70M40 112h70M145 12v28m0 80v20M180 80h35" class="w"/><path d="M28 118h24M28 124h24" class="w"/><circle cx="40" cy="70" r="3" class="n"/><circle cx="40" cy="112" r="3" class="n"/><rect x="30" y="28" width="20" height="26" rx="3" class="r"/><rect x="30" y="76" width="20" height="26" rx="3" class="r"/><rect x="110" y="40" width="70" height="80" rx="6" class="r"/><text x="132" y="84">555</text><text x="0" y="16">VCC</text><text x="56" y="45">R1</text><text x="56" y="93">R2</text><text x="58" y="126">C</text><text x="96" y="66">7</text><text x="88" y="108">6·2</text><text x="150" y="34">8·4</text><text x="150" y="134">1</text><text x="186" y="74">out</text></svg>'
  };

  /* ---------- Genel araç arayüzü ---------- */
  var buildGeneric = function () {
    var mode = T.modes ? (params.get('m') && T.modes.some(function (m) { return m.id === params.get('m'); }) ? params.get('m') : T.modes[0].id) : null;
    var card = el('div', 'calc-card');
    var top = el('div', 'calc-top');
    if (T.presets) {
      var pr = T.presets;
      var w = el('label', 'calc-preset');
      w.appendChild(el('span', 'calc-label', L(pr.label)));
      var sel = el('select', 'calc-select');
      pr.options.forEach(function (o) { var op = el('option', null, esc(L(o[1]))); op.value = o[0]; sel.appendChild(op); });
      state[pr.id] = params.get(pr.id) || pr.options[0][0];
      sel.value = state[pr.id];
      w.appendChild(sel);
      if (pr.options[0][3]) { // renk noktası
        var sw = el('span', 'calc-swatch'); w.appendChild(sw);
        var paint = function () { var o = pr.options.filter(function (x) { return x[0] === sel.value; })[0]; sw.style.background = o[3]; };
        paint(); sel.addEventListener('change', paint);
      }
      sel.addEventListener('change', function () {
        state[pr.id] = sel.value;
        var o = pr.options.filter(function (x) { return x[0] === sel.value; })[0];
        if (pr.set && o[2] != null) { inputs[pr.set].value = o[2].replace('.', LANG === 'tr' ? ',' : '.'); state[pr.set] = inputs[pr.set].value; }
        if (T.onPreset) T.onPreset(sel.value, function (fid, val, u) {
          inputs[fid].value = val.replace('.', LANG === 'tr' ? ',' : '.'); state[fid] = inputs[fid].value;
          if (unitSel[fid] && u != null) { unitSel[fid].value = u; state[fid + '_u'] = String(u); }
        });
        refresh();
      });
      top.appendChild(w);
    }
    if (T.modes) {
      var segw = el('div', 'calc-modewrap');
      segw.appendChild(el('span', 'calc-label', L(T.modeLabel) || TX.mode));
      var seg = el('div', 'seg');
      T.modes.forEach(function (m) {
        var b = el('button', 'seg-btn', esc(L(m.label))); b.type = 'button'; b.setAttribute('data-mode', m.id);
        b.addEventListener('click', function () { mode = m.id; refresh(); });
        seg.appendChild(b);
      });
      segw.appendChild(seg); top.appendChild(segw);
    }
    if (top.children.length) card.appendChild(top);

    var grid = el('div', 'calc-grid');
    var left = el('div', 'calc-inputs');
    var right = el('div', 'calc-results');
    grid.appendChild(left); grid.appendChild(right); card.appendChild(grid);
    if (T.diagram && DIAG[T.diagram]) { var dg = el('div', 'calc-diagram', DIAG[T.diagram]); left.appendChild(dg); }

    var inputs = {}, unitSel = {}, rows = {}, labels = {};
    T.fields.forEach(function (f) {
      var row = el('div', 'calc-field'); rows[f.id] = row;
      var lab = el('label', 'calc-label'); labels[f.id] = lab; row.appendChild(lab);
      if (f.type === 'seg') {
        var sg = el('div', 'seg sm');
        state[f.id] = params.get(f.id) || f.def;
        f.options.forEach(function (o) {
          var b = el('button', 'seg-btn', esc(L(o[1]))); b.type = 'button'; b.setAttribute('data-v', o[0]);
          b.addEventListener('click', function () {
            if (T.listDefs && state[f.id] !== o[0]) T.fields.forEach(function (lf) { if (lf.type === 'list') { state[lf.id] = T.listDefs[o[0]].slice(); lf._draw(); } });
            state[f.id] = o[0]; refresh();
          });
          sg.appendChild(b);
        });
        inputs[f.id] = sg; row.appendChild(sg);
      } else if (f.type === 'select') {
        var s = el('select', 'calc-select');
        f.options.forEach(function (o) { var op = el('option', null, esc(L(o[1]))); op.value = o[0]; s.appendChild(op); });
        state[f.id] = params.get(f.id) || f.def; s.value = state[f.id];
        s.addEventListener('change', function () { state[f.id] = s.value; refresh(); });
        inputs[f.id] = s; row.appendChild(s);
      } else if (f.type === 'list') {
        var box = el('div', 'calc-list');
        var vals = params.get(f.id) ? params.get(f.id).split(';') : f.def.slice();
        state[f.id] = vals;
        var draw = function () {
          box.innerHTML = '';
          state[f.id].forEach(function (val, i) {
            var r = el('div', 'calc-input');
            var inp = el('input'); inp.type = 'text'; inp.inputMode = 'decimal'; inp.value = val; inp.setAttribute('aria-label', L(f.label) + ' ' + (i + 1));
            inp.addEventListener('input', function () { state[f.id][i] = inp.value; refresh(true); });
            r.appendChild(inp);
            var u = el('span', 'calc-unit-static'); u.setAttribute('data-q', '1'); r.appendChild(u);
            if (state[f.id].length > 2) {
              var x = el('button', 'calc-x', '×'); x.type = 'button'; x.setAttribute('aria-label', LANG === 'tr' ? 'Sil' : 'Remove');
              x.addEventListener('click', function () { state[f.id].splice(i, 1); draw(); refresh(); });
              r.appendChild(x);
            }
            box.appendChild(r);
          });
          if (state[f.id].length < 10) {
            var add = el('button', 'calc-add', LANG === 'tr' ? '+ Değer ekle' : '+ Add value'); add.type = 'button';
            add.addEventListener('click', function () { state[f.id].push(''); draw(); var ins = box.querySelectorAll('input'); ins[ins.length - 1].focus(); });
            box.appendChild(add);
          }
          paintListUnits();
        };
        var paintListUnits = function () { var q = f.q(state); box.querySelectorAll('[data-q]').forEach(function (u) { u.textContent = q; }); };
        f._draw = draw; f._paint = paintListUnits;
        row.appendChild(box); inputs[f.id] = box;
        draw();
      } else {
        var wrap = el('div', 'calc-input');
        var inp = el('input'); inp.type = 'text'; inp.inputMode = 'decimal'; inp.autocomplete = 'off'; inp.id = 'f-' + f.id;
        var pv = params.get(f.id);
        inp.value = pv != null ? pv : (f.def || '').replace('.', LANG === 'tr' ? ',' : '.');
        if (f.optional) inp.placeholder = TX.optional;
        lab.setAttribute('for', inp.id);
        inp.addEventListener('input', function () { state[f.id] = inp.value; refresh(true); });
        state[f.id] = inp.value;
        wrap.appendChild(inp); inputs[f.id] = inp;
        if (f.q && UNITS[f.q]) {
          var us = el('select', 'calc-unit');
          UNITS[f.q].forEach(function (u, i) { var op = el('option', null, LANG === 'en' && u[2] ? u[2] : u[0]); op.value = i; us.appendChild(op); });
          var defU = f.du != null ? f.du : 1;
          var pu = params.get(f.id + '_u');
          us.value = pu != null ? pu : defU;
          state[f.id + '_u'] = us.value;
          us.setAttribute('aria-label', L(f.label) + (LANG === 'tr' ? ' birimi' : ' unit'));
          us.addEventListener('change', function () { state[f.id + '_u'] = us.value; refresh(); });
          unitSel[f.id] = us; wrap.appendChild(us);
        } else if (f.unit) {
          wrap.appendChild(el('span', 'calc-unit-static', esc(L(f.unit))));
        }
        row.appendChild(wrap);
      }
      if (f.hint) row.appendChild(el('div', 'calc-hint', esc(L(f.hint))));
      left.appendChild(row);
    });

    var valueOf = function (f) {
      if (f.type === 'list') { var mult = 1; return state[f.id].map(function (s) { return parseNum(s) * mult; }); }
      if (f.type === 'seg' || f.type === 'select') return state[f.id];
      var x = parseNum(state[f.id]);
      if (f.q && UNITS[f.q]) x *= UNITS[f.q][parseInt(state[f.id + '_u'], 10)][1];
      return x;
    };

    var refresh = function (typing) {
      // görünürlük ve etiketler
      var show = T.modes ? T.modes.filter(function (m) { return m.id === mode; })[0].show : null;
      if (T.modes) {
        card.querySelectorAll('[data-mode]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-mode') === mode ? 'true' : 'false'); });
        state.m = mode;
      }
      T.fields.forEach(function (f) {
        var vis = (!show || show.indexOf(f.id) > -1 || f.type === 'seg' && !show) && !(f.hidden && f.hidden(state, mode));
        if (show && f.type !== 'seg' && f.type !== 'select' && show.indexOf(f.id) < 0) vis = false;
        if (show && (f.type === 'seg' || f.type === 'select') && show.indexOf(f.id) < 0 && !(T.modes && T.modes.every(function (m) { return m.show.indexOf(f.id) < 0; }))) vis = false;
        if (f.hidden && f.hidden(state, mode)) vis = false;
        rows[f.id].hidden = !vis;
        labels[f.id].innerHTML = esc(L(typeof f.label === 'function' ? f.label(state) : f.label)) + (f.optional ? ' <span class="opt">(' + TX.optional + ')</span>' : '');
        if (f.type === 'seg') inputs[f.id].querySelectorAll('[data-v]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === state[f.id] ? 'true' : 'false'); });
        if (f.type === 'list' && f._paint) f._paint();
      });
      var dgu = card.querySelector('#dg-up'), dgl = card.querySelector('#dg-low');
      if (dgu && state.chip) { dgu.textContent = LANG === 'tr' ? 'Üst' : 'Top'; dgl.textContent = LANG === 'tr' ? 'Alt' : 'Bot'; }
      // değerler
      var v = {}, ok = true;
      T.fields.forEach(function (f) {
        if (rows[f.id].hidden) return;
        v[f.id] = valueOf(f);
        var bad = f.type !== 'list' && f.type !== 'seg' && f.type !== 'select' && !f.optional && !isFinite(v[f.id]);
        if (inputs[f.id].classList) inputs[f.id].classList.toggle('bad', bad && state[f.id] !== '');
        if (bad) ok = false;
      });
      right.innerHTML = '';
      right.appendChild(el('div', 'calc-res-title', TX.results));
      if (!ok) { right.appendChild(el('p', 'calc-empty', TX.fill)); right.appendChild(actions()); saveURL(); return; }
      var out = T.calc(v, mode, state) || {};
      var list = el('div', 'calc-res-list');
      (out.results || []).forEach(function (r) {
        var it = el('div', 'res' + (r.primary ? ' primary' : '') + (r.accent ? ' accent' : ''));
        it.appendChild(el('div', 'res-label', esc(L(r.label))));
        it.appendChild(el('div', 'res-value', esc(r.value)));
        if (r.sub) it.appendChild(el('div', 'res-sub', esc(r.sub)));
        list.appendChild(it);
      });
      right.appendChild(list);
      (out.warn || []).forEach(function (w) { right.appendChild(el('div', 'calc-note warn', '⚠ ' + esc(L(w)))); });
      (out.info || []).forEach(function (w) { right.appendChild(el('div', 'calc-note', 'ⓘ ' + esc(L(w)))); });
      right.appendChild(actions());
      saveURL();
    };
    root.innerHTML = '';
    root.appendChild(card);
    refresh();
  };

  /* ---------- Renk kodu arayüzü ---------- */
  var buildColor = function () {
    var bandsN = parseInt(params.get('n') || '4', 10); if ([4, 5, 6].indexOf(bandsN) < 0) bandsN = 4;
    var sel = (params.get('b') || '').split(',').filter(Boolean);
    var defaults = { 4: ['yellow', 'violet', 'red', 'gold'], 5: ['brown', 'black', 'black', 'brown', 'brown'], 6: ['brown', 'black', 'black', 'brown', 'brown', 'brown'] };
    if (sel.length !== bandsN) sel = defaults[bandsN].slice();
    var card = el('div', 'calc-card');
    var top = el('div', 'calc-top');
    var segw = el('div', 'calc-modewrap'); segw.appendChild(el('span', 'calc-label', LANG === 'tr' ? 'Bant sayısı' : 'Number of bands'));
    var seg = el('div', 'seg'); [4, 5, 6].forEach(function (n) {
      var b = el('button', 'seg-btn', n + (LANG === 'tr' ? ' bant' : ' bands')); b.type = 'button'; b.setAttribute('data-n', n);
      b.addEventListener('click', function () { bandsN = n; sel = defaults[n].slice(); draw(); }); seg.appendChild(b);
    });
    segw.appendChild(seg); top.appendChild(segw);
    var rev = el('label', 'calc-preset'); rev.appendChild(el('span', 'calc-label', LANG === 'tr' ? 'Değerden renk bul' : 'Find colours from value'));
    var rin = el('div', 'calc-input'); var ri = el('input'); ri.type = 'text'; ri.placeholder = LANG === 'tr' ? 'ör. 4k7, 220, 1M' : 'e.g. 4k7, 220, 1M'; rin.appendChild(ri);
    rin.appendChild(el('span', 'calc-unit-static', 'Ω')); rev.appendChild(rin); top.appendChild(rev);
    card.appendChild(top);
    var stage = el('div', 'rc-stage'); card.appendChild(stage);
    var picker = el('div', 'rc-picker'); card.appendChild(picker);
    var right = el('div', 'calc-results wide'); card.appendChild(right);
    root.innerHTML = ''; root.appendChild(card);

    var roleOf = function (i) {
      var digits = bandsN === 4 ? 2 : 3;
      if (i < digits) return 'digit';
      if (i === digits) return 'mult';
      if (i === digits + 1) return 'tol';
      return 'tc';
    };
    var roleName = { digit: { tr: 'Hane', en: 'Digit' }, mult: { tr: 'Çarpan', en: 'Multiplier' }, tol: { tr: 'Tolerans', en: 'Tolerance' }, tc: { tr: 'Sıcaklık katsayısı', en: 'Temp. coefficient' } };
    var allowed = function (role, i) {
      return COLORS.filter(function (c) {
        if (role === 'digit') return c[3] != null && !(i === 0 && c[3] === 0);
        if (role === 'mult') return c[4] != null;
        if (role === 'tol') return c[5] != null;
        return c[6] != null;
      });
    };
    var draw = function () {
      seg.querySelectorAll('[data-n]').forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-n') === bandsN ? 'true' : 'false'); });
      // direnç çizimi
      var xs = bandsN === 4 ? [92, 122, 152, 226] : bandsN === 5 ? [86, 112, 138, 164, 226] : [80, 104, 128, 152, 204, 232];
      var svg = '<svg viewBox="0 0 320 110" class="rc-svg" role="img" aria-label="' + (LANG === 'tr' ? 'Direnç' : 'Resistor') + '"><defs><linearGradient id="rcb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e7d6b5"/><stop offset=".5" stop-color="#cdb48a"/><stop offset="1" stop-color="#a88c60"/></linearGradient><linearGradient id="rcs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient></defs>' +
        '<path d="M0 55h62M258 55h62" stroke="#9aa6bb" stroke-width="5" stroke-linecap="round"/>' +
        '<path d="M70 30q-12 0-12 25t12 25h14q8 0 12-6h128q4 6 12 6h14q12 0 12-25t-12-25h-14q-8 0-12 6H96q-4-6-12-6z" fill="url(#rcb)"/>';
      sel.forEach(function (c, i) { svg += '<rect x="' + xs[i] + '" y="' + (i === 0 || i === bandsN - 1 ? 30 : 36) + '" width="14" height="' + (i === 0 || i === bandsN - 1 ? 50 : 38) + '" fill="' + CI[c][2] + '"/>'; });
      svg += '<path d="M70 30q-12 0-12 25t12 25h14q8 0 12-6h128q4 6 12 6h14q12 0 12-25t-12-25h-14q-8 0-12 6H96q-4-6-12-6z" fill="url(#rcs)"/></svg>';
      stage.innerHTML = svg;
      // seçiciler
      picker.innerHTML = '';
      sel.forEach(function (c, i) {
        var role = roleOf(i);
        var col = el('div', 'rc-col');
        col.appendChild(el('div', 'rc-col-title', (i + 1) + '. ' + esc(L(roleName[role]))));
        var grid = el('div', 'rc-swatches');
        allowed(role, i).forEach(function (cc) {
          var b = el('button', 'rc-sw'); b.type = 'button'; b.style.setProperty('--c', cc[2]);
          b.title = L(cc[1]); b.setAttribute('aria-label', L(cc[1]));
          b.setAttribute('aria-pressed', cc[0] === c ? 'true' : 'false');
          b.addEventListener('click', function () { sel[i] = cc[0]; draw(); });
          grid.appendChild(b);
        });
        col.appendChild(grid);
        col.appendChild(el('div', 'rc-col-name', esc(L(CI[c][1]))));
        picker.appendChild(col);
      });
      // sonuç
      var digits = bandsN === 4 ? 2 : 3, num = 0;
      for (var k = 0; k < digits; k++) num = num * 10 + CI[sel[k]][3];
      var val = num * CI[sel[digits]][4], tol = CI[sel[digits + 1]][5];
      right.innerHTML = '';
      right.appendChild(el('div', 'calc-res-title', TX.results));
      var list = el('div', 'calc-res-list cols');
      var add = function (lab, v, primary, sub) { var it = el('div', 'res' + (primary ? ' primary' : '')); it.appendChild(el('div', 'res-label', esc(lab))); it.appendChild(el('div', 'res-value', esc(v))); if (sub) it.appendChild(el('div', 'res-sub', esc(sub))); list.appendChild(it); };
      add(LANG === 'tr' ? 'Direnç değeri' : 'Resistance', fmtSI(val, 'Ω'), true);
      add(LANG === 'tr' ? 'Tolerans' : 'Tolerance', '±' + pct(NF(tol)), true);
      add(LANG === 'tr' ? 'Aralık' : 'Range', fmtSI(val * (1 - tol / 100), 'Ω') + ' – ' + fmtSI(val * (1 + tol / 100), 'Ω'));
      if (bandsN === 6) add(LANG === 'tr' ? 'Sıcaklık katsayısı' : 'Temperature coefficient', CI[sel[5]][6] + ' ppm/°C');
      right.appendChild(list);
      right.appendChild(actions());
      state = { n: bandsN, b: sel.join(',') };
      saveURL();
    };
    ri.addEventListener('input', function () {
      var x = parseNum(ri.value);
      if (!(x > 0)) return;
      var digits = bandsN === 4 ? 2 : 3;
      var exp = Math.floor(Math.log10(x)) - (digits - 1);
      var mant = Math.round(x / Math.pow(10, exp));
      if (mant >= Math.pow(10, digits)) { mant /= 10; exp += 1; }
      if (exp < -2 || exp > 9) return;
      var ds = String(mant).split('').map(Number);
      var dn = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'grey', 'white'];
      var mult = exp === -1 ? 'gold' : exp === -2 ? 'silver' : dn[exp];
      for (var k = 0; k < digits; k++) sel[k] = dn[ds[k]];
      sel[digits] = mult;
      draw();
    });
    draw();
  };

  /* ---------- SMD kodu arayüzü ---------- */
  var decodeRes = function (code) {
    var c = code.trim().toUpperCase().replace(/\s/g, '');
    if (!c) return null;
    var m;
    if ((m = c.match(/^(\d{2})([ZYRXSABHCDEF])$/))) {
      var i = parseInt(m[1], 10); if (i < 1 || i > 96) return { err: true };
      return { v: E96[i - 1] * 100 * EIA96_MULT[m[2]], sys: 'EIA-96 (±' + pct('1') + ')' };
    }
    if (/^\d*R\d*$/.test(c) && c.length >= 2) return { v: parseFloat(c.replace('R', '.')) || 0, sys: LANG === 'tr' ? 'R = ondalık nokta' : 'R = decimal point' };
    if ((m = c.match(/^(\d{2})(\d)$/))) return { v: parseInt(m[1], 10) * Math.pow(10, +m[2]), sys: LANG === 'tr' ? '3 haneli (±%5)' : '3-digit (±5%)' };
    if ((m = c.match(/^(\d{3})(\d)$/))) return { v: parseInt(m[1], 10) * Math.pow(10, +m[2]), sys: LANG === 'tr' ? '4 haneli (±%1)' : '4-digit (±1%)' };
    if (c === '0' || c === '000' || c === '0000') return { v: 0, sys: LANG === 'tr' ? 'Sıfır ohm (köprü)' : 'Zero-ohm (jumper)' };
    return { err: true };
  };
  var decodeCap = function (code) {
    var c = code.trim().toUpperCase().replace(/\s/g, '');
    if (!c) return null;
    var m = c.match(/^(\d)R(\d)([A-Z]?)$/);
    if (m) return { v: parseFloat(m[1] + '.' + m[2]) * 1e-12, tol: CAP_TOL[m[3]] };
    m = c.match(/^(\d{2})(\d)([A-Z]?)$/);
    if (m) { var mult = +m[2] === 8 ? 0.01 : +m[2] === 9 ? 0.1 : Math.pow(10, +m[2]); return { v: parseInt(m[1], 10) * mult * 1e-12, tol: CAP_TOL[m[3]] }; }
    m = c.match(/^(\d{1,2})([A-Z]?)$/);
    if (m) return { v: parseInt(m[1], 10) * 1e-12, tol: CAP_TOL[m[2]] };
    return { err: true };
  };
  var buildSMD = function () {
    var kind = params.get('k') === 'c' ? 'c' : 'r';
    var card = el('div', 'calc-card');
    var top = el('div', 'calc-top');
    var segw = el('div', 'calc-modewrap'); segw.appendChild(el('span', 'calc-label', LANG === 'tr' ? 'Bileşen' : 'Component'));
    var seg = el('div', 'seg');
    [['r', LANG === 'tr' ? 'SMD direnç' : 'SMD resistor'], ['c', LANG === 'tr' ? 'Kondansatör' : 'Capacitor']].forEach(function (o) {
      var b = el('button', 'seg-btn', o[1]); b.type = 'button'; b.setAttribute('data-k', o[0]);
      b.addEventListener('click', function () { kind = o[0]; inp.value = kind === 'r' ? '103' : '104'; upd(); }); seg.appendChild(b);
    });
    segw.appendChild(seg); top.appendChild(segw); card.appendChild(top);
    var grid = el('div', 'calc-grid'); var left = el('div', 'calc-inputs'); var right = el('div', 'calc-results');
    var row = el('div', 'calc-field'); row.appendChild(el('label', 'calc-label', LANG === 'tr' ? 'Üzerindeki kod' : 'Marking code'));
    var w = el('div', 'calc-input big'); var inp = el('input'); inp.type = 'text'; inp.autocomplete = 'off'; inp.spellcheck = false;
    inp.value = params.get('c') || '103'; w.appendChild(inp); row.appendChild(w);
    var hint = el('div', 'calc-hint'); row.appendChild(hint); left.appendChild(row);
    var ex = el('div', 'calc-examples'); left.appendChild(ex);
    grid.appendChild(left); grid.appendChild(right); card.appendChild(grid);
    root.innerHTML = ''; root.appendChild(card);
    var upd = function () {
      seg.querySelectorAll('[data-k]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-k') === kind ? 'true' : 'false'); });
      hint.textContent = kind === 'r'
        ? (LANG === 'tr' ? '3 haneli (103), 4 haneli (1002), R\'li (4R7) ve EIA-96 (01C) kodlarını tanır.' : 'Understands 3-digit (103), 4-digit (1002), R-notation (4R7) and EIA-96 (01C) codes.')
        : (LANG === 'tr' ? 'Seramik kondansatör kodu: 104, 473J, 2R2… (pF cinsinden)' : 'Ceramic capacitor codes: 104, 473J, 2R2… (in pF)');
      ex.innerHTML = '';
      (kind === 'r' ? ['103', '4702', '4R7', '01C', '68X'] : ['104', '103', '471', '225K', '2R2']).forEach(function (c) {
        var b = el('button', 'chip-sm btn-chip', c); b.type = 'button'; b.addEventListener('click', function () { inp.value = c; upd(); }); ex.appendChild(b);
      });
      var r = kind === 'r' ? decodeRes(inp.value) : decodeCap(inp.value);
      right.innerHTML = ''; right.appendChild(el('div', 'calc-res-title', TX.results));
      inp.parentNode.classList.toggle('bad', !!(r && r.err));
      if (!r) { right.appendChild(el('p', 'calc-empty', TX.fill)); }
      else if (r.err) { right.appendChild(el('div', 'calc-note warn', '⚠ ' + (LANG === 'tr' ? 'Bu kodu tanıyamadım. Kodu tekrar kontrol et.' : 'Could not read this code. Please check it.'))); }
      else {
        var list = el('div', 'calc-res-list');
        var add = function (lab, v, p) { var it = el('div', 'res' + (p ? ' primary' : '')); it.appendChild(el('div', 'res-label', esc(lab))); it.appendChild(el('div', 'res-value', esc(v))); list.appendChild(it); };
        if (kind === 'r') { add(LANG === 'tr' ? 'Direnç değeri' : 'Resistance', fmtSI(r.v, 'Ω'), true); add(LANG === 'tr' ? 'Kod sistemi' : 'Code system', r.sys); }
        else {
          add(LANG === 'tr' ? 'Kapasite' : 'Capacitance', fmtSI(r.v, 'F'), true);
          add('pF', NF(r.v * 1e12, 6) + ' pF'); add('nF / µF', NF(r.v * 1e9, 6) + ' nF · ' + NF(r.v * 1e6, 6) + ' µF');
          if (r.tol) add(LANG === 'tr' ? 'Tolerans' : 'Tolerance', LANG === 'tr' ? r.tol : r.tol.replace(/%(\d+)/g, '$1%').replace(/,/g, '.'));
        }
        right.appendChild(list);
      }
      right.appendChild(actions());
      state = { k: kind, c: inp.value }; saveURL();
    };
    inp.addEventListener('input', upd);
    upd();
  };

  if (id === 'color') buildColor();
  else if (id === 'smd') buildSMD();
  else buildGeneric();
})();
