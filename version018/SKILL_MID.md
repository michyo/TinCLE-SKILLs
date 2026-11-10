---
name: tincle-mid
description: Use when converting MML to Standard MIDI files using the arancini utility, and rendering MIDI to retro Chiptune WAV/OGG audio using the tiramisu utility. [TinCLE Special Skill v0.18]
---

# SKILL_MID.md - TinCLE Talent Chip for Music Data Conversion [MML -> MID, MID -> WAV/OGG]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

## arancini [MML to MIDI Conversion]

This document defines the instructions for using `arancini`, the official TinCLE utility for converting MML (Music Macro Language) files into standard `.mid` (Standard MIDI File Format 1) files.

### Usage

```bash
arancini <input.mml> <output.mid>
```

#### Arguments:
* `<input.mml>`: The path to the text file containing your MML composition.
* `<output.mid>`: The destination path for the generated Standard MIDI File.

#### MML to MIDI Mapping:
* **Channels (`CHn:`)**: Maps directly to MIDI tracks and channels. Up to 8 channels.
* **Tempo (`Tn`)**: Encoded into the Set Tempo Meta Event in Track 0.
* **Volume (`Vn`)**: Converted from the 0-15 scale to MIDI Velocity (0-127) and Control Change 7 (Volume).
* **Patch (`@n`)**: Directly maps to standard MIDI Program Change messages.
* **Notes (`A`-`G`, `R`)**: Generates Note On and Note Off events with precise delta times based on `MIDI_TICKS_PER_QUARTER = 480`.

### Example

1. Create a `song.mml`:
   ```text
   T120
   CH1: @0 V12 O4 C4 D4 E4 F4 G2 R2
   CH2: @33 V10 O3 C2 C2 C1
   ```
2. Convert it:
   ```bash
   arancini song.mml song.mid
   ```
3. The resulting `song.mid` is now ready to be imported into any modern DAW or standard MIDI player.

---

## tiramisu [Retro Audio Chiptune Renderer]

`tiramisu` is a single-executable, pure CUI chiptune renderer based on the ChiptuneMIDI engine. It converts standard MIDI (`.mid`) files into 8-bit retro audio waveforms and exports them as `.wav` or `.ogg` files without relying on external UI libraries like Qt.

### Features
- **Standalone Execution:** Runs as a single command-line tool with no Qt or GUI dependencies.
- **Waveform Customization:** Supports setting specific retro waveforms (`square`, `triangle`, `saw`) for individual channels or applying one waveform to all channels using the `-all:<wave>` flag.
- **Format Support:** Renders output to both `.wav` and `.ogg` formats directly from the memory buffer.
- **Cross-Platform C99 / C++11:** Uses standard C++ headers and includes the core C99 MIDI/audio synthesis libraries in the tree.

### Usage

Run the tool from the command line passing the input file, output file, and optional waveform settings.

#### Basic Syntax
```sh
tiramisu <input.mid> <output.[wav|ogg]> [ch1_wave] [ch2_wave] ...
```

#### Examples

**Default rendering (all channels default to 'saw'):**
```sh
./tiramisu song.mid output.wav
```

**Override all channels to use the 'square' waveform:**
```sh
./tiramisu song.mid output.ogg -all:square
```

**Specify individual channel waveforms (e.g., ch1=square, ch2=triangle, ch3=saw, rest default to saw):**
```sh
./tiramisu song.mid output.wav square triangle saw
```

### Integrating within TinCLE
This tool is used by the AI assistant and the TinCLE ecosystem to programmatically generate chiptune renditions of MIDI data. The resulting `.wav` or `.ogg` files can be directly loaded into TinCLE's sound system (via Howler.js or direct asset inclusion).
