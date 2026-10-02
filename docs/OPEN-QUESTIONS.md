# Open questions

What has not been checked, said plainly:

- **Real hardware.** Everything was measured in openMSX. Nobody has run the
  patched cartridge on a real MSX2 or MSX1 yet.
- **Other MSX2 machines.** The MSX2 measurements are on the Philips NMS 8250
  (50 Hz). The patch only asks the BIOS whether it is an MSX2 (byte 0x002D)
  and uses nothing specific to that model, but Japanese MSX2s, the MSX2+ and
  the turbo R have not been tried.
- **More than eight per line.** When five or six players pile up with the
  ball and its shadow, more than eight sprites still fall on a line; the VDP
  then leaves out the farthest ones, with no flicker to share them out.
  Measured: 1.7 sprites per frame on average, 22 in the worst frame. Whether
  sharing those out, as the original does, would look better than leaving the
  ones behind out is a matter of taste that has not been tried.
- **The second table on an MSX2.** The game still builds the reversed list
  and copies it to 0x3F00 every frame, where on an MSX2 nobody looks. It
  costs 128 bytes of VRAM writes per frame; it was left so as not to touch
  the game's code.
- **The screens with the sample figure.** TRADE has been seen on the MSX2
  with the figure in its colours; the team cards (LEFT TEAM, RIGHT TEAM) use
  the same routine, `viste_jugador`, but have not been seen one by one.
