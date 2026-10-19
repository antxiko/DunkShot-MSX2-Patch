"""Las cifras y los textos que publica la web del parche, contra lo que mide el
repositorio.

Lo que se rompe solo: una cifra que envejece en tools/contenido_web.py, un
tamano de la tabla de trozos que ya no es el que ensambla la herramienta, un
texto copiado de otro juego, una imagen de la galeria que no existe. Lo del
IPS corre sin la ROM; la tabla de trozos ensambla con pasmo.
"""

import os
import re
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.path.insert(0, os.path.join(RAIZ, "tests"))

import contenido_web as cw  # noqa: E402
from test_parche import lee_ips, IPS, BYTES_CAMBIADOS, TRAMOS  # noqa: E402

PAGINAS_EN = {"GETTING-STARTED", "THE-FLICKER", "THE-PATCH", "IN-THE-EMULATOR", "OPEN-QUESTIONS"}
PAGINAS_ES = {"EMPEZAR", "EL-PARPADEO", "EL-PARCHE", "EN-EL-EMULADOR", "PREGUNTAS-ABIERTAS"}


def texto(*ruta):
    return open(os.path.join(RAIZ, *ruta), encoding="utf-8").read()


class LasCifras(unittest.TestCase):
    def test_bytes_tramos_e_ips_son_los_del_fichero(self):
        regs = lee_ips(IPS)
        self.assertEqual(cw.IPS, os.path.getsize(IPS))
        self.assertEqual(cw.TRAMOS, len(regs))
        self.assertEqual(cw.TRAMOS, len(TRAMOS))
        self.assertEqual(cw.BYTES, sum(len(b) for _, b in regs))
        self.assertEqual(cw.BYTES, BYTES_CAMBIADOS)

    def test_los_textos_dicen_las_mismas_cifras(self):
        for fn in ("README.md", os.path.join("docs", "THE-PATCH.md")):
            t = " ".join(texto(fn).split())          # los saltos de linea, como espacios
            self.assertIn("292", t, fn)
            self.assertIn("164", t, fn)
            self.assertIn("24 stretches", t, fn)
        for fn in ("README.es.md", os.path.join("docs", "es", "EL-PARCHE.md")):
            t = " ".join(texto(fn).split())
            self.assertIn("292", t, fn)
            self.assertIn("164", t, fn)
            self.assertIn("24 tramos", t, fn)

    def test_la_medida_por_cuadro_es_la_de_las_tablas(self):
        for clave, en, es in (("original_msx1", "66.7", "66,7"),
                              ("parcheado_msx1", "69.5", "69,5"),
                              ("parcheado_msx2", "1.7", "1,7")):
            self.assertEqual(cw.por_cuadro(clave, "en"), en)
            self.assertEqual(cw.por_cuadro(clave, "es"), es)
            cuadros, _, peor = cw.MEDIDA[clave]
            fila_en = re.compile(r"\| %s \| %s \| %s \|" % (re.escape(f"{cuadros:,}"), en, peor))
            fila_es = re.compile(r"\| %s \| %s \| %s \|" % (re.escape(f"{cuadros:,}".replace(",", ".")), es, peor))
            self.assertRegex(texto("docs", "IN-THE-EMULATOR.md"), fila_en)
            self.assertRegex(texto("docs", "es", "EN-EL-EMULADOR.md"), fila_es)

    def test_los_sha_son_los_publicados(self):
        for fn in ("README.md", "README.es.md"):
            t = texto(fn)
            self.assertIn(cw.SHA_ORIGINAL[:8], t, fn)
            self.assertIn(cw.SHA_PARCHEADO[:8], t, fn)
        for fn in (("docs", "GETTING-STARTED.md"), ("docs", "es", "EMPEZAR.md")):
            t = texto(*fn)
            self.assertIn(cw.SHA_ORIGINAL, t, fn)
            self.assertIn(cw.SHA_PARCHEADO, t, fn)

    def test_la_tabla_de_trozos_es_la_que_ensambla_la_herramienta(self):
        """Necesita pasmo, como el resto de `make` (PATH o PASMO=...)."""
        import parche_msx2 as p
        medidos = {"0x%04X" % org: len(p.ensambla(n, f)) for n, (org, _, f) in p.trozos("1").items()}
        for fn in (("docs", "THE-PATCH.md"), ("docs", "es", "EL-PARCHE.md")):
            filas = dict(re.findall(r"^\|[^|]+\| (0x[0-9A-F]{4}) \| (\d+) \|$", texto(*fn), re.M))
            self.assertEqual({k: int(v) for k, v in filas.items()}, medidos, fn)


class LasPaginas(unittest.TestCase):
    def test_las_cinco_paginas_en_los_dos_idiomas(self):
        for carpeta, nombres in (("docs", PAGINAS_EN), (os.path.join("docs", "es"), PAGINAS_ES)):
            hay = {fn[:-3] for fn in os.listdir(os.path.join(RAIZ, carpeta)) if fn.endswith(".md")}
            self.assertEqual(hay, nombres, carpeta)

    def test_estan_todas_las_de_la_galeria(self):
        imgdir = os.path.join(RAIZ, "docs", "imagenes")
        for fich, es, en in cw.GALERIA:
            self.assertTrue(os.path.exists(os.path.join(imgdir, fich)), fich)
            self.assertTrue(es and en, fich)
        self.assertTrue(os.path.exists(os.path.join(imgdir, cw.LOGOTIPO)))

    def test_no_sobran_imagenes(self):
        """Cada PNG de docs/imagenes lo usa la portada o alguna pagina."""
        usadas = {cw.LOGOTIPO} | {f for f, _, _ in cw.GALERIA}
        for carpeta in ("docs", os.path.join("docs", "es")):
            for fn in os.listdir(os.path.join(RAIZ, carpeta)):
                if fn.endswith(".md"):
                    usadas |= set(re.findall(r"imagenes/([\w.-]+\.png)", texto(carpeta, fn)))
        hay = set(os.listdir(os.path.join(RAIZ, "docs", "imagenes")))
        self.assertEqual(hay, usadas)


class NadaDeOtroJuego(unittest.TestCase):
    OTROS = re.compile(r"Q\*bert|qbert|Konami|RC-7\d\d|Hinotori|Rastan|Mahjong", re.I)

    def test_la_licencia_y_los_avisos_son_de_este_juego(self):
        for fn in ("LICENSE", "AVISO-LEGAL.md", "LEGAL-NOTICE.md", "README.md", "README.es.md"):
            t = texto(fn)
            self.assertIn("Dunk Shot", t, fn)
            self.assertIsNone(self.OTROS.search(t), fn)

    def test_las_herramientas_no_apuntan_a_otro_juego(self):
        for fn in os.listdir(os.path.join(RAIZ, "tools")):
            if not fn.endswith((".py", ".sh", ".tcl")):
                continue
            self.assertNotIn("qbert", texto("tools", fn).lower(), fn)

    def test_ni_los_textos_publicados(self):
        for carpeta in ("docs", os.path.join("docs", "es")):
            for fn in os.listdir(os.path.join(RAIZ, carpeta)):
                if fn.endswith(".md"):
                    self.assertIsNone(self.OTROS.search(texto(carpeta, fn)), os.path.join(carpeta, fn))


if __name__ == "__main__":
    unittest.main()
