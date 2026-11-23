"""Novedades de la web: lo último que se ha incluido, de lo más reciente a lo más antiguo.

Para anunciar algo nuevo, añadir una línea a NOVEDADES (fecha «AAAA-MM-DD HH:MM»).
tipo: Foto, Documentos, Persona, Datos, Prensa o Web. enlace: página a la que lleva al tocarla.
"""
NOVEDADES = [
    # fecha, tipo, título, texto, enlace, imagen (opcional)
    ("2026-11-22 23:45", "Documentos", "8 documentos de Salvador en Venezuela",
     "Su llegada a La Guaira (1835), el expediente de soltería y la boda de 1862, bautismos de sus hijos y entierros en La Victoria.",
     "personas/salvador-naranjo-cabrera.html", "img/docs/venezuela/1862-06-28_Matrimonio_Salvador_Naranjo_y_Josefa_Cabrera_LaVictoria.jpg"),
    ("2026-11-22 23:45", "Documentos", "4 documentos de Francisco Javier en Aragua",
     "Soltería y dispensa de 1857 con el árbol de los Cabrera, su entierro con música (1866) y la boda y el entierro de su hija.",
     "personas/francisco-javier-naranjo-cabrera.html", "img/docs/venezuela/1857_Dispensa_Francisco_Javier_Naranjo_y_Maria_de_Jesus_Zumbado_01_arbol_Cabrera.jpg"),
    ("2026-11-22 23:45", "Documentos", "Manuel: soltería de 1872 y bautismos de sus hijos",
     "El expediente dice que su padre Adrián seguía vivo en Gran Canaria en 1872. Con los bautismos de Ignacio, Adrián y Luisa Elena.",
     "personas/manuel-naranjo-cabrera.html", "img/docs/venezuela/1872_Solteria_Manuel_Naranjo_e_Inelda_del_Nogal_01_portada.jpg"),
    ("2026-11-22 23:45", "Documentos", "La boda de Pedro Cabrera (1860)",
     "El hermano de Josefa Antonia se casa en La Victoria; la partida confirma que su madre se llamaba María Isidora Padrón.",
     "personas/antonia-cabrera-padron.html", "img/docs/venezuela/1860-04-16_Matrimonio_Pedro_Cabrera_hijo_de_Pedro_Cabrera_y_Maria_Isidora_Padron_tio_de_Felix_LaVictoria.jpg"),
    ("2026-11-22 23:34", "Web", "Las generaciones, en el árbol",
     "Cada fila del árbol indica su generación, contada desde Diego Pérez Naranjo (h. 1470): Félix y Rosalía son la XII.",
     "index.html", ""),
    ("2026-11-22 22:52", "Foto", "Retrato de Quirina Fernández",
     "Rehecho en óvalo a partir de la foto con Elvira, con la cara entera.",
     "personas/quirina-fernandez-fernandez.html", "img/fotos/quirina-fernandez-fernandez.jpg"),
    ("2026-11-22 22:45", "Foto", "Retrato de Josefa Antonia Cabrera de Quintana y Padrón",
     "La madre de los dieciocho hermanos Naranjo Cabrera (Telde, 1800). Del árbol de Luisa Virginia Henríquez Guerra en Geneanet.",
     "personas/antonia-cabrera-padron.html", "img/fotos/antonia-cabrera-padron.jpg"),
    ("2026-11-22 22:45", "Persona", "Ana Antonia Naranjo Cabrera y los Falcón Naranjo",
     "Ficha nueva, con su retrato y una foto del matrimonio con Juan Falcón de Llarena, y sus diez hijos en el árbol.",
     "personas/ana-naranjo-cabrera.html", "img/fotos/matrimonio-falcon-naranjo.jpg"),
    ("2026-11-22 22:45", "Foto", "Retrato y firma de Manuel Naranjo Cabrera",
     "Con su boda en San Sebastián de los Reyes (1872), su muerte (1913) y su hijo León Domingo.",
     "personas/manuel-naranjo-cabrera.html", "img/fotos/manuel-naranjo-cabrera.jpg"),
    ("2026-11-22 22:45", "Foto", "Retrato de Inocencia «Nina» Naranjo Fernández",
     "Publicado en MyHeritage.",
     "personas/inocencia-naranjo-fernandez.html", "img/fotos/inocencia-naranjo-fernandez.jpg"),
    ("2026-11-22 22:37", "Foto", "Retrato de Hugo Ángel Fernández Arada",
     "Publicado en MyHeritage, que le da 1910-1984; nuestros datos dicen 1913.",
     "personas/hugo-fernandez-arada.html", "img/fotos/hugo-fernandez-arada.jpg"),
    ("2026-11-22 22:14", "Web", "Ficha y cronología de cada persona",
     "El árbol se organiza como Geneanet: al tocar a alguien se ven sus datos, su familia y su cronología.",
     "index.html", ""),
    ("2026-11-22 16:44", "Datos", "Félix Naranjo Fernández, hijo de Natalio",
     "Corregido en el árbol y en las fichas: es hijo de Natalio Naranjo Rodríguez, no de Agustín.",
     "personas/felix-naranjo-fernandez.html", ""),
    ("2026-11-22 16:33", "Datos", "Los padres de Rosalía Rodríguez Valdés",
     "Agustín Rodríguez de Sosa y Regina de los Ángeles Valdés Delgado, con sus hermanos Carolina, Lucas y Juan.",
     "index.html#rosalia-rodriguez-valdes", ""),
    ("2026-11-22 16:33", "Datos", "258 personas en el árbol",
     "Todo el árbol de Geneanet (de Diego Pérez Naranjo, h. 1470, a las ramas de Telde y Las Palmas) unido a nuestra investigación de Cuba y Venezuela.",
     "index.html", ""),
    ("2026-11-22 16:05", "Prensa", "El viaje del Trinidad (1878)",
     "La llegada del barco a La Habana en el Diario de la Marina y la carta de los pasajeros que elogia a «D. Félix Naranjo».",
     "viajes.html", "img/prensa/1878-diario-marina-trinidad.jpg"),
    ("2026-11-22 16:05", "Prensa", "Félix Naranjo Fernández en Tenerife (1933 y 1936)",
     "Dos noticias de la prensa de Santa Cruz que encajan con el Félix que llegó de Cuba en 1924.",
     "personas/felix-naranjo-fernandez.html", "img/prensa/1933-hoy-felix-naranjo-fernandez.jpg"),
    ("2026-11-22 16:05", "Foto", "Fotos de la familia de Pinar del Río",
     "Félix Naranjo Cabrera, Quirina, Juana y José Naranjo Fernández.",
     "personas/juana-naranjo-fernandez.html", "img/fotos/juana-naranjo-fernandez.jpg"),
    ("2026-11-22 16:05", "Web", "Nace la web de los Naranjo de Telde",
     "Fichas de la familia, viajes, cronología y fuentes.",
     "personas.html", ""),
]

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

def ordenadas():
    return sorted(NOVEDADES, key=lambda n: n[0], reverse=True)

def tarjeta(n, base=""):
    fecha, tipo, titulo, texto, enlace, img = n
    a, m, d = fecha[:10].split("-")
    foto = f'<img src="{base}{img}" alt="" loading="lazy">' if img else f'<span class="nov-sin-img">{ {"Web": "✥", "Datos": "❦"}.get(tipo, "✎") }</span>'
    return (f'<a class="novedad" href="{base}{enlace}"><span class="nov-fecha"><b>{int(d)}</b>{MESES[int(m) - 1]}<small>{a}</small></span>'
            f'<span class="nov-img">{foto}</span><span class="nov-cuerpo"><span class="nov-tipo t-{tipo.lower()}">{tipo}</span>'
            f'<b>{titulo}</b><small>{texto}</small></span><span class="nov-ir" aria-hidden="true">›</span></a>')

def lista(limite=None, base=""):
    return '<div class="novedades">' + "".join(tarjeta(n, base) for n in ordenadas()[:limite]) + "</div>"
