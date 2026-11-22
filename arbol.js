/* Líneas del árbol al estilo clásico: cada progenitor baja un trazo corto, los dos se unen
   con una barra y desde su centro baja la línea que se reparte hasta cada hijo.
   Se recalcula al cambiar el tamaño de la ventana. Sin desplazamiento horizontal. */
(function () {
  var cont = document.querySelector('.pedigri');
  if (!cont) return;
  var enlaces = JSON.parse(cont.getAttribute('data-enlaces') || '[]');
  var verdes = {};
  JSON.parse(cont.getAttribute('data-verdes') || '[]').forEach(function (v) { verdes[v] = true; });
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'lineas');
  svg.setAttribute('aria-hidden', 'true');
  cont.insertBefore(svg, cont.firstChild);

  function caja(id) {
    var e = cont.querySelector('[data-id="' + id + '"]');
    if (!e) return null;
    var r = e.getBoundingClientRect(), c = cont.getBoundingClientRect();
    return { x: r.left - c.left, y: r.top - c.top, w: r.width, h: r.height, cx: r.left - c.left + r.width / 2 };
  }
  function trazo(d, verde) {
    var p = document.createElementNS(NS, 'path');
    p.setAttribute('d', d);
    p.setAttribute('class', verde ? 'trazo verde' : 'trazo');
    svg.appendChild(p);
  }

  function dibujar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var c = cont.getBoundingClientRect();
    svg.setAttribute('width', c.width);
    svg.setAttribute('height', c.height);
    svg.setAttribute('viewBox', '0 0 ' + c.width + ' ' + c.height);
    var em = parseFloat(getComputedStyle(cont).fontSize) || 12;

    enlaces.forEach(function (e) {
      var padres = e.p.map(caja).filter(Boolean);
      var hijos = e.h.map(function (id) { var b = caja(id); if (b) b.id = id; return b; }).filter(Boolean);
      if (!padres.length || !hijos.length) return;
      var verde = hijos.some(function (h) { return verdes[h.id]; });
      var baseP = Math.max.apply(null, padres.map(function (p) { return p.y + p.h; }));
      var topH = Math.min.apply(null, hijos.map(function (h) { return h.y; }));
      var barra = baseP + Math.min(0.8 * em, (topH - baseP) * 0.3);   // une a la pareja
      var bus = baseP + (topH - baseP) * 0.62;                          // reparte a los hijos
      var xs = padres.map(function (p) { return p.cx; });
      var xm = (Math.min.apply(null, xs) + Math.max.apply(null, xs)) / 2;

      // trazos cortos de cada progenitor y barra que los une
      padres.forEach(function (p) { trazo('M' + p.cx + ' ' + (p.y + p.h) + ' V' + barra, verde); });
      if (padres.length > 1) trazo('M' + Math.min.apply(null, xs) + ' ' + barra + ' H' + Math.max.apply(null, xs), verde);
      // bajada desde el centro de la pareja hasta el reparto
      trazo('M' + xm + ' ' + barra + ' V' + bus, verde);
      // reparto: primero los neutros y encima los verdes
      var hx = hijos.map(function (h) { return h.cx; }).concat([xm]);
      var neutros = hijos.filter(function (h) { return !verdes[h.id]; });
      var vs = hijos.filter(function (h) { return verdes[h.id]; });
      if (neutros.length) {
        var nx = neutros.map(function (h) { return h.cx; }).concat([xm]);
        trazo('M' + Math.min.apply(null, nx) + ' ' + bus + ' H' + Math.max.apply(null, nx), false);
        neutros.forEach(function (h) { trazo('M' + h.cx + ' ' + bus + ' V' + (h.y - 1), false); });
      }
      if (vs.length) {
        var vx = vs.map(function (h) { return h.cx; }).concat([xm]);
        trazo('M' + Math.min.apply(null, vx) + ' ' + bus + ' H' + Math.max.apply(null, vx), true);
        vs.forEach(function (h) { trazo('M' + h.cx + ' ' + bus + ' V' + (h.y - 1), true); });
      }
    });
  }

  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(dibujar, 60); });
  window.addEventListener('load', dibujar);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(dibujar);
  dibujar();
})();
