"""Genera la web «Los Naranjo de Telde».
Todo el contenido está en este archivo (PERSONAS, páginas generales). Para cambiar algo:
editar aquí y ejecutar   python _construir.py
"""
import pathlib, html

RAIZ = pathlib.Path(__file__).parent

def ver(nombre):
    """Marca de versión para que los navegadores no usen una copia antigua en caché."""
    import hashlib
    return nombre + "?v=" + hashlib.sha1((RAIZ / nombre).read_bytes()).hexdigest()[:8]
FS = "https://www.familysearch.org"

def ark(codigo, texto=None):
    return f'<a href="{FS}/ark:/61903/{codigo}" target="_blank" rel="noopener">{texto or "Ver en FamilySearch"}</a>'

def perfil(id_, texto=None):
    return f'<a href="{FS}/tree/person/details/{id_}" target="_blank" rel="noopener">{texto or "Perfil " + id_ + " en el Árbol de FamilySearch"}</a>'

JABLE = "https://jable.ulpgc.es/jable/"

# ----------------------------------------------------------------------------------
# DOCUMENTOS CON IMAGEN  (img = recorte o página; grande = imagen completa opcional)
# ----------------------------------------------------------------------------------
DOC = {
    "trinidad1878": dict(
        titulo="Llegada del Trinidad a La Habana (Diario de la Marina, 27 dic 1878)",
        imgs=["img/prensa/1878-diario-marina-trinidad.jpg"],
        grande="img/prensa/1878-diario-marina-p1-completa.jpg",
        texto="«Día 25. — Las Palmas de Gran Canaria y Gibara en 47 días bca. esp. Trinidad, cap. Marrero, tons. 449, trip. 25, con frutos, á Martínez, Galván y Cp. — Pasajeros 298.»",
        fuente='<i>Diario de la Marina</i> (La Habana), 27 dic 1878, p. 1, «Puerto de la Habana. Entradas de travesía». <a href="https://ufdc.ufl.edu/UF00001565/18265" target="_blank" rel="noopener">UF Digital Collections</a>.'),
    "carta1879": dict(
        titulo="Carta de los pasajeros del Trinidad (El Independiente, 13 feb 1879)",
        imgs=["img/prensa/1879-independiente-carta-felix-juan.jpg", "img/prensa/1879-independiente-carta-inicio.jpg"],
        grande="img/prensa/1879-independiente-p2-completa.jpg",
        texto="«También merece que de D. Félix Naranjo y de D. Antonio Ojeda digamos que en los servicios tan necesarios que voluntariamente se obligaron á desempeñar hemos hallado muchas comodidades.» — Firmada en «Habana, Diciembre 28 de 1878». El primer firmante es Juan Naranjo Cabrera.",
        fuente=f'<i>El Independiente</i> (Las Palmas), 13 feb 1879, p. 2. <a href="{JABLE}el.independiente/1879/02/13/0002.htm" target="_blank" rel="noopener">Jable (ULPGC)</a>.'),
    "hoy1933": dict(
        titulo="Félix Naranjo Fernández denuncia el robo de su bicicleta (Hoy, 21 feb 1933)",
        imgs=["img/prensa/1933-hoy-felix-naranjo-fernandez.jpg"],
        grande="img/prensa/1933-hoy-p2-completa.jpg",
        texto="«Félix Naranjo Fernández ha presentado una denuncia en la Comisaría de Vigilancia, por hurto de una bicicleta de su propiedad.»",
        fuente=f'<i>Hoy</i>, diario republicano de Tenerife, 21 feb 1933, p. 2. <a href="{JABLE}hoy/1933/02/21/0002.htm" target="_blank" rel="noopener">Jable (ULPGC)</a>.'),
    "gaceta1936": dict(
        titulo="Félix Naranjo, de 31 años, en la Casa de Socorro (Gaceta de Tenerife, 14 mar 1936)",
        imgs=["img/prensa/1936-gaceta-tenerife-felix-naranjo.jpg"],
        grande="img/prensa/1936-gaceta-tenerife-p6-completa.jpg",
        texto="«Félix Naranjo, de 31 años de edad, domiciliado en la calle de Santa Rosalía, de herida incisa en el dedo pulgar de la mano izquierda; leve.»",
        fuente=f'<i>Gaceta de Tenerife</i>, 14 mar 1936, p. 6, sección «Casa de Socorro». <a href="{JABLE}gaceta.de.tenerife/1936/03/14/0006.htm" target="_blank" rel="noopener">Jable (ULPGC)</a>.'),
}

# ----------------------------------------------------------------------------------
# PERSONAS
#   nombre, fechas, resumen, datos [(etiqueta, valor)], vida [(fecha, hecho)],
#   docs [claves de DOC], enlaces [html], pendiente [texto], padres/conyuge/hijos [slugs]
# ----------------------------------------------------------------------------------
P = {}
def persona(slug, **k):
    k.setdefault("datos", []); k.setdefault("vida", []); k.setdefault("docs", [])
    k.setdefault("enlaces", []); k.setdefault("pendiente", []); k.setdefault("familia", [])
    P[slug] = k

persona("adrian-naranjo-cubas", nombre="Adrián Naranjo y Cubas", fechas="n. 1799",
    resumen="Vecino de Telde y perito agrónomo de Canarias. Padre de dieciocho hijos, los Naranjo Cabrera, varios de los cuales emigraron a Venezuela y Cuba.",
    datos=[("Nacimiento", "1799 (según el Árbol de FamilySearch)"), ("Padres", "Salvador González Naranjo y Ana Rosalía de Cubas Ortega y Medina (Geneanet)"), ("Abuelos", "Cayetano Naranjo Muñiz y María Margarita González de la Fuente; Adrián José Nicolás de Cubas y Medina y María de los Ángeles de Ortega y Medina"), ("Esposa", "Antonia Cabrera y Padrón (Josefa Antonia Cabrera de Quintana y Padrón)"), ("Matrimonio", "Telde, 27 sep 1818"), ("Hijos", "18 según el Árbol de FamilySearch")],
    vida=[("27 sep 1818", "Se casa en Telde con Antonia Cabrera y Padrón."), ("1857-1861", "Aparece como vecino de Telde en listas de contribuyentes del Boletín Oficial de Canarias."), ("25 jul 1859", "Renuncia a su cargo de perito agrónomo de Canarias (Boletín Oficial de Canarias).")],
    enlaces=[perfil("KCFZ-LSS")],
    familia=["antonia-cabrera-padron", "salvador-naranjo-cabrera", "francisco-javier-naranjo-cabrera", "jose-naranjo-cabrera", "manuel-naranjo-cabrera", "juan-naranjo-cabrera", "felix-naranjo-cabrera"])

persona("antonia-cabrera-padron", nombre="Antonia Cabrera y Padrón", fechas="c. Telde, 1818",
    resumen="Josefa Antonia Cabrera de Quintana y Padrón, madre de los dieciocho hermanos Naranjo Cabrera. Su familia (los Cabrera y los Padrón) tenía también una rama en Aragua, Venezuela.",
    datos=[("Padres", "Pedro de Alcántara Cabrera de Quintana y María Isidro (Isidora) de Ortega Padrón y Chil"), ("Esposo", "Adrián Naranjo y Cubas (Telde, 1818)"), ("Hermano", "Pedro Cabrera, que vivió en La Victoria (Venezuela) y se casó allí en 1860")],
    vida=[("27 sep 1818", "Se casa en Telde con Adrián Naranjo y Cubas."), ("16 abr 1860", f"Su hermano Pedro Cabrera se casa en La Victoria con María del Carmen Zumbado; testigo, su hijo Salvador Naranjo. {ark('3:1:33S7-9RRF-9MZ5', 'Imagen en FamilySearch')}")],
    enlaces=[perfil("K88R-8XN")],
    familia=["adrian-naranjo-cubas", "felix-naranjo-cabrera"])

persona("felix-naranjo-cabrera", nombre="Félix Naranjo Cabrera", fechas="n. Telde, 20 oct 1843", clave=True, foto="img/fotos/felix-naranjo-cabrera.jpg", pie_foto="Retrato identificado por la familia como Félix Naranjo Cabrera.",
    resumen="Labrador de Telde. Vivió temporadas en La Victoria (Venezuela), donde estaban sus hermanos, y en 1878 se embarcó para Cuba, la tierra de su mujer. Sus hijos formaron la rama cubana de la familia, en Pinar del Río.",
    datos=[("Nacimiento", "Telde, 20 oct 1843"), ("Padres", "Adrián Naranjo y Cubas y Antonia Cabrera y Padrón"), ("Oficio", "Labrador (acta de 1875)"), ("Esposa", "Rosalía Rodríguez Valdés, natural de Cuba"), ("Matrimonio", "Telde, 16 jun 1870 (velados el 17 oct 1874)"), ("Hijos", "Agustín Benito (1875), Adrián Salvador (1877) y Natalio (1878)"), ("Defunción", "Desconocida")],
    vida=[("16 jun 1870", "Se casa en Telde con Rosalía Rodríguez Valdés."),
          ("3 abr 1875", "Nace su hijo Agustín. En el acta civil, Félix figura «domiciliado en el pueblo de la Victoria en Caracas»."),
          ("2 may 1877", "Nace su hijo Adrián Salvador en Telde."),
          ("h. 8 nov 1878", "Sale de Las Palmas hacia Cuba en el bergantín-barca <i>Trinidad</i>, con su hermano Juan."),
          ("1 dic 1878", "Nace su hijo Natalio en Telde, con Félix ya en alta mar."),
          ("25 dic 1878", "Llega a La Habana tras 47 días de viaje, con escala en Gibara."),
          ("28 dic 1878", "Los pasajeros le dan las gracias públicamente por «los servicios que voluntariamente» prestó a bordo.")],
    docs=["trinidad1878", "carta1879"],
    enlaces=[perfil("MRKQ-LVM")],
    pendiente=["Su defunción: las memorias familiares dicen que «se quedó en Canarias». Hay que pedirla al Registro Civil y a la parroquia de Telde.",
               "No aparece en ningún registro de La Victoria (Venezuela) de 1864 a 1890, ni en los protocolos consulares de Pinar del Río (1900-1901) y La Habana (1902-1908)."],
    familia=["adrian-naranjo-cubas", "antonia-cabrera-padron", "rosalia-rodriguez-valdes", "agustin-naranjo-rodriguez", "adrian-naranjo-rodriguez", "natalio-naranjo-rodriguez", "salvador-naranjo-cabrera", "juan-naranjo-cabrera"])

persona("rosalia-rodriguez-valdes", nombre="Rosalía Rodríguez Valdés", fechas="n. Consolación del Sur (Cuba)", clave=True,
    resumen="Cubana de Pinar del Río, casada en Telde con Félix. Según la tradición familiar volvió a Cuba con sus hijos y otros parientes antes de 1900.",
    datos=[("Nacimiento", "Consolación del Sur, provincia de Pinar del Río (Cuba)"), ("Padres", "Agustín Rodríguez de Sosa y Regina de los Ángeles Valdés Delgado"), ("Hermanos", "Carolina (madrina de Natalio), Lucas y Juan Rodríguez Valdés"), ("Esposo", "Félix Naranjo Cabrera (Telde, 16 jun 1870)")],
    vida=[("16 jun 1870", "Se casa en Telde con Félix Naranjo Cabrera."), ("1875-1878", "Nacen en Telde sus hijos Agustín, Adrián y Natalio."), ("antes de 1900", "Vuelve a Cuba con sus hijos y sus hermanos Lucas y Juan; unas 16 personas de la familia (memorias de Nina).")],
    docs=[],
    enlaces=[perfil("GC44-R8Z")],
    pendiente=["Su bautismo en Consolación del Sur: esos libros no están en FamilySearch.", "Su defunción en Cuba.", "Las matrículas parroquiales de Telde (1886-1907) dirían en qué año se marchó."],
    familia=["felix-naranjo-cabrera", "agustin-naranjo-rodriguez", "adrian-naranjo-rodriguez", "natalio-naranjo-rodriguez"])

persona("agustin-naranjo-rodriguez", nombre="Agustín Benito Naranjo Rodríguez", fechas="Telde, 1875 – Pinar del Río, h. 1950-1955", clave=True,
    resumen="El mayor de los tres hermanos. Emigró a Cuba y formó su familia en Pinar del Río con Quirina Fernández. Su vínculo con Félix y Rosalía está documentado en el nacimiento de su hija Inocencia.",
    datos=[("Nacimiento", "Telde, 3 abr 1875 (bautizado el mismo día)"), ("Padres", "Félix Naranjo Cabrera y Rosalía Rodríguez Valdés"), ("Madrina", "Su abuela Regina de los Ángeles Valdés Delgado"), ("Pareja", "Quirina Fernández Fernández, natural de San Luis (Pinar del Río), hija de Antonio Fernández (canario) e Inocencia Fernández"), ("Hijos", "Juana (1908), José (1914), Inocencia «Nina» (1915) y Felicita"), ("Residencia", "Pinar del Río (consta en 1927)"), ("Defunción", "Carretera de La Coloma, Pinar del Río, entre 1950 y 1955 (tradición familiar)")],
    vida=[("3 abr 1875", "Nace y se bautiza en Telde."), ("antes de 1900", "Emigra a Cuba con su madre y sus hermanos."), ("24 jun 1908", "Nace su hija Juana."), ("26 abr 1914", "Nace su hijo José."), ("20 jun 1915", "Nace su hija Inocencia «Nina» en el Barrio Primero de Ovas, Pinar del Río."), ("4 oct 1927", "Comparece en el Registro Civil de Pinar del Río para inscribir a Inocencia; consta como natural de Canarias, hijo de Félix y Rosalía."), ("h. 1950-1955", "Muere en la carretera de La Coloma, Pinar del Río.")],
    docs=[],
    enlaces=[perfil("GLX3-WSP")],
    pendiente=["Su defunción en el Registro Civil de Pinar del Río.", "Su matrimonio civil con Quirina, si lo hubo.", "Archivo Nacional de Cuba: Registro General de Españoles de 1899-1900."],
    familia=["felix-naranjo-cabrera", "rosalia-rodriguez-valdes", "quirina-fernandez-fernandez", "juana-naranjo-fernandez", "jose-naranjo-fernandez", "inocencia-naranjo-fernandez", "adrian-naranjo-rodriguez", "natalio-naranjo-rodriguez"])

persona("quirina-fernandez-fernandez", nombre="Quirina Úrsula Fernández Fernández", fechas="n. San Luis (Pinar del Río)", foto="img/fotos/quirina-fernandez.jpg",
    resumen="Cubana de San Luis, en la provincia de Pinar del Río, hija de un canario. Compañera de Agustín Naranjo y madre de sus hijos.",
    datos=[("Nacimiento", "San Luis, Pinar del Río (Cuba)"), ("Padres", "Antonio Fernández (canario) e Inocencia Fernández"), ("Pareja", "Agustín Benito Naranjo Rodríguez"), ("Hijos", "Juana, José, Inocencia «Nina» y Felicita Naranjo Fernández")],
    enlaces=[perfil("GLX3-6WW")],
    familia=["agustin-naranjo-rodriguez", "juana-naranjo-fernandez", "jose-naranjo-fernandez", "inocencia-naranjo-fernandez", "felicita-naranjo-fernandez"])

persona("juana-naranjo-fernandez", nombre="Juana Naranjo Fernández", fechas="1908 – Lisboa, 2012", foto="img/fotos/juana-naranjo-fernandez.jpg",
    resumen="Hija de Agustín y Quirina, la mayor de los hermanos conocidos. Según la familia murió en Lisboa con 104 años.",
    datos=[("Nacimiento", "24 jun 1908 (Cuba)"), ("Padres", "Agustín Naranjo Rodríguez y Quirina Fernández Fernández"), ("Defunción", "12 oct 2012, Lisboa (Portugal)")],
    pendiente=["Documentar su nacimiento y su defunción."],
    familia=["agustin-naranjo-rodriguez", "quirina-fernandez-fernandez", "inocencia-naranjo-fernandez", "jose-naranjo-fernandez", "felicita-naranjo-fernandez"])

persona("jose-naranjo-fernandez", nombre="José Naranjo Fernández", fechas="1914 – 1989", foto="img/fotos/jose-naranjo-fernandez.jpg",
    resumen="Hijo de Agustín y Quirina.",
    datos=[("Nacimiento", "26 abr 1914 (Cuba)"), ("Padres", "Agustín Naranjo Rodríguez y Quirina Fernández Fernández"), ("Defunción", "2 ago 1989")],
    pendiente=["Documentar su nacimiento y su defunción."],
    familia=["agustin-naranjo-rodriguez", "quirina-fernandez-fernandez", "inocencia-naranjo-fernandez", "juana-naranjo-fernandez", "felicita-naranjo-fernandez"])

persona("felicita-naranjo-fernandez", nombre="Felicita Naranjo Fernández", fechas="sin fechas documentadas",
    resumen="Hija de Agustín y Quirina, según el árbol familiar. Sin documentar.",
    datos=[("Padres", "Agustín Naranjo Rodríguez y Quirina Fernández Fernández")],
    pendiente=["Cualquier documento que confirme su nacimiento."],
    familia=["agustin-naranjo-rodriguez", "quirina-fernandez-fernandez", "juana-naranjo-fernandez", "jose-naranjo-fernandez", "inocencia-naranjo-fernandez"])

persona("adrian-naranjo-rodriguez", nombre="Adrián Salvador Naranjo Rodríguez", fechas="n. Telde, 2 may 1877", clave=True,
    resumen="El segundo de los hermanos. Lleva el nombre de su abuelo y de su padrino, el tío Salvador de Venezuela. En 1900 estaba en Pinar del Río.",
    datos=[("Nacimiento", "Telde, 2 may 1877; bautizado el 4 may"), ("Padres", "Félix Naranjo Cabrera y Rosalía Rodríguez Valdés"), ("Padrino", "Su tío Salvador Naranjo Cabrera")],
    vida=[("2 may 1877", "Nace en Telde."), ("5 abr 1900", "Se inscribe como español en Pinar del Río, «25 años, soltero, natural de Santa Cruz de Tenerife» (memorias familiares; la edad cuadra mejor con Agustín).")],
    docs=[],
    pendiente=["Ver la inscripción de 1900 en el Archivo Nacional de Cuba (Registro General de Españoles).", "Su vida posterior en Cuba."],
    familia=["felix-naranjo-cabrera", "rosalia-rodriguez-valdes", "agustin-naranjo-rodriguez", "natalio-naranjo-rodriguez", "salvador-naranjo-cabrera"])

persona("natalio-naranjo-rodriguez", nombre="Natalio Naranjo Rodríguez", fechas="n. Telde, 1 dic 1878", clave=True,
    resumen="El menor. Nació en Telde cuando su padre ya navegaba hacia La Habana. Emigró a Cuba con su madre y sus hermanos. Fue padre de Félix Naranjo Fernández, que en 1924 se fue a Canarias.",
    datos=[("Nacimiento", "Telde, 1 dic 1878; bautizado el 9 dic"), ("Padres", "Félix Naranjo Cabrera y Rosalía Rodríguez Valdés"), ("Madrina", "Su tía Carolina Rodríguez Valdés"), ("Hijos", "Félix Naranjo Fernández (n. h. 1904-1905, en Cuba)")],
    vida=[("1 dic 1878", "Nace en Telde; su padre había salido hacia Cuba unas tres semanas antes."), ("antes de 1900", "Emigra a Cuba con su madre y sus hermanos."), ("h. 1904-1905", "Nace en Cuba su hijo Félix Naranjo Fernández."), ("1924", "Su hijo Félix se va a Canarias (memorias de Nina).")],
    docs=[],
    pendiente=["Cualquier documento suyo en Cuba: matrimonio (con una Fernández), nacimiento de su hijo Félix, defunción."],
    familia=["felix-naranjo-cabrera", "rosalia-rodriguez-valdes", "felix-naranjo-fernandez", "agustin-naranjo-rodriguez", "adrian-naranjo-rodriguez"])

persona("inocencia-naranjo-fernandez", nombre="Inocencia María «Nina» Naranjo Fernández", fechas="Pinar del Río, 1915 – La Habana, 2010",
    resumen="Hija de Agustín y Quirina. Su certificado de nacimiento es la prueba de que su padre era hijo de Félix y Rosalía. Sus memorias recogen la historia de la familia en Cuba.",
    datos=[("Nacimiento", "20 jun 1915, Barrio Primero de Ovas, Pinar del Río (Cuba)"), ("Padres", "Agustín Naranjo (natural de Canarias) y Quirina Fernández (natural de San Luis)"), ("Abuelos paternos", "matrimonio de origen: Félix y Rosalía"), ("Abuelos maternos", "Antonio e Inocencia"), ("Esposo", "Hugo Ángel Fernández Arada (Pinar del Río, 2 oct 1913 – entre 1984 y 1989)"), ("Defunción", "La Habana, 2010")],
    vida=[("20 jun 1915", "Nace en el Barrio Primero de Ovas, Pinar del Río."), ("4 oct 1927", "Su padre la inscribe en el Registro Civil de Pinar del Río."), ("2010", "Muere en La Habana.")],
    docs=[],
    enlaces=[perfil("GLX3-JVF")],
    familia=["agustin-naranjo-rodriguez", "quirina-fernandez-fernandez", "hugo-fernandez-arada", "juana-naranjo-fernandez", "jose-naranjo-fernandez", "felicita-naranjo-fernandez"])

persona("hugo-fernandez-arada", nombre="Hugo Ángel Fernández Arada", fechas="Pinar del Río, 1913 – h. 1984-1989",
    resumen="Esposo de Inocencia «Nina» Naranjo Fernández. Tuvieron cinco hijos, nacidos entre 1942 y 1955.",
    datos=[("Nacimiento", "2 oct 1913, Pinar del Río (Cuba)"), ("Esposa", "Inocencia María Naranjo Fernández"), ("Hijos", "Cinco, nacidos entre 1942 y 1955 (personas vivas: no se publican sus datos)"), ("Defunción", "Entre 1984 y 1989")],
    pendiente=["Documentar su matrimonio con Inocencia y su defunción."],
    familia=["inocencia-naranjo-fernandez"])

persona("felix-naranjo-fernandez", nombre="Félix Naranjo Fernández", fechas="n. h. 1904-1905 · Cuba y Santa Cruz de Tenerife",
    resumen="Hijo de Natalio Naranjo Rodríguez; lleva el nombre de su abuelo Félix. Nació en Cuba y en 1924 se fue a Canarias. Un Félix Naranjo Fernández vivía en Santa Cruz de Tenerife en los años treinta con la edad que le corresponde: muy probablemente es él.",
    datos=[("Padre", "Natalio Naranjo Rodríguez (según la familia)"), ("Madre", "De apellido Fernández; sin identificar"), ("Abuelos paternos", "Félix Naranjo Cabrera y Rosalía Rodríguez Valdés"), ("Nacimiento", "Hacia 1904-1905, en Cuba (tenía 31 años en marzo de 1936)"), ("Domicilio", "Calle de Santa Rosalía, Santa Cruz de Tenerife (1936)"), ("Nota", "Las memorias de Nina cuentan que Félix, nacido en Cuba, se fue a Canarias en 1924 para curarse y ya no volvió.")],
    vida=[("1924", "Viaja de Cuba a Canarias (tradición familiar)."), ("21 feb 1933", "Denuncia el robo de su bicicleta en Santa Cruz de Tenerife."), ("14 mar 1936", "Atendido en la Casa de Socorro por un corte en el pulgar; «de 31 años, domiciliado en la calle de Santa Rosalía».")],
    docs=["hoy1933", "gaceta1936"],
    pendiente=["Padrón municipal de Santa Cruz (1930-1945): daría su fecha y lugar de nacimiento y el nombre de su madre.", "Libros de enterramientos de los cementerios de Santa Cruz.", "Con eso, pedir su defunción o matrimonio al Registro Civil."],
    familia=["natalio-naranjo-rodriguez", "felix-naranjo-cabrera", "rosalia-rodriguez-valdes"])

persona("salvador-naranjo-cabrera", nombre="Salvador José Naranjo Cabrera", fechas="Telde, 1819 – Venezuela",
    resumen="El mayor de los hermanos Naranjo Cabrera. Llegó a Venezuela con 18 años y se estableció en La Victoria (Aragua). Fue padrino de su sobrino Adrián Salvador en 1877.",
    datos=[("Nacimiento", "Telde, 23 nov 1819"), ("Llegada a Venezuela", "Hacia 1837, con 18 años"), ("Esposa", "Josefa Cabrera Padrón, hija de Apolinario Cabrera y Ana Padrón"), ("Matrimonio", "La Victoria (Aragua), 28 jun 1862"), ("Hijos conocidos", "Antonia Evarista (1862), Adrián Eulogio (1866-1942, Caracas), Narciso (h. 1867-1900), José (h. 1869-1881), Rafael de Jesús (1870), Rosa y Aurelia (enterradas en 1900)")],
    vida=[("h. 1837", "Llega de Canarias a Venezuela."),
          ("16 abr 1860", f"Testigo en la boda de su tío Pedro Cabrera en La Victoria. {ark('3:1:33S7-9RRF-9MZ5', 'Imagen')}"),
          ("1862", f"Expediente de soltería y dispensa para casarse: «natural de la isla de Gran Canaria», hijo de Adrián Naranjo y Antonia Cabrera. {ark('3:1:33SQ-GRR1-9LQB', 'Imagen')}"),
          ("28 jun 1862", f"Se casa en La Victoria con Josefa Cabrera; testigo, su hermano Manuel. {ark('1:1:X9LX-X2RV', 'Registro')} · {ark('3:1:33SQ-GRRF-999K', 'Imagen')}"),
          ("10 mar 1866", f"Nace su hijo Adrián Eulogio del Carmen, que murió en Caracas en 1942. {ark('1:1:6DRG-YSCL', 'Registro')}"),
          ("1867", "Padrino de su sobrino póstumo Francisco Javier, en San Sebastián."),
          ("4 may 1877", "Padrino de su sobrino Adrián Salvador en Telde."),
          ("6 oct 1881", f"Muere su hijo José, de 12 años, en La Victoria. {ark('3:1:33SQ-GRRB-SZ13', 'Imagen')}"),
          ("1900", f"Entierros de sus hijos Rosa (17 mar), Narciso (16 jun, 33 años) y Aurelia (13 sep) en La Victoria. {ark('1:1:XSX4-8PC4', 'Rosa')} · {ark('1:1:XSXC-C9N7', 'Aurelia')}")],
    enlaces=[perfil("MRKQ-LZV"), perfil("GRC9-9QP", "Su hijo Adrián Eulogio (GRC9-9QP)")],
    familia=["adrian-naranjo-cubas", "felix-naranjo-cabrera", "francisco-javier-naranjo-cabrera", "manuel-naranjo-cabrera", "adrian-naranjo-rodriguez"])

persona("francisco-javier-naranjo-cabrera", nombre="Francisco Javier Naranjo Cabrera", fechas="Telde, 1820 – San Sebastián (Aragua), 1866",
    resumen="Uno de los hermanos Naranjo Cabrera que emigraron a Venezuela. Se casó en Aragua con María de Jesús Zumbado y murió joven; su último hijo nació ocho meses después de su muerte.",
    datos=[("Nacimiento", "Telde, 1820"), ("Esposa", "María de Jesús Zumbado (1857, con dispensa de parentesco)"), ("Defunción", "San Sebastián (Aragua), 21 oct 1866"), ("Hijos conocidos", "Josefa Antonia (casada en 1878 con Rafael Ortega), Francisco Javier (póstumo, 1867); quizá Rosario")],
    vida=[("1857", "Expediente de dispensa para casarse con María de Jesús Zumbado; incluye un árbol de parentesco con los abuelos Pedro Cabrera y María Isidora Padrón."),
          ("21 oct 1866", f"Entierro en San Sebastián, «natural de las Canarias», casado con María de Jesús Zumbado; entierro de primera con música. {ark('3:1:33SQ-GRRL-9CZ6', 'Imagen')}"),
          ("5 ago 1867", f"Bautismo de su hijo póstumo Francisco Javier; padrino, su hermano Salvador. {ark('3:1:33S7-9RRL-9Q26', 'Imagen')}"),
          ("30 sep 1878", f"Su hija Josefa Antonia se casa en San Sebastián con Rafael Ortega. {ark('3:1:33SQ-GRRL-BDH', 'Imagen')}")],
    familia=["adrian-naranjo-cubas", "salvador-naranjo-cabrera", "manuel-naranjo-cabrera", "felix-naranjo-cabrera"])

persona("manuel-naranjo-cabrera", nombre="Manuel Naranjo Cabrera", fechas="1839 – 1913 · La Victoria (Aragua)",
    resumen="Uno de los hermanos Naranjo Cabrera, establecido en La Victoria (Aragua, Venezuela). Fue padrino de muchos niños del pueblo y testigo en la boda de su hermano Salvador.",
    datos=[("Nacimiento", "1839"), ("Defunción", "1913"), ("Esposa", "Inelda (Ynelda) del Nogal"), ("Hijos", "8 según el Árbol de FamilySearch; entre ellos Luisa Elena de Lourdes (bautizada en San Sebastián el 1 nov 1895)")],
    vida=[("28 jun 1862", "Testigo en la boda de su hermano Salvador en La Victoria."), ("1865-1871", "Padrino en al menos ocho bautismos de La Victoria."), ("13 ene 1877", f"Padrino de Adrián María de los Dolores, hijo de Rómulo Navarro y Rosario Naranjo (¿sobrina suya?). {ark('3:1:33S7-9RRV-98HN', 'Imagen')}")],
    enlaces=[perfil("MRKQ-LJD")],
    familia=["adrian-naranjo-cubas", "salvador-naranjo-cabrera", "francisco-javier-naranjo-cabrera", "felix-naranjo-cabrera"])

persona("juan-naranjo-cabrera", nombre="Juan Naranjo Cabrera", fechas="n. 1841",
    resumen="Uno de los hermanos Naranjo Cabrera. Viajó a Cuba en 1878 en el Trinidad, con su hermano Félix. Es el primer firmante de la carta de los pasajeros escrita en La Habana el 28 dic 1878.",
    datos=[("Nacimiento", "1841"), ("Matrimonio", "Las Palmas, 1868 (según el Árbol de FamilySearch)")],
    vida=[("h. 8 nov 1878", "Sale de Las Palmas hacia Cuba con Félix en el <i>Trinidad</i>."), ("28 dic 1878", "Firma, el primero, la carta de agradecimiento de los pasajeros en La Habana.")],
    docs=["carta1879"],
    pendiente=["Qué fue de él en Cuba. No confundirlo con el Juan Naranjo Cabrera de San Lorenzo (Las Palmas), nacido hacia 1880."],
    familia=["adrian-naranjo-cubas", "felix-naranjo-cabrera"])

persona("jose-naranjo-cabrera", nombre="José Naranjo Cabrera", fechas="1836 – 1896",
    resumen="Uno de los hermanos Naranjo Cabrera. Sus hijos nacieron entre Cuba y Las Palmas y formaron una rama habanera de la familia, que pudo acoger a Rosalía y a sus hijos.",
    datos=[("Nacimiento", "1836"), ("Defunción", "1896"), ("Esposa", "… Martínez de Escobar"), ("Hijos", "Adrián Naranjo Martínez de Escobar (Puerto Príncipe 1865 – La Habana 1938) y Bartolomé (Las Palmas 1874, casado en La Habana con Ángela Hernández)")],
    vida=[("1865", "Nace su hijo Adrián en Puerto Príncipe (Camagüey, Cuba)."), ("1874", "Nace su hijo Bartolomé en Las Palmas."), ("1938", "Muere su hijo Adrián en La Habana, con descendencia.")],
    familia=["adrian-naranjo-cubas", "felix-naranjo-cabrera"])

ORDEN_PERSONAS = ["adrian-naranjo-cubas", "antonia-cabrera-padron",
    "salvador-naranjo-cabrera", "francisco-javier-naranjo-cabrera", "jose-naranjo-cabrera", "manuel-naranjo-cabrera", "juan-naranjo-cabrera", "felix-naranjo-cabrera", "rosalia-rodriguez-valdes",
    "agustin-naranjo-rodriguez", "quirina-fernandez-fernandez", "adrian-naranjo-rodriguez", "natalio-naranjo-rodriguez",
    "juana-naranjo-fernandez", "felicita-naranjo-fernandez", "inocencia-naranjo-fernandez", "hugo-fernandez-arada", "jose-naranjo-fernandez", "felix-naranjo-fernandez"]

# ----------------------------------------------------------------------------------
# PLANTILLA
# ----------------------------------------------------------------------------------
MENU = [("index.html", "Árbol"), ("personas.html", "Personas"), ("viajes.html", "Viajes"), ("cronologia.html", "Cronología"), ("fuentes.html", "Fuentes y pendientes")]

BARCO = '''<svg class="barco" viewBox="0 0 64 40" aria-hidden="true"><path d="M6 28 h52 l-7 8 H13 z" fill="currentColor"/><path d="M31 4 v24 M31 4 l-15 20 h15 M33 7 l13 17 h-13" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M31 4 l7 -2" stroke="currentColor" stroke-width="1.4"/></svg>'''

def pagina(nombre_archivo, titulo, descripcion, contenido, base="", actual=None, clase=""):
    menu = "\n".join(f'    <a href="{base}{h}"{" aria-current=\"page\"" if h == actual else ""}>{n}</a>' for h, n in MENU)
    doc = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descripcion)}">
<link rel="icon" href="{base}img/escudo-naranjo.png">
<link rel="stylesheet" href="{base}{ver('estilo.css')}">
</head>
<body class="{clase}">
<header class="sitio"><div class="envoltura cabecera">
  <a class="sello" href="{base}index.html" title="Inicio"><img src="{base}img/escudo-naranjo.png" alt="Escudo de los Naranjo"></a>
  <div class="titulos">
    <a class="marca" href="{base}index.html">Los <span>Naranjo</span> de Telde</a>
    <span class="lema">De Gran Canaria a Venezuela y Cuba · siglos XIX y XX</span>
  </div>
  <nav class="menu">
{menu}
  </nav>
</div></header>
<main class="envoltura">
{contenido}
</main>
<footer><div class="envoltura">
  {BARCO.replace('class="barco"', 'class="barco pie"')}
  <p>Investigación familiar en curso. Solo se publican personas fallecidas.<br>
  Fuentes: archivo parroquial y Registro Civil de Telde, memorias familiares, FamilySearch, Jable (ULPGC), UF Digital Collections, Hemeroteca Digital BNE y el libro <i>Los Naranjos</i> (escudo).</p>
</div></footer>
</body>
</html>
"""
    destino = RAIZ / nombre_archivo
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    print("generada", nombre_archivo)

# ----------------------------------------------------------------------------------
# PIEZAS
# ----------------------------------------------------------------------------------
def nodo(slug, base=""):
    p = P[slug]
    clase = "persona" + (" clave" if p.get("clave") else "") + (" dudosa" if p.get("dudosa") else "") + (" con-foto" if p.get("foto") else "")
    foto = f'<img class="miniatura" src="{base}{p["foto"]}" alt="" loading="lazy">' if p.get("foto") else ""
    docs = f'<i class="marca-docs" title="{len(p["docs"])} documento(s)">{len(p["docs"])} doc.</i>' if p.get("docs") else ""
    return f'<a class="{clase}" href="{base}personas/{slug}.html">{foto}<b>{p["nombre"]}</b><small>{p["fechas"]}</small>{docs}</a>'

def nodo_libre(nombre, fechas, clase="persona tenue"):
    return f'<span class="{clase}"><b>{nombre}</b><small>{fechas}</small></span>'

def bloque_doc(clave, base):
    d = DOC[clave]
    imgs = "".join(f'<a href="{base}{i}" target="_blank" title="Abrir a tamaño completo"><img src="{base}{i}" alt="{html.escape(d["titulo"])}" loading="lazy"></a>' for i in d["imgs"])
    grande = f' · <a href="{base}{d["grande"]}" target="_blank">Ver la página completa</a>' if d.get("grande") else ""
    return f"""<figure class="documento">
  <div class="imagenes">{imgs}</div>
  <figcaption><b>{d["titulo"]}</b><br><span class="transcripcion">{d["texto"]}</span><br><span class="fuente">{d["fuente"]}{grande}</span></figcaption>
</figure>"""

# ----------------------------------------------------------------------------------
# ÁRBOL (portada)
# ----------------------------------------------------------------------------------
MAPA = '''<svg class="mapa" viewBox="0 0 900 300" role="img" aria-label="Rutas de la familia: de Gran Canaria a La Guaira (Venezuela) y a La Habana (Cuba)">
  <defs>
    <pattern id="olas" width="40" height="12" patternUnits="userSpaceOnUse"><path d="M0 6 q10 -6 20 0 t20 0" fill="none" stroke="currentColor" stroke-opacity=".12" stroke-width="1"/></pattern>
  </defs>
  <rect width="900" height="300" fill="url(#olas)"/>
  <!-- costas esquemáticas -->
  <path class="tierra" d="M0 40 C60 50 120 30 170 60 C200 75 230 70 265 88 L300 100 C280 110 240 108 205 112 C170 116 120 104 80 110 C50 114 20 106 0 108 Z"/>
  <path class="tierra" d="M150 250 C220 236 300 240 360 250 C420 258 470 244 520 262 L520 300 L150 300 Z"/>
  <path class="tierra" d="M820 20 C850 30 880 26 900 36 L900 120 C880 112 860 118 840 110 C830 80 815 50 820 20 Z"/>
  <g class="islas"><circle cx="760" cy="150" r="5"/><circle cx="782" cy="158" r="6"/><circle cx="740" cy="160" r="4"/><circle cx="802" cy="150" r="4"/><circle cx="720" cy="152" r="3"/><circle cx="825" cy="142" r="4"/></g>
  <!-- rutas -->
  <path class="ruta" d="M780 158 C640 140 480 110 300 96"/>
  <path class="ruta" d="M780 160 C650 200 520 238 400 250"/>
  <!-- rótulos -->
  <text x="700" y="185" class="rotulo">Gran Canaria · Telde</text>
  <text x="845" y="70" class="rotulo">España</text>
  <text x="160" y="85" class="rotulo">Cuba</text>
  <text x="262" y="128" class="rotulo pequeno">La Habana · Pinar del Río</text>
  <text x="300" y="285" class="rotulo">Venezuela</text>
  <text x="380" y="242" class="rotulo pequeno">La Guaira · La Victoria</text>
  <text x="520" y="105" class="rotulo pequeno it">1878 · bergantín-barca Trinidad, 47 días</text>
  <text x="560" y="222" class="rotulo pequeno it">h. 1837-1860 · los Naranjo Cabrera a Venezuela</text>
  <g transform="translate(540 110) scale(.7)" class="nave">BARCO</g>
  <g transform="translate(600 190) scale(.6)" class="nave">BARCO</g>
  <text x="440" y="30" class="rosa">✥</text>
</svg>'''.replace("BARCO", BARCO.replace('<svg class="barco" viewBox="0 0 64 40" aria-hidden="true">', "").replace("</svg>", ""))

def portada():
    import sys
    sys.path.insert(0, str(RAIZ))
    import _datos_arbol
    personas = _datos_arbol.generar(P, RAIZ / "arbol-datos.js")
    atajos = [
        ("salvador-gonzalez-naranjo", "Todo el árbol", "desde Telde, s. XVIII"),
        ("diego-perez-naranjo", "Los primeros Naranjo", "h. 1470"),
        ("gregorio-suarez-navarro-naranjo", "Gregorio Suárez Navarro Naranjo", "1668"),
        ("adrian-naranjo-cubas", "Adrián Naranjo y Cubas y sus 18 hijos", "1799"),
        ("felix-naranjo-cabrera", "Félix y Rosalía", "1870"),
        ("salvador-naranjo-cabrera", "La rama de Venezuela", "h. 1837"),
        ("patricio-naranjo-cabrera", "Los Naranjo de Puerto Príncipe", "Cuba"),
        ("agustin-naranjo-rodriguez", "La rama de Pinar del Río", "Cuba"),
    ]
    botones = "".join(f'<button type="button" data-id="{i}"><b>{t}</b><small>{f}</small></button>' for i, t, f in atajos if i in personas)
    contenido = f"""
<section class="portada">
  <div class="escudo-grande"><img src="img/escudo-naranjo.png" alt="Escudo de armas de los Naranjo: en campo de oro, un naranjo de sinople frutado y un leopardo pasante al pie del tronco"><p>«De oro, un árbol de sinople, frutado de oro, y un leopardo de su color natural, pasante al pie del tronco.»<br><span>Armas de los Naranjo, según <i>Los Naranjos</i></span></p></div>
  <div class="presentacion">
    <h1>Árbol genealógico</h1>
    <p class="entradilla">Los Naranjo de Telde, una familia de Gran Canaria con antepasados conocidos desde finales del siglo XV. En el XIX varios hermanos Naranjo Cabrera cruzaron el Atlántico hacia Venezuela y Cuba, y una de sus ramas echó raíces en Pinar del Río.</p>
    <p class="instrucciones">Los Naranjo aparecen con toda su descendencia; las ramas de otros apellidos están plegadas: pulse «▾ ver hijos» para abrirlas. Pulse sobre cualquier persona para ponerla en el centro, con sus padres y abuelos encima; debajo del árbol verá su ficha, con enlaces a documentos y fotos.</p>
    <div class="leyenda"><span><i class="muestra naranjo"></i>Apellido Naranjo</span><span><i class="muestra"></i>Otros apellidos</span><span><i class="muestra borde-verde"></i>Rama que llegó a Pinar del Río (Cuba)</span></div>
  </div>
</section>
<div class="herramientas">
  <form class="buscador" role="search" autocomplete="off"><label for="buscar-persona">Buscar a una persona</label><input id="buscar-persona" type="search" list="lista-personas" placeholder="Escriba un nombre: Natalio, Patricio, Tascón…"><datalist id="lista-personas"></datalist><button type="submit">Ir</button></form>
  <nav class="atajos" aria-label="Ir a una rama de la familia">{botones}</nav>
</div>
<div id="arbol" class="arbol-din" data-inicio="salvador-gonzalez-naranjo" aria-live="polite"><noscript><p class="nota-arbol">El árbol interactivo necesita JavaScript. Puede consultar las <a href="personas.html">fichas de cada persona</a>.</p></noscript></div>
<section id="ficha-breve" class="ficha-breve" aria-live="polite"></section>
<script src="{ver('arbol-datos.js')}"></script>
<script src="{ver('arbol.js')}"></script>
<p class="nota-arbol">{len([x for x in personas.values() if not x.get("priv")])} personas. Las generaciones antiguas y las ramas de Telde y Las Palmas proceden del árbol de Cristo Santana Naranjo en Geneanet, basado en el libro <i>Historia de los Naranjo en Canarias</i> de Miguel Rodríguez Díaz de Quintana. La rama de Pinar del Río, la de Venezuela y los padres de Quirina son de nuestra investigación. Solo se publican datos de personas fallecidas.</p>

<h2>Las rutas de la familia</h2>
{MAPA}
<p class="nota-arbol">El árbol sigue abierto: ver <a href="fuentes.html">pendientes</a> y <a href="viajes.html">viajes</a>.</p>
"""
    pagina("index.html", "Los Naranjo de Telde · Árbol genealógico", "Árbol genealógico de los Naranjo de Telde (Gran Canaria), con sus ramas en Venezuela y Cuba.", contenido, actual="index.html", clase="inicio")

# ----------------------------------------------------------------------------------
# FICHAS
# ----------------------------------------------------------------------------------
def ficha(slug):
    p = P[slug]; base = "../"
    datos = "".join(f"<tr><th>{e}</th><td>{v}</td></tr>" for e, v in p["datos"])
    vida = "".join(f'<tr><td class="fecha">{f}</td><td>{h}</td></tr>' for f, h in p["vida"])
    docs = "".join(bloque_doc(d, base) for d in p["docs"])
    enlaces = "".join(f"<li>{e}</li>" for e in p["enlaces"])
    pend = "".join(f"<li>{x}</li>" for x in p["pendiente"])
    fam = "".join(f'<li><a href="{s}.html">{P[s]["nombre"]}</a> <span class="fechas">· {P[s]["fechas"]}</span></li>' for s in p["familia"] if s in P)
    aviso = '<p class="aviso">Ficha provisional: el parentesco con la familia está <b>sin confirmar</b>.</p>' if p.get("dudosa") else ""
    pie = f'<span class="pie-retrato">{p["pie_foto"]}</span>' if p.get("pie_foto") else ""
    retrato = f'<div><a class="retrato" href="{base}{p["foto"]}" target="_blank" title="Ver la foto completa"><img src="{base}{p["foto"]}" alt="Retrato de {html.escape(p["nombre"])}"></a>{pie}</div>' if p.get("foto") else ""
    partes = [f"""<p class="migas"><a href="../index.html">Árbol</a> › <a href="../personas.html">Personas</a> › {p["nombre"]} · <a href="../index.html#{slug}">ver en el árbol</a></p>
<div class="encabezado-ficha{" con-retrato" if retrato else ""}">
{retrato}
<div>
<h1>{p["nombre"]}</h1>
<p class="entradilla">{p["fechas"]}</p>
{aviso}
<p class="resumen">{p["resumen"]}</p>
</div>
</div>
<div class="ficha">
<div class="col">
<h2>Datos</h2>
<div class="tabla"><table class="datos">{datos}</table></div>"""]
    if vida:
        partes.append(f'<h2>Su vida en fechas</h2><div class="tabla"><table>{vida}</table></div>')
    partes.append("</div><aside class=\"col lateral\">")
    if fam:
        partes.append(f'<h3>Familia</h3><ul class="lista">{fam}</ul>')
    if enlaces:
        partes.append(f'<h3>En internet</h3><ul class="lista">{enlaces}</ul>')
    if pend:
        partes.append(f'<h3>Pendiente</h3><ul class="lista pendiente">{pend}</ul>')
    partes.append("</aside></div>")
    if docs:
        partes.append(f'<h2>Documentos y hallazgos</h2><p class="instrucciones">Pulse en una imagen para verla a tamaño completo.</p>{docs}')
    pagina(f"personas/{slug}.html", f'{p["nombre"]} · Los Naranjo de Telde', p["resumen"], "\n".join(partes), base=base, actual="personas.html")

def indice_personas():
    filas = "".join(f'<a class="tarjeta enlace{" clave" if P[s].get("clave") else ""}" href="personas/{s}.html"><h3>{P[s]["nombre"]}</h3><p class="fechas">{P[s]["fechas"]}</p><p>{P[s]["resumen"]}</p><p class="cuenta">{len(P[s]["docs"])} documento(s) con imagen</p></a>' for s in ORDEN_PERSONAS)
    pagina("personas.html", "Personas · Los Naranjo de Telde", "Fichas de cada miembro de la familia Naranjo de Telde.", f'<h1>Personas</h1><p class="entradilla">Una ficha por persona, con sus datos, su vida en fechas y los documentos encontrados.</p><div class="tarjetas">{filas}</div>', actual="personas.html")

# ----------------------------------------------------------------------------------
# PÁGINAS GENERALES
# ----------------------------------------------------------------------------------
def viajes():
    c = f"""<h1>Viajes y emigración</h1>
<p class="entradilla">Como tantas familias canarias del siglo XIX, los Naranjo de Telde buscaron fortuna al otro lado del Atlántico: primero en Venezuela, después en Cuba, y algunos volvieron a Canarias.</p>
{MAPA}
<h2>Venezuela: los Naranjo Cabrera en Aragua</h2>
<p>Hacia 1837 <a href="personas/salvador-naranjo-cabrera.html">Salvador</a>, con 18 años, llegó a Venezuela, llamado por su tío Fernando Cabrera. Le siguieron sus hermanos <a href="personas/francisco-javier-naranjo-cabrera.html">Francisco Javier</a> y <a href="personas/manuel-naranjo-cabrera.html">Manuel</a>. Se asentaron en La Victoria y San Sebastián, en los valles de Aragua, donde ya vivían parientes Cabrera y Zumbado. En 1875, cuando nació su primer hijo, Félix también figuraba como vecino de La Victoria, aunque en los libros de esa parroquia no aparece ni una vez entre 1864 y 1890.</p>
<h2>Cuba: el viaje del <i>Trinidad</i> (1878)</h2>
<p>A comienzos de noviembre de 1878 salió de Las Palmas el bergantín-barca <i>Trinidad</i>, del capitán Domingo Marrero, con 298 pasajeros. Entre ellos iban <a href="personas/felix-naranjo-cabrera.html">Félix</a> y su hermano <a href="personas/juan-naranjo-cabrera.html">Juan</a>. Tras 47 días y una escala en Gibara, llegó a La Habana el día de Navidad. Tres días después los pasajeros escribieron una carta pública de agradecimiento en la que elogiaban a «D. Félix Naranjo». En Telde quedaban Rosalía y sus hijos: Natalio había nacido el 1 de diciembre, con su padre ya en el mar.</p>
{bloque_doc("trinidad1878", "")}
{bloque_doc("carta1879", "")}
<h2>Rosalía y los hijos en Pinar del Río</h2>
<p>Según las memorias de Inocencia «Nina», antes de 1900 se fueron a Cuba unas dieciséis personas de la familia: Rosalía, sus hijos y sus hermanos Lucas y Juan. Se establecieron en la provincia de Pinar del Río, la tierra natal de Rosalía. No se ha encontrado todavía la lista de su barco: en los buques de emigrantes, la prensa habanera solo publicaba el número de pasajeros.</p>
<h2>Vuelta a Canarias</h2>
<p>En 1924, Félix, nacido en Cuba e hijo de Natalio, cruzó el Atlántico en sentido contrario para curarse en Canarias y ya no regresó. Un <a href="personas/felix-naranjo-fernandez.html">Félix Naranjo Fernández</a> vivía en Santa Cruz de Tenerife en los años treinta.</p>"""
    pagina("viajes.html", "Viajes y emigración · Los Naranjo de Telde", "Las rutas de la familia Naranjo: Telde, Venezuela y Cuba.", c, actual="viajes.html")

def cronologia():
    filas = [
        ("1668", "Nace Gregorio Suárez Navarro Naranjo, el antepasado más antiguo conocido de la familia (Geneanet).", "adrian-naranjo-cubas"),
        ("1773", "Nace Ana Rosalía de Cubas Ortega y Medina, madre de Adrián Naranjo y Cubas.", "adrian-naranjo-cubas"),
        ("1799", "Nace Adrián Naranjo y Cubas, hijo de Salvador González Naranjo y Ana Rosalía de Cubas.", "adrian-naranjo-cubas"),
        ("27 sep 1818", "Adrián se casa en Telde con Antonia Cabrera y Padrón.", "adrian-naranjo-cubas"),
        ("23 nov 1819", "Nace Salvador, el hermano mayor de Félix.", "salvador-naranjo-cabrera"),
        ("h. 1837", "Salvador llega a Venezuela con 18 años.", "salvador-naranjo-cabrera"),
        ("20 oct 1843", "Nace Félix Naranjo Cabrera en Telde.", "felix-naranjo-cabrera"),
        ("1857", "Francisco Javier se casa en Aragua con María de Jesús Zumbado.", "francisco-javier-naranjo-cabrera"),
        ("25 jul 1859", "Adrián Naranjo y Cubas renuncia como perito agrónomo de Canarias.", "adrian-naranjo-cubas"),
        ("28 jun 1862", "Salvador se casa en La Victoria con Josefa Cabrera.", "salvador-naranjo-cabrera"),
        ("21 oct 1866", "Muere Francisco Javier en San Sebastián (Aragua).", "francisco-javier-naranjo-cabrera"),
        ("16 jun 1870", "Félix Naranjo Cabrera se casa en Telde con Rosalía Rodríguez Valdés, natural de Cuba.", "felix-naranjo-cabrera"),
        ("3 abr 1875", "Nace Agustín Benito. Félix figura como vecino de La Victoria (Venezuela).", "agustin-naranjo-rodriguez"),
        ("2 may 1877", "Nace Adrián Salvador.", "adrian-naranjo-rodriguez"),
        ("h. 8 nov 1878", "Los hermanos Félix y Juan Naranjo Cabrera salen de Las Palmas hacia Cuba en el <i>Trinidad</i>.", "juan-naranjo-cabrera"),
        ("1 dic 1878", "Nace Natalio, con su padre en alta mar.", "natalio-naranjo-rodriguez"),
        ("25 dic 1878", "El <i>Trinidad</i> llega a La Habana.", "felix-naranjo-cabrera"),
        ("antes de 1900", "Rosalía y los hijos emigran a Cuba (tradición familiar).", "rosalia-rodriguez-valdes"),
        ("5 abr 1900", "Adrián se inscribe como español en Pinar del Río (tradición familiar).", "adrian-naranjo-rodriguez"),
        ("24 jun 1908", "Nace Juana, hija de Agustín y Quirina.", "juana-naranjo-fernandez"),
        ("26 abr 1914", "Nace José, hijo de Agustín y Quirina.", "jose-naranjo-fernandez"),
        ("20 jun 1915", "Nace Inocencia «Nina», hija de Agustín y Quirina, en Pinar del Río.", "inocencia-naranjo-fernandez"),
        ("1924", "Félix Naranjo Fernández, hijo de Natalio y nacido en Cuba, viaja a Canarias (tradición familiar).", "felix-naranjo-fernandez"),
        ("4 oct 1927", "<b>Agustín inscribe a su hija Inocencia en Pinar del Río</b>: «natural de Canarias», hijo de Félix y Rosalía.", "agustin-naranjo-rodriguez"),
        ("21 feb 1933", "Félix Naranjo Fernández, en Santa Cruz de Tenerife.", "felix-naranjo-fernandez"),
        ("14 mar 1936", "«Félix Naranjo, de 31 años», en la Casa de Socorro de Santa Cruz.", "felix-naranjo-fernandez"),
        ("h. 1950-1955", "Muere Agustín en la carretera de La Coloma, Pinar del Río (tradición familiar).", "agustin-naranjo-rodriguez"),
        ("2 ago 1989", "Muere José Naranjo Fernández.", "jose-naranjo-fernandez"),
        ("2010", "Muere Inocencia «Nina» en La Habana.", "inocencia-naranjo-fernandez"),
        ("12 oct 2012", "Muere Juana Naranjo Fernández en Lisboa.", "juana-naranjo-fernandez"),
    ]
    t = "".join(f'<tr><td class="fecha">{f}</td><td>{h}</td><td><a href="personas/{s}.html">{P[s]["nombre"]}</a></td></tr>' for f, h, s in filas)
    pagina("cronologia.html", "Cronología · Los Naranjo de Telde", "Fechas de la familia Naranjo de Telde, de 1668 a 2012.", f'<h1>Cronología</h1><p class="entradilla">Las fechas marcadas como «tradición familiar» vienen de las memorias y aún no tienen documento.</p><div class="tabla"><table><thead><tr><th>Fecha</th><th>Hecho</th><th>Ficha</th></tr></thead><tbody>{t}</tbody></table></div>', actual="cronologia.html")

def fuentes():
    c = """<h1>Fuentes y pendientes</h1>
<p class="entradilla">Dónde se ha buscado, qué se ha encontrado y qué queda por pedir.</p>
<h2>Fuentes consultadas</h2>
<div class="tabla"><table><thead><tr><th>Fuente</th><th>Qué se buscó</th><th>Resultado</th></tr></thead><tbody>
<tr><td>Parroquia de San Juan Bautista de Telde</td><td>Matrimonio de 1870 y bautismos de 1875-1878</td><td>Certificaciones (no se publican; datos en las fichas)</td></tr>
<tr><td>Registro Civil de Telde</td><td>Nacimiento de Agustín (1875)</td><td>Acta completa</td></tr>
<tr><td>Registro del Estado Civil de Pinar del Río</td><td>Nacimiento de Inocencia (1915)</td><td>Certificación: abuelos paternos Félix y Rosalía</td></tr>
<tr><td>FamilySearch: registros de Venezuela</td><td>La Victoria y San Sebastián (Aragua), Caracas</td><td>Muchos documentos de Salvador, Francisco Javier y Manuel; nada de Félix (1864-1890)</td></tr>
<tr><td>Jable, prensa canaria (ULPGC)</td><td>Naranjo, Félix Naranjo, Rodríguez Valdés, pasajeros…</td><td>Carta del <i>Trinidad</i> (1879); Félix Naranjo en Tenerife (1933, 1936)</td></tr>
<tr><td><i>Diario de la Marina</i> (UF Digital Collections)</td><td>Llegadas a La Habana, 1878</td><td>Llegada del <i>Trinidad</i>, 25 dic 1878</td></tr>
<tr><td>Protocolos de los consulados de España en Cuba (AHPM)</td><td>Pinar del Río 1900-1901; La Habana 1902-1908</td><td>Ningún Naranjo de la familia</td></tr>
<tr><td>Hemeroteca Digital BNE</td><td>Félix Naranjo Cabrera, Natalio Naranjo, Rosalía Rodríguez Valdés</td><td>Solo homónimos (una rama Naranjo Cabrera de San Lorenzo, Las Palmas)</td></tr>
<tr><td>Find a Grave, Geneanet, PARES</td><td>Naranjo en Cuba y Canarias</td><td>Nada de la familia</td></tr>
</tbody></table></div>
<h2>Pendiente</h2>
<ul class="lista pendiente">
<li><b>Telde:</b> defunción de Félix (Registro Civil y parroquia) y matrículas parroquiales de 1886-1907, que dirían cuándo se fue Rosalía a Cuba.</li>
<li><b>Pinar del Río:</b> defunción de Agustín (h. 1950-1955) y nacimientos de Juana, José, Felicita y Félix en el Registro Civil.</li>
<li><b>Archivo Nacional de Cuba:</b> Registro General de Españoles de 1899-1900 (inscripción de Adrián).</li>
<li><b>Santa Cruz de Tenerife:</b> padrón municipal de 1930-1945 y cementerios, para identificar a Félix Naranjo Fernández.</li>
<li><b>Archivo Histórico Provincial de Las Palmas:</b> pasaportes y licencias de embarque.</li>
</ul>
<h2>Sobre las imágenes</h2>
<p>Los recortes de prensa proceden de Jable (Universidad de Las Palmas de Gran Canaria) y de UF Digital Collections (Universidad de Florida). Las partidas de nacimiento, bautismo y matrimonio no se publican; sus datos figuran en las fichas. Los documentos de Venezuela se enlazan a FamilySearch, donde pueden verse gratuitamente con una cuenta.</p>"""
    pagina("fuentes.html", "Fuentes y pendientes · Los Naranjo de Telde", "Fuentes consultadas y búsquedas pendientes.", c, actual="fuentes.html")

if __name__ == "__main__":
    portada(); indice_personas(); viajes(); cronologia(); fuentes()
    for s in P: ficha(s)
    # limpiar páginas antiguas
    for viejo in ["historia.html", "cuba.html", "venezuela.html", "tenerife.html"]:
        f = RAIZ / viejo
        if f.exists(): f.unlink()
