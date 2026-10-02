# Dunk Shot (MSX) — el parche MSX2 contra el parpadeo

*(Also available [in English](README.md).)*

Un parche extraoficial para **Dunk Shot** (HAL Laboratory, 1986), el cartucho
de 32 KB para MSX. Cada jugador del juego son cuatro sprites y el MSX1 pinta
cuatro por línea, así que el juego los reparte y los jugadores parpadean. Un
MSX2 pinta ocho por línea: este parche lleva el juego a SCREEN 4 y apaga el
reparto. En un MSX1 el mismo fichero se juega como el original.

**La web**: https://antxiko.github.io/DunkShot-MSX2-Patch/es/

| | |
|---|---|
| el parche | `parche/dunkshot_msx2.ips`, 292 bytes |
| bytes cambiados | 164, en 24 tramos; ningún patrón movido |
| sprites sin pintar por cuadro | 66,7 (original, MSX1) → 1,7 (parcheado, MSX2) |
| peor cuadro | 166 → 22 |
| en un MSX1 | como el original |
| probado | en openMSX (MSX1 y Philips NMS 8250); **todavía no en una máquina real** |

No se distribuye ninguna ROM, ni la original ni la parcheada: pones tu propio
volcado (sha256 `a1891e03...`) y el IPS hace el resto. El resultado tiene que
dar sha256 `e5e14b0f...`.

## Cómo aplicarlo

Con cualquier herramienta de IPS, o como explica [Empezar](docs/es/EMPEZAR.md).
Luego, en openMSX:

```
openmsx -machine Philips_NMS_8250 -cart dunkshot_msx2.rom
```

## Cómo generarlo

Hace falta Python 3, GNU make, [Pasmo](https://pasmo.speccy.org/) y tu volcado
como `dunkshot.rom` en la raíz:

```
make            # listado, reensamblado, controles, el parche y los tests
make parche     # solo el parche
```

Este repositorio parte del
[desensamblado comentado de Dunk Shot](https://github.com/antxiko/DunkShot-disassembly),
con su historial, así que cada dirección que toca el parche se puede buscar en
`src/dunkshot.asm`.

## Aviso

El juego es de HAL Laboratory; aquí solo están el parche, el análisis, los
comentarios y las herramientas. Ver [AVISO-LEGAL.md](AVISO-LEGAL.md).
