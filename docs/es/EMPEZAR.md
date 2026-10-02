# Empezar

Aquí se distribuye un parche, `parche/dunkshot_msx2.ips` (292 bytes), nunca
una imagen del cartucho. Hace falta tu propio volcado de **Dunk Shot** (HAL
Laboratory, 1986), el cartucho de 32 KB con sha256
`a1891e038566596a9f67067b8ea4694709aa9fee93c8ac0379360b30ea3abe62`.

## Cómo aplicarlo

Con cualquier herramienta de IPS (Lunar IPS, Floating IPS, `flips`...), o con
estas líneas de Python:

    rom = bytearray(open("dunkshot.rom", "rb").read())
    ips = open("parche/dunkshot_msx2.ips", "rb").read()
    i = 5
    while ips[i:i + 3] != b"EOF":
        a, n = int.from_bytes(ips[i:i + 3], "big"), int.from_bytes(ips[i + 3:i + 5], "big")
        rom[a:a + n] = ips[i + 5:i + 5 + n]
        i += 5 + n
    open("dunkshot_msx2.rom", "wb").write(rom)

El resultado tiene que dar sha256
`e5e14b0f7b188b77ae7b8daa28d98ee1e8c9bfc3d6479b9b93c0afbfd1037e6c`. Es un
cartucho de 32 KB sin mapeador. En openMSX:

    openmsx -machine Philips_NMS_8250 -cart dunkshot_msx2.rom

Debería valer cualquier MSX2; en un MSX1 se juega como el original, con su
parpadeo.

## Cómo generarlo

Hace falta Python 3, GNU make, [Pasmo](https://pasmo.speccy.org/) y tu volcado
como `dunkshot.rom` en la raíz del repositorio:

    make            # el listado, el reensamblado, los controles, el parche y los tests
    make parche     # solo el parche: work/dunkshot_msx2.rom y parche/dunkshot_msx2.ips
    make web        # esta web, en docs/

`tools/parche_msx2.py` ensambla los trozos nuevos con Pasmo, comprueba que cada
byte que pisa es el que espera, parchea los operandos y escribe la ROM
parcheada, el IPS y `parche/parche_msx2.asm`, el listado del código nuevo.
`tests/test_parche.py` comprueba que el IPS devuelve exactamente esa ROM y que
solo toca los 24 tramos que declara.

## Qué más hay en el repositorio

Este repositorio parte del
[desensamblado comentado de Dunk Shot](https://antxiko.github.io/DunkShot-disassembly/es/),
con su historial: `src/dunkshot.asm` es el listado que reensambla el original
byte a byte, y cada dirección de estas páginas se puede buscar allí. Las
herramientas del desensamblado siguen aquí (`make` las pasa); las del parche
son:

- `tools/parche_msx2.py`: el parche.
- `tools/omsx_parpadeo.tcl` y `tools/lanza_parpadeo.sh`: un openMSX que cuenta,
  cada cuadro, los sprites que el VDP no pinta
  ([En el emulador](EN-EL-EMULADOR.md)).
