/* Árbol dinámico de los Naranjo.
   Una persona en el centro; arriba sus padres, abuelos y bisabuelos; a su lado su pareja;
   debajo sus hijos (y los nietos de las ramas abiertas). Pulsar a cualquiera lo pone en el centro.
   Las líneas se dibujan en un SVG a partir de la posición real de cada recuadro, y todo
   se recoloca con el ancho de la pantalla: nunca hay desplazamiento horizontal. */
(function () {
  'use strict';
  var D = window.ARBOL, P = D && D.personas;
  var raiz = document.getElementById('arbol');
  var panel = document.getElementById('ficha-breve');
  if (!P || !raiz) return;
  var NS = 'http://www.w3.org/2000/svg';
  var INICIO = raiz.getAttribute('data-inicio');
  var foco = null, abiertos = {}, anchoPrevio = 0, svg = null;

  /* ---------------- utilidades ---------------- */
  function crear(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }
  function lista(id, campo) { return (P[id] && P[id][campo]) || []; }
  function padresOrden(id) {
    var ps = lista(id, 'p'), pa = null, ma = null;
    ps.forEach(function (x) { if (P[x].s === 'f') { if (!ma) ma = x; else if (!pa) pa = x; } else { if (!pa) pa = x; else if (!ma) ma = x; } });
    return [pa, ma];
  }
  function hermanos(id) {
    var vistos = {}, r = [];
    lista(id, 'p').forEach(function (p) {
      lista(p, 'h').forEach(function (h) { if (h !== id && !vistos[h]) { vistos[h] = 1; r.push(h); } });
    });
    return r;
  }
  function plural(n, uno, varios) { return n + ' ' + (n === 1 ? uno : varios); }

  /* ---------------- recuadros ---------------- */
  function caja(id, extra) {
    var p = P[id];
    var e = crear(p.priv ? 'span' : 'button', 'nodo' + (p.nj ? ' naranjo' : '') + (p.v ? ' verde' : '') + (p.priv ? ' privado' : '') + (extra ? ' ' + extra : ''));
    if (!p.priv) e.type = 'button';
    e.setAttribute('data-id', id);
    e.title = p.n + (p.f ? ' (' + p.f + ')' : '');
    if (p.fo) { var im = crear('img'); im.src = p.fo; im.alt = ''; im.loading = 'lazy'; e.appendChild(im); }
    var t = crear('span', 'txt');
    t.appendChild(crear('span', 'nom', p.n));
    if (p.f) t.appendChild(crear('span', 'fec', p.f));
    e.appendChild(t);
    return e;
  }

  // Los Naranjo se muestran con toda su descendencia; las ramas de otros apellidos, plegadas
  function abierto(id) {
    if (abiertos.hasOwnProperty(id)) return abiertos[id];
    return !!P[id].nj;
  }

  function conDescendencia(id, nivel) { return lista(id, 'h').length > 0 && nivel < 30 && abierto(id); }

  // Si ningún hijo tiene su rama abierta, los hijos van en fila y centrados.
  // Si alguno la tiene, la familia se escalona: una línea baja por la izquierda y de ella
  // salen los hijos; los que no tienen rama abierta se agrupan en filas.
  function contenedor(base, ids, nivel) {
    var c = crear('div', base);
    if (!ids.some(function (h) { return conDescendencia(h, nivel); })) {
      ids.forEach(function (h) { c.appendChild(unidad(h, nivel)); });
      return c;
    }
    c.classList.add('indentado');
    var grupo = null;
    ids.forEach(function (h) {
      var u = unidad(h, nivel);
      if (conDescendencia(h, nivel)) { grupo = null; c.appendChild(u); }
      else {
        if (!grupo) { grupo = crear('div', 'grupo-hojas'); c.appendChild(grupo); }
        grupo.appendChild(u);
      }
    });
    return c;
  }

  function unidad(id, nivel) {
    var u = crear('div', 'unidad');
    u.setAttribute('data-u', id);
    var par = crear('div', 'pareja');
    par.appendChild(caja(id, 'hijo'));
    lista(id, 'c').forEach(function (c) { par.appendChild(caja(c, 'conyuge')); });
    u.appendChild(par);
    var hs = lista(id, 'h');
    if (hs.length) {
      if (nivel < 30 && abierto(id)) {
        var sub = contenedor('hijos', hs, nivel + 1);
        if (sub.classList.contains('indentado')) u.classList.add('izq');
        u.appendChild(sub);
        if (abiertos[id] === true) {   // abierta a mano: se puede volver a plegar
          var cerrar = crear('button', 'desplegar abierto', '▴ plegar los hijos de ' + P[id].n.split(' ')[0]);
          cerrar.type = 'button'; cerrar.setAttribute('data-plegar', id);
          u.appendChild(cerrar);
        }
      } else {
        var b = crear('button', 'desplegar', '▾ ver ' + plural(hs.length, 'hijo', 'hijos'));
        b.type = 'button'; b.setAttribute('data-desplegar', id);
        b.title = 'Mostrar los hijos de ' + P[id].n;
        u.appendChild(b);
      }
    }
    return u;
  }

  /* ---------------- composición ---------------- */
  function componer() {
    raiz.innerHTML = '';
    anchoPrevio = raiz.clientWidth;
    var niveles = anchoPrevio >= 700 ? 3 : 2;
    svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'lineas'); svg.setAttribute('aria-hidden', 'true');
    raiz.appendChild(svg);

    // antepasados: fila L tiene 2^L huecos; los padres de la casilla k están en 2k y 2k+1
    var filas = [], actual = [foco];
    for (var L = 1; L <= niveles; L++) {
      var sig = [];
      actual.forEach(function (id) { var pp = id ? padresOrden(id) : [null, null]; sig.push(pp[0], pp[1]); });
      if (!sig.some(Boolean)) break;
      filas[L] = sig; actual = sig;
    }
    var asc = crear('div', 'asc');
    for (L = filas.length - 1; L >= 1; L--) {
      var fila = crear('div', 'fila-asc');
      fila.style.setProperty('--n', filas[L].length);
      filas[L].forEach(function (id, j) {
        var h = crear('div', 'hueco');
        if (id) {
          var c = caja(id, 'asc');
          c.setAttribute('data-slot', L + '-' + j);
          h.appendChild(c);
        }
        fila.appendChild(h);
      });
      asc.appendChild(fila);
    }
    raiz.appendChild(asc);

    // la persona en el centro, su pareja a la derecha y sus hermanos a la izquierda
    var ff = crear('div', 'fila-foco');
    var izq = crear('div', 'lado izq'), cen = crear('div', 'centro'), der = crear('div', 'lado der');
    var hs = hermanos(foco);
    if (hs.length) {
      var bh = crear('button', 'ver-hermanos', '⇆ ' + plural(hs.length, 'hermano', 'hermanos'));
      bh.type = 'button'; bh.setAttribute('data-hermanos', '1');
      izq.appendChild(bh);
    }
    var cf = caja(foco, 'foco'); cf.setAttribute('data-slot', '0-0'); cf.setAttribute('aria-current', 'true');
    cen.appendChild(cf);
    lista(foco, 'c').forEach(function (c) { der.appendChild(caja(c, 'conyuge')); });
    ff.appendChild(izq); ff.appendChild(cen); ff.appendChild(der);
    raiz.appendChild(ff);

    // descendientes
    var hijos = lista(foco, 'h');
    if (hijos.length) {
      raiz.appendChild(contenedor('desc', hijos, 1));
    } else {
      raiz.appendChild(crear('p', 'sin-hijos', 'No constan hijos en el árbol.'));
    }
    dibujar();
  }

  /* ---------------- líneas ---------------- */
  function rect(e) {
    var r = e.getBoundingClientRect(), c = raiz.getBoundingClientRect();
    return { x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height, r: r.right - c.left, b: r.bottom - c.top, cx: r.left - c.left + r.width / 2, cy: r.top - c.top + r.height / 2 };
  }
  function trazo(d, cls) {
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', d); p.setAttribute('class', 'trazo' + (cls ? ' ' + cls : ''));
    svg.appendChild(p);
  }
  function esVerde(a, b) { return P[a] && P[b] && P[a].v && P[b].v; }

  // pareja: barra entre los dos recuadros y punto del que bajan los hijos
  function anclaPareja(caja1, conyuges) {
    var a = rect(caja1);
    if (conyuges.length === 1) {
      var b = rect(conyuges[0]);
      if (Math.abs(a.cy - b.cy) < Math.min(a.h, b.h) / 2 && (a.r < b.x || b.r < a.x)) {
        var i = a.r < b.x ? a : b, d = a.r < b.x ? b : a;
        trazo('M' + i.r + ' ' + i.cy + ' H' + d.x, 'union');
        return { x: (i.r + d.x) / 2, y: i.cy };
      }
    }
    conyuges.forEach(function (c) {
      var b = rect(c);
      if (b.x > a.r) trazo('M' + a.r + ' ' + a.cy + ' H' + (a.r + b.x) / 2 + ' V' + b.cy + ' H' + b.x, 'union');
      else if (b.y > a.b) trazo('M' + b.cx + ' ' + b.y + ' V' + a.b, 'union');
    });
    return { x: a.cx, y: a.b };
  }

  // de una pareja a sus hijos, aunque los hijos ocupen varias filas
  function bajar(ancla, unidades, idPadre, em) {
    if (!unidades.length) return;
    var filas = [];
    unidades.forEach(function (u) {
      var r = rect(u), f = filas.filter(function (f) { return Math.abs(f.y - r.y) < 3; })[0];
      if (!f) { f = { y: r.y, us: [] }; filas.push(f); }
      f.us.push({ el: u, r: r });
    });
    filas.sort(function (a, b) { return a.y - b.y; });
    var x = ancla.x, y = ancla.y, W = raiz.clientWidth;
    filas.forEach(function (f, n) {
      f.us.sort(function (a, b) { return a.r.x - b.r.x; });
      var bus = f.y - 1.2 * em;
      if (n > 0) {
        // buscar un hueco entre las unidades de la fila anterior para bajar sin cruzar recuadros
        var prev = filas[n - 1].us, cand = [Math.max(2, prev[0].r.x - 0.5 * em), Math.min(W - 2, prev[prev.length - 1].r.r + 0.5 * em)];
        for (var i = 0; i + 1 < prev.length; i++) cand.push((prev[i].r.r + prev[i + 1].r.x) / 2);
        var gx = cand.reduce(function (m, c) { return Math.abs(c - x) < Math.abs(m - x) ? c : m; }, cand[0]);
        trazo('M' + x + ' ' + y + ' H' + gx, '');
        x = gx;
      }
      trazo('M' + x + ' ' + y + ' V' + bus, '');
      var xs = [x];
      f.us.forEach(function (u) {
        var hijo = u.el.querySelector('.nodo.hijo'), r = rect(hijo), id = hijo.getAttribute('data-id');
        xs.push(r.cx);
        trazo('M' + r.cx + ' ' + bus + ' V' + (r.y - 1), esVerde(idPadre, id) ? 'verde' : '');
      });
      trazo('M' + Math.min.apply(null, xs) + ' ' + bus + ' H' + Math.max.apply(null, xs), '');
      // si la rama verde pasa por esta fila, se repasa en verde su tramo
      var verdes = f.us.filter(function (u) { return esVerde(idPadre, u.el.getAttribute('data-u')); });
      if (verdes.length) {
        var vx = verdes.map(function (u) { return rect(u.el.querySelector('.nodo.hijo')).cx; }).concat([x]);
        trazo('M' + Math.min.apply(null, vx) + ' ' + bus + ' H' + Math.max.apply(null, vx), 'verde');
        trazo('M' + x + ' ' + y + ' V' + bus, 'verde');
      }
      y = bus;
    });
  }

  function dibujar() {
    if (!svg) return;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var c = raiz.getBoundingClientRect();
    svg.setAttribute('width', c.width); svg.setAttribute('height', c.height);
    svg.setAttribute('viewBox', '0 0 ' + c.width + ' ' + c.height);
    var em = parseFloat(getComputedStyle(raiz).fontSize) || 12;

    // antepasados: cada pareja baja a su hijo
    var slots = {};
    Array.prototype.forEach.call(raiz.querySelectorAll('[data-slot]'), function (e) { slots[e.getAttribute('data-slot')] = e; });
    Object.keys(slots).forEach(function (k) {
      var L = +k.split('-')[0], j = +k.split('-')[1];
      var hijo = slots[k], pa = slots[(L + 1) + '-' + (2 * j)], ma = slots[(L + 1) + '-' + (2 * j + 1)];
      var ps = [pa, ma].filter(Boolean);
      if (!ps.length) return;
      var h = rect(hijo), rs = ps.map(rect);
      var idH = hijo.getAttribute('data-id');
      var verde = ps.some(function (p) { return esVerde(p.getAttribute('data-id'), idH); }) ? 'verde' : '';
      var baseP = Math.max.apply(null, rs.map(function (r) { return r.b; }));
      var barra = baseP + Math.min(0.8 * em, (h.y - baseP) * 0.35);
      var xs = rs.map(function (r) { return r.cx; });
      var xm = (Math.min.apply(null, xs) + Math.max.apply(null, xs)) / 2;
      rs.forEach(function (r) { trazo('M' + r.cx + ' ' + r.b + ' V' + barra, verde); });
      if (rs.length > 1) trazo('M' + Math.min.apply(null, xs) + ' ' + barra + ' H' + Math.max.apply(null, xs), verde);
      var medio = barra + (h.y - barra) / 2;
      trazo('M' + xm + ' ' + barra + ' V' + medio + ' H' + h.cx + ' V' + (h.y - 1), verde);
    });

    // la persona del centro y su pareja
    var cf = raiz.querySelector('.nodo.foco');
    var conyF = Array.prototype.slice.call(raiz.querySelectorAll('.fila-foco .der .nodo'));
    var ancla = anclaPareja(cf, conyF);
    var desc = raiz.querySelector('.desc');
    if (desc) {
      conectar(ancla, desc, foco, em);
      // cada hijo con su pareja y, si la rama está abierta, con sus propios hijos
      Array.prototype.forEach.call(desc.querySelectorAll('.unidad'), function (u) {
        var hijo = u.querySelector(':scope > .pareja > .nodo.hijo');
        var cs = Array.prototype.slice.call(u.querySelectorAll(':scope > .pareja > .nodo.conyuge'));
        var a = anclaPareja(hijo, cs);
        var sub = u.querySelector(':scope > .hijos');
        if (sub) conectar(a, sub, u.getAttribute('data-u'), em);
      });
    }
  }

  function conectar(ancla, cont, idPadre, em) {
    if (!cont.classList.contains('indentado')) {
      bajar(ancla, Array.prototype.slice.call(cont.children), idPadre, em);
      return;
    }
    // familia escalonada: línea vertical a la izquierda y ramales hacia cada hijo
    var c = rect(cont), tx = c.x + 0.9 * em, y0 = c.y + 0.9 * em;
    var fin = y0, finVerde = null, algunoVerde = false;
    function cajaHijo(u) { return u.querySelector(':scope > .pareja > .nodo.hijo'); }
    Array.prototype.forEach.call(cont.children, function (el) {
      if (el.classList.contains('unidad')) {
        var hb = cajaHijo(el), b = rect(hb), v = esVerde(idPadre, hb.getAttribute('data-id'));
        trazo('M' + tx + ' ' + b.cy + ' H' + b.x, v ? 'verde' : '');
        fin = Math.max(fin, b.cy);
        if (v) { algunoVerde = true; finVerde = Math.max(finVerde || 0, b.cy); }
        return;
      }
      // grupo de hijos sin rama abierta: una barra por cada fila del grupo
      var filas = [];
      Array.prototype.forEach.call(el.children, function (u) {
        var hb = cajaHijo(u), b = rect(hb), f = filas.filter(function (f) { return Math.abs(f.y - rect(u).y) < 3; })[0];
        if (!f) { f = { y: rect(u).y, hs: [] }; filas.push(f); }
        f.hs.push({ b: b, id: hb.getAttribute('data-id') });
      });
      filas.forEach(function (f) {
        var bus = f.y - 1.1 * em, xmax = tx, vmax = null;
        f.hs.forEach(function (h) {
          var v = esVerde(idPadre, h.id);
          trazo('M' + h.b.cx + ' ' + bus + ' V' + (h.b.y - 1), v ? 'verde' : '');
          xmax = Math.max(xmax, h.b.cx);
          if (v) vmax = Math.max(vmax || 0, h.b.cx);
        });
        trazo('M' + tx + ' ' + bus + ' H' + xmax, '');
        if (vmax !== null) { trazo('M' + tx + ' ' + bus + ' H' + vmax, 'verde'); algunoVerde = true; finVerde = Math.max(finVerde || 0, bus); }
        fin = Math.max(fin, bus);
      });
    });
    var bajada = 'M' + ancla.x + ' ' + ancla.y + ' V' + y0 + ' H' + tx;
    trazo(bajada, ''); trazo('M' + tx + ' ' + y0 + ' V' + fin, '');
    if (algunoVerde) { trazo(bajada, 'verde'); trazo('M' + tx + ' ' + y0 + ' V' + finVerde, 'verde'); }
  }

  /* ---------------- ficha breve (debajo del árbol) ---------------- */
  function enlaces(ids) {
    var f = document.createDocumentFragment();
    ids.forEach(function (id, n) {
      if (n) f.appendChild(document.createTextNode(' · '));
      var p = P[id];
      if (p.priv) { f.appendChild(crear('span', 'privado', p.n + ' (' + p.f + ')')); return; }
      var b = crear('button', 'enlace-persona' + (p.nj ? ' naranjo' : ''), p.n);
      b.type = 'button'; b.setAttribute('data-id', id);
      f.appendChild(b);
      if (p.f) f.appendChild(crear('span', 'fec', ' ' + p.f));
    });
    return f;
  }
  function fila(dl, titulo, ids) {
    if (!ids.length) return;
    dl.appendChild(crear('dt', '', titulo));
    var dd = crear('dd'); dd.appendChild(enlaces(ids)); dl.appendChild(dd);
  }
  function ficha() {
    if (!panel) return;
    var p = P[foco];
    panel.innerHTML = '';
    var cab = crear('div', 'cab');
    if (p.fo) { var im = crear('img', 'retrato-mini'); im.src = p.fo; im.alt = 'Retrato de ' + p.n; cab.appendChild(im); }
    var tt = crear('div');
    tt.appendChild(crear('h2', '', p.n));
    var linea = [p.f, p.l].filter(Boolean).join(' · ');
    if (linea) tt.appendChild(crear('p', 'fechas', linea));
    cab.appendChild(tt);
    panel.appendChild(cab);
    if (p.r) panel.appendChild(crear('p', 'resumen', p.r));
    if (p.t && p.t !== p.r) {
      var tx = crear('p', 'texto');
      if (p.g) tx.appendChild(crear('b', '', 'En el árbol de Geneanet: '));
      tx.appendChild(document.createTextNode(p.t.charAt(0).toUpperCase() + p.t.slice(1)));
      panel.appendChild(tx);
    }
    var dl = crear('dl', 'parientes');
    fila(dl, 'Padres', lista(foco, 'p'));
    fila(dl, lista(foco, 'c').length > 1 ? 'Matrimonios' : (p.s === 'f' ? 'Esposo' : 'Esposa'), lista(foco, 'c'));
    fila(dl, 'Hijos', lista(foco, 'h'));
    var hs = hermanos(foco);
    if (hs.length) { fila(dl, 'Hermanos', hs); dl.lastChild.id = 'hermanos'; }
    panel.appendChild(dl);
    var ac = crear('p', 'acciones');
    if (p.fi) {
      var a = crear('a', 'boton', 'Abrir su ficha completa' + (p.nd ? ' · ' + plural(p.nd, 'documento', 'documentos') : '') + (p.fo ? ' y foto' : ''));
      a.href = 'personas/' + p.fi + '.html'; ac.appendChild(a);
    }
    if (p.g) {
      var g = crear('a', 'boton secundario', 'Ver en Geneanet ↗');
      g.href = D.geneanet + p.g; g.target = '_blank'; g.rel = 'noopener'; ac.appendChild(g);
    }
    if (ac.childNodes.length) panel.appendChild(ac);
    panel.appendChild(crear('p', 'fuente', p.g
      ? 'Fuente: árbol de Cristo Santana Naranjo en Geneanet, basado en «Historia de los Naranjo en Canarias» de Miguel Rodríguez Díaz de Quintana' + (p.fi ? ', completado con nuestra investigación.' : '.')
      : 'Fuente: investigación familiar (registros parroquiales y civiles, FamilySearch, prensa y memorias de la familia).'));
  }

  /* ---------------- navegación ---------------- */
  function enfocar(id, historial) {
    if (!P[id] || P[id].priv) return;
    var cambia = id !== foco;
    foco = id;
    if (cambia) abiertos = {};
    componer(); ficha();
    var buscador = document.getElementById('buscar-persona');
    if (buscador && cambia) buscador.value = '';
    if (historial && cambia) {
      try { history.pushState({ id: id }, '', '#' + id); } catch (e) { location.hash = id; }
    }
    if (cambia) {
      document.title = P[id].n + ' · Árbol de los Naranjo de Telde';
      var arriba = raiz.getBoundingClientRect().top;
      if (historial && (arriba < 0 || arriba > window.innerHeight * 0.6)) raiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
      raiz.classList.remove('entra'); void raiz.offsetWidth; raiz.classList.add('entra');
    }
  }

  raiz.addEventListener('click', function (ev) {
    var t = ev.target.closest('[data-desplegar],[data-plegar],[data-ir],[data-hermanos],.nodo[data-id]');
    if (!t) return;
    if (t.hasAttribute('data-desplegar')) { abiertos[t.getAttribute('data-desplegar')] = true; componer(); return; }
    if (t.hasAttribute('data-plegar')) { abiertos[t.getAttribute('data-plegar')] = false; componer(); return; }
    if (t.hasAttribute('data-ir')) { enfocar(t.getAttribute('data-ir'), true); return; }
    if (t.hasAttribute('data-hermanos')) { var h = document.getElementById('hermanos'); if (h) h.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    enfocar(t.getAttribute('data-id'), true);
  });
  if (panel) panel.addEventListener('click', function (ev) {
    var t = ev.target.closest('.enlace-persona[data-id]');
    if (t) enfocar(t.getAttribute('data-id'), true);
  });
  Array.prototype.forEach.call(document.querySelectorAll('.atajos [data-id]'), function (b) {
    b.addEventListener('click', function () { enfocar(b.getAttribute('data-id'), true); });
  });

  // buscador
  var buscador = document.getElementById('buscar-persona'), opciones = document.getElementById('lista-personas');
  if (buscador && opciones) {
    var porTexto = {};
    Object.keys(P).filter(function (id) { return !P[id].priv; })
      .sort(function (a, b) { return P[a].n.localeCompare(P[b].n, 'es'); })
      .forEach(function (id) {
        var t = P[id].n + (P[id].f ? ' (' + P[id].f + ')' : '');
        if (porTexto[t]) t += ' · ' + id;
        porTexto[t] = id;
        var o = document.createElement('option'); o.value = t; opciones.appendChild(o);
      });
    function buscar() {
      var v = buscador.value.trim();
      if (porTexto[v]) { enfocar(porTexto[v], true); buscador.blur(); return true; }
      return false;
    }
    buscador.addEventListener('input', buscar);
    buscador.addEventListener('change', buscar);
    buscador.form && buscador.form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (buscar()) return;
      var v = buscador.value.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
      if (!v) return;
      var t = Object.keys(porTexto).filter(function (k) { return k.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').indexOf(v) >= 0; })[0];
      if (t) { enfocar(porTexto[t], true); buscador.blur(); }
    });
  }

  function desdeDireccion() {
    var id = decodeURIComponent(location.hash.replace(/^#/, ''));
    return P[id] && !P[id].priv ? id : null;
  }
  window.addEventListener('popstate', function () { enfocar(desdeDireccion() || INICIO, false); });
  window.addEventListener('hashchange', function () { var id = desdeDireccion(); if (id && id !== foco) enfocar(id, false); });

  var espera;
  window.addEventListener('resize', function () {
    clearTimeout(espera);
    espera = setTimeout(function () {
      if (Math.abs(raiz.clientWidth - anchoPrevio) > 1) componer(); else dibujar();
    }, 80);
  });
  window.addEventListener('load', dibujar);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(dibujar);
  // las fotos cambian el alto de algún recuadro al cargar
  raiz.addEventListener('load', function () { dibujar(); }, true);

  enfocar(desdeDireccion() || INICIO, false);
})();
