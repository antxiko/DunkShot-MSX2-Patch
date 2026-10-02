# The flicker

Every player in Dunk Shot is four 16 × 16 sprites stacked on top of each other:
hair, upper skin, shirt and lower skin. Six players are 24 sprites; with the
net, the ball, its shadow and the arrow, 28 of the 32 the VDP has. Two of a
player's four sprites can fall on the same line, so two players side by side
already fill the four sprites per line the TMS9918 of the MSX1 can draw. From
the fifth on, the VDP does not draw them.

## How the game shares them out

The flicker is not an accident: the game manages it.

![The 160 poses of four sprites](imagenes/poses.png)

1. `0x5E1B` sorts the seven groups (six players and the ball) by depth, the
   nearest first, with a bubble sort, and leaves each one's place in field
   +0x0E of its record.
2. `0x5C0B` builds their attributes in that order in the list at 0xE7B0
   (`0x5C40` works out each player's four sprites from the position of the
   feet and the offsets of the pose).
3. `0x5BAB` copies the same groups reversed into 0xE730 and sends the two
   lists to the two attribute tables, 0x1B00 and 0x1F00.
4. On every interrupt `0x5B77` flips bit 2 of register 5: one frame the VDP
   shows the table with the near players in front, the next the one with the
   far players in front.

When players bunch up, the sprites that do not fit on a line are a different
set each frame: what is lost one frame is drawn the next, at 30 Hz on a 60 Hz
machine. That is the flicker.

![The fixed sprites: net, ball, shadow and arrow](imagenes/sprites_fijos.png)

## What changes on an MSX2

The V9938 of the MSX2, in sprite mode 2 (SCREEN 4 and up), draws eight sprites
per line instead of four. With eight, four players can share a line, and the
moments when more than eight pile up are few. The patch takes the game to
SCREEN 4 and, on an MSX2, **stops the alternation**: register 5 always points
at the table sorted by depth. The game's code does not change; it keeps
sorting and building both lists, but the VDP only shows the first one.

So on an MSX2 the nearest player is always in front, and who is in front no
longer changes from frame to frame. When more than eight sprites do fall on a
line, the ones the VDP leaves out are the last in the table, the farthest,
which are the ones behind anyway. The numbers are in
[In the emulator](IN-THE-EMULATOR.md); how it is done, in
[The patch](THE-PATCH.md).

On an MSX1 nothing changes: the two tables keep alternating as in the
original, only moved to other addresses.
