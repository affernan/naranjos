/* Árbol de los Naranjo, organizado como el árbol en línea de Geneanet:
   - tres pestañas: Árbol, Ficha y Cronología, siempre de la persona seleccionada;
   - el árbol es un lienzo que se arrastra y se amplía; arriba los antepasados (cuatro generaciones),
     en el centro la persona con sus hermanos y su pareja, y debajo sus hijos;
   - al tocar a alguien el árbol se rehace a su alrededor y el panel lateral derecho muestra
     sus datos («Individuo») o su familia («Familia»). */
(function () {
  'use strict';
  var D = window.ARBOL, P = D && D.personas, app = document.getElementById('app');
  if (!P || !app) return;
  var NS = 'http://www.w3.org/2000/svg';
  var lienzo = document.getElementById('lienzo'), lateral = document.getElementById('lateral');
  var fichaEl = document.getElementById('ficha'), cronoEl = document.getElementById('cronologia');
  var etiqueta = document.getElementById('gn-nombre');

  // foco: persona alrededor de la que se dibuja el árbol; sel: persona seleccionada (al abrir, ninguna)
  var estado = { foco: null, sel: null, tab: 'arbol', lado: 'individuo', s: 1, tx: 0, ty: 0, lateral: false };
  var mundo = null, focoXY = null, tamMundo = { w: 0, h: 0 };

  /* ---------------- utilidades ---------------- */
  function $(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function lista(id, c) { return (P[id] && P[id][c]) || []; }
  function ev(id) { return (P[id] && P[id].e) || {}; }
  function esMovil() { return window.innerWidth < 760; }
  function anio(t) { var m = /(\d{4})/.exec(t || ''); return m ? +m[1] : null; }
  function padresOrden(id) {
    var pa = null, ma = null;
    lista(id, 'p').forEach(function (x) { if (P[x].s === 'f') { if (!ma) ma = x; else if (!pa) pa = x; } else { if (!pa) pa = x; else if (!ma) ma = x; } });
    return [pa, ma];
  }
  function hermanosCon(id) {
    var ps = lista(id, 'p');
    if (!ps.length) return [id];
    var vistos = {}, r = [];
    ps.forEach(function (p) { lista(p, 'h').forEach(function (h) { if (!vistos[h]) { vistos[h] = 1; r.push(h); } }); });
    if (r.indexOf(id) < 0) r.push(id);
    return r.sort(function (a, b) { return (anioNac(a) || 9999) - (anioNac(b) || 9999); });
  }
  function anioNac(id) {
    var e = ev(id);
    if (e.n && anio(e.n[0])) return anio(e.n[0]);
    var f = P[id].f || '';
    return f.charAt(0) === '†' ? null : anio(f);
  }
  function anioMuerte(id) {
    var e = ev(id);
    if (e.d && anio(e.d[0])) return anio(e.d[0]);
    var f = P[id].f || '', ys = f.match(/\d{4}/g) || [];
    if (f.charAt(0) === '†') return ys[0] ? +ys[0] : null;
    return ys.length > 1 ? +ys[ys.length - 1] : null;
  }
  var SILUETA = {
    m: '<svg viewBox="0 0 40 48" aria-hidden="true"><circle cx="20" cy="15" r="9"/><path d="M3 48c0-11 7.5-18 17-18s17 7 17 18z"/></svg>',
    f: '<svg viewBox="0 0 40 48" aria-hidden="true"><path d="M20 4C12 4 8.5 9.5 8.5 17c0 6 .5 10-3 14h29c-3.5-4-3-8-3-14C31.5 9.5 28 4 20 4z"/><circle class="cara" cx="20" cy="16.5" r="7.2"/><path d="M3 48c0-10 7.5-16 17-16s17 6 17 16z"/></svg>'
  };
  function retrato(id, cls) {
    var p = P[id], s = $('span', cls || 'gn-foto');
    if (p.fo) { var im = $('img'); im.src = p.fo; im.alt = ''; im.loading = 'lazy'; s.appendChild(im); }
    else s.innerHTML = SILUETA[p.s === 'f' ? 'f' : 'm'];
    return s;
  }
  function boton(id, texto, cls) {
    var b = $('button', cls || 'gn-enlace', texto || P[id].n);
    b.type = 'button'; b.setAttribute('data-ir', id);
    return b;
  }

  /* ---------------- árbol: cajas ---------------- */
  function caja(id, extra) {
    var p = P[id];
    var e = $(p.priv ? 'span' : 'button', 'gn-caja ' + (p.s === 'f' ? 'mujer' : 'hombre') + (p.nj ? ' naranjo' : '') + (extra ? ' ' + extra : '') + (p.priv ? ' privado' : ''));
    if (!p.priv) { e.type = 'button'; e.setAttribute('data-id', id); }
    e.title = p.n + (p.f ? ' (' + p.f + ')' : '');
    if (!p.priv) e.appendChild(retrato(id));
    var t = $('span', 'gn-txt');
    t.appendChild($('span', 'gn-nom', p.n));
    if (p.f) t.appendChild($('span', 'gn-fec', p.f));
    e.appendChild(t);
    return e;
  }

  var ANCHO = 176, HUECO = 14, ENTRE = 52;
  var ANCHO_GEN = [ANCHO, ANCHO, ANCHO, 158, 140];

  function componerArbol() {
    var foco = estado.foco, G = 4, cajas = [], mostrados = {};
    function poner(id, x, fila, w, cls) { cajas.push({ id: id, x: x, fila: fila, w: w, cls: cls || '' }); mostrados[id] = true; }

    // antepasados: cada pareja centrada sobre su hijo; los huecos sin datos no ocupan sitio
    var memo = {};
    function anchoSub(id, g) {
      var k = id + '/' + g;
      if (memo[k] != null) return memo[k];
      var ps = g < G ? padresOrden(id).filter(Boolean) : [];
      var bloque = ps.reduce(function (s, p) { return s + anchoSub(p, g + 1); }, 0) + HUECO * Math.max(0, ps.length - 1);
      return (memo[k] = Math.max(ANCHO_GEN[g], bloque));
    }
    function ponerPadres(id, g, cx) {
      if (g >= G) return;
      var ps = padresOrden(id).filter(Boolean);
      if (!ps.length) return;
      var bloque = ps.reduce(function (s, p) { return s + anchoSub(p, g + 1); }, 0) + HUECO * (ps.length - 1);
      var x = cx - bloque / 2;
      ps.forEach(function (p) {
        var w = anchoSub(p, g + 1);
        poner(p, x + w / 2, -(g + 1), ANCHO_GEN[g + 1], 'asc');
        ponerPadres(p, g + 1, x + w / 2);
        x += w + HUECO;
      });
    }
    ponerPadres(foco, 0, 0);

    // fila central: hermanos por orden de nacimiento; la pareja, junto a la persona
    var fila = hermanosCon(foco), k = fila.indexOf(foco);
    var conyuges = lista(foco, 'c');
    fila = fila.slice(0, k + 1).concat(conyuges.filter(function (c) { return fila.indexOf(c) < 0; }), fila.slice(k + 1));
    fila.forEach(function (id, i) {
      var cls = id === foco ? (estado.sel === foco ? 'foco' : 'ancla') : (conyuges.indexOf(id) >= 0 ? 'conyuge' : 'hermano');
      poner(id, (i - k) * (ANCHO + HUECO), 0, ANCHO, cls);
    });

    // hijos, centrados bajo la pareja
    var hijos = lista(foco, 'h');
    var cxPareja = conyuges.length ? (ANCHO + HUECO) / 2 : 0;
    // si son muchos (más de 8), en dos filas, una encima de la otra
    var porFila = hijos.length > 8 ? Math.ceil(hijos.length / 2) : hijos.length;
    hijos.forEach(function (h, i) {
      var r = i < porFila ? 1 : 2, j = r === 1 ? i : i - porFila, n = r === 1 ? porFila : hijos.length - porFila;
      var total = n * ANCHO + (n - 1) * HUECO;
      poner(h, cxPareja - total / 2 + ANCHO / 2 + j * (ANCHO + HUECO), r, ANCHO, 'hijo');
    });

    // dibujar las cajas para medir su alto
    mundo = $('div', 'gn-mundo');
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'gn-lineas'); svg.setAttribute('aria-hidden', 'true');
    mundo.appendChild(svg);
    lienzo.innerHTML = '';
    lienzo.appendChild(mundo);
    var minX = Infinity, maxX = -Infinity;
    cajas.forEach(function (c) {
      var mas = lista(c.id, 'p').concat(lista(c.id, 'h'), lista(c.id, 'c')).some(function (x) { return !mostrados[x] && P[x] && !P[x].priv; });
      c.el = caja(c.id, c.cls + (mas ? ' mas' : ''));
      c.el.style.width = c.w + 'px';
      mundo.appendChild(c.el);
      minX = Math.min(minX, c.x - c.w / 2); maxX = Math.max(maxX, c.x + c.w / 2);
    });
    var filas = {};
    cajas.forEach(function (c) { c.h = c.el.offsetHeight; filas[c.fila] = Math.max(filas[c.fila] || 0, c.h); });
    var orden = Object.keys(filas).map(Number).sort(function (a, b) { return a - b; });
    var topFila = {}, y = 24;
    orden.forEach(function (f) { topFila[f] = y; y += filas[f] + ENTRE; });
    var margen = 30, dx = margen - minX;
    cajas.forEach(function (c) {
      c.cx = c.x + dx; c.left = c.cx - c.w / 2; c.top = topFila[c.fila];
      c.el.style.left = c.left + 'px'; c.el.style.top = c.top + 'px';
    });
    tamMundo = { w: maxX - minX + 2 * margen, h: y - ENTRE + 24 };
    mundo.style.width = tamMundo.w + 'px'; mundo.style.height = tamMundo.h + 'px';
    svg.setAttribute('width', tamMundo.w); svg.setAttribute('height', tamMundo.h);

    // líneas
    var porId = {};
    cajas.forEach(function (c) { porId[c.id + '|' + c.fila] = c; });
    function trazo(d, verde) { var p = document.createElementNS(NS, 'path'); p.setAttribute('d', d); p.setAttribute('class', verde ? 'verde' : ''); svg.appendChild(p); }
    function v(a, b) { return P[a] && P[b] && P[a].v && P[b].v; }
    function horquilla(padres, hijosC, idHijoRef) {
      if (!padres.length || !hijosC.length) return;
      var baseP = Math.max.apply(null, padres.map(function (p) { return p.top + p.h; }));
      var topH = Math.min.apply(null, hijosC.map(function (h) { return h.top; }));
      var barra = baseP + 10, bus = topH - 16;
      var xs = padres.map(function (p) { return p.cx; });
      var xm = (Math.min.apply(null, xs) + Math.max.apply(null, xs)) / 2;
      var verdeP = padres.some(function (p) { return P[p.id].v; });
      padres.forEach(function (p) { trazo('M' + p.cx + ' ' + (p.top + p.h) + 'V' + barra, P[p.id].v && hijosC.some(function (h) { return v(p.id, h.id); })); });
      if (padres.length > 1) trazo('M' + Math.min.apply(null, xs) + ' ' + barra + 'H' + Math.max.apply(null, xs), verdeP && hijosC.some(function (h) { return P[h.id].v; }));
      var hx = hijosC.map(function (h) { return h.cx; });
      trazo('M' + xm + ' ' + barra + 'V' + bus, false);
      trazo('M' + Math.min.apply(null, hx.concat([xm])) + ' ' + bus + 'H' + Math.max.apply(null, hx.concat([xm])), false);
      hijosC.forEach(function (h) { trazo('M' + h.cx + ' ' + bus + 'V' + h.top, false); });
      var verdes = hijosC.filter(function (h) { return padres.some(function (p) { return v(p.id, h.id); }); });
      if (verdes.length) {
        trazo('M' + xm + ' ' + barra + 'V' + bus, true);
        verdes.forEach(function (h) { trazo('M' + xm + ' ' + bus + 'H' + h.cx + 'V' + h.top, true); });
      }
    }
    // antepasados (filas -1 a -4): cada persona con sus padres
    cajas.forEach(function (c) {
      if (c.fila > 0 || c.fila <= -G) return;
      if (c.fila === 0 && c.id !== foco) return;
      var ps = lista(c.id, 'p').map(function (p) { return porId[p + '|' + (c.fila - 1)]; }).filter(Boolean);
      if (!ps.length) return;
      if (c.fila === 0) {
        // los padres de la persona central bajan a todos sus hermanos
        var hs = cajas.filter(function (x) { return x.fila === 0 && (x.cls.indexOf('hermano') >= 0 || x.id === foco) && lista(x.id, 'p').some(function (p) { return ps.some(function (q) { return q.id === p; }); }); });
        horquilla(ps, hs);
      } else horquilla(ps, [c]);
    });
    // pareja
    var cf = porId[foco + '|0'];
    conyuges.forEach(function (cid, i) {
      var cc = porId[cid + '|0']; if (!cc) return;
      var y = cf.top + Math.min(cf.h, cc.h) / 2 + i * 6;
      trazo('M' + (cf.left + cf.w) + ' ' + y + 'H' + cc.left, P[foco].v && P[cid].v);
    });
    // hijos
    var hc1 = cajas.filter(function (c) { return c.fila === 1; }).sort(function (a, b) { return a.cx - b.cx; });
    var hc2 = cajas.filter(function (c) { return c.fila === 2; }).sort(function (a, b) { return a.cx - b.cx; });
    if (hc1.length) {
      var c1 = conyuges.length ? porId[conyuges[0] + '|0'] : null;
      var ax = c1 ? (cf.left + cf.w + c1.left) / 2 : cf.cx;
      var ay = c1 ? cf.top + Math.min(cf.h, c1.h) / 2 : cf.top + cf.h;
      var bus1 = Math.min.apply(null, hc1.map(function (h) { return h.top; })) - 16;
      trazo('M' + ax + ' ' + ay + 'V' + bus1, false);
      trazo('M' + Math.min.apply(null, hc1.map(function (h) { return h.cx; }).concat([ax])) + ' ' + bus1 + 'H' + Math.max.apply(null, hc1.map(function (h) { return h.cx; }).concat([ax])), false);
      hc1.forEach(function (h) { trazo('M' + h.cx + ' ' + bus1 + 'V' + h.top, false); });
      var gx = null, bus2 = null;
      if (hc2.length) {
        // la segunda fila se alcanza bajando por el hueco de la primera más cercano al centro
        var huecos = [];
        for (var i = 0; i + 1 < hc1.length; i++) huecos.push((hc1[i].left + hc1[i].w + hc1[i + 1].left) / 2);
        if (!huecos.length) huecos.push(hc1[0].left + hc1[0].w + 10);
        gx = huecos.reduce(function (m, x) { return Math.abs(x - ax) < Math.abs(m - ax) ? x : m; }, huecos[0]);
        bus2 = Math.min.apply(null, hc2.map(function (h) { return h.top; })) - 16;
        trazo('M' + gx + ' ' + bus1 + 'V' + bus2, false);
        trazo('M' + Math.min.apply(null, hc2.map(function (h) { return h.cx; }).concat([gx])) + ' ' + bus2 + 'H' + Math.max.apply(null, hc2.map(function (h) { return h.cx; }).concat([gx])), false);
        hc2.forEach(function (h) { trazo('M' + h.cx + ' ' + bus2 + 'V' + h.top, false); });
      }
      // la línea verde hasta el hijo de la rama de Pinar del Río
      if (P[foco].v) {
        hc1.filter(function (h) { return P[h.id].v; }).forEach(function (h) { trazo('M' + ax + ' ' + ay + 'V' + bus1 + 'H' + h.cx + 'V' + h.top, true); });
        hc2.filter(function (h) { return P[h.id].v; }).forEach(function (h) { trazo('M' + ax + ' ' + ay + 'V' + bus1 + 'H' + gx + 'V' + bus2 + 'H' + h.cx + 'V' + h.top, true); });
      }
    }
    focoXY = { x: cf.cx, y: cf.top + cf.h / 2 };
    mundo.classList.add('entra');
  }

  /* ---------------- árbol: mover y ampliar ---------------- */
  function aplicar() { if (mundo) mundo.style.transform = 'translate(' + estado.tx + 'px,' + estado.ty + 'px) scale(' + estado.s + ')'; }
  function anchoVisible() {
    var w = lienzo.clientWidth;
    if (estado.lateral && !esMovil()) w -= lateral.offsetWidth;
    return w;
  }
  // Ajusta el zoom para que se vean todos los niveles sin desplazarse en vertical,
  // y centra en horizontal la persona del centro (o el árbol entero, si cabe)
  function centrar() {
    if (!focoXY) return;
    var w = anchoVisible(), h = lienzo.clientHeight;
    var minimo = esMovil() ? 0.42 : 0.5;
    estado.s = Math.max(minimo, Math.min(1, (h - 16) / tamMundo.h));
    if (tamMundo.w * estado.s <= w) estado.tx = (w - tamMundo.w * estado.s) / 2;
    else estado.tx = Math.min(0, Math.max(w - tamMundo.w * estado.s, w / 2 - focoXY.x * estado.s));
    var alto = tamMundo.h * estado.s;
    estado.ty = alto <= h ? (h - alto) / 2 : 8;
    aplicar();
  }
  function zoom(f, cx, cy) {
    var s = Math.max(0.3, Math.min(1.8, estado.s * f));
    if (cx == null) { cx = anchoVisible() / 2; cy = lienzo.clientHeight / 2; }
    estado.tx = cx - (cx - estado.tx) * (s / estado.s);
    estado.ty = cy - (cy - estado.ty) * (s / estado.s);
    estado.s = s; aplicar();
  }

  var punteros = {}, arrastre = null, movido = false, pinza = null;
  lienzo.addEventListener('pointerdown', function (e) {
    punteros[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(punteros);
    if (ids.length === 1) { arrastre = { x: e.clientX, y: e.clientY, tx: estado.tx, ty: estado.ty }; movido = false; }
    if (ids.length === 2) {
      var a = punteros[ids[0]], b = punteros[ids[1]];
      pinza = { d: Math.hypot(a.x - b.x, a.y - b.y), s: estado.s }; arrastre = null;
    }
  });
  lienzo.addEventListener('pointermove', function (e) {
    if (!punteros[e.pointerId]) return;
    punteros[e.pointerId] = { x: e.clientX, y: e.clientY };
    var ids = Object.keys(punteros);
    if (pinza && ids.length === 2) {
      var a = punteros[ids[0]], b = punteros[ids[1]], r = lienzo.getBoundingClientRect();
      var d = Math.hypot(a.x - b.x, a.y - b.y);
      zoom((pinza.s * d / pinza.d) / estado.s, (a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top);
      movido = true; return;
    }
    if (!arrastre) return;
    var dx = e.clientX - arrastre.x, dy = e.clientY - arrastre.y;
    if (!movido && Math.abs(dx) + Math.abs(dy) < 6) return;
    if (!movido) { movido = true; try { lienzo.setPointerCapture(e.pointerId); } catch (x) {} lienzo.classList.add('arrastrando'); }
    estado.tx = arrastre.tx + dx; estado.ty = arrastre.ty + dy; aplicar();
  });
  function soltar(e) {
    delete punteros[e.pointerId];
    if (Object.keys(punteros).length < 2) pinza = null;
    if (!Object.keys(punteros).length) { arrastre = null; lienzo.classList.remove('arrastrando'); }
  }
  lienzo.addEventListener('pointerup', soltar);
  lienzo.addEventListener('pointercancel', soltar);
  lienzo.addEventListener('wheel', function (e) {
    if (!e.ctrlKey && !e.metaKey) return;          // con la rueda sola la página se desplaza como siempre
    e.preventDefault();
    var r = lienzo.getBoundingClientRect();
    zoom(e.deltaY < 0 ? 1.12 : 1 / 1.12, e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });
  lienzo.addEventListener('click', function (e) {
    if (movido) { movido = false; return; }
    var c = e.target.closest('.gn-caja[data-id]');
    if (!c) return;
    var id = c.getAttribute('data-id');
    if (id === estado.sel) { abrirLateral(true); return; }
    seleccionar(id, true);
    if (!esMovil() && !estado.lateral) { abrirLateral(true); centrar(); }
  });
  app.querySelector('.gn-controles').addEventListener('click', function (e) {
    var b = e.target.closest('[data-ctrl]'); if (!b) return;
    var c = b.getAttribute('data-ctrl');
    if (c === 'mas') zoom(1.2); else if (c === 'menos') zoom(1 / 1.2);
    else if (c === 'info') { if (!estado.sel) seleccionar(estado.foco, true); abrirLateral(!estado.lateral || !estado.sel); }
    else centrar();
  });

  /* ---------------- panel lateral ---------------- */
  function abrirLateral(si) {
    if (!estado.sel) si = false;
    estado.lateral = si;
    app.classList.toggle('sin-lateral', !si);
    if (si) pintarLateral();
  }
  function seccion(titulo, fecha, lineas, ir) {
    var s = $('div', 'gn-hecho');
    var cab = $('div', 'gn-hecho-cab');
    cab.appendChild($('span', 'gn-hecho-tit', titulo));
    if (fecha) cab.appendChild($('span', 'gn-hecho-fecha', fecha));
    s.appendChild(cab);
    lineas.forEach(function (l) { if (l) { if (typeof l === 'string') s.appendChild($('p', '', l)); else s.appendChild(l); } });
    return s;
  }
  function tarjeta(id, detalle) {
    var p = P[id], b = $(p.priv ? 'div' : 'button', 'gn-tarjeta ' + (p.s === 'f' ? 'mujer' : 'hombre') + (p.nj ? ' naranjo' : ''));
    if (!p.priv) { b.type = 'button'; b.setAttribute('data-ir', id); }
    if (!p.priv) b.appendChild(retrato(id));
    var t = $('span', 'gn-txt');
    t.appendChild($('b', '', p.n));
    var e = ev(id), info = detalle || [e.n ? ('✶ ' + [e.n[0], e.n[1]].filter(Boolean).join(' · ')) : '', p.f && !e.n ? p.f : ''].filter(Boolean).join(' ');
    if (info) t.appendChild($('small', '', info));
    b.appendChild(t);
    return b;
  }
  function pintarLateral() {
    var id = estado.foco, p = P[id], e = ev(id);
    lateral.innerHTML = '';
    var cab = $('div', 'gn-lat-cab');
    if (estado.lado === 'familia') {
      var atras = $('button', 'gn-atras', '‹'); atras.type = 'button'; atras.title = 'Volver a sus datos'; atras.setAttribute('data-lado', 'individuo');
      cab.appendChild(atras);
    } else cab.appendChild(retrato(id, 'gn-foto grande'));
    var tt = $('div', 'gn-lat-tit');
    tt.appendChild($('h2', '', p.n));
    if (e.o && estado.lado !== 'familia') tt.appendChild($('p', 'gn-oficio', e.o));
    cab.appendChild(tt);
    var x = $('button', 'gn-cerrar', '×'); x.type = 'button'; x.title = 'Cerrar'; x.setAttribute('data-cerrar', '1');
    cab.appendChild(x);
    lateral.appendChild(cab);

    var cuerpo = $('div', 'gn-lat-cuerpo');
    if (estado.lado === 'individuo') {
      if (e.n) cuerpo.appendChild(seccion('Nacimiento', e.n[0], [e.n[1]]));
      if (e.b) cuerpo.appendChild(seccion('Bautismo', e.b[0], [e.b[1]]));
      (e.m || []).forEach(function (m) {
        var con = null;
        if (m[0] && P[m[0]]) { con = $('p', ''); con.appendChild(document.createTextNode('con ')); con.appendChild(boton(m[0])); }
        cuerpo.appendChild(seccion('Matrimonio', m[1], [con, m[2]]));
      });
      lista(id, 'c').forEach(function (c) {
        if ((e.m || []).some(function (m) { return m[0] === c; })) return;
        var con = $('p', ''); con.appendChild(document.createTextNode('con ')); con.appendChild(boton(c));
        cuerpo.appendChild(seccion('Unión', '', [con]));
      });
      if (e.d || e.nota) cuerpo.appendChild(seccion('Defunción', e.d ? e.d[0] : '', [e.d ? e.d[1] : '', e.nota]));
      if (!e.n && !e.d && p.f) cuerpo.appendChild(seccion('Fechas', p.f, []));
      if (p.r) cuerpo.appendChild(seccion('Notas', '', [p.r]));
      var f = seccion('Fuentes', '', [p.g ? 'Árbol de Cristo Santana Naranjo en Geneanet, basado en «Historia de los Naranjo en Canarias», de Miguel Rodríguez Díaz de Quintana.' : '', (!p.g || p.fi) ? 'Investigación familiar: registros parroquiales y civiles, FamilySearch, prensa y memorias de la familia.' : '']);
      f.classList.add('fuentes'); cuerpo.appendChild(f);
      var ac = $('div', 'gn-acciones');
      var bf = $('button', 'gn-boton', p.fi ? 'Ficha completa, con documentos' : 'Ver su ficha'); bf.type = 'button'; bf.setAttribute('data-tab', 'ficha'); ac.appendChild(bf);
      if (p.g) { var g = $('a', 'gn-boton sec', 'Geneanet ↗'); g.href = D.geneanet + p.g; g.target = '_blank'; g.rel = 'noopener'; ac.appendChild(g); }
      cuerpo.appendChild(ac);
    } else {
      var ps = lista(id, 'p');
      if (ps.length) { cuerpo.appendChild($('h3', 'gn-lat-sec', 'Padres')); ps.forEach(function (x) { cuerpo.appendChild(tarjeta(x)); }); }
      var cs = lista(id, 'c'), hs = lista(id, 'h');
      if (cs.length || hs.length) {
        cuerpo.appendChild($('h3', 'gn-lat-sec', 'Uniones'));
        (cs.length ? cs : [null]).forEach(function (c, i) {
          var u = $('div', 'gn-union');
          var m = (e.m || []).filter(function (m) { return m[0] === c; })[0];
          if (c) {
            u.appendChild(seccion(m ? 'Matrimonio' : 'Unión', m ? m[1] : '', [m ? m[2] : '']));
            u.appendChild(tarjeta(c));
          }
          var suyos = hs.filter(function (h) { return !c || cs.length === 1 || lista(h, 'p').indexOf(c) >= 0; });
          if (i === 0 && cs.length > 1) suyos = hs.filter(function (h) { return lista(h, 'p').indexOf(c) >= 0 || lista(h, 'p').length < 2; });
          if (suyos.length) {
            u.appendChild($('p', 'gn-sub', 'Hijos'));
            suyos.forEach(function (h) { var t = tarjeta(h); t.classList.add('hijo'); u.appendChild(t); });
          }
          cuerpo.appendChild(u);
        });
      }
      var her = hermanosCon(id).filter(function (h) { return h !== id; });
      if (her.length) { cuerpo.appendChild($('h3', 'gn-lat-sec', 'Hermanos')); her.forEach(function (h) { cuerpo.appendChild(tarjeta(h)); }); }
    }
    lateral.appendChild(cuerpo);
    var pie = $('div', 'gn-lat-pie');
    [['individuo', 'Individuo'], ['familia', 'Familia']].forEach(function (t) {
      var b = $('button', estado.lado === t[0] ? 'activo' : '', t[1]); b.type = 'button'; b.setAttribute('data-lado', t[0]);
      pie.appendChild(b);
    });
    lateral.appendChild(pie);
  }
  lateral.addEventListener('click', function (e) {
    var t = e.target.closest('[data-ir],[data-lado],[data-cerrar],[data-tab]');
    if (!t) return;
    if (t.hasAttribute('data-cerrar')) return abrirLateral(false);
    if (t.hasAttribute('data-lado')) { estado.lado = t.getAttribute('data-lado'); return pintarLateral(); }
    if (t.hasAttribute('data-tab')) return cambiarTab(t.getAttribute('data-tab'), true);
    seleccionar(t.getAttribute('data-ir'), true);
  });

  /* ---------------- pestaña Ficha ---------------- */
  function sexo(id) { return P[id].s === 'f' ? '♀' : '♂'; }
  function li(id, extra) {
    var l = $('li', P[id].s === 'f' ? 'mujer' : 'hombre');
    l.appendChild($('span', 'sx', sexo(id) + ' '));
    if (P[id].priv) l.appendChild(document.createTextNode(P[id].n));
    else if (id === estado.foco) l.appendChild($('b', '', P[id].n));
    else l.appendChild(boton(id));
    var f = P[id].f; if (f) l.appendChild(document.createTextNode(' ' + f));
    if (extra) l.appendChild(document.createTextNode(extra));
    return l;
  }
  function sinSeleccion(el) {
    el.innerHTML = '';
    el.appendChild($('p', 'gn-vacio', 'Toque a una persona en el árbol para ver aquí su ' + (el === fichaEl ? 'ficha.' : 'cronología.')));
    var b = $('button', 'gn-boton', 'Ir al árbol'); b.type = 'button'; b.setAttribute('data-tab-ir', 'arbol');
    el.appendChild(b);
  }
  function pintarFicha() {
    if (!estado.sel) return sinSeleccion(fichaEl);
    var id = estado.foco, p = P[id], e = ev(id);
    fichaEl.innerHTML = '';
    var cab = $('div', 'gn-ficha-cab');
    if (p.fo) { var a = $('a', 'gn-retrato'); a.href = p.fo; a.target = '_blank'; var im = $('img'); im.src = p.fo; im.alt = 'Retrato de ' + p.n; a.appendChild(im); cab.appendChild(a); }
    var tt = $('div');
    var h = $('h2', 'gn-ficha-nombre'); h.appendChild($('span', 'sx', sexo(id) + ' ')); h.appendChild(document.createTextNode(p.n)); tt.appendChild(h);
    var ul = $('ul', 'gn-datos');
    function dato(t, x) { if (x && (x[0] || x[1])) ul.appendChild($('li', '', t + (x[0] ? ' el ' + x[0] : '') + (x[1] ? ' – ' + x[1] : ''))); }
    var fem = p.s === 'f';
    dato(fem ? 'Nacida' : 'Nacido', e.n); dato(fem ? 'Bautizada' : 'Bautizado', e.b); dato(fem ? 'Fallecida' : 'Fallecido', e.d);
    if (e.nota) ul.appendChild($('li', '', e.nota));
    if (!e.n && !e.d && p.f) ul.appendChild($('li', '', p.f));
    if (e.o) ul.appendChild($('li', '', e.o));
    tt.appendChild(ul);
    cab.appendChild(tt);
    fichaEl.appendChild(cab);
    if (p.r) fichaEl.appendChild($('p', 'gn-resumen', p.r));

    function bloque(titulo) { var s = $('section', 'gn-bloque'); s.appendChild($('h3', '', titulo)); fichaEl.appendChild(s); return s; }
    var ps = lista(id, 'p');
    if (ps.length) { var b1 = bloque('Padres'), u1 = $('ul'); ps.forEach(function (x) { u1.appendChild(li(x)); }); b1.appendChild(u1); }
    var cs = lista(id, 'c'), hs = lista(id, 'h');
    if (cs.length || hs.length) {
      var b2 = bloque('Casamiento(s) e hijo(s)'), u2 = $('ul');
      (cs.length ? cs : [null]).forEach(function (c, i) {
        var l = $('li', 'gn-casamiento');
        var m = (e.m || []).filter(function (m) { return m[0] === c; })[0];
        if (c) {
          l.appendChild(document.createTextNode((m ? (fem ? 'Casada' : 'Casado') : 'Unión') + (m && m[1] ? ' el ' + m[1] : '') + (m && m[2] ? ', ' + m[2] : '') + ', con '));
          l.appendChild(P[c].priv ? document.createTextNode(P[c].n) : boton(c));
          if (P[c].f) l.appendChild(document.createTextNode(' ' + P[c].f));
        } else l.appendChild(document.createTextNode('Hijos'));
        var suyos = hs.filter(function (h) { return !c || cs.length === 1 || lista(h, 'p').indexOf(c) >= 0 || (i === 0 && lista(h, 'p').length < 2); });
        if (suyos.length) { var uh = $('ul'); suyos.forEach(function (x) { uh.appendChild(li(x)); }); l.appendChild(uh); }
        u2.appendChild(l);
      });
      b2.appendChild(u2);
    }
    var her = hermanosCon(id);
    if (her.length > 1) { var b3 = bloque('Hermanos'), u3 = $('ul'); her.forEach(function (x) { u3.appendChild(li(x)); }); b3.appendChild(u3); }
    if (p.t && p.g) { var b4 = bloque('Notas de Geneanet'); b4.appendChild($('p', '', p.t.charAt(0).toUpperCase() + p.t.slice(1))); }
    if (p.fh) { var b5 = $('section', 'gn-bloque gn-propia'); b5.innerHTML = p.fh; fichaEl.appendChild(b5); }
    var b6 = bloque('Fuentes'), u6 = $('ul');
    if (p.g) { var lg = $('li'); lg.appendChild(document.createTextNode('Árbol de Cristo Santana Naranjo en Geneanet, basado en «Historia de los Naranjo en Canarias», de Miguel Rodríguez Díaz de Quintana. ')); var a2 = $('a', '', 'Ver en Geneanet ↗'); a2.href = D.geneanet + p.g; a2.target = '_blank'; a2.rel = 'noopener'; lg.appendChild(a2); u6.appendChild(lg); }
    if (!p.g || p.fi) u6.appendChild($('li', '', 'Investigación familiar: registros parroquiales y civiles, FamilySearch, prensa y memorias de la familia.'));
    if (p.fi) { var lf = $('li'); var a3 = $('a', '', 'Abrir esta ficha en una página aparte'); a3.href = 'personas/' + p.fi + '.html'; lf.appendChild(a3); u6.appendChild(lf); }
    b6.appendChild(u6);
  }
  [fichaEl, cronoEl].forEach(function (el) {
    el.addEventListener('click', function (e) { var t = e.target.closest('[data-tab-ir]'); if (t) cambiarTab('arbol', true); });
  });
  fichaEl.addEventListener('click', function (e) { var t = e.target.closest('[data-ir]'); if (t) seleccionar(t.getAttribute('data-ir'), true); });

  /* ---------------- pestaña Cronología ---------------- */
  var MES = { ene: 1, feb: 2, mar: 3, abr: 4, may: 5, jun: 6, jul: 7, ago: 8, sep: 9, oct: 10, nov: 11, dic: 12 };
  function claveFecha(f) {
    var y = anio(f); if (!y) return null;
    var m = /(\d{1,2}) (\w{3}) \d{4}/.exec(f || ''), mm = /([a-z]{3}) \d{4}/.exec(f || '');
    return y * 10000 + ((mm && MES[mm[1]]) || 0) * 100 + (m ? +m[1] : 0);
  }
  function pintarCronologia() {
    if (!estado.sel) return sinSeleccion(cronoEl);
    var id = estado.foco, p = P[id], n0 = anioNac(id), sucesos = [];
    function add(fecha, titulo, quien, lugar) { var k = claveFecha(fecha); if (k) sucesos.push({ k: k, fecha: fecha, t: titulo, q: quien, l: lugar }); }
    function g(x, h, m) { return P[x].s === 'f' ? m : h; }
    function vida(x, rol) {
      var e = ev(x);
      if (e.n) add(e.n[0], rol ? 'Nacimiento ' + rol : 'Nacimiento', rol ? x : null, e.n[1]);
      else if (anioNac(x) && rol) add(String(anioNac(x)), 'Nacimiento ' + rol, x, '');
      if (e.b && !rol) add(e.b[0], 'Bautismo', null, e.b[1]);
      if (e.d) add(e.d[0], rol ? 'Defunción ' + rol : 'Defunción', rol ? x : null, e.d[1]);
      else if (anioMuerte(x)) add(String(anioMuerte(x)), rol ? 'Defunción ' + rol : 'Defunción', rol ? x : null, '');
      (e.m || []).forEach(function (m) { add(m[1], rol ? 'Matrimonio ' + rol : 'Matrimonio', rol ? [x, m[0]] : m[0], m[2]); });
    }
    vida(id, '');
    lista(id, 'p').forEach(function (x) { var e = ev(x); var y = e.d ? e.d[0] : (anioMuerte(x) ? String(anioMuerte(x)) : ''); if (y) add(y, 'Defunción ' + g(x, 'del padre', 'de la madre'), x, e.d ? e.d[1] : ''); });
    hermanosCon(id).filter(function (x) { return x !== id; }).forEach(function (x) { vida(x, g(x, 'de un hermano', 'de una hermana')); });
    lista(id, 'h').forEach(function (x) {
      vida(x, g(x, 'de un hijo', 'de una hija'));
      lista(x, 'h').forEach(function (y) { var e = ev(y); if (e.n) add(e.n[0], 'Nacimiento ' + g(y, 'de un nieto', 'de una nieta'), y, e.n[1]); else if (anioNac(y)) add(String(anioNac(y)), 'Nacimiento ' + g(y, 'de un nieto', 'de una nieta'), y, ''); });
    });
    sucesos.sort(function (a, b) { return a.k - b.k; });
    // no repetir el mismo suceso
    var vistos = {};
    sucesos = sucesos.filter(function (s) { var k = s.t + '|' + s.k + '|' + [].concat(s.q || '').join(); if (vistos[k]) return false; vistos[k] = 1; return true; });

    cronoEl.innerHTML = '';
    cronoEl.appendChild($('h2', 'gn-crono-tit', 'Cronología de ' + p.n));
    cronoEl.appendChild($('p', 'gn-crono-sub', 'Los acontecimientos de su vida y de su familia cercana. Los que no tienen fecha no aparecen.'));
    if (!sucesos.length) { cronoEl.appendChild($('p', 'gn-vacio', 'No hay acontecimientos con fecha.')); return; }
    var ol = $('ol', 'gn-linea');
    sucesos.forEach(function (s) {
      var li2 = $('li', 'gn-suceso' + (s.q ? '' : ' propio'));
      var col = $('div', 'gn-cuando');
      var aprox = /^(h\.|entre)/.test(s.fecha);
      col.appendChild($('b', '', (aprox ? 'h. ' : '') + anio(s.fecha)));
      var resto = s.fecha.replace(/\s*\d{4}.*$/, '').replace(/^(h\.|entre)\s*/, '');
      if (resto) col.appendChild($('span', '', resto));
      var y = anio(s.fecha);
      // la edad solo tiene sentido mientras la persona vivía: si ya había muerto (o tendría
      // una edad imposible, cuando no se sabe su muerte) no se pone
      var muerte = anioMuerte(id);
      if (n0 && y && y >= n0) {
        if (muerte && y > muerte) col.appendChild($('small', 'tras', 'tras su muerte'));
        else if (!muerte && y - n0 > 95) col.appendChild($('small', 'tras', 'probablemente ya fallecido' + (p.s === 'f' ? 'a' : '')));
        else col.appendChild($('small', '', (y - n0) + ' años'));
      }
      li2.appendChild(col);
      var cu = $('div', 'gn-que');
      cu.appendChild($('b', '', s.t));
      if (s.q) {
        var pq = $('p', '');
        [].concat(s.q).filter(Boolean).forEach(function (x, i) { if (i) pq.appendChild(document.createTextNode(' y ')); pq.appendChild(P[x].priv ? document.createTextNode(P[x].n) : boton(x)); });
        if (pq.childNodes.length) cu.appendChild(pq);
      }
      if (s.l) cu.appendChild($('p', 'gn-lugar', s.l));
      li2.appendChild(cu);
      ol.appendChild(li2);
    });
    cronoEl.appendChild(ol);
  }
  cronoEl.addEventListener('click', function (e) { var t = e.target.closest('[data-ir]'); if (t) seleccionar(t.getAttribute('data-ir'), true); });

  /* ---------------- navegación ---------------- */
  function cambiarTab(tab, historial) {
    estado.tab = tab;
    Array.prototype.forEach.call(app.querySelectorAll('.gn-pestanas [data-tab]'), function (b) { b.setAttribute('aria-selected', b.getAttribute('data-tab') === tab ? 'true' : 'false'); });
    Array.prototype.forEach.call(app.querySelectorAll('.gn-panel'), function (p) { p.hidden = p.getAttribute('data-panel') !== tab; });
    if (tab === 'ficha') pintarFicha();
    if (tab === 'cronologia') pintarCronologia();
    if (tab === 'arbol') { componerArbol(); centrar(); }
    if (historial) guardarDireccion();
  }
  function guardarDireccion() {
    var h = estado.sel ? '#' + estado.sel + (estado.tab !== 'arbol' ? '/' + estado.tab : '') : (estado.tab !== 'arbol' ? '#/' + estado.tab : '');
    if (location.hash !== h && !(h === '' && !location.hash)) {
      try { history.pushState(null, '', h || location.pathname + location.search); } catch (x) { location.hash = h; }
    }
  }
  function rotulo() {
    etiqueta.textContent = estado.sel ? P[estado.sel].n : 'Toque a una persona para ver sus datos';
    etiqueta.classList.toggle('vacio', !estado.sel);
  }
  function seleccionar(id, historial) {
    if (!P[id] || P[id].priv) return;
    estado.foco = estado.sel = id;
    rotulo();
    document.title = P[id].n + ' · Árbol de los Naranjo de Telde';
    if (estado.tab === 'arbol') { componerArbol(); centrar(); }
    else if (estado.tab === 'ficha') { pintarFicha(); app.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
    else { pintarCronologia(); app.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
    if (estado.lateral) pintarLateral();
    if (historial) guardarDireccion();
  }
  app.querySelector('.gn-pestanas').addEventListener('click', function (e) {
    var b = e.target.closest('[data-tab]'); if (b) cambiarTab(b.getAttribute('data-tab'), true);
  });

  // buscador
  var buscador = document.getElementById('buscar-persona'), opciones = document.getElementById('lista-personas'), porTexto = {};
  Object.keys(P).filter(function (id) { return !P[id].priv; }).sort(function (a, b) { return P[a].n.localeCompare(P[b].n, 'es'); }).forEach(function (id) {
    var t = P[id].n + (P[id].f ? ' (' + P[id].f + ')' : '');
    if (porTexto[t]) t += ' · ' + id;
    porTexto[t] = id;
    var o = document.createElement('option'); o.value = t; opciones.appendChild(o);
  });
  function normal(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function buscar(exacto) {
    var v = buscador.value.trim(); if (!v) return;
    var id = porTexto[v];
    if (!id && !exacto) { var n = normal(v); var k = Object.keys(porTexto).filter(function (t) { return normal(t).indexOf(n) >= 0; })[0]; id = k && porTexto[k]; }
    if (id) { seleccionar(id, true); buscador.value = ''; buscador.blur(); }
  }
  buscador.addEventListener('change', function () { buscar(true); });
  buscador.form.addEventListener('submit', function (e) { e.preventDefault(); buscar(false); });

  function leerDireccion() {
    var h = decodeURIComponent(location.hash.replace(/^#/, '')).split('/');
    return { id: P[h[0]] && !P[h[0]].priv ? h[0] : null, tab: ['ficha', 'cronologia'].indexOf(h[1]) >= 0 ? h[1] : 'arbol' };
  }
  window.addEventListener('popstate', function () {
    var d = leerDireccion();
    estado.sel = d.id; estado.foco = d.id || app.getAttribute('data-inicio');
    rotulo();
    if (!estado.sel) abrirLateral(false);
    cambiarTab(d.tab, false); if (estado.lateral) pintarLateral();
  });
  var espera, anchoPrevio = window.innerWidth;
  window.addEventListener('resize', function () {
    clearTimeout(espera);
    espera = setTimeout(function () {
      if (Math.abs(window.innerWidth - anchoPrevio) < 2) return;
      anchoPrevio = window.innerWidth;
      if (estado.tab === 'arbol') { componerArbol(); centrar(); }
    }, 120);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (estado.tab === 'arbol') { componerArbol(); centrar(); } });

  // arranque
  // al abrir sin dirección no hay nadie seleccionado: se ve el árbol entero desde la raíz
  var d0 = leerDireccion();
  estado.sel = d0.id;
  estado.foco = d0.id || app.getAttribute('data-inicio');
  estado.lateral = !!d0.id && !esMovil();
  app.classList.toggle('sin-lateral', !estado.lateral);
  rotulo();
  cambiarTab(d0.tab, false);
  if (estado.lateral) pintarLateral();
})();
