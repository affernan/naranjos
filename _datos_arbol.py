"""Construye arbol-datos.js: el grafo familiar del árbol dinámico de la portada.

Une dos fuentes:
  1. La exportación del árbol de Cristo Santana Naranjo en Geneanet
     (../05_Geneanet/exportacion_2026-11/p0..p3.txt), con duplicados fusionados.
  2. Nuestra investigación (rama de Pinar del Río, Venezuela, padres de Quirina…).
Solo personas fallecidas: Geneanet ya oculta a los vivos («Persona privada») y además
se descarta a quien haya nacido en 1925 o después sin fecha de defunción.
"""
import json, pathlib, re, unicodedata

RAIZ = pathlib.Path(__file__).parent
ORIGEN = RAIZ.parent / "05_Geneanet" / "exportacion_2026-11"
GENEANET = "https://gw.geneanet.org/csantananaranjo?lang=es&"

# ------------------------------------------------------------------ duplicados de Geneanet
# Geneanet tiene dos listas de los hijos de Adrián Naranjo y Cubas: una resumida (solo el año,
# sacada del libro) y otra detallada. Se fusionan en la detallada.
ALIAS = {
    "antonio|naranjo cabrera|0": "antonio|naranjo cabrera|2",
    "patricio|naranjo cabrera|0": "patricio|naranjo cabrera|2",
    "hilario|naranjo cabrera|0": "maria hilaria|naranjo cabrera|0",
    "leandra|naranjo cabrera|0": "leandra|naranjo cabrera|2",
    "felipe|naranjo cabrera|0": "felipe|naranjo cabrera|2",
    "adrian|naranjo cabrera|0": "adrian jose nicolas|naranjo cabrera|0",
    "rosario|naranjo cabrera|0": "maria del rosario|naranjo cabrera|0",
    "pedro|naranjo cabrera|0": "pedro|naranjo cabrera|2",
    "pino|naranjo cabrera|0": "maria del pino|naranjo cabrera|0",
    "jesus|naranjo cabrera|0": "maria del jesus|naranjo cabrera|0",
    "jose|naranjo cabrera|0": "jose|naranjo cabrera|2",
    "manuel|naranjo cabrera|0": "manuel|naranjo cabrera|2",
    "juan|naranjo cabrera|0": "juan|naranjo cabrera|3",
    "natalia|naranjo cabrera|0": "natalia|naranjo cabrera|2",
    # cónyuges de la lista resumida
    "ana|munoz|0": "ana ventura|munoz de penaranda|0",
    "carmen|rodriguez|0": "maria del carmen|rodriguez de vega y bravo de laguna|0",
    "romualdo|naranjo navarro|0": "romualdo|navarro rodriguez|0",
    "luis|bravo zais|0": "luis de los santos|bravo de laguna y saz|0",
    "manuela|tascon del rio|0": "manuel antonio|tascon del rio|0",
    "adela|naranjo martin|0": "adela|martinez de escobar y lujan|0",
    "concepcion|cabrera|0": "maria de la concepcion|cabrera sanchez|0",
    # nietos de la lista resumida
    "luis|bravo naranjo|0": "luis|bravo de laguna y naranjo|0",
    "maria del carmen|laine febles|0": "maria de la candelaria|laine febles|0",
    "antonia|naranjo martin|0": "antonia|naranjo martinez de escobar|0",
    "amaranto|naranjo martin|0": "amaranto|naranjo martinez de escobar|0",
    "adrian|naranjo martin|0": "adrian|naranjo martinez de escobar|0",
    "bartolome|naranjo martin|0": "bartolome|naranjo martinez de escobar|0",
    "emiliana|naranjo martin|0": "emiliana|naranjo martinez de escobar|0",
    "jacinto|naranjo martin|0": "jacinto amaranto maria de los dolores|naranjo martinez de escobar|0",
    "eugenia|morello|0": "eugenia|morello colonna|0",
    "aurora|aguero|0": "aurora|ajeno|0",
    "angela|hernandez|0": "angela|hernandez|2",
    "agustin|perez medina|0": "agustin|perez medina|2",
    "maria del pino|sall bravo de laguna|2": "maria del pino|sall bravo de laguna|0",
    "eduardo|sall bravo de laguna|2": "eduardo|sall bravo de laguna|0",
}

# claves de Geneanet que ya tienen ficha propia en la web (id = slug de la ficha)
FICHAS = {
    "adrian jose nicolas|naranjo de cubas|0": "adrian-naranjo-cubas",
    "josefa antonia|cabrera de quintana y padon|0": "antonia-cabrera-padron",
    "felix|naranjo cabrera|0": "felix-naranjo-cabrera",
    "rosalia|rodriguez valdes|0": "rosalia-rodriguez-valdes",
    "salvador|naranjo cabrera|1": "salvador-naranjo-cabrera",
    "francisco javier|naranjo cabrera|0": "francisco-javier-naranjo-cabrera",
    "jose|naranjo cabrera|2": "jose-naranjo-cabrera",
    "manuel|naranjo cabrera|2": "manuel-naranjo-cabrera",
    "juan|naranjo cabrera|3": "juan-naranjo-cabrera",
}

NOMBRES_F = set("""maria ana josefa antonia rosalia leandra natalia juana isabel elvira constanza leonor
hipolita francisca margarita encarnacion adela emiliana serafina adorcinda agustina elena obdulia justa felisa
amelia rita esperanza genara aurora angela eugenia carmen pilar candelaria concepcion asuncion aurelia rosa luisa
matilde paula catalina clotilde gloria josefina felicidad celina alejandra rosenda marie manuela regina carolina
quirina inocencia felicita inelda""".split())

def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def a_slug(s):
    s = sin_tildes(s).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ------------------------------------------------------------------ lectura
def leer():
    lineas = []
    for i in range(4):
        lineas += (ORIGEN / f"p{i}.txt").read_text(encoding="utf-8").splitlines()
    return lineas

class Persona(dict):
    pass

G = {}            # clave canónica -> datos
ORDEN = []

def canon(k):
    k = k.strip()
    return ALIAS.get(k, k)

def alta(k, nombre=None, texto=None):
    crudo = k.strip()
    k = canon(crudo)
    if k not in G:
        G[k] = dict(k=k, n="", t="", conyuges=[], padres=[], hijos=[])
        ORDEN.append(k)
    p = G[k]
    propio = crudo == k          # la línea es de la clave canónica, no de un duplicado
    if nombre and (not p["n"] or (propio and (not p.get("n_ok") or len(nombre) > len(p["n"])))):
        p["n"] = nombre
        if propio: p["n_ok"] = True
    if texto and (not p["t"] or (propio and (not p.get("t_ok") or len(texto) > len(p["t"])))):
        p["t"] = texto
        if propio: p["t_ok"] = True
    return p

def anadir(lista, x):
    if x and x not in lista:
        lista.append(x)

def procesar():
    raiz = None
    pila = {}
    modo = "D"
    for ln in leer():
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith("#"):
            if ln.startswith("#p "):
                m = re.match(r"#p (.+?) n (.+?) oc (\d+)", ln)
                raiz = canon(f"{m[1].replace('+', ' ')}|{m[2].replace('+', ' ')}|{m[3]}")
                modo = "D"
            elif ln.startswith("#desc "):
                raiz = canon(ln[6:]); modo = "D"
            elif ln.startswith("#ascendientes"):
                raiz = canon("felix|naranjo cabrera|0"); modo = "A"
            alta(raiz)
            pila = {0: raiz}
            continue
        campos = [c.strip() for c in ln.split("¦")]
        while len(campos) < 5:
            campos.append("")
        tipo, clave, nombre, texto, extra = campos[:5]
        prof = int(tipo[1:])
        if texto.startswith("Persona privada") or nombre.startswith("Persona privada"):
            pila[prof] = None
            continue
        p = alta(clave, nombre, texto if modo == "D" else None)
        k = p["k"]
        pila[prof] = k
        if modo == "D":
            padre = pila.get(prof - 1)
            if padre:
                anadir(G[padre]["hijos"], k)
                anadir(p["padres"], padre)
            for par in filter(None, extra.split(";")):
                ck, _, cn = par.partition("=")
                if not ck or cn.startswith("Persona privada"):
                    continue
                c = alta(ck, cn)
                anadir(p["conyuges"], c["k"]); anadir(c["conyuges"], k)
        else:  # ascendientes: el 5.º campo trae «P=clave;P=clave» (padre; madre)
            hijo = pila.get(prof - 1)
            if hijo:
                anadir(G[hijo]["padres"], k); anadir(p["hijos"], hijo)
            padres = [x.partition("=")[2] for x in extra.split(";") if "=" in x]
            if len(padres) == 2:
                a, b = alta(padres[0]), alta(padres[1])
                anadir(a["conyuges"], b["k"]); anadir(b["conyuges"], a["k"])
            if texto and not p.get("tA"):
                p["tA"] = texto

# ------------------------------------------------------------------ fechas y sexo
def anio(patron, t):
    m = re.search(patron + r"[^.,;]*?(\d{4})", t)
    if not m:
        return ""
    trozo = m.group(0)
    return ("c. " if "alrededor" in trozo else "") + m.group(1)

def fechas_de(p):
    t = p["t"]
    n = anio(r"nacid[oa]", t)
    d = anio(r"fallecid[oa]", t)
    if not n and not d and p.get("tA"):
        a = p["tA"].replace("ca ", "c. ")
        return re.sub(r"(\d{4})-(\d{4})", r"\1 – \2", a.replace("†", "† "))
    if n and d:
        return f"{n} – {d}"
    if n:
        return n
    if d:
        return f"† {d}"
    return ""

def sexo_de(p):
    # el primer verbo del texto se refiere a la persona (los siguientes pueden ser del cónyuge)
    m = re.search(r"(nacid|fallecid|bautizad|Casad)([oa])", p["t"])
    if m:
        return "f" if m.group(2) == "a" else "m"
    primero = sin_tildes(p["k"].split("|")[0].split()[0]).lower()
    return "f" if primero in NOMBRES_F else "m"

def nombre_de(p):
    n = p["n"] or p["k"].split("|")[0].title()
    nombre_k, apellidos_k, _ = p["k"].split("|")
    # algunos hijos de Juan Naranjo Cabrera aparecen solo con el nombre de pila
    if apellidos_k and sin_tildes(apellidos_k.split()[0]).lower() not in sin_tildes(n).lower():
        n = f"{n} " + " ".join(w if w in ("de", "y", "la", "del", "los") else w.capitalize() for w in apellidos_k.split())
    return n

# ------------------------------------------------------------------ nuestra investigación
EXTRA = []   # (id, nombre, fechas, sexo, [padres], [cónyuges], texto)

def propia(id_, nombre, fechas="", sexo="", padres=(), conyuges=(), texto=""):
    EXTRA.append((id_, nombre, fechas, sexo, list(padres), list(conyuges), texto))

def nuestras_personas():
    F, R = "felix|naranjo cabrera|0", "rosalia|rodriguez valdes|0"
    propia("agustin-naranjo-rodriguez", "Agustín Benito Naranjo Rodríguez", "1875 – h. 1950-55", "m", [F, R], ["quirina-fernandez-fernandez"],
           "Nació en Telde el 3 de abril de 1875. Emigró a Cuba y formó su familia en Pinar del Río.")
    propia("adrian-naranjo-rodriguez", "Adrián Salvador Naranjo Rodríguez", "1877", "m", [F, R], [],
           "Nació en Telde el 2 de mayo de 1877; su padrino fue su tío Salvador. En 1900 estaba en Pinar del Río.")
    propia("natalio-naranjo-rodriguez", "Natalio Naranjo Rodríguez", "1878", "m", [F, R], [],
           "Nació en Telde el 1 de diciembre de 1878, con su padre ya camino de La Habana.")
    # hermanos de Rosalía (bautismos de Telde y memorias familiares)
    RP = ["agustin|rodriguez de sosa|0", "regina|valdes delgado|0"]
    propia("carolina-rodriguez-valdes", "Carolina Rodríguez Valdés", "", "f", RP, [], "Hermana de Rosalía; madrina de su sobrino Natalio en Telde (1878).")
    propia("lucas-rodriguez-valdes", "Lucas Rodríguez Valdés", "", "m", RP, [], "Hermano de Rosalía. Volvió a Cuba con ella antes de 1900 (memorias familiares).")
    propia("juan-rodriguez-valdes", "Juan Rodríguez Valdés", "", "m", RP, [], "Hermano de Rosalía. Volvió a Cuba con ella antes de 1900 (memorias familiares).")
    # Pinar del Río
    propia("antonio-fernandez", "Antonio Fernández", "", "m", [], ["inocencia-fernandez"], "Canario, padre de Quirina (certificado de nacimiento de su nieta Inocencia).")
    propia("inocencia-fernandez", "Inocencia Fernández", "", "f", [], ["antonio-fernandez"], "Madre de Quirina.")
    propia("quirina-fernandez-fernandez", "Quirina Úrsula Fernández Fernández", "", "f", ["antonio-fernandez", "inocencia-fernandez"], ["agustin-naranjo-rodriguez"],
           "Natural de San Luis, en la provincia de Pinar del Río.")
    AQ = ["agustin-naranjo-rodriguez", "quirina-fernandez-fernandez"]
    propia("felix-naranjo-fernandez", "Félix Naranjo Fernández", "h. 1904-1905", "m", ["natalio-naranjo-rodriguez"], [], "Hijo de Natalio. Nacido en Cuba; en 1924 se fue a Canarias. Vivía en Santa Cruz de Tenerife en los años treinta.")
    propia("juana-naranjo-fernandez", "Juana Naranjo Fernández", "1908 – 2012", "f", AQ, [], "Nació el 24 de junio de 1908 y murió en Lisboa el 12 de octubre de 2012.")
    propia("jose-naranjo-fernandez", "José Naranjo Fernández", "1914 – 1989", "m", AQ, [], "Nació el 26 de abril de 1914; murió el 2 de agosto de 1989.")
    propia("inocencia-naranjo-fernandez", "Inocencia «Nina» Naranjo Fernández", "1915 – 2010", "f", AQ, ["hugo-fernandez-arada"],
           "Nació el 20 de junio de 1915 en el Barrio Primero de Ovas (Pinar del Río); murió en La Habana en 2010.")
    propia("felicita-naranjo-fernandez", "Felicita Naranjo Fernández", "", "f", AQ, [], "Hija de Agustín y Quirina según el árbol familiar.")
    propia("hugo-fernandez-arada", "Hugo Ángel Fernández Arada", "1913 – h. 1984-89", "m", [], ["inocencia-naranjo-fernandez"], "Nació en Pinar del Río el 2 de octubre de 1913.")
    propia("hijos-de-nina", "Cinco hijos (personas vivas)", "", "", ["inocencia-naranjo-fernandez", "hugo-fernandez-arada"], [],
           "Los cinco hijos de Inocencia y Hugo viven; no se publican sus datos.")
    # Venezuela (FamilySearch)
    S = "salvador|naranjo cabrera|1"
    propia("apolinario-cabrera", "Apolinario Cabrera", "", "m", [], ["ana-padron"], "Padre de Josefa Cabrera Padrón.")
    propia("ana-padron", "Ana Padrón", "", "f", [], ["apolinario-cabrera"], "Madre de Josefa Cabrera Padrón.")
    propia("josefa-cabrera-padron", "Josefa Cabrera Padrón", "", "f", ["apolinario-cabrera", "ana-padron"], [S], "Casada con Salvador Naranjo Cabrera en La Victoria (Aragua, Venezuela) el 28 de junio de 1862.")
    SJ = [S, "josefa-cabrera-padron"]
    propia("antonia-evarista-naranjo-cabrera", "Antonia Evarista Naranjo Cabrera", "1862", "f", SJ, [], "Nacida en La Victoria (Venezuela).")
    propia("adrian-eulogio-naranjo-cabrera", "Adrián Eulogio del Carmen Naranjo Cabrera", "1866 – 1942", "m", SJ, [], "Nació en La Victoria el 10 de marzo de 1866 y murió en Caracas en 1942.")
    propia("narciso-naranjo-cabrera", "Narciso Naranjo Cabrera", "h. 1867 – 1900", "m", SJ, [], "Enterrado en La Victoria el 16 de junio de 1900, con 33 años.")
    propia("jose-naranjo-cabrera-1869", "José Naranjo Cabrera", "h. 1869 – 1881", "m", SJ, [], "Murió en La Victoria el 6 de octubre de 1881, con 12 años.")
    propia("rafael-de-jesus-naranjo-cabrera", "Rafael de Jesús Naranjo Cabrera", "1870", "m", SJ, [], "Nacido en La Victoria (Venezuela).")
    propia("rosa-naranjo-cabrera", "Rosa Naranjo Cabrera", "† 1900", "f", SJ, [], "Enterrada en La Victoria el 17 de marzo de 1900.")
    propia("aurelia-naranjo-cabrera", "Aurelia Naranjo Cabrera", "† 1900", "f", SJ, [], "Enterrada en La Victoria el 13 de septiembre de 1900.")
    FJ = "francisco javier|naranjo cabrera|0"
    propia("maria-de-jesus-zumbado", "María de Jesús Zumbado", "", "f", [], [FJ], "Casada con Francisco Javier Naranjo Cabrera en Aragua (Venezuela) en 1857, con dispensa de parentesco.")
    FZ = [FJ, "maria-de-jesus-zumbado"]
    propia("josefa-antonia-naranjo-zumbado", "Josefa Antonia Naranjo Zumbado", "", "f", FZ, ["rafael-ortega"], "Casada en San Sebastián (Aragua) el 30 de septiembre de 1878 con Rafael Ortega.")
    propia("rafael-ortega", "Rafael Ortega", "", "m", [], ["josefa-antonia-naranjo-zumbado"], "")
    propia("francisco-javier-naranjo-zumbado", "Francisco Javier Naranjo Zumbado", "1867", "m", FZ, [], "Hijo póstumo: bautizado en San Sebastián el 5 de agosto de 1867; su padrino fue su tío Salvador.")
    M = "manuel|naranjo cabrera|2"
    propia("inelda-del-nogal", "Inelda del Nogal Macías", "1855 – 1935", "f", [], [M], "Esposa de Manuel Naranjo Cabrera, con quien se casó en San Sebastián de los Reyes (Aragua) en 1872.")
    propia("leon-domingo-naranjo-del-nogal", "León Domingo Naranjo del Nogal", "1892 – 1953", "m", [M, "inelda-del-nogal"], [], "Hijo de Manuel Naranjo Cabrera e Inelda del Nogal (árbol de luisitahg en Geneanet).")
    # Ana Antonia y los Falcón Naranjo (árbol de luisitahg en Geneanet)
    A = "ana|naranjo cabrera|0"
    propia("juan-falcon-de-llarena", "Juan Falcón de Llarena", "", "m", [], [A], "Esposo de Ana Antonia Naranjo Cabrera.")
    AF = [A, "juan-falcon-de-llarena"]
    for slug, nombre, fechas, sexo in [("pilar-falcon-naranjo", "Pilar Falcón Naranjo", "1881 – 1912", "f"), ("ana-falcon-naranjo", "Ana Falcón Naranjo", "1884 – 1940", "f"),
                                       ("josefa-cristina-falcon-naranjo", "Josefa Cristina Falcón Naranjo", "1885 – 1912", "f"), ("maria-del-pino-falcon-naranjo", "María del Pino Falcón Naranjo", "1888", "f"),
                                       ("salvador-falcon-naranjo", "Salvador Falcón Naranjo", "1890 – 1927", "m"), ("carmelo-falcon-naranjo", "Carmelo Falcón Naranjo", "1891 – 1958", "m"),
                                       ("consuelo-falcon-naranjo", "Consuelo Falcón Naranjo", "1892", "f"), ("adan-falcon-naranjo", "Adán Falcón Naranjo", "", "m"),
                                       ("eva-falcon-naranjo", "Eva Falcón Naranjo", "", "f"), ("juan-falcon-naranjo", "Juan Falcón Naranjo", "", "m")]:
        propia(slug, nombre, fechas, sexo, AF, [], "Hijo de Ana Antonia Naranjo Cabrera y Juan Falcón de Llarena (árbol de luisitahg en Geneanet)." if sexo == "m" else "Hija de Ana Antonia Naranjo Cabrera y Juan Falcón de Llarena (árbol de luisitahg en Geneanet).")
    propia("luisa-elena-naranjo-del-nogal", "Luisa Elena de Lourdes Naranjo del Nogal", "1895", "f", [M, "inelda-del-nogal"], [], "Bautizada en San Sebastián (Aragua) el 1 de noviembre de 1895.")
    propia("pedro-cabrera-padron", "Pedro Cabrera", "", "m", ["pedro|de alcantara cabrera de quintana|0", "maria isidro|de ortega padron y chil|0"], ["maria-del-carmen-zumbado"],
           "Hermano de Josefa Antonia Cabrera. Vivió en La Victoria (Venezuela), donde se casó el 16 de abril de 1860.")
    propia("maria-del-carmen-zumbado", "María del Carmen Zumbado", "", "f", [], ["pedro-cabrera-padron"], "")

# datos que corrigen o completan a Geneanet
CORRIGE = {
    "regina|valdes delgado|0": dict(n="Regina de los Ángeles Valdés Delgado", t="Madre de Rosalía y madrina de su nieto Agustín en Telde (1875). Geneanet escribe «Valdés Delgano»."),
    "agustin|rodriguez de sosa|0": dict(n="Agustín Rodríguez de Sosa", t="Padre de Rosalía Rodríguez Valdés."),
    "rosalia|rodriguez valdes|0": dict(f="", l="Nacida en Consolación del Sur, Pinar del Río (Cuba)"),
    "felix|naranjo cabrera|0": dict(f="1843"),
    "salvador|naranjo cabrera|1": dict(f="1819", l="Murió en Venezuela", n="Salvador José Naranjo Cabrera"),
    "francisco javier|naranjo cabrera|0": dict(f="1820 – 1866"),
    "manuel|naranjo cabrera|2": dict(f="1839 – 1913"),
    "ana|naranjo cabrera|0": dict(n="Ana Antonia Naranjo Cabrera"),
    "josefa antonia|cabrera de quintana y padon|0": dict(n="Josefa Antonia Cabrera de Quintana y Padrón", f="1800"),
    "adrian jose nicolas|naranjo de cubas|0": dict(n="Adrián Naranjo y Cubas"),
}


# ------------------------------------------------------------------ hechos de cada persona
MESES = dict(enero="ene", febrero="feb", marzo="mar", abril="abr", mayo="may", junio="jun", julio="jul", agosto="ago",
             septiembre="sep", setiembre="sep", octubre="oct", noviembre="nov", diciembre="dic")
OFICIO = re.compile(r"^(Agricultor|Comerciante|Capit|M[eé]dico|Organ|Teniente|Propietario|Abogado|Perito|Maestro|Escritor|Poet|Humorista|Universal|Fundador|Licenciad|Labrador)")

def fecha_de(s):
    """«el 20 de octubre de 1843» -> «20 oct 1843»; «alrededor de 1879» -> «h. 1879»."""
    s = s.strip()
    m = re.match(r"(?:el |en )?(alrededor de )?(?:(\d{1,2}) de )?(?:([a-záéíóú]+) (?:de )?)?(\d{4})$", s)
    if not m:
        return ""
    h, dia, mes, anio = m.groups()
    partes = [dia or "", MESES.get(mes or "", ""), anio]
    return ("h. " if h else "") + " ".join(x for x in partes if x)

def lugar_de(segs):
    l = ", ".join(x.strip(" .") for x in segs if x.strip(" ."))
    return l.replace("Baustina", "Bautista").replace("Baustita", "Bautista")

def hechos_de(t):
    """Separa el texto de Geneanet en nacimiento, bautismo, defunción, oficio y matrimonio."""
    e = {}
    if not t:
        return e
    t = t.strip()
    m = re.search(r"(?:^|\.\s*)(Casad[oa]\b|Con )", t)
    indiv, matr = (t[:m.start()], t[m.start():].lstrip(". ")) if m else (t, "")
    segs = [x.strip() for x in indiv.split(",")]
    segs = [x for x in segs if x and "…" not in x]
    actual, lugar, oficio = None, [], []
    for sg in segs:
        k = re.match(r"(nacid|bautizad|fallecid)[oa]\b(.*)$", sg)
        if k:
            if actual: e[actual[0]] = [actual[1], lugar_de(lugar)]
            lugar = []
            actual = ({"nacid": "n", "bautizad": "b", "fallecid": "d"}[k.group(1)], fecha_de(k.group(2)))
        elif oficio or OFICIO.match(sg):
            oficio.append(sg.strip(" ."))
        elif sg.startswith("Fallecid"):
            e["nota"] = sg.strip(" .")
        elif actual:
            lugar.append(sg)
    if actual: e[actual[0]] = [actual[1], lugar_de(lugar)]
    if oficio:
        e["o"] = ", ".join(oficio)
    if matr and "Persona privada" not in matr:
        cortado = "…" in matr
        matr = matr.split("…")[0]
        partes = re.split(r",?\s+con\s+|^Con\s+", matr, maxsplit=1)
        cab = partes[0]; con = partes[1] if len(partes) > 1 else ""
        hs = [x.strip() for x in cab.split(",") if x.strip()]
        if cortado and not con and len(hs) > 1:
            hs = hs[:-1]          # el último trozo quedó cortado en la exportación
        fecha = fecha_de(re.sub(r"^Casad[oa]\s*", "", hs[0])) if hs else ""
        lugar = lugar_de(hs[1:])
        nombre = re.split(r"[,.]", con)[0].strip()
        e["m0"] = [nombre, fecha, lugar]
    return e

# hechos de nuestra investigación (o que completan a Geneanet): n, b, d = [fecha, lugar]; m = [[cónyuge, fecha, lugar]]
HECHOS = {
    "felix-naranjo-cabrera": dict(o="Labrador"),
    "adrian-naranjo-cubas": dict(o="Agricultor; perito agrónomo de Canarias hasta 1859"),
    "rosalia-rodriguez-valdes": dict(n=["", "Consolación del Sur, Pinar del Río (Cuba)"]),
    "agustin-naranjo-rodriguez": dict(n=["3 abr 1875", "Telde, Gran Canaria"], b=["3 abr 1875", "Telde, Gran Canaria"], d=["h. 1950-1955", "Carretera de La Coloma, Pinar del Río (Cuba)"]),
    "adrian-naranjo-rodriguez": dict(n=["2 may 1877", "Telde, Gran Canaria"], b=["4 may 1877", "Telde, Gran Canaria"]),
    "natalio-naranjo-rodriguez": dict(n=["1 dic 1878", "Telde, Gran Canaria"], b=["9 dic 1878", "Telde, Gran Canaria"]),
    "quirina-fernandez-fernandez": dict(n=["", "San Luis, Pinar del Río (Cuba)"]),
    "felix-naranjo-fernandez": dict(n=["h. 1904-1905", "Cuba"]),
    "juana-naranjo-fernandez": dict(n=["24 jun 1908", "Cuba"], d=["12 oct 2012", "Lisboa (Portugal)"]),
    "jose-naranjo-fernandez": dict(n=["26 abr 1914", "Cuba"], d=["2 ago 1989", ""]),
    "inocencia-naranjo-fernandez": dict(n=["20 jun 1915", "Barrio Primero de Ovas, Pinar del Río (Cuba)"], d=["2010", "La Habana (Cuba)"]),
    "hugo-fernandez-arada": dict(n=["2 oct 1913", "Pinar del Río (Cuba)"], d=["entre 1984 y 1989", ""]),
    "salvador-naranjo-cabrera": dict(d=["", "Venezuela"], m=[["josefa-cabrera-padron", "28 jun 1862", "La Victoria, Aragua (Venezuela)"]]),
    "francisco-javier-naranjo-cabrera": dict(d=["21 oct 1866", "San Sebastián, Aragua (Venezuela)"], m=[["maria-de-jesus-zumbado", "1857", "Aragua (Venezuela)"]]),
    "manuel-naranjo-cabrera": dict(n=["27 ago 1839", "Telde, Gran Canaria"], d=["5 oct 1913", "San Sebastián de los Reyes, Aragua (Venezuela)"], m=[["inelda-del-nogal", "9 mar 1872", "San Sebastián de los Reyes, Aragua (Venezuela)"]]),
    "antonia-cabrera-padron": dict(n=["1800", "Telde, Gran Canaria"]),
    "ana-naranjo-cabrera": dict(m=[["juan-falcon-de-llarena", "", ""]]),
    "adrian-eulogio-naranjo-cabrera": dict(n=["10 mar 1866", "La Victoria, Aragua (Venezuela)"], d=["1942", "Caracas (Venezuela)"]),
    "narciso-naranjo-cabrera": dict(n=["h. 1867", ""], d=["16 jun 1900", "La Victoria, Aragua (Venezuela)"]),
    "jose-naranjo-cabrera-1869": dict(n=["h. 1869", ""], d=["6 oct 1881", "La Victoria, Aragua (Venezuela)"]),
    "antonia-evarista-naranjo-cabrera": dict(n=["1862", "La Victoria, Aragua (Venezuela)"]),
    "rafael-de-jesus-naranjo-cabrera": dict(n=["1870", "La Victoria, Aragua (Venezuela)"]),
    "rosa-naranjo-cabrera": dict(d=["17 mar 1900", "La Victoria, Aragua (Venezuela)"]),
    "aurelia-naranjo-cabrera": dict(d=["13 sep 1900", "La Victoria, Aragua (Venezuela)"]),
    "josefa-antonia-naranjo-zumbado": dict(m=[["rafael-ortega", "30 sep 1878", "San Sebastián, Aragua (Venezuela)"]]),
    "francisco-javier-naranjo-zumbado": dict(b=["5 ago 1867", "San Sebastián, Aragua (Venezuela)"]),
    "luisa-elena-naranjo-del-nogal": dict(b=["1 nov 1895", "San Sebastián, Aragua (Venezuela)"]),
    "pedro-cabrera-padron": dict(m=[["maria-del-carmen-zumbado", "16 abr 1860", "La Victoria, Aragua (Venezuela)"]]),
}

# ------------------------------------------------------------------ generación
def generar(P_fichas=None, destino=None, cuerpo_ficha=None):
    G.clear(); ORDEN.clear(); EXTRA.clear()
    procesar()
    # en las listas de descendientes solo consta un progenitor: el otro es su cónyuge, si tuvo uno solo
    for p in G.values():
        if len(p["padres"]) == 1:
            par = G[p["padres"][0]]
            if len(par["conyuges"]) == 1:
                anadir(p["padres"], par["conyuges"][0]); anadir(G[par["conyuges"][0]]["hijos"], p["k"])
    # padres de Rosalía (Geneanet: página de Rosalía)
    alta("agustin|rodriguez de sosa|0", "Agustín Rodríguez de Sosa")
    alta("regina|valdes delgado|0", "Regina Valdés Delgado")
    for k in ("agustin|rodriguez de sosa|0", "regina|valdes delgado|0"):
        anadir(G[k]["hijos"], "rosalia|rodriguez valdes|0"); anadir(G["rosalia|rodriguez valdes|0"]["padres"], k)
    anadir(G["agustin|rodriguez de sosa|0"]["conyuges"], "regina|valdes delgado|0")
    anadir(G["regina|valdes delgado|0"]["conyuges"], "agustin|rodriguez de sosa|0")

    # ids
    ids, usados = {}, set()
    for k in ORDEN:
        if k in FICHAS:
            i = FICHAS[k]
        else:
            nom, ap, oc = k.split("|")
            i = a_slug(f"{nom} {ap}")
            while i in usados:
                i += "-b"
        usados.add(i); ids[k] = i

    personas = {}
    for k in ORDEN:
        p = G[k]
        nom, ap, oc = k.split("|")
        d = dict(n=nombre_de(p), f=fechas_de(p), s=sexo_de(p), t=p["t"],
                 g=f"p={nom.replace(' ', '+')}&n={ap.replace(' ', '+')}&oc={oc}",
                 p=[ids[x] for x in p["padres"]], c=[ids[x] for x in p["conyuges"]], h=[ids[x] for x in p["hijos"]])
        if k in CORRIGE:
            c = CORRIGE[k]
            d["n"] = c.get("n", d["n"]); d["f"] = c.get("f", d["f"])
            if c.get("l"): d["l"] = c["l"]
            if c.get("t"): d["t"] = c["t"] + (" " + d["t"] if d["t"] and d["t"] != c["t"] else "")
        d["e"] = hechos_de(p["t"])
        personas[ids[k]] = d
    ids_k = dict(ids)

    nuestras_personas()
    def ref(x):
        return ids_k.get(canon(x), x)
    for id_, nombre, fechas, sexo, padres, conyuges, texto in EXTRA:
        personas[id_] = dict(n=nombre, f=fechas, s=sexo, t=texto, g="", p=[], c=[], h=[], e={}, propia=1)
    for id_, nombre, fechas, sexo, padres, conyuges, texto in EXTRA:
        d = personas[id_]
        for x in padres:
            x = ref(x); anadir(d["p"], x); anadir(personas[x]["h"], id_)
        for x in conyuges:
            x = ref(x); anadir(d["c"], x); anadir(personas[x]["c"], id_)

    for i, d in personas.items():
        e = d["e"]
        m0 = e.pop("m0", None)
        if m0:
            nombre, fecha, lugar = m0
            clave = sin_tildes(nombre).lower().split()[:1]
            con = [c for c in d["c"] if clave and sin_tildes(personas[c]["n"]).lower().startswith(clave[0])] or d["c"][:1]
            e["m"] = [[con[0] if con else "", fecha, lugar]]
        for campo, valor in HECHOS.get(i, {}).items():
            if campo in ("n", "b", "d") and campo in e:
                e[campo] = [valor[0] or e[campo][0], valor[1] or e[campo][1]]
            else:
                e[campo] = valor
        for campo in ("n", "b", "d"):
            if campo in e and not any(e[campo]): del e[campo]

    # orden de los padres (padre, madre) y de los hijos (por año)
    def anio_n(i):
        m = re.search(r"\d{4}", personas[i]["f"] or "")
        return int(m.group(0)) if m else 9999
    for i, d in personas.items():
        d["p"].sort(key=lambda x: 0 if personas[x]["s"] == "m" else 1)
        d["h"].sort(key=anio_n)

    # privacidad: nacidos en 1925 o después sin defunción
    fuera = [i for i, d in personas.items() if not d.get("propia") and re.match(r"(c\. )?(19[2-9][5-9]|19[3-9]\d|20\d\d)$", d["f"] or "")]
    for i in fuera:
        for d in personas.values():
            for campo in ("p", "c", "h"):
                if i in d[campo]: d[campo].remove(i)
        del personas[i]

    # generaciones, contadas desde el Naranjo más antiguo conocido (Diego Pérez Naranjo, h. 1470 = I):
    # hijos +1, padres -1, cónyuges la misma; la primera asignación es la que vale
    from collections import deque
    gen = {"diego-perez-naranjo": 1}
    cola = deque(["diego-perez-naranjo"])
    while cola:
        i = cola.popleft()
        for campo, salto in (("h", 1), ("p", -1), ("c", 0)):
            for x in personas[i][campo]:
                if x in personas and x not in gen:
                    gen[x] = gen[i] + salto
                    cola.append(x)
    for i, g in gen.items():
        personas[i]["gn"] = g

    # rama de Pinar del Río: antepasados y descendientes de Agustín (y sus parejas)
    verde = set()
    def subir(i):
        if i in verde: return
        verde.add(i)
        for x in personas[i]["p"]: subir(x)
    def bajar(i):
        verde.add(i)
        for x in personas[i]["c"]: verde.add(x)
        for x in personas[i]["h"]: bajar(x)
    subir("agustin-naranjo-rodriguez"); bajar("agustin-naranjo-rodriguez")

    for i, d in personas.items():
        if "naranjo" in sin_tildes(d["n"]).lower() or i == "hijos-de-nina": d["nj"] = 1
        if i in verde: d["v"] = 1
        if i == "hijos-de-nina": d["priv"] = 1
        if P_fichas and i in P_fichas:
            d["fi"] = i
            if P_fichas[i].get("foto"): d["fo"] = P_fichas[i]["foto"]
            d["r"] = P_fichas[i].get("resumen", "")
            d["nd"] = len(P_fichas[i].get("docs", []))
        if cuerpo_ficha and d.get("fi"):
            d["fh"] = cuerpo_ficha(i)
        if not d["e"]: del d["e"]
        d.pop("l", None)
        if not d["t"]: del d["t"]
        if not d["g"]: del d["g"]
        d.pop("propia", None)
        for campo in ("p", "c", "h"):
            if not d[campo]: del d[campo]

    js = "/* Generado por _datos_arbol.py — no editar a mano. */\nwindow.ARBOL = " + json.dumps(
        dict(geneanet=GENEANET, personas=personas), ensure_ascii=False, separators=(",", ":")) + ";\n"
    (destino or RAIZ / "arbol-datos.js").write_text(js, encoding="utf-8")
    print(f"arbol-datos.js: {len(personas)} personas ({len(fuera)} excluidas por posible privacidad)")
    return personas

if __name__ == "__main__":
    generar()
