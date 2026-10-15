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

  /* ---------- Devre kartı animasyonu (sadece ana sayfa) ----------
     - Soluk PCB izleri, pad'ler, çipler ve dirençler
     - İzler boyunca ilerleyen parlak "akım darbeleri"
     - Masaüstünde fareyi takip eden hafif ışık
     - Aşağı kaydırdıkça animasyon yavaşça soluklaşır, içerik okunur kalır */
  var canvas = document.getElementById('circuit-canvas');
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext('2d');
    var W = 0, H = 0, frame = 0, lastW = 0, lastDraw = 0;
    var nodes = [], clines = [], chips = [], resistors = [], adj = [], pulses = [];
    var small = false;
    var GOLD = '212,165,116';
    var mouse = { x: -9999, y: -9999, on: false };

    var init = function () {
      small = window.innerWidth < 760;
      W = canvas.width = window.innerWidth;
      // Telefonda adres çubuğu açılıp kapanınca yeniden çizmemek için biraz fazla yükseklik
      H = canvas.height = Math.max(window.innerHeight, document.documentElement.clientHeight) + (small ? 120 : 0);
      canvas.style.height = H + 'px';
      lastW = W;
      nodes = []; clines = []; chips = []; resistors = []; adj = []; pulses = [];
      var g = small ? 64 : 56;
      var keep = small ? 0.5 : 0.62;
      var cols = Math.ceil(W / g) + 1, rows = Math.ceil(H / g) + 1;
      var grid = {};
      for (var r = 0; r < rows; r++) {
        for (var c = 0; c < cols; c++) {
          if (Math.random() < keep) {
            grid[r + ',' + c] = nodes.length;
            adj.push([]);
            nodes.push({
              x: c * g + (Math.random() * 8 - 4), y: r * g + (Math.random() * 8 - 4),
              pulse: Math.random() * Math.PI * 2, spd: 0.003 + Math.random() * 0.004,
              via: Math.random() > 0.85, flash: 0
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
            clines.push({ a: a, b: b, prog: 0, spd: 0.0015 + Math.random() * 0.002, delay: Math.floor(Math.random() * 200) });
            adj[a].push(b); adj[b].push(a);
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

    /* Akım darbeleri: bir pad'den başlayıp izler boyunca rastgele yol alır */
    var MAX_PULSES = function () { return small ? 3 : 7; };
    var spawnPulse = function () {
      var tries = 20, start;
      while (tries--) { start = Math.floor(Math.random() * nodes.length); if (adj[start] && adj[start].length) break; }
      if (!adj[start] || !adj[start].length) return;
      var next = adj[start][Math.floor(Math.random() * adj[start].length)];
      pulses.push({ from: start, to: next, t: 0, speed: 0.03 + Math.random() * 0.025, steps: 14 + Math.floor(Math.random() * 18), trail: [], life: 1 });
    };
    var stepPulse = function (pl) {
      pl.t += pl.speed;
      if (pl.t >= 1) {
        nodes[pl.to].flash = 1;
        pl.steps--;
        var opts = adj[pl.to].filter(function (n) { return n !== pl.from; });
        if (!opts.length || pl.steps <= 0) { pl.dying = true; pl.t = 1; }
        else { pl.from = pl.to; pl.to = opts[Math.floor(Math.random() * opts.length)]; pl.t = 0; }
      }
      var a = nodes[pl.from], b = nodes[pl.to], t = Math.min(pl.t, 1);
      var x = a.x + (b.x - a.x) * t, y = a.y + (b.y - a.y) * t;
      if (!pl.dying) pl.trail.push(x, y);
      if (pl.trail.length > 44 || (pl.dying && pl.trail.length)) pl.trail.splice(0, 2);
      return !(pl.dying && pl.trail.length === 0);
    };
    var drawPulse = function (pl) {
      var tr = pl.trail, n = tr.length / 2;
      if (n < 2) return;
      ctx.lineCap = 'round';
      for (var k = 1; k < n; k++) {
        var al = (k / n) * 0.55;
        ctx.strokeStyle = 'rgba(' + GOLD + ',' + al + ')';
        ctx.lineWidth = 1 + (k / n) * 1.6;
        ctx.beginPath(); ctx.moveTo(tr[(k - 1) * 2], tr[(k - 1) * 2 + 1]); ctx.lineTo(tr[k * 2], tr[k * 2 + 1]); ctx.stroke();
      }
      if (!pl.dying) {
        var hx = tr[tr.length - 2], hy = tr[tr.length - 1];
        var gr = ctx.createRadialGradient(hx, hy, 0, hx, hy, 14);
        gr.addColorStop(0, 'rgba(240,200,150,0.75)');
        gr.addColorStop(1, 'rgba(' + GOLD + ',0)');
        ctx.fillStyle = gr;
        ctx.beginPath(); ctx.arc(hx, hy, 14, 0, Math.PI * 2); ctx.fill();
      }
    };

    var drawFrame = function () {
      ctx.clearRect(0, 0, W, H);
      frame++;
      var i, l, na, nb, g;
      // Fareyi takip eden hafif ışık (masaüstü)
      if (mouse.on && !small) {
        var mg = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 260);
        mg.addColorStop(0, 'rgba(' + GOLD + ',0.07)');
        mg.addColorStop(1, 'rgba(' + GOLD + ',0)');
        ctx.fillStyle = mg;
        ctx.fillRect(mouse.x - 260, mouse.y - 260, 520, 520);
      }
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
      // Akım darbeleri (izler çizildikten sonra başlar)
      if (!reduceMotion && frame > 160) {
        if (pulses.length < MAX_PULSES() && Math.random() < 0.04) spawnPulse();
        pulses = pulses.filter(stepPulse);
        pulses.forEach(drawPulse);
      }
      // Pad ve via'lar
      ctx.lineWidth = 1;
      for (i = 0; i < nodes.length; i++) {
        var n = nodes[i];
        n.pulse += n.spd;
        g = 0.12 + Math.sin(n.pulse) * 0.06;
        if (n.flash > 0) { g += n.flash * 0.5; n.flash *= 0.94; if (n.flash < 0.02) n.flash = 0; }
        if (mouse.on && !small) {
          var dx = n.x - mouse.x, dy = n.y - mouse.y, d2 = dx * dx + dy * dy;
          if (d2 < 48400) g += (1 - Math.sqrt(d2) / 220) * 0.22;
        }
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

    var visible = true;
    var loop = function (t) {
      requestAnimationFrame(loop);
      if (!visible) return;
      // Telefonda ~30 fps yeterli; pil dostu
      if (small && t - lastDraw < 32) return;
      lastDraw = t;
      drawFrame();
    };

    // Aşağı kaydırdıkça soluklaş; tamamen görünmezse çizimi durdur
    var onScroll = function () {
      var k = Math.min(1, window.scrollY / (window.innerHeight * 0.9));
      var op = 1 - k * 0.75;
      canvas.style.opacity = canvas.classList.contains('show') ? op : '';
      visible = op > 0.05;
    };
    window.addEventListener('scroll', onScroll, { passive: true });

    if (window.matchMedia && window.matchMedia('(hover: hover)').matches) {
      window.addEventListener('pointermove', function (e) { mouse.x = e.clientX; mouse.y = e.clientY; mouse.on = true; }, { passive: true });
      document.addEventListener('pointerleave', function () { mouse.on = false; });
    }

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
      onScroll();
      setTimeout(function () { canvas.style.transition = 'opacity .35s ease'; }, 1300);
      if (!reduceMotion) requestAnimationFrame(loop);
    }, 500);
  }

  /* ---------- Ana sayfa: kaydırdıkça renk geçişi ---------- */
  var toned = [].slice.call(document.querySelectorAll('[data-tone]'));
  if (toned.length) {
    document.body.classList.add('tone-enabled');
    var themeMeta = document.querySelector('meta[name="theme-color"]');
    var currentTone = 'dark', toneTick = false;
    var updateTone = function () {
      toneTick = false;
      var mid = window.innerHeight * 0.55, tone = toned[0].getAttribute('data-tone');
      for (var i = 0; i < toned.length; i++) {
        if (toned[i].getBoundingClientRect().top <= mid) tone = toned[i].getAttribute('data-tone');
      }
      if (tone !== currentTone) {
        currentTone = tone;
        document.body.classList.toggle('tone-light', tone === 'light');
        if (themeMeta) themeMeta.setAttribute('content', tone === 'light' ? '#f3eee5' : '#111110');
      }
    };
    window.addEventListener('scroll', function () {
      if (!toneTick) { toneTick = true; requestAnimationFrame(updateTone); }
    }, { passive: true });
    window.addEventListener('resize', updateTone);
    updateTone();
  }

  /* ---------- Ana sayfa: bölümler kaydırdıkça yumuşakça belirir ---------- */
  if (toned.length && !reduceMotion && 'IntersectionObserver' in window) {
    var items = [].slice.call(document.querySelectorAll('.home-sections .section-head, .home-sections .card, .home-sections .service, .home-sections .review, .home-sections .post-item'));
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var t = en.target;
          t.classList.add('in'); io.unobserve(t);
          // Animasyon bitince sınıfları kaldır; kartların hover efekti normale dönsün
          setTimeout(function () { t.classList.remove('will-appear', 'in'); t.style.transitionDelay = ''; }, 1100);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) {
      // Sayfa açıldığında zaten görünenleri gizleme
      if (el.getBoundingClientRect().top < window.innerHeight) return;
      var sib = el.parentElement ? [].indexOf.call(el.parentElement.children, el) : 0;
      el.style.transitionDelay = Math.min(sib, 3) * 90 + 'ms';
      el.classList.add('will-appear');
      io.observe(el);
    });
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
      btn.textContent = form.getAttribute('data-sending') || 'Gönderiliyor…';
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

  var EN = document.documentElement.lang === 'en';

  /* ---------- Şematik / PCB / 3D sekmeleri ---------- */
  document.querySelectorAll('.dv').forEach(function (dv) {
    var tabs = [].slice.call(dv.querySelectorAll('[role="tab"]'));
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') select(tabs[(i + 1) % tabs.length], true);
        if (e.key === 'ArrowLeft') select(tabs[(i - 1 + tabs.length) % tabs.length], true);
      });
    });
  });

  /* ---------- Filtre ve arama (projeler / yazılar) ---------- */
  var norm = function (t) {
    return (t || '').toLocaleLowerCase('tr').replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g')
      .replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c').normalize('NFD').replace(/[̀-ͯ]/g, '');
  };
  document.querySelectorAll('[data-filter]').forEach(function (scope) {
    var input = scope.querySelector('[data-filter-search]');
    var chips = [].slice.call(scope.querySelectorAll('[data-filter-tag]'));
    var items = [].slice.call(scope.querySelectorAll('[data-filter-item]'));
    var sections = [].slice.call(scope.querySelectorAll('[data-filter-section]'));
    var empty = scope.querySelector('[data-filter-empty]');
    var active = '';
    items.forEach(function (it) { it._text = norm(it.textContent + ' ' + it.getAttribute('data-tags')); });
    var apply = function () {
      var q = norm(input ? input.value.trim() : '');
      var words = q ? q.split(/\s+/) : [];
      var shown = 0;
      items.forEach(function (it) {
        var tags = (it.getAttribute('data-tags') || '').split('|');
        var ok = (!active || tags.indexOf(active) > -1) && words.every(function (w) { return it._text.indexOf(w) > -1; });
        it.classList.toggle('is-hidden', !ok);
        if (ok) shown++;
      });
      sections.forEach(function (sec) {
        sec.classList.toggle('is-hidden', !sec.querySelector('[data-filter-item]:not(.is-hidden)'));
      });
      if (empty) empty.hidden = shown > 0;
    };
    var setTag = function (tag) {
      active = tag;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-filter-tag') === tag ? 'true' : 'false'); });
      try {
        var url = new URL(location.href);
        if (tag) url.searchParams.set('tag', tag); else url.searchParams.delete('tag');
        history.replaceState(null, '', url);
      } catch (e) {}
      apply();
    };
    chips.forEach(function (c) { c.addEventListener('click', function () { setTag(c.getAttribute('data-filter-tag')); }); });
    if (input) input.addEventListener('input', apply);
    // Kart üzerindeki etiketlere tıklayınca sayfa yenilenmeden filtrele
    scope.querySelectorAll('a.tag').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var t = new URL(a.href).searchParams.get('tag');
        if (t && chips.some(function (c) { return c.getAttribute('data-filter-tag') === t; })) {
          e.preventDefault(); setTag(t); scope.scrollIntoView({ behavior: 'smooth' });
        }
      });
    });
    var initial = new URLSearchParams(location.search).get('tag');
    if (initial && chips.some(function (c) { return c.getAttribute('data-filter-tag') === initial; })) setTag(initial);
  });

  /* ---------- Fotoğraf galerisi (büyütme, ileri/geri, kaydırma) ---------- */
  var imgs = [].slice.call(document.querySelectorAll('.blog-img'));
  if (imgs.length) {
    var box = document.createElement('div');
    box.className = 'lightbox' + (imgs.length === 1 ? ' single' : '');
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', EN ? 'Photo' : 'Fotoğraf');
    box.innerHTML =
      '<div class="lightbox-count" aria-live="polite"></div>' +
      '<button class="lightbox-btn lightbox-close" aria-label="' + (EN ? 'Close' : 'Kapat') + '">×</button>' +
      '<button class="lightbox-btn lightbox-prev" aria-label="' + (EN ? 'Previous' : 'Önceki') + '">←</button>' +
      '<button class="lightbox-btn lightbox-next" aria-label="' + (EN ? 'Next' : 'Sonraki') + '">→</button>' +
      '<div class="lightbox-stage"><img alt=""></div><div class="lightbox-cap"></div>';
    document.body.appendChild(box);
    var big = box.querySelector('img'), cap = box.querySelector('.lightbox-cap'), count = box.querySelector('.lightbox-count');
    var idx = 0, lastFocus = null;
    var captionOf = function (img) {
      var fig = img.closest('figure, .dv-panel');
      var fc = fig && fig.querySelector('figcaption');
      return fc ? fc.textContent : img.alt;
    };
    var show = function (i) {
      idx = (i + imgs.length) % imgs.length;
      var im = imgs[idx];
      big.src = im.currentSrc || im.src;
      big.alt = im.alt;
      cap.textContent = captionOf(im);
      count.textContent = (idx + 1) + ' / ' + imgs.length;
    };
    var open = function (i) {
      lastFocus = document.activeElement;
      show(i);
      box.classList.add('open');
      document.body.style.overflow = 'hidden';
      box.querySelector('.lightbox-close').focus();
    };
    var close = function () {
      box.classList.remove('open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus({ preventScroll: true });
    };
    imgs.forEach(function (img, i) {
      img.setAttribute('tabindex', '0');
      img.setAttribute('role', 'button');
      img.addEventListener('click', function () { open(i); });
      img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    });
    box.querySelector('.lightbox-close').addEventListener('click', close);
    box.querySelector('.lightbox-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
    box.querySelector('.lightbox-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
    box.addEventListener('click', function (e) { if (e.target === box || e.target.classList.contains('lightbox-stage')) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
    // Parmakla kaydırma
    var sx = null, sy = 0;
    box.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
    box.addEventListener('touchmove', function (e) {
      if (sx === null) return;
      var dx = e.touches[0].clientX - sx;
      if (Math.abs(dx) > Math.abs(e.touches[0].clientY - sy)) big.style.transform = 'translateX(' + dx * 0.4 + 'px)';
    }, { passive: true });
    box.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      big.style.transform = '';
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) show(idx + (dx < 0 ? 1 : -1));
      else if (dy > 90 && Math.abs(dy) > Math.abs(dx)) close();
      sx = null;
    });
  }
})();
