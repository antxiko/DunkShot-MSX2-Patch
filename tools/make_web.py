#!/usr/bin/env python3
"""Genera la portada de la web del PARCHE, en los dos idiomas.

La maquinaria no nombra ningun juego: el nombre, la cabecera, las cifras, los
hallazgos y la galeria salen de tools/contenido_web.py. Aqui solo van los
rotulos de la pagina. El diseno es el compartido por la serie
(tools/estilo_web.py) y la pagina sale autocontenida, con las imagenes
embebidas como data URI.

Uso: make_web.py <docs/imagenes> <salida.html> <idioma>
"""
import base64
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo_web import ESTILO                                   # noqa: E402
from contenido_web import (NOMBRE, COMPANIA, PORTADA, HALLAZGOS, GALERIA, LOGOTIPO,  # noqa: E402
                           BYTES, TRAMOS, IPS, MEDIDA, por_cuadro)


def mil(n, idioma):
    return f"{n:,}".replace(",", "." if idioma == "es" else ",")


TXT = {
    "es": dict(
        nav=[("#numbers", "Las cifras"), ("#findings", "Lo que hace"),
             ("#screens", "En openMSX")],
        docnav=[("EMPEZAR.html", "Empezar"), ("EL-PARPADEO.html", "El parpadeo"),
                ("EL-PARCHE.html", "El parche"),
                ("EN-EL-EMULADOR.html", "En el emulador"),
                ("PREGUNTAS-ABIERTAS.html", "Preguntas abiertas")],
        otro=("../", "In English"),
        h_num="El parche en cifras", h_find="Lo que hace, y lo que hubo que saber",
        h_scr="En openMSX",
        cifras=[(por_cuadro("original_msx1", "es"), "sprites sin pintar por cuadro, original en MSX1"),
                (por_cuadro("parcheado_msx2", "es"), "sprites sin pintar por cuadro, parcheado en MSX2"),
                (f"{MEDIDA['original_msx1'][2]} &rarr; {MEDIDA['parcheado_msx2'][2]}", "en el peor cuadro"),
                (mil(BYTES, "es"), f"bytes cambiados en {TRAMOS} tramos"),
                (mil(IPS, "es"), "bytes de IPS"),
                ("0", "patrones movidos")],
        nota_scr="Capturas de openMSX con la ROM de cada pie; las órdenes que "
                 "las sacan están en En el emulador.",
        pie_leg="Parche extraoficial. El juego es de sus autores y de " + COMPANIA +
                ", y la imagen del cartucho no se distribuye: solo el IPS.",
    ),
    "en": dict(
        nav=[("#numbers", "The numbers"), ("#findings", "What it does"),
             ("#screens", "In openMSX")],
        docnav=[("GETTING-STARTED.html", "Getting started"),
                ("THE-FLICKER.html", "The flicker"),
                ("THE-PATCH.html", "The patch"),
                ("IN-THE-EMULATOR.html", "In the emulator"),
                ("OPEN-QUESTIONS.html", "Open questions")],
        otro=("es/", "En castellano"),
        h_num="The patch in numbers",
        h_find="What it does, and what had to be known",
        h_scr="In openMSX",
        cifras=[(por_cuadro("original_msx1", "en"), "sprites not drawn per frame, original on MSX1"),
                (por_cuadro("parcheado_msx2", "en"), "sprites not drawn per frame, patched on MSX2"),
                (f"{MEDIDA['original_msx1'][2]} &rarr; {MEDIDA['parcheado_msx2'][2]}", "in the worst frame"),
                (mil(BYTES, "en"), f"bytes changed in {TRAMOS} stretches"),
                (mil(IPS, "en"), "bytes of IPS"),
                ("0", "patterns moved")],
        nota_scr="openMSX screenshots of the ROM each caption names; the "
                 "commands that take them are in In the emulator.",
        pie_leg="Unofficial patch. The game belongs to its authors and to " + COMPANIA +
                ", and the cartridge image is not distributed: only the IPS.",
    ),
}


def img64(ruta):
    with open(ruta, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def main(argv):
    if len(argv) < 4:
        print(__doc__)
        return 2
    imgdir, salida, idioma = argv[1:4]
    t = dict(TXT[idioma], **PORTADA[idioma])

    # El "logotipo" de la cabecera no es un montaje ni una captura: es la
    # pantalla de titulo que pinta el propio cartucho, dibujada desde la ROM
    # (contenido_web.LOGOTIPO). Si el PNG no esta, el trabajo NO esta hecho: se
    # cae al texto, y eso se ve.
    ruta_logo = os.path.join(imgdir, LOGOTIPO)
    cabecera = (f'<img src="{img64(ruta_logo)}" alt="{NOMBRE}">'
                if os.path.exists(ruta_logo)
                else f"<h1>{NOMBRE}</h1>")

    nav = "".join(f'<a href="{h}">{x}</a>' for h, x in t["nav"])
    nav += "".join(f'<a href="{h}">{x}</a>' for h, x in t["docnav"])
    nav += (f'<a href="{t["otro"][0]}" style="margin-left:auto;color:var(--oro)">'
            f'{t["otro"][1]}</a>')

    cifras = "".join(f'<div class="cifra"><b>{v}</b><span>{e}</span></div>'
                     for v, e in t["cifras"])
    halls = "".join(f'<div class="hall"><h3>{tit}</h3>{cuerpo}</div>'
                    for tit, cuerpo in HALLAZGOS[idioma])
    imgs = ""
    faltan = []
    for fich, es, en in GALERIA:
        # un "{}" en el nombre se sustituye por el idioma: asi la lamina de
        # figuras sale rotulada en el idioma de la pagina
        if "{}" in fich:
            fich = fich.format("" if idioma == "es" else "_" + idioma)
        ruta = os.path.join(imgdir, fich)
        if not os.path.exists(ruta):
            faltan.append(fich)
            continue
        pie = es if idioma == "es" else en
        alt = re.sub(r"<[^>]+>", "", pie)
        imgs += (f'<figure><img src="{img64(ruta)}" alt="{alt}">'
                 f'<figcaption>{pie}</figcaption></figure>')
    if faltan:
        print("  (faltan %d imagenes: %s)" % (len(faltan), " ".join(faltan)))

    html = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t['titulo']}</title>
<style>{ESTILO}</style>
<header class="top">
  {cabecera}
  <p class="claim">{t['claim']}</p>
  <p class="ficha">{' - '.join(t['ficha'])}</p>
</header>
<p class="ficha" style="border:1px solid var(--oro);padding:.8em 1em;margin:1.5em 0">
{t['aviso']}</p>
<nav>{nav}</nav>
<section id="numbers">
  <h2>{t['h_num']}</h2>
  <div class="cifras">{cifras}</div>
</section>
<section id="findings"><h2>{t['h_find']}</h2>{halls}</section>
<section id="screens">
  <h2>{t['h_scr']}</h2>
  <p class="n">{t['nota_scr']}</p>
  <div class="galeria">{imgs}</div>
</section>
<footer><p>{t['pie_leg']}</p></footer>
"""
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)
    print("  %s: %d KB (%s)" % (salida, len(html) // 1024, idioma))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
