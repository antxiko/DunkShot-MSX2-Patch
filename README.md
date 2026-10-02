# Dunk Shot (MSX) — the MSX2 patch against the flicker

*(También disponible [en castellano](README.es.md).)*

An unofficial patch for **Dunk Shot** (HAL Laboratory, 1986), the 32 KB MSX
cartridge. Every player in the game is four sprites and the MSX1 draws four
per line, so the game shares them out and the players flicker. An MSX2 draws
eight per line: this patch takes the game to SCREEN 4 and turns the sharing
off. On an MSX1 the same file plays as the original.

**The website**: https://antxiko.github.io/DunkShot-MSX2-Patch/

| | |
|---|---|
| the patch | `parche/dunkshot_msx2.ips`, 292 bytes |
| bytes changed | 164, in 24 stretches; no pattern moved |
| sprites not drawn per frame | 66.7 (original, MSX1) → 1.7 (patched, MSX2) |
| worst frame | 166 → 22 |
| on an MSX1 | as the original |
| tested | in openMSX (MSX1 and Philips NMS 8250); **not yet on real hardware** |

No ROM is distributed, neither the original nor the patched one: you supply
your own dump (sha256 `a1891e03...`) and the IPS does the rest. The result
must give sha256 `e5e14b0f...`.

## Applying it

With any IPS tool, or as [Getting started](docs/GETTING-STARTED.md) explains.
Then, in openMSX:

```
openmsx -machine Philips_NMS_8250 -cart dunkshot_msx2.rom
```

## Building it

You need Python 3, GNU make, [Pasmo](https://pasmo.speccy.org/) and your dump
as `dunkshot.rom` at the root:

```
make            # listing, reassembly, checks, the patch and the tests
make parche     # only the patch
```

This repository starts from the
[commented disassembly of Dunk Shot](https://github.com/antxiko/DunkShot-disassembly),
with its history, so every address the patch touches can be looked up in
`src/dunkshot.asm`.

## Notice

The game belongs to HAL Laboratory; only the patch, the analysis, the comments
and the tools are here. See [LEGAL-NOTICE.md](LEGAL-NOTICE.md).
