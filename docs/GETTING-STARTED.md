# Getting started

What is distributed here is a patch, `parche/dunkshot_msx2.ips` (292 bytes),
never a cartridge image. You need your own dump of **Dunk Shot** (HAL
Laboratory, 1986), the 32 KB cartridge with sha256
`a1891e038566596a9f67067b8ea4694709aa9fee93c8ac0379360b30ea3abe62`.

## Applying it

With any IPS tool (Lunar IPS, Floating IPS, `flips`...), or with these lines of
Python:

    rom = bytearray(open("dunkshot.rom", "rb").read())
    ips = open("parche/dunkshot_msx2.ips", "rb").read()
    i = 5
    while ips[i:i + 3] != b"EOF":
        a, n = int.from_bytes(ips[i:i + 3], "big"), int.from_bytes(ips[i + 3:i + 5], "big")
        rom[a:a + n] = ips[i + 5:i + 5 + n]
        i += 5 + n
    open("dunkshot_msx2.rom", "wb").write(rom)

The result must have sha256
`e5e14b0f7b188b77ae7b8daa28d98ee1e8c9bfc3d6479b9b93c0afbfd1037e6c`. It is a
plain 32 KB cartridge, no mapper. In openMSX:

    openmsx -machine Philips_NMS_8250 -cart dunkshot_msx2.rom

Any MSX2 should do; on an MSX1 it plays as the original, flicker included.

## Building it

You need Python 3, GNU make, [Pasmo](https://pasmo.speccy.org/) and your dump
as `dunkshot.rom` at the root of the repository:

    make            # the listing, reassembly, checks, the patch and the tests
    make parche     # only the patch: work/dunkshot_msx2.rom and parche/dunkshot_msx2.ips
    make web        # this website, in docs/

`tools/parche_msx2.py` assembles the new pieces with Pasmo, checks that every
byte it overwrites is the one it expects, patches the operands and writes the
patched ROM, the IPS and `parche/parche_msx2.asm`, the listing of the new code.
`tests/test_parche.py` checks that the IPS gives back exactly that ROM and
touches only the 24 stretches it declares.

## What else is in the repository

This repository starts from the
[commented disassembly of Dunk Shot](https://antxiko.github.io/DunkShot-disassembly/),
with its history: `src/dunkshot.asm` is the listing that reassembles the
original byte for byte, and every address on these pages can be looked up
there. The tools of the disassembly are still here (`make` runs them); the
ones of the patch are:

- `tools/parche_msx2.py`: the patch.
- `tools/omsx_parpadeo.tcl` and `tools/lanza_parpadeo.sh`: an openMSX that
  counts, every frame, the sprites the VDP does not draw
  ([In the emulator](IN-THE-EMULATOR.md)).
