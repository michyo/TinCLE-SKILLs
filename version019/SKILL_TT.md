---
name: tincle-tt
description: Use when generating seamless procedural 2D/3D tileable PNG textures from text-based `.turd` DSL files using TinCLE's `turdtex` CLI tool (Tiny Ultimate Rendering Dumper of TEXture). Covers syntax, 8 built-in pattern types, multi-stop color ramps, blend modes, and production recipes. [TinCLE Tool Skill v0.19]
---

# SKILL_TT.md - TinCLE Procedural Texture Specification (`turdtex`)

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.
  * *Unauthorized copying, redistribution, commercial resale, or claim of authorship regarding this prompt architecture and talent chips (`SKILL_*.md`) are strictly prohibited.*
* **Official Website:** https://michyo.net/tincle/
* **Tool Credits:** Created with General Assistants: Jules & Gyaru Sono.

Under this skill, the AI agent shall act in strict accordance with the following rules when designing, authoring, or generating procedural textures for TinCLE projects.

---

## 1. Overview & Philosophy

* **Tool Name:** `turdtex` (**T**iny **U**ltimate **R**endering **D**umper of **TEX**ture)
* **Purpose:** A zero-dependency, standalone Pure C99 CLI tool that compiles lightweight, stack-based `.turd` text scripts into **100% seamless (tileable) 24-bit RGB PNG textures**.
* **Seamless by Default:** Every pattern generator automatically wraps mathematically across horizontal and vertical boundaries. Do **NOT** write `tile: true` or any tiling flags—tiling is always ON.
* **Deterministic Output:** Unlike random-seed generators (`fartbox`), `turdtex` uses fixed deterministic math/hashing (similar to `pisstrak`'s reproducible MML). The exact same `.turd` file always produces the exact same pixel-for-pixel PNG, making iterative color and contrast refinement reliable.
* **Output Format:** 24-bit RGB PNG (3 channels, **no alpha/transparency channel**). Best suited for terrain, floors, walls, bricks, rocks, lava, wood, marble, sci-fi panels, and repeating backgrounds.

---

## 2. CLI Usage & AI Workflow

### Command Line Invocation
```bash
turdtex <input.turd> [-o <output.png>]
```
* `<input.turd>`: Path to the `.turd` text definition file (mandatory).
* `-o <output.png>`: Output PNG path (optional; defaults to `output.png` if omitted).
* **Error Condition:** If no layer block (`[...]`) is defined in the `.turd` file, `turdtex` exits with an error (`No layers defined`).

### AI Execution Guidelines
* **Autonomous / Agentic AIs:** Write the `.turd` file directly into the project folder, execute `turdtex <name>.turd -o <name>.png` via CLI, verify success, and load the resulting `.png` once inside `game_load()` using `tincle_load_image()`.
* **Interactive Chat AIs:** Provide the complete `.turd` file content in a clean code block along with the exact `turdtex` command for the user to run.
* **Asset Packaging Reminder:** Ensure `.png` is registered in `exsass.txt` so `asspack` and `emcass` include the generated textures in release/Web builds.

---

## 3. Strict `.turd` File Syntax & Anti-Bug Rules

**[CRITICAL WARNING] Never output search citations or footnotes (e.g., `[cite: 1]`, `[1]`) anywhere inside `.turd` files. Output ONLY clean, valid `.turd` syntax.**

### Structure Overview
A `.turd` file consists of an optional **Global Header** followed by **1 to 32 Layer Blocks** processed strictly from **top to bottom**.

```text
; Global Header (MUST appear before the first '[' layer header)
width: 512
height: 512

; Layer Blocks (processed top-to-bottom)
[Layer: LayerName]
type: <pattern_type>
frequency: <integer >= 1>
color_ramp: <#RRGGBB, #RRGGBB, ...>
blend: <blend_mode>
opacity: <0.0 to 1.0>
```

### Mandatory Parser Constraints (`[CRITICAL ANTI-BUG RULES]`)
1. **Comments MUST start with `;` (Semicolon):**
   * **NEVER use `#` for comments.** The parser only skips empty lines and lines whose first non-whitespace character is `;`. A `#` line containing a colon (`:`) will be misparsed.
   * **NEVER put inline comments at the end of a property line** (e.g., `type: wood ; grain` is INVALID and breaks string matching). Always place `;` comments on their own dedicated lines.
2. **Global Header Placement:** `width` and `height` (defaults: `512` and `512`) **MUST** appear before the first `[` line. Any `width`/`height` placed after a layer header is ignored.
3. **Layer Limit:** Maximum **32 layers** per file (`MAX_LAYERS = 32`). Every line beginning with `[` starts a new layer block.
4. **Line Length Limit:** Maximum **255 characters** per line (`char line[256]`). Keep `color_ramp` lines clean and concise.
5. **Color Format (`#RRGGBB` only):** Colors MUST be 6-digit hexadecimal RGB (e.g., `#ff8800` or `ff8800`). **NEVER** use 3-digit shorthand (`#fff`) or 8-digit RGBA (`#ff8800ff`).
6. **Color Ramp Limit:** Supports **1 to 8 colors** (`MAX_RAMP_COLORS = 8`), comma-separated. Colors beyond the 8th are ignored.
7. **Case-Insensitive Keys/Values:** Keys (`type`, `frequency`, `color_ramp`, `blend`, `opacity`, `width`, `height`) and values are case-insensitive.
8. **Layer 0 Blending Rule:** Layer 0 blends against a solid black canvas (`#000000`). Always set the first layer to `blend: normal` and `opacity: 1.0` unless you intentionally want a darkened base.

### Layer Property Defaults
If omitted within a layer block, properties default to:
* `type`: `perlin`
* `frequency`: `1` (integers `< 1` are clamped to `1`)
* `color_ramp`: `#000000, #ffffff`
* `blend`: `normal`
* `opacity`: `1.0`

---

## 4. Built-in Pattern Types (`type`)

All 8 generators return a normalized scalar value `t` in the range `[0.0, 1.0]` which is mapped linearly across `color_ramp` (`0.0` = first color, `1.0` = last color).

| `type` | Value Mapping (`0.0` → `1.0`) & Behavior | Ideal Game Uses |
| :--- | :--- | :--- |
| `perlin` | Smooth tileable Perlin noise (`0.0` = valleys/dark, `1.0` = peaks/bright). | Dirt, clouds, organic noise, surface grit (`overlay`), color variation/weathering (`multiply`). |
| `voronoi` | Distance to nearest cell center $F_1$ (`0.0` = cell center, `1.0` = cell boundary). | Pebbles, organic cobblestones, foliage clusters, grime/stain blotches, cellular skin. |
| `voronoi_edge` | Border distance $F_2 - F_1$ (`0.0` = exact crack/seam center, `1.0` = cell interior). | Glowing lava/magma cracks, parched cracked earth, ice fractures, stained glass, magic runes. |
| `brick` | Staggered horizontal brick masonry (`freq` cols × `freq * 2` rows). `0.0` = mortar/grout; `0.8`–`1.0` = beveled brick face (brightest at brick center). | Castle walls, dungeon brickwork, urban facades, retro FPS corridors. |
| `wood` | Vertical sine-wave bands warped by Perlin noise (`0.0`–`1.0`). | Wooden planks, library furniture, doors, tree bark, logs. |
| `marble` | Diagonal sine veins distorted by 2-octave Perlin turbulence (`0.0`–`1.0`). | Polished temple marble, luxury stone floors, toxic slime/acid pools, plasma/energy flows. |
| `metal` | `freq` × `freq` square sci-fi panels with beveled edges and 4 corner rivets. Exact bands: `0.05` = groove/seam, `0.30`–`0.70` = edge bevel, `0.70` = flat face, `0.70`–`1.00` = raised corner rivets. | Sci-fi spaceship hulls, industrial bulkheads, reinforced bunker floors, plain panels (via ramp trick). |
| `checker` | Sharp binary grid (`0.0` or `1.0`). `frequency` is automatically rounded up to an even integer `>= 2` to guarantee seamless edges. | Chessboards, mansion floor tiles, puzzle grids, retro floor patterns. |

---

## 5. Blend Modes (`blend`) & Layering Strategy

| `blend` | Behavior | Best Practice |
| :--- | :--- | :--- |
| `normal` | Replaces base color with layer color (scaled by `opacity`). | Always use on Layer 0 (`opacity: 1.0`), or for semi-transparent color washes. |
| `multiply` | Multiplies base × layer (darkens/tints). White (`#ffffff`) leaves base unchanged. | Macro color variation, dirt/grime, heat variation, ambient shading (`frequency: 2`–`5`, `opacity: 0.25`–`0.7`). |
| `add` | Adds layer to base (brightens/glows, clamped at white). Black (`#000000`) leaves base unchanged. | Emissive highlights, glowing cracks, magical sheen, metallic specular accents. |
| `overlay` | Combines multiply (darks) and screen (lights) for contrast/detail. | Fine surface grain/roughness/scratches using `perlin` with `#000000, #ffffff` and low `opacity` (`0.15`–`0.35`). |

### Recommended 3-Layer Formula
For rich, game-ready textures, stack layers in this order:
1. **Layer 1 (Structure / Base):** Primary pattern (`brick`, `wood`, `voronoi_edge`, `metal`, etc.) with `blend: normal`, `opacity: 1.0`.
2. **Layer 2 (Micro Surface Grit):** High-frequency `perlin` (`frequency: 20`–`36`) with `#000000, #ffffff`, `blend: overlay`, `opacity: 0.15`–`0.35`.
3. **Layer 3 (Macro Weathering / Tone Variation):** Low-frequency `perlin` or `voronoi` (`frequency: 2`–`5`) with `#887766, #ffffff` (or warm/cool tint), `blend: multiply`, `opacity: 0.3`–`0.6`.

---

## 6. Advanced `color_ramp` Mastery (Zero-Code Techniques)

`color_ramp` interpolates `t` (`0.0`–`1.0`) evenly across `N` stops (from 1 up to 8 colors). Exploiting stop positions unlocks patterns far beyond naive 2-color gradients:

* **Technique A — Rivetless Plain Sci-Fi Metal Panel (`metal`):**
  * In `metal`, the flat face is `0.70` and corner rivets occupy `0.70`–`1.00`.
  * By providing a **4-stop ramp** (stops at `0.00`, `0.33`, `0.67`, `1.00`) where **Stop 3 and Stop 4 are identical** (e.g., `#14171a, #3e454d, #7a8594, #7a8594`), the flat face and rivets receive the exact same color—cleanly erasing the rivets while keeping grooves and beveled edges intact!
* **Technique B — Thin Glowing Cracks (`voronoi_edge`):**
  * Repeat the dark interior rock color across the last 2–3 stops (e.g., 7 stops: `#ffffcc, #ff8800, #d92600, #593825, #2b2927, #262423, #262423`) to keep magma veins crisp and bright near `0.0` while keeping the cooled stone uniform.
* **Technique C — Solid Color Tint Layer:**
  * A 1-color `color_ramp` (e.g., `color_ramp: #334455`) outputs a flat uniform color across the entire texture, useful for subtle tinting via `multiply` or `add`.

---

## 7. Production Recipe Library (`.turd` Templates)

### 7.1 Grassy Ground (`grass.turd`)
```text
width: 512
height: 512

; Layer 1: Soil base
[Layer: Dirt]
type: perlin
frequency: 8
color_ramp: #2b1d0c, #4a351a
blend: normal
opacity: 1.0

; Layer 2: Grass blades
[Layer: GrassStrands]
type: voronoi
frequency: 32
color_ramp: #1a4d0f, #55aa2b
blend: overlay
opacity: 1.0

; Layer 3: Natural shade variation
[Layer: Shade]
type: perlin
frequency: 4
color_ramp: #000000, #ffffff
blend: multiply
opacity: 0.3
```

### 7.2 Staggered Brick Wall (`brick.turd`)
```text
width: 512
height: 512

; Layer 1: Staggered bricks (first color = mortar, second = brick face)
[Layer: BrickBase]
type: brick
frequency: 6
color_ramp: #cccccc, #b24a22
blend: normal
opacity: 1.0

; Layer 2: Surface roughness
[Layer: Roughness]
type: perlin
frequency: 32
color_ramp: #000000, #ffffff
blend: overlay
opacity: 0.3

; Layer 3: Firing color variation
[Layer: ColorVariation]
type: perlin
frequency: 4
color_ramp: #4a1500, #ffaa55
blend: multiply
opacity: 0.7
```

### 7.3 Glowing Magma / Lava (`lava.turd`)
```text
width: 512
height: 512

; Layer 1: Glowing cracks and dark volcanic crust
[Layer: MagmaCracks]
type: voronoi_edge
frequency: 7
color_ramp: #ffffcc, #ff8800, #d92600, #593825, #2b2927, #262423, #262423
blend: normal
opacity: 1.0

; Layer 2: Heat intensity variation
[Layer: HeatGlow]
type: perlin
frequency: 5
color_ramp: #aa6644, #ffffff
blend: multiply
opacity: 0.45

; Layer 3: Volcanic grit
[Layer: SurfaceGrit]
type: perlin
frequency: 32
color_ramp: #111111, #eeeeee
blend: overlay
opacity: 0.15
```

### 7.4 Heavy Wood Grain (`wood.turd`)
```text
width: 512
height: 512

; Layer 1: Wood rings and grain
[Layer: WoodGrain]
type: wood
frequency: 6
color_ramp: #3b200e, #5e3619, #7a4924, #4a2811, #6b3e1d
blend: normal
opacity: 1.0

; Layer 2: Fine wood fiber
[Layer: WoodFiber]
type: perlin
frequency: 28
color_ramp: #000000, #ffffff
blend: overlay
opacity: 0.2

; Layer 3: Natural aging variation
[Layer: Aging]
type: perlin
frequency: 3
color_ramp: #997755, #ffffff
blend: multiply
opacity: 0.4
```

### 7.5 Temple Marble (`marble.turd`)
*(Tip: Swap `color_ramp` to `#052205, #116611, #44cc22, #ccff44` for an instant DOOM-style toxic slime pool!)*
```text
width: 512
height: 512

; Layer 1: Marble veins
[Layer: MarbleVeins]
type: marble
frequency: 4
color_ramp: #3a3d42, #7d828a, #c8ccd1, #e8eaed, #f4f5f7, #ffffff
blend: normal
opacity: 1.0

; Layer 2: Subtle stone grain
[Layer: StoneGrit]
type: perlin
frequency: 20
color_ramp: #222222, #dddddd
blend: overlay
opacity: 0.15
```

### 7.6 Sci-Fi Riveted Metal Panel (`metal.turd`)
```text
width: 512
height: 512

; Layer 1: Beveled metal panels with corner rivets
[Layer: MetalPanel]
type: metal
frequency: 4
color_ramp: #14171a, #3e454d, #68727d, #8a95a3, #cdd6e0
blend: normal
opacity: 1.0

; Layer 2: Brushed scratches
[Layer: Scratches]
type: perlin
frequency: 36
color_ramp: #000000, #ffffff
blend: overlay
opacity: 0.25

; Layer 3: Oil grime and wear
[Layer: Grime]
type: voronoi
frequency: 5
color_ramp: #8c7a6b, #ffffff
blend: multiply
opacity: 0.35
```

### 7.7 Plain Rivetless Metal Panel (`metal_plain.turd`)
```text
width: 512
height: 512

; Layer 1: 4-stop ramp with stops 3 and 4 identical to hide corner rivets
[Layer: PlainPanel]
type: metal
frequency: 4
color_ramp: #14171a, #3e454d, #7a8594, #7a8594
blend: normal
opacity: 1.0

; Layer 2: Fine surface scratches
[Layer: Scratches]
type: perlin
frequency: 36
color_ramp: #000000, #ffffff
blend: overlay
opacity: 0.25

; Layer 3: Subtle weathering
[Layer: Grime]
type: voronoi
frequency: 5
color_ramp: #8c7a6b, #ffffff
blend: multiply
opacity: 0.3
```

### 7.8 Antique Checkerboard Tile (`checker.turd`)
```text
width: 512
height: 512

; Layer 1: 8x8 tile grid
[Layer: TileGrid]
type: checker
frequency: 8
color_ramp: #2b241f, #dfd5c5
blend: normal
opacity: 1.0

; Layer 2: Stone surface texture
[Layer: TileTexture]
type: perlin
frequency: 24
color_ramp: #111111, #eeeeee
blend: overlay
opacity: 0.25

; Layer 3: Aged dirt wash
[Layer: DirtWash]
type: perlin
frequency: 3
color_ramp: #aa9988, #ffffff
blend: multiply
opacity: 0.3
```
