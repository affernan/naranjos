"""Documentos de Venezuela (FamilySearch) para las fichas de los Naranjo Cabrera y los Cabrera.

Las imágenes originales están en ../04_Hallazgos_Venezuela/documentos/ y las copias reducidas
para la web en img/docs/venezuela/. `copiar_imagenes()` las regenera; `registrar(DOC, P)` añade
los documentos a las fichas. No se publican los bautismos en que la familia solo fue madrina o padrino.
"""
import pathlib

RAIZ = pathlib.Path(__file__).parent
ORIGEN = RAIZ.parent / "04_Hallazgos_Venezuela" / "documentos"
DESTINO = RAIZ / "img" / "docs" / "venezuela"
FS = "https://www.familysearch.org/ark:/61903/"

# (clave, ficha, título, [(archivo, ark de la imagen)], texto, ark del registro indexado)
GRUPOS = [
    # ---- Salvador
    ("ve_salvador_llegada", "salvador-naranjo-cabrera", "Salvador Naranjo, testigo en Caracas: llegó a La Guaira el 4 dic 1835 (expediente de 1837-1839)",
     [("1837-1839_Expediente_Salvador_Naranjo_llegada_a_LaGuaira_1835_a.jpg", "3:1:33SQ-GRTW-DRL"), ("1837-1839_Expediente_Salvador_Naranjo_llegada_a_LaGuaira_1835_b.jpg", "3:1:33S7-9RTW-DDD")],
     "En el expediente de soltería de Miguel Rodríguez, de Telde, declara como testigo «Salvador Naranjo, natural del lugar de Telde en la Isla de la Gran Canaria», de 21 años. Ambos se embarcaron en Canarias en 1835 y llegaron al puerto de La Guaira el 4 de diciembre de 1835.", ""),
    ("ve_salvador_solteria", "salvador-naranjo-cabrera", "Expediente de soltería de Salvador Naranjo (La Victoria y Caracas, 1862)",
     [("1862_Solteria_Salvador_Naranjo_01_portada.jpg", "3:1:33S7-9RR1-9K5X"), ("1862_Solteria_Salvador_Naranjo_02_hijo_de_Adrian_y_Antonia_Cabrera.jpg", "3:1:33SQ-GRR1-9LQB"),
      ("1862_Solteria_Salvador_Naranjo_03_testigos_Fernando_y_Pedro_Cabrera.jpg", "3:1:33SQ-GRR1-9L31"), ("1862_Solteria_Salvador_Naranjo_04_fiscal.jpg", "3:1:33SQ-GRR1-9L35"),
      ("1862_Solteria_Salvador_Naranjo_05_auto_provisor.jpg", "3:1:33SQ-GRR1-9L3B")],
     "«Año de 1862. Soltería de Salvador Naranjo, natural de la Gran Canaria y vecino de la Victoria para contraer matrimonio con Josefa Cabrera.» Salvador, mayor de 42 años, llegó a Venezuela con 18 desde Canarias y es hijo legítimo de «Alvian» [Adrián] Naranjo y Antonia Cabrera. Declaran sus tíos Fernando y Pedro Cabrera (La Victoria, 15 mar 1862). Aprobado en Caracas el 8 abr y el 19 may 1862.", ""),
    ("ve_salvador_matrimonio", "salvador-naranjo-cabrera", "Matrimonio de Salvador Naranjo y Josefa Cabrera (La Victoria, 28 jun 1862)",
     [("1862-06-28_Matrimonio_Salvador_Naranjo_y_Josefa_Cabrera_LaVictoria.jpg", "3:1:33SQ-GRRF-999K")],
     "«…contrajeron Salvador Naranjo, hijo legítimo de Adrián Naranjo y Antonia Cabrera, y Josefa Cabrera, hija legítima de Apolinario Cabrera y Ana Padrón, vecinos de esta parroquia. Fueron testigos Manuel Naranjo y Ana Padrón…» — Primera partida de la página derecha; eran primos y necesitaron dispensa.", "1:1:X9LX-X2RV"),
    ("ve_salvador_adrian_eulogio", "salvador-naranjo-cabrera", "Bautismo de su hijo Adrián Eulogio del Carmen (San Sebastián, 25 dic 1866)",
     [("1866-12-25_Bautismo_Adrian_Eulogio_del_Carmen_hijo_de_Salvador_Naranjo_SanSebastian.jpg", "3:1:33S7-9RRX-S17")],
     "Adrián Eulogio del Carmen, nacido el 10 mar 1866, hijo de Salvador Naranjo y Josefa Cabrera. Murió en Caracas en 1942.", "1:1:6DRG-YSCL"),
    ("ve_salvador_antonio", "salvador-naranjo-cabrera", "Bautismo de su hijo Antonio (1868)",
     [("1868_Bautismo_Antonio_hijo_de_Salvador_Naranjo_Camatagua.jpg", "3:1:33S7-9RRX-SLB")],
     "Antonio, nacido el 23 oct 1868, hijo de Salvador Naranjo y «Josefa de Canaria». El índice dice Camatagua, pero la partida está en el libro de San Sebastián.", "1:1:6DRP-MYPG"),
    ("ve_salvador_rafael", "salvador-naranjo-cabrera", "Bautismo de su hijo Rafael de Jesús (La Victoria, 13 jul 1871)",
     [("1871-07-13_Bautismo_Rafael_de_Jesus_hijo_de_Salvador_Naranjo_y_Josefa_Cabrera.jpg", "3:1:33SQ-GRRG-9TS2")],
     "Rafael de Jesús, nacido el 11 nov 1870, hijo de Salvador Naranjo y Josefa Cabrera; padrinos Rafael Cabrera y Merced Travieso.", ""),
    ("ve_salvador_jose", "salvador-naranjo-cabrera", "Defunción de su hijo José, de 12 años (La Victoria, 6 oct 1881)",
     [("1881-10-06_Defuncion_Jose_Naranjo_hijo_de_Salvador_LaVictoria.jpg", "3:1:33SQ-GRRB-SZ13")],
     "José Naranjo, de 12 años, hijo legítimo de Salvador Naranjo y Josefa Cabrera.", ""),
    ("ve_salvador_entierros", "salvador-naranjo-cabrera", "Entierros de sus hijos Rosa, Narciso y Aurelia (La Victoria, 1900)",
     [("1900-03-17_Entierro_Rosa_Naranjo_hija_de_Salvador_LaVictoria.jpg", "3:1:33SQ-GRRB-S7B7"),
      ("1900-06-16_Entierro_Narciso_Naranjo_33_anos_hijo_de_Salvador_Naranjo_y_Josefa_Cabrera_LaVictoria.jpg", "3:1:33S7-9RRB-S4Q8"),
      ("1900-09-13_Entierro_Aurelia_Naranjo_hija_de_Salvador_LaVictoria.jpg", "3:1:33SQ-GRRB-S7Y2")],
     "Rosa (17 mar 1900), Narciso «Obsequio», de 33 años (16 jun 1900), y Aurelia (13 sep 1900), los tres hijos de Salvador Naranjo y Josefa Cabrera.", "1:1:XSX4-8PC4"),
    # ---- Francisco Javier
    ("ve_fj_solteria", "francisco-javier-naranjo-cabrera", "Expediente de soltería de Francisco Javier Naranjo (Caracas, 28 may 1857)",
     [("1857_Solteria_Francisco_Javier_Naranjo_01.jpg", "3:1:33SQ-GRT9-SVHS"), ("1857_Solteria_Francisco_Javier_Naranjo_02.jpg", "3:1:33SQ-GRT9-SVW7"), ("1857_Solteria_Francisco_Javier_Naranjo_03.jpg", "3:1:33SQ-GRT9-SVYW")],
     "«Francisco Javier Naranjo natural de la Ciudad de Telde Isla de Gran Canaria y vecino de San Sebastián de los Reyes…» quiere casarse con María de Jesús Zumbado, de Charallave. Declara su «tío carnal» Fernando Cabrera, que lo trajo de Telde con 14 años.", ""),
    ("ve_fj_dispensa", "francisco-javier-naranjo-cabrera", "Dispensa de parentesco para casarse con María de Jesús Zumbado, con árbol de los Cabrera (1857)",
     [("1857_Dispensa_Francisco_Javier_Naranjo_y_Maria_de_Jesus_Zumbado_01_arbol_Cabrera.jpg", "3:1:33SQ-GRTS-XHP"), ("1857_Dispensa_Francisco_Javier_Naranjo_y_Maria_de_Jesus_Zumbado_02.jpg", "3:1:33S7-9RTS-NFV")],
     "El cura de San Sebastián dibuja el árbol de parentesco: tronco común Pedro Cabrera; Pedro Cabrera casó con María [Isidora] Padrón; su hija Antonia Cabrera con Adrián Naranjo; de ellos, Francisco Javier. Testigos Fernando y Pedro Cabrera: «hace veinte y un años llegó a Venezuela».", ""),
    ("ve_fj_entierro", "francisco-javier-naranjo-cabrera", "Entierro de Francisco Javier Naranjo (San Sebastián, 21 oct 1866)",
     [("1866-10-21_Entierro_Francisco_Javier_Naranjo_hermano_de_Felix_SanSebastian.jpg", "3:1:33SQ-GRRL-9CZ6")],
     "Entierro «mayor de primera clase», con música, del adulto Francisco Javier Naranjo, natural de Canarias, vecino de San Sebastián, casado con María de Jesús Zumbado.", ""),
    ("ve_fj_josefa_antonia", "francisco-javier-naranjo-cabrera", "Su hija Josefa Antonia: matrimonio (1878) y entierro (1909) en San Sebastián",
     [("1878-09-30_Matrimonio_Josefa_Antonia_Naranjo_hija_de_Francisco_Javier_y_Rafael_Ortega_SanSebastian.jpg", "3:1:33SQ-GRRL-BDH"),
      ("1909-06-07_Entierro_Josefa_Antonia_Naranjo_hija_de_Francisco_Javier_SanSebastian.jpg", "3:1:33SQ-GRR2-NNN")],
     "30 sep 1878: se casan Rafael Ortega y Josefa Antonia Naranjo, natural de La Victoria, hija legítima de Francisco Javier Naranjo, difunto, y María de Jesús Zumbado. 7 jun 1909: su entierro en San Sebastián.", "1:1:XSQS-84TS"),
    # ---- Manuel
    ("ve_manuel_solteria", "manuel-naranjo-cabrera", "Expediente de soltería de Manuel Naranjo e Inelda del Nogal (La Victoria, 1872)",
     [("1872_Solteria_Manuel_Naranjo_e_Inelda_del_Nogal_01_portada.jpg", "3:1:33S7-9RRK-9YQC"), ("1872_Solteria_Manuel_Naranjo_e_Inelda_del_Nogal_02.jpg", "3:1:33S7-9RRK-9YM8"),
      ("1872_Solteria_Manuel_Naranjo_e_Inelda_del_Nogal_03_padre_vive_en_Gran_Canaria.jpg", "3:1:33SQ-GRRK-9YNV")],
     "«1872. Justificación de soltería y libertad de Manuel Naranjo, español y vecino de la Victoria…» Testigos: Fernando Cabrera, «mi tío carnal», Antonio Cabrera, primo hermano, y Domingo Benítez. Fernando declara que Manuel «ocurrió a la Gran Canaria, donde vive su padre»: Adrián Naranjo seguía vivo en 1872.", ""),
    ("ve_manuel_hijos", "manuel-naranjo-cabrera", "Bautismos de sus hijos Ignacio (1873), Adrián de Jesús (1874) y Luisa Elena de Lourdes (1895)",
     [("1873-04-14_Bautismo_Ignacio_hijo_de_Manuel_Naranjo_e_Ynelda_Nogal.jpg", "3:1:33S7-9RRG-9BNC"), ("1874-08-09_Bautismo_Adrian_de_Jesus_hijo_de_Manuel_Naranjo.jpg", "3:1:33S7-9RRG-9YPD"),
      ("1895-11-01_Bautismo_Luisa_Elena_de_Lourdes_hija_de_Manuel_Naranjo_e_Ynelda_del_Nogal_SanSebastian.jpg", "3:1:33S7-9RRL-9FMS")],
     "(Manuel) Ignacio, nacido el 17 feb 1873, y Adrián de Jesús, nacido el 7 jun 1874 (Adrián Ramón Naranjo del Nogal, 1874-1975), bautizados en La Victoria; Luisa Elena de Lourdes, bautizada en San Sebastián el 1 nov 1895. Todos hijos de Manuel Naranjo e Ynelda del Nogal.", "1:1:6ZKS-C3P6"),
    ("ve_manuel_nieta", "manuel-naranjo-cabrera", "Matrimonio de su nieta Lourdes Naranjo González (Caracas, 17 sep 1927)",
     [("1927-09-17_Matrimonio_Lourdes_Naranjo_Gonzalez_hija_de_Adrian_Naranjo_nieta_de_Manuel_Caracas.jpg", "3:1:33S7-9RR1-KRS")],
     "José Sabino se casa con Lourdes Naranjo González, hija de Adrián Naranjo y Caridad González.", "1:1:4D9C-YC6Z"),
    # ---- los Cabrera (hermano de Josefa Antonia)
    ("ve_pedro_cabrera", "antonia-cabrera-padron", "Matrimonio de su hermano Pedro Cabrera (La Victoria, 16 abr 1860)",
     [("1860-04-16_Matrimonio_Pedro_Cabrera_hijo_de_Pedro_Cabrera_y_Maria_Isidora_Padron_tio_de_Felix_LaVictoria.jpg", "3:1:33S7-9RRF-9MZ5")],
     "Pedro Cabrera, hijo de Pedro Cabrera y María Isidora Padrón, se casa con María del Carmen Zumbado, con dispensa de tercer grado de consanguinidad. Testigos: su sobrino Salvador Naranjo y María de Jesús Zumbado. Confirma que la madre de Josefa Antonia se llamaba María Isidora Padrón.", ""),
    ("ve_pedro_cabrera_hijo", "antonia-cabrera-padron", "Bautismo de su sobrino Ramón Valentín Cabrera Zumbado (La Victoria, 30 dic 1870)",
     [("1870-12-30_Bautismo_Ramon_Valentin_hijo_de_Pedro_Cabrera_y_Maria_del_Carmen_Zumbado.jpg", "3:1:33SQ-GRRG-9TXX")],
     "Ramón Valentín, hijo de Pedro Cabrera y María del Carmen Zumbado.", ""),
]

def copiar_imagenes():
    from PIL import Image
    DESTINO.mkdir(parents=True, exist_ok=True)
    for _, _, _, imgs, _, _ in GRUPOS:
        for archivo, _ in imgs:
            dst = DESTINO / (pathlib.Path(archivo).stem + ".jpg")
            if dst.exists():
                continue
            src = ORIGEN / archivo
            if not src.exists():           # la defunción de 1881 está en PDF
                import fitz
                pdf = fitz.open(ORIGEN / (pathlib.Path(archivo).stem + ".pdf"))
                pdf[0].get_pixmap(dpi=150).save(str(dst.with_suffix(".png")))
                src = dst.with_suffix(".png")
            im = Image.open(src).convert("RGB")
            im.thumbnail((1500, 1500))
            im.save(dst, quality=80, optimize=True, progressive=True)
            if src.suffix == ".png" and src.parent == DESTINO:
                src.unlink()

def registrar(DOC, P):
    for clave, ficha, titulo, imgs, texto, indexado in GRUPOS:
        enlaces = " · ".join(f'<a href="{FS}{ark}" target="_blank" rel="noopener">imagen {i + 1}</a>' if len(imgs) > 1 else f'<a href="{FS}{ark}" target="_blank" rel="noopener">imagen en FamilySearch</a>'
                             for i, (_, ark) in enumerate(imgs))
        if indexado:
            enlaces += f' · <a href="{FS}{indexado}" target="_blank" rel="noopener">registro indexado</a>'
        DOC[clave] = dict(titulo=titulo, imgs=[f"img/docs/venezuela/{pathlib.Path(a).stem}.jpg" for a, _ in imgs],
                          texto=texto, fuente=f"Registros parroquiales y diocesanos de Venezuela (FamilySearch): {enlaces}.")
        if ficha in P and clave not in P[ficha]["docs"]:
            P[ficha]["docs"].append(clave)

if __name__ == "__main__":
    copiar_imagenes()
    print("ok")
