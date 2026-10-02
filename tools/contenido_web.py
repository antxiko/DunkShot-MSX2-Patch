#!/usr/bin/env python3
"""EL CONTENIDO de la web de este parche: lo unico que es de este proyecto.

md2html.py y make_web.py son la maquinaria y no llevan dentro el nombre de
ningun juego: lo leen de aqui.

Las cifras estan medidas, y tests/test_web.py las coteja:
  - BYTES, TRAMOS e IPS: los imprime `make parche` (tools/parche_msx2.py) y
    los cuenta el test sobre parche/dunkshot_msx2.ips.
  - Las de parpadeo: work/p_msx1_antes, work/p_msx1_d4 y work/p_msx2_d4,
    tools/lanza_parpadeo.sh (docs/IN-THE-EMULATOR.md tiene las ordenes).
"""

NOMBRE = "Dunk Shot — MSX2 patch"
COMPANIA = "HAL Laboratory"
ANIO = 1986
REPOSITORIO = "https://github.com/antxiko/DunkShot-MSX2-Patch"
DESENSAMBLADO = "https://antxiko.github.io/DunkShot-disassembly/"

# El parche (make parche)
BYTES = 164
TRAMOS = 24
IPS = 292
SHA_ORIGINAL = "a1891e038566596a9f67067b8ea4694709aa9fee93c8ac0379360b30ea3abe62"
SHA_PARCHEADO = "e5e14b0f7b188b77ae7b8daa28d98ee1e8c9bfc3d6479b9b93c0afbfd1037e6c"

# La medida (tools/lanza_parpadeo.sh, 30 s de partido): (cuadros, sprites sin pintar, peor cuadro)
MEDIDA = {
    "original_msx1": (1798, 119936, 166),
    "parcheado_msx1": (1798, 124875, 175),
    "parcheado_msx2": (1505, 2513, 22),
}


def por_cuadro(clave, idioma):
    """Sprites sin pintar por cuadro, con un decimal y la coma o el punto de cada idioma."""
    cuadros, sobrantes, _ = MEDIDA[clave]
    d = "%.1f" % (sobrantes / cuadros)
    return d.replace(".", ",") if idioma == "es" else d


PIE_LEGAL = {
    "es": "<em>Dunk Shot</em> lo public&oacute; HAL Laboratory para MSX en 1986; "
          "son 32 KB. Todos los derechos sobre el juego siguen siendo de sus "
          "titulares. Esto es un parche extraoficial: aqu&iacute; solo se "
          "distribuye el fichero de diferencias, nunca la imagen del cartucho.",
    "en": "<em>Dunk Shot</em> was published by HAL Laboratory for the MSX in 1986; "
          "it is 32 KB. All rights in the game remain with their holders. This "
          "is an unofficial patch: only the difference file is distributed "
          "here, never the cartridge image.",
}

PORTADA = {
    "es": dict(
        titulo="Dunk Shot (MSX) - el parche MSX2 contra el parpadeo",
        claim="El baloncesto de HAL Laboratory parpadea porque cada jugador son "
              "cuatro sprites y el MSX1 pinta cuatro por línea. Un MSX2 pinta "
              "ocho: este parche de 164 bytes lleva el juego a SCREEN 4 y apaga "
              "el reparto, y en un MSX1 se sigue jugando como el original.",
        ficha=["HAL Laboratory - <b>(c) 1986 HAL Laboratory</b>",
               "Parche IPS de <b>292 bytes</b>, extraoficial",
               "<b>MSX2</b> (y MSX1 tal cual)",
               "Original <b>a1891e03...</b>"],
        aviso="<b>Probado en openMSX, todavía no en una máquina real.</b> Las "
              "capturas son de la ROM parcheada corriendo en openMSX (un MSX1 y "
              "un Philips NMS 8250), y las cifras salen de una sonda que cuenta, "
              "cuadro a cuadro, los sprites que el VDP no pinta. No se "
              "distribuye ninguna ROM: solo el IPS. Sale del "
              "<a href=\"" + DESENSAMBLADO + "es/\">desensamblado comentado</a>, "
              "donde se puede buscar cada dirección.",
    ),
    "en": dict(
        titulo="Dunk Shot (MSX) - the MSX2 patch against the flicker",
        claim="HAL Laboratory's basketball flickers because every player is "
              "four sprites and the MSX1 draws four per line. An MSX2 draws "
              "eight: this 164-byte patch takes the game to SCREEN 4 and turns "
              "the sharing off, and on an MSX1 it still plays as the original.",
        ficha=["HAL Laboratory - <b>(c) 1986 HAL Laboratory</b>",
               "A <b>292-byte</b> IPS patch, unofficial",
               "<b>MSX2</b> (and MSX1 as it was)",
               "Original <b>a1891e03...</b>"],
        aviso="<b>Tested in openMSX, not yet on real hardware.</b> The "
              "screenshots are of the patched ROM running in openMSX (an MSX1 "
              "and a Philips NMS 8250), and the numbers come from a probe that "
              "counts, frame by frame, the sprites the VDP does not draw. No ROM "
              "is distributed: only the IPS. It comes from the "
              "<a href=\"" + DESENSAMBLADO + "\">commented disassembly</a>, where "
              "every address can be looked up.",
    ),
}

HALLAZGOS = {
    "es": [
        ("El parpadeo lo gestiona el juego",
         "<p>Cada cuadro <code>0x5E1B</code> ordena los siete grupos por "
         "profundidad, <code>0x5C0B</code> monta sus atributos en ese orden, "
         "<code>0x5BAB</code> los copia también al revés y la interrupción "
         "(<code>0x5B77</code>) enseña una u otra tabla: un cuadro van delante "
         "los cercanos y al siguiente los lejanos. En un MSX2 el parche deja "
         "siempre la ordenada: el más cercano delante y sin cambiar de un "
         "cuadro a otro.</p>"),
        ("En el modo 2, colores primero y atributos en +0x200",
         "<p>El registro 5 señala un bloque de 1 KB: la tabla de colores de "
         "sprite, 16 bytes por sprite, ocupa la primera mitad, y los atributos "
         "van 0x200 más allá. Ponerlos al revés deja la pantalla sin un solo "
         "sprite, y eso fue lo primero que salió.</p>"),
        ("El único sitio libre era 0x3C00",
         "<p>Bajo los 16 KB del MSX1 el juego no usa nada de 0x3C00 a 0x3FFF: "
         "colores en 0x3C00, atributos en 0x3E00 y la segunda tabla del MSX1 en "
         "0x3F00. No se mueve ni un patrón, y el mismo fichero vale en los dos "
         "MSX.</p>"),
        ("El código nuevo, en huérfanos del cartucho",
         "<p>El relleno de 0xBFD4 y tres rutinas que no llama nadie "
         "(<code>0x6EA0</code>, <code>0x6F30</code>, <code>0x7AAE</code>), "
         "encontradas al trazar el desensamblado. Y la figura de muestra de "
         "los menús de equipo conserva sus colores: el modo 2 no lee el color "
         "del atributo, así que el parche se los copia a la tabla de "
         "colores.</p>"),
    ],
    "en": [
        ("The game manages the flicker",
         "<p>Every frame <code>0x5E1B</code> sorts the seven groups by depth, "
         "<code>0x5C0B</code> builds their attributes in that order, "
         "<code>0x5BAB</code> copies them reversed as well and the interrupt "
         "(<code>0x5B77</code>) shows one table or the other: one frame the "
         "near players are in front, the next the far ones. On an MSX2 the "
         "patch always leaves the sorted one: the nearest in front, and no "
         "change from frame to frame.</p>"),
        ("In mode 2, colours first and attributes at +0x200",
         "<p>Register 5 points at a 1 KB block: the sprite colour table, 16 "
         "bytes per sprite, takes the first half, and the attributes sit 0x200 "
         "further on. Put them the other way round and the screen has not a "
         "single sprite, which is the first thing that came out.</p>"),
        ("The only free room was 0x3C00",
         "<p>Below the 16 KB of the MSX1 the game uses nothing from 0x3C00 to "
         "0x3FFF: colours at 0x3C00, attributes at 0x3E00 and the MSX1's second "
         "table at 0x3F00. Not one pattern moves, and the same file works on "
         "both MSXs.</p>"),
        ("The new code, in the cartridge's orphans",
         "<p>The filler at 0xBFD4 and three routines nobody calls "
         "(<code>0x6EA0</code>, <code>0x6F30</code>, <code>0x7AAE</code>), found "
         "when the disassembly was traced. And the sample figure of the team "
         "menus keeps its colours: mode 2 does not read the attribute's colour, "
         "so the patch copies them into the colour table.</p>"),
    ],
}

# La cabecera: el rotulo del titulo, dibujado desde la ROM por el desensamblado
LOGOTIPO = "rotulo.png"

GALERIA = [
    ("partido_original.png",
     "El original en un MSX1 (C-BIOS_MSX1_JP): en este cuadro faltan "
     "jugadores, y al del centro le faltan el pelo y la camiseta. 66,7 sprites "
     "sin pintar por cuadro en treinta segundos de partido.",
     "The original on an MSX1 (C-BIOS_MSX1_JP): in this frame players are "
     "missing, and the one in the middle has no hair or shirt. 66.7 sprites "
     "not drawn per frame over thirty seconds of a match."),
    ("partido_msx2.png",
     "El parcheado en el Philips NMS 8250: SCREEN 4, ocho sprites por línea, "
     "todos los jugadores de la ventana enteros, con el balón y la red. 1,7 "
     "sprites sin pintar por cuadro.",
     "The patched cartridge on the Philips NMS 8250: SCREEN 4, eight sprites "
     "per line, every player in the window whole, with the ball and the net. "
     "1.7 sprites not drawn per frame."),
    ("partido_msx1.png",
     "El parcheado en un MSX1: las dos tablas siguen alternando, ahora en "
     "0x3E00 y 0x3F00, y parpadea como el original.",
     "The patched cartridge on an MSX1: the two tables still alternate, now "
     "at 0x3E00 and 0x3F00, and it flickers as the original."),
    ("trade_msx2.png",
     "TRADE en el MSX2: la figura de muestra con su piel, su pelo y su "
     "camiseta, copiados a la tabla de colores de sprite por "
     "<code>0x6F30</code>.",
     "TRADE on the MSX2: the sample figure with its skin, hair and shirt, "
     "copied into the sprite colour table by <code>0x6F30</code>."),
]
