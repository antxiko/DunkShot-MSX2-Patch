# El parpadeo

Cada jugador de Dunk Shot son cuatro sprites de 16 × 16 apilados: pelo, piel de
arriba, camiseta y piel de abajo. Seis jugadores son 24 sprites; con la red, el
balón, su sombra y la flecha, 28 de los 32 que tiene el VDP. Dos de los cuatro
sprites de un jugador pueden caer en la misma línea, así que con dos jugadores
lado a lado ya se llenan los cuatro sprites por línea que pinta el TMS9918 del
MSX1. Del quinto en adelante, el VDP no los pinta.

## Cómo los reparte el juego

El parpadeo no es un accidente: el juego lo gestiona.

![Las 160 poses de cuatro sprites](../imagenes/poses.png)

1. `0x5E1B` ordena los siete grupos (seis jugadores y el balón) por
   profundidad, el más cercano primero, con una burbuja, y deja el puesto de
   cada uno en el campo +0x0E de su registro.
2. `0x5C0B` monta sus atributos en ese orden en la lista de 0xE7B0 (`0x5C40`
   calcula los cuatro sprites de cada jugador desde la posición de los pies y
   los desplazamientos de la pose).
3. `0x5BAB` copia los mismos grupos al revés en 0xE730 y manda las dos listas a
   las dos tablas de atributos, 0x1B00 y 0x1F00.
4. En cada interrupción `0x5B77` cambia el bit 2 del registro 5: un cuadro el
   VDP enseña la tabla con los cercanos delante y al siguiente la que tiene
   delante a los lejanos.

Cuando los jugadores se juntan, los sprites que no caben en una línea son
otros en cada cuadro: lo que se pierde en uno se pinta en el siguiente, a 30 Hz
en una máquina de 60 Hz. Ese es el parpadeo.

![Los sprites fijos: red, balón, sombra y flecha](../imagenes/sprites_fijos.png)

## Qué cambia en un MSX2

El V9938 del MSX2, en el modo de sprites 2 (SCREEN 4 en adelante), pinta ocho
sprites por línea en vez de cuatro. Con ocho, caben cuatro jugadores en una
línea, y los momentos en que se amontonan más de ocho son pocos. El parche
lleva el juego a SCREEN 4 y, en un MSX2, **apaga la alternancia**: el registro
5 señala siempre la tabla ordenada por profundidad. El código del juego no
cambia; sigue ordenando y montando las dos listas, pero el VDP solo enseña la
primera.

Así que en un MSX2 el jugador más cercano va siempre delante, y quién va
delante ya no cambia de un cuadro a otro. Cuando sí caen más de ocho sprites
en una línea, los que el VDP deja fuera son los últimos de la tabla, los más
lejanos, que son los que quedan detrás de todos modos. Las cifras están en
[En el emulador](EN-EL-EMULADOR.md); cómo se hace, en
[El parche](EL-PARCHE.md).

En un MSX1 no cambia nada: las dos tablas siguen alternando como en el
original, solo que en otras direcciones.
