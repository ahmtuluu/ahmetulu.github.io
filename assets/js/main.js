/* =========================================================
   ahmetulu.com.tr — ortak script
   - Mobil menü
   - Ana sayfa yazı makinesi efekti
   - Arka plan devre kartı animasyonu (telefonda hafif)
   - İletişim formu
   - Yazılardaki fotoğrafları büyütme
   ========================================================= */
(function () {
  'use strict';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobil menü ---------- */
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    var closeMenu = function () {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    };
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav-links a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
    window.addEventListener('resize', function () { if (window.innerWidth > 760) closeMenu(); });
  }

  /* ---------- Yazı makinesi (ana sayfa) ---------- */
  var title = document.getElementById('homeTitle');
  if (title) {
    var reveals = document.querySelectorAll('.reveal');
    var showRest = function () { reveals.forEach(function (el) { el.classList.add('show'); }); };
    if (reduceMotion) {
      showRest();
    } else {
      var lines = [].map.call(title.querySelectorAll('.tline'), function (el) {
        return { text: el.textContent, tag: el.tagName.toLowerCase() };
      });
      title.style.minHeight = title.offsetHeight + 'px';
      title.innerHTML = '';
      var li = 0, ci = 0, current = null;
      var cursor = document.createElement('span');
      cursor.className = 'cursor-blink';
      cursor.setAttribute('aria-hidden', 'true');
      var label = document.querySelector('.home-label');
      if (label) setTimeout(function () { label.classList.add('show'); }, 250);
      var type = function () {
        if (li >= lines.length) {
          cursor.remove();
          setTimeout(showRest, 150);
          return;
        }
        if (ci === 0) {
          current = document.createElement(lines[li].tag);
          current.className = 'tline';
          title.appendChild(current);
          current.appendChild(cursor);
        }
        current.insertBefore(document.createTextNode(lines[li].text[ci]), cursor);
        ci++;
        if (ci >= lines[li].text.length) { li++; ci = 0; setTimeout(type, 300); }
        else setTimeout(type, 50);
      };
      setTimeout(type, 500);
    }
  }

  /* ---------- Devre kartı animasyonu ---------- */
  var canvas = document.getElementById('circuit-canvas');
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d');
    var W = 0, H = 0, frame = 0, lastW = 0, lastDraw = 0;
    var nodes = [], clines = [], chips = [], resistors = [];
    var small = false;
    var GOLD = '212,165,116';

    var init = function () {
      small = window.innerWidth < 760;
      W = canvas.width = window.innerWidth;
      // Telefonda adres çubuğu açılıp kapanınca yeniden çizmemek için biraz fazla yükseklik
      H = canvas.height = Math.max(window.innerHeight, document.documentElement.clientHeight) + (small ? 120 : 0);
      canvas.style.height = H + 'px';
      lastW = W;
      nodes = []; clines = []; chips = []; resistors = [];
      var g = small ? 64 : 56;
      var keep = small ? 0.5 : 0.62;
      var cols = Math.ceil(W / g) + 1, rows = Math.ceil(H / g) + 1;
      var grid = {};
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          if (Math.random() < keep) {
            grid[r + ',' + c] = nodes.length;
            nodes.push({
              x: c * g + (Math.random() * 8 - 4), y: r * g + (Math.random() * 8 - 4),
              pulse: Math.random() * Math.PI * 2, spd: 0.003 + Math.random() * 0.004,
              via: Math.random() > 0.85
            });
          }
        }
      }
      // Sadece yatay/dikey komşular (PCB izi gibi)
      for (var key in grid) {
        var p = key.split(','), rr = +p[0], cc = +p[1], a = grid[key];
        [[rr, cc + 1], [rr + 1, cc]].forEach(function (n) {
          var b = grid[n[0] + ',' + n[1]];
          if (b !== undefined && Math.random() > 0.35) {
            clines.push({ a: a, b: b, prog: 0, spd: 0.0015 + Math.random() * 0.002, delay: Math.floor(Math.random() * 200), signal: Math.random(), sigSpd: 0.003 + Math.random() * 0.005 });
          }
        });
      }
      var chipCount = Math.floor(W * H / (small ? 200000 : 120000));
      for (var i = 0; i < chipCount; i++) {
        var w = 30 + Math.floor(Math.random() * 30), h = 20 + Math.floor(Math.random() * 20);
        chips.push({ x: Math.random() * (W - 80) + 40, y: Math.random() * (H - 60) + 30, w: w, h: h, pulse: Math.random() * Math.PI * 2, spd: 0.002 + Math.random() * 0.003, pins: Math.floor(w / 8) });
      }
      var resCount = Math.floor(W * H / (small ? 110000 : 60000));
      for (var j = 0; j < resCount; j++) {
        resistors.push({ x: Math.random() * (W - 60) + 30, y: Math.random() * (H - 40) + 20, rot: Math.random() > 0.5 ? 0 : Math.PI / 2, pulse: Math.random() * Math.PI * 2, spd: 0.002 + Math.random() * 0.003 });
      }
      if (reduceMotion) { clines.forEach(function (l) { l.prog = 1; }); drawFrame(); }
    };

    var drawFrame = function () {
      ctx.clearRect(0, 0, W, H);
      frame++;
      var i, l, na, nb, g;
      // İzler: tek seferde çiz
      ctx.beginPath();
      for (i = 0; i < clines.length; i++) {
        l = clines[i];
        if (!reduceMotion && frame > l.delay) l.prog = Math.min(1, l.prog + l.spd);
        if (l.prog <= 0) continue;
        na = nodes[l.a]; nb = nodes[l.b];
        ctx.moveTo(na.x, na.y);
        ctx.lineTo(na.x + (nb.x - na.x) * l.prog, na.y + (nb.y - na.y) * l.prog);
      }
      ctx.strokeStyle = 'rgba(' + GOLD + ',0.08)';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      // Sinyaller
      if (!reduceMotion) {
        ctx.beginPath();
        for (i = 0; i < clines.length; i++) {
          l = clines[i];
          if (l.prog < 1) continue;
          l.signal += l.sigSpd; if (l.signal > 1) l.signal = 0;
          na = nodes[l.a]; nb = nodes[l.b];
          var sx = na.x + (nb.x - na.x) * l.signal, sy = na.y + (nb.y - na.y) * l.signal;
          ctx.moveTo(sx + 1.5, sy);
          ctx.arc(sx, sy, 1.5, 0, Math.PI * 2);
        }
        ctx.fillStyle = 'rgba(' + GOLD + ',0.4)';
        ctx.fill();
      }
      // Pad ve via'lar
      ctx.lineWidth = 1;
      for (i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.pulse += n.spd;
        g = 0.12 + Math.sin(n.pulse) * 0.06;
        ctx.strokeStyle = 'rgba(' + GOLD + ',' + g + ')';
        if (n.via) {
          ctx.beginPath(); ctx.arc(n.x, n.y, 4, 0, Math.PI * 2); ctx.stroke();
          ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 0.8) + ')';
          ctx.beginPath(); ctx.arc(n.x, n.y, 1.5, 0, Math.PI * 2); ctx.fill();
        } else {
          ctx.strokeRect(n.x - 3, n.y - 3, 6, 6);
          ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 0.4) + ')';
          ctx.fillRect(n.x - 1.5, n.y - 1.5, 3, 3);
        }
      }
      // Çipler
      for (i = 0; i < chips.length; i++) {
        var c = chips[i];
        c.pulse += c.spd;
        g = 0.1 + Math.sin(c.pulse) * 0.04;
        var cx = c.x - c.w / 2, cy = c.y - c.h / 2;
        ctx.strokeStyle = 'rgba(' + GOLD + ',' + g + ')';
        ctx.strokeRect(cx, cy, c.w, c.h);
        ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 0.15) + ')';
        ctx.fillRect(cx, cy, c.w, c.h);
        ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 1.2) + ')';
        for (var p = 0; p < c.pins; p++) {
          var px = cx + 8 + p * 8;
          if (px > cx + c.w - 4) break;
          ctx.fillRect(px - 1.5, cy - 4, 3, 4);
          ctx.fillRect(px - 1.5, cy + c.h, 3, 4);
        }
      }
      // Dirençler
      for (i = 0; i < resistors.length; i++) {
        var r = resistors[i];
        r.pulse += r.spd;
        g = 0.1 + Math.sin(r.pulse) * 0.05;
        ctx.save();
        ctx.translate(r.x, r.y); ctx.rotate(r.rot);
        ctx.strokeStyle = 'rgba(' + GOLD + ',' + g + ')';
        ctx.strokeRect(-12, -4, 24, 8);
        ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 0.2) + ')';
        ctx.fillRect(-12, -4, 24, 8);
        ctx.fillStyle = 'rgba(' + GOLD + ',' + (g * 1.5) + ')';
        ctx.fillRect(-18, -3, 6, 6); ctx.fillRect(12, -3, 6, 6);
        ctx.restore();
      }
    };

    var loop = function (t) {
      requestAnimationFrame(loop);
      // Telefonda ~30 fps yeterli; pil dostu
      if (small && t - lastDraw < 32) return;
      lastDraw = t;
      drawFrame();
    };

    init();
    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        // Sadece genişlik değişince (ör. telefon yan çevrilince) yeniden kur
        if (window.innerWidth !== lastW) init();
      }, 200);
    });
    setTimeout(function () {
      canvas.classList.add('show');
      if (!reduceMotion) requestAnimationFrame(loop);
    }, 500);
  }

  /* ---------- İletişim formu ---------- */
  var form = document.getElementById('contactForm');
  if (form) {
    var ok = document.getElementById('formSuccess');
    var err = document.getElementById('formError');
    var btn = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      err.classList.remove('show');
      btn.disabled = true;
      var oldText = btn.textContent;
      btn.textContent = 'Gönderiliyor…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('hata');
          form.style.display = 'none';
          ok.classList.add('show');
        })
        .catch(function () {
          err.classList.add('show');
          btn.disabled = false;
          btn.textContent = oldText;
        });
    });
  }

  /* ---------- Fotoğraf büyütme ---------- */
  var imgs = document.querySelectorAll('.blog-img');
  if (imgs.length) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Fotoğraf');
    box.innerHTML = '<button class="lightbox-close" aria-label="Kapat">×</button><img alt="">';
    document.body.appendChild(box);
    var big = box.querySelector('img');
    var close = function () { box.classList.remove('open'); document.body.style.overflow = ''; };
    imgs.forEach(function (img) {
      img.setAttribute('tabindex', '0');
      var open = function () {
        big.src = img.currentSrc || img.src; big.alt = img.alt;
        box.classList.add('open'); document.body.style.overflow = 'hidden';
      };
      img.addEventListener('click', open);
      img.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
    box.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }
})();
