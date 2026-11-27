---
name: tincle-sd
description: Use when create or manage sprite generation tasks for the TinCLE spidcook tool. [TinCLE Tool Skill v0.19]
---

# SKILL_SD: TinCLE Procedural Sprite Generator (spidcook)

## Overview
`spidcook` (SPrite Image Direct COOKer) is a command-line procedural generation tool designed specifically for the TinCLE ecosystem. It allows AI agents to instantly generate symmetric, highly-detailed, retro-style spaceship and mech sprites without relying on external graphic editors or manual pixel placement. By setting the canopy color to skin tone, you can also use them as a sprite for human characters.

## Command Usage
```bash
spidcook [filename] [width] [height] [direction] [color1] [color2] [color3] [color4]
```

### Important Rule: Fully Optional Parameters
All arguments are completely optional. If you omit any arguments, `spidcook` will automatically apply safe default values and generate a randomized palette.

* `spidcook` (Runs with all defaults: `spidcook.png`, 48x48, up, random colors)
* `spidcook myship.png 64 64` (Generates a 64x64 ship facing up with random colors)
* `spidcook myship.png 32 64 right` (Generates a ship, rotates it right, random colors)

### Help Command
* `spidcook -h`: Displays a quick help reference in the console. (Must be the first argument).

## Parameter Details

1. **filename**: The output PNG filename. (Default: `spidcook.png`)
2. **width**: Canvas width in pixels.
  * **Range:** 16 to 128. (Default: `48`). Values outside this range will be clipped automatically.
3. **height**: Canvas height in pixels.
  * **Range:** 16 to 128. (Default: `48`). Values outside this range will be clipped automatically.
4. **direction**: The facing direction of the sprite.
  * **Values:** `up`, `down`, `left`, `right`. (Default: `up`).
  * **CRITICAL ROTATION BEHAVIOR:** The procedural generation logic always builds the ship facing `up` using the specified `width` and `height`. If `left` or `right` is specified, the entire canvas is rotated 90 degrees *after* generation. **This means the final output image will have its width and height swapped.** (e.g., Requesting `width=32`, `height=64`, `direction=right` will result in a final output image that is `64` pixels wide and `32` pixels high).
5. **color1-4**: HEX color codes for the sprite palette. (e.g., `FFFFFF` or `#FFFFFF`).
  * `color1`: Outline & internal mechanical structures.
  * `color2`: Main armor color.
  * `color3`: Sub/Accent parts color.
  * `color4`: Glowing parts (Canopy/Cockpit).
  * *Note:* If colors are omitted, `spidcook` intelligently computes a highly aesthetic randomized color scheme based on complementary and analogous color theories.
