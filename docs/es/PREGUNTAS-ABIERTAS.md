# Preguntas abiertas

Lo que no está comprobado, dicho claro:

- **Una máquina real.** Todo está medido en openMSX. Nadie ha pasado aún el
  cartucho parcheado por un MSX2 o un MSX1 de verdad.
- **Otros MSX2.** Las medidas de MSX2 son del Philips NMS 8250 (50 Hz). El
  parche solo le pregunta a la BIOS si es un MSX2 (el byte 0x002D) y no usa
  nada propio de ese modelo, pero los MSX2 japoneses, el MSX2+ y el turbo R
  no se han probado.
- **Más de ocho por línea.** Cuando cinco o seis jugadores se amontonan con
  el balón y su sombra, siguen cayendo más de ocho sprites en una línea; el
  VDP deja fuera entonces los más lejanos, sin parpadeo que los reparta.
  Medido: 1,7 sprites por cuadro de media, 22 en el peor cuadro. Si repartir
  esos, como hace el original, quedaría mejor que dejar fuera los de atrás es
  cuestión de gusto, y no se ha probado.
- **La segunda tabla en un MSX2.** El juego sigue montando la lista invertida
  y copiándola a 0x3F00 cada cuadro, donde en un MSX2 no mira nadie. Cuesta
  128 bytes de escritura en VRAM por cuadro; se dejó así para no tocar el
  código del juego.
- **Las pantallas con la figura de muestra.** TRADE se ha visto en el MSX2 con
  la figura en sus colores; las fichas de equipo (LEFT TEAM, RIGHT TEAM) usan
  la misma rutina, `viste_jugador`, pero no se han visto una a una.
