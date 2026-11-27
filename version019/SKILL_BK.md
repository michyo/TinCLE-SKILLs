---
name: tincle-bk
description: Use when building retro 2D games and interactive apps in TinCLE with the `babka` addon (ORB: Omnipotent Realizable BASIC) targeting both Windows EXE (`babka.dll`) and WebAssembly HTML5 (`babka.wasm`). Covers C99 host integration, build pipelines, best practices, and the complete ORB language and command reference. [TinCLE Add-On Skill v0.19]
---

# SKILL_BK.md - TinCLE Add-On Talent Chip: babka (ORB: Omnipotent Realizable BASIC)

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.
  * *Unauthorized copying, redistribution, commercial resale, or claim of authorship regarding this prompt architecture and talent chips (`SKILL_*.md`) are strictly prohibited.*
* **Official Website:** https://michyo.net/tincle/
* **Module:** `babka` (**B**ASIC **A**ncient **B**ytecode **K**ernel **A**ctuator) — `babka.dll` (Windows) / `babka.wasm` (Emscripten Side Module)
* **Language Dialect:** **ORB** (**O**mnipotent **R**ealizable **B**ASIC) — classic 1980s line-numbered home-computer BASIC dialect + modern 24/32-bit color, UTF-8/IME, USF sprite fonts, 64 sprites, `SPEED` controller, PSG + YM2413 (OPLL) FM synthesis.
* **Document Structure:**
  * **Part 1** covers TinCLE C99 host integration, build/packaging pipelines, and AI agent workflows.
  * **Part 2** is the standalone, Single-Source-of-Truth **ORB Language & Command Reference** (designed for direct extraction as `ORB.md`).

Under this skill, the AI agent shall act in strict accordance with the specifications below. **Never hallucinate unimplemented legacy BASIC statements** (e.g., `PEEK`, `POKE`, `VPEEK`, `VPOKE`, `USR`, `CALL`, `BLOAD`, `BSAVE`, `DEF USR`, `KEY`, `BASE`, `PLAY` rhythm percussion mode, or random-access `FIELD`/`LSET`/`RSET`/`GET`/`PUT #`). Only the commands, functions, ranges, and behaviors explicitly documented here exist in `babka`.

---

# Part 1: TinCLE Integration, Build Pipeline & AI Workflow

## 1.1 Overview & Required File Layout

`babka` embeds a Pure C++17 non-blocking BASIC bytecode VM (`babka_core`) paired with a TinCLE/SDL2 video, input, file I/O, and 44.1 kHz audio runtime (`babka_runtime`) into a single drop-in TinCLE addon:

* **Windows Target:** 32-bit native DLL (`babka.dll`), statically linked against `libgcc`, `libstdc++`, and `libwinpthread` (depends only on `KERNEL32.dll`, Windows UCRT, `SDL2.dll`, and `tincle.dll`).
* **WebAssembly Target:** Emscripten dynamic side module (`babka.wasm`, built with `-s SIDE_MODULE=2`) linked externally alongside `game.c` via `emcass`.
* **No Subfolders Rule:** Following TinCLE conventions, keep `game.c`, `AUTOEXEC.BAS`, USF font manifests/pages (`font.json`, `font_p0.png`), `cursor.png`, `font.ttf`, `exsass.txt`, `babka.dll`, and `babka.wasm` in the **project root**.

### Minimum File Layout

| Platform | Required Runtime / Build Files |
| :--- | :--- |
| **Development Root** | `game.c`, `AUTOEXEC.BAS`, `font.json`, `font_p0.png`, `cursor.png`, `font.ttf`, `exsass.txt`, `template.html`, `CREDITS.txt`, `libs/tincle.h`, `libs/tincle.a`, `libs/babka.h`, `babka.dll`, `babka.wasm` |
| **Windows Distribution** | `game.exe`, `tincle.dll`, `SDL2.dll`, `SDL2_ttf.dll`, `SDL2_gfx.dll`, `babka.dll`, `game.data` (via `asspack`), `CREDITS.txt` |
| **WebAssembly Distribution** | `index.html`, `index.js`, `index.wasm`, `index.data`, `babka.wasm` |

---

## 1.2 C99 Host API (`libs/babka.h`)

Include `#include "libs/tincle.h"` and `#include "libs/babka.h"` in your C99 host (`game.c`). `babka` automatically registers its own SDL event hook via `tincle_set_event_callback()` during `babka_init()` and removes it during `babka_shutdown()`.

### Configuration Struct (`BabkaConfig`)

```c
typedef struct BabkaConfig {
    const char* entry_script;   /* Default: "AUTOEXEC.BAS" */
    const char* default_font;   /* Default: "font.json" (USF) */
    int default_speed;          /* Default: 100 (standard 60 fps retro pace) */
    bool show_error_screen;     /* true: render BASIC syntax/runtime error on screen */
} BabkaConfig;
```

* Passing `NULL` to `babka_init(NULL)` applies all defaults above (`"AUTOEXEC.BAS"`, `"font.json"`, `100`, `true`).
* **Note on `default_speed`:** In `babka_init()`, values `<= 0` fall back to `100`. To run at unlimited speed (`SPEED 0`), set `SPEED 0` inside your BASIC script.

### Public C99 Functions (6 Exported Symbols)

| Function Signature | Behavior & Notes |
| :--- | :--- |
| `bool babka_init(const BabkaConfig* cfg);` | Resets VM, loads default USF font into slot 0, initializes `SCREEN 1` (256x192, 32x24 grid) and 44.1 kHz PSG+FM audio, hooks SDL events, and loads/compiles `entry_script`. Returns `true` even on compile error or missing script if `show_error_screen` is `true` so the screen remains visible. |
| `void babka_update(float dt);` | Advances cursor blink timer, runs one non-blocking VM frame slice respecting `SPEED` and `VSYNC`/`WAIT`, polls input/events, pumps WebAudio lookahead buffers on Emscripten, and prints unhandled runtime errors if `show_error_screen` is `true`. |
| `void babka_draw(void);` | Renders the 4 virtual layers (Backdrop, Graphic VRAM, Sprites, Text VRAM) onto an internal composite texture, clears the physical screen with the border color via `tincle_clear()`, and integer-scales (`SDL_ScaleModeNearest`) to the output window. |
| `void babka_shutdown(void);` | Removes the SDL event hook, stops active text input, destroys textures/USF pages, and shuts down SDL2/WebAudio + PSG/FM synthesizers. *(Virtual files are flushed and closed by BASIC `CLOSE` / `END`.)* |
| `int babka_get_status(void);` | Returns public VM state: **`0`** = `RUNNING` (includes `WAIT_VSYNC` and `WAIT_SLEEP`), **`1`** = `ENDED` (`END`/`STOP`/EOF), **`2`** = `ERROR`, **`3`** = `WAITING_INPUT` (`INPUT`/`LINE INPUT`). |
| `const char* babka_get_last_error(void);` | Returns UTF-8 pointer to the last syntax/runtime error message (e.g., `"Syntax error in 120"`), or `""` if none. |

### Minimal Copy-Paste Host Template (`game.c`)

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include "libs/babka.h"
#ifndef __EMSCRIPTEN__
#include <windows.h>
#endif

static void app_update(float dt) { babka_update(dt); }
static void app_draw(void)       { babka_draw(); }

static void app_load(void) {
    BabkaConfig cfg;
    cfg.entry_script = "AUTOEXEC.BAS";
    cfg.default_font = "font.json";
    cfg.default_speed = 100;
    cfg.show_error_screen = true;
    babka_init(&cfg);
    tincle_add_state(0, app_update, app_draw);
    tincle_change_state(0);
}

#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) {
    (void)argc; (void)argv;
    tincle_start(app_load, "TinCLE babka", false, 1280, 720, TINCLE_MODE_2D_NORMAL);
    return 0;
}
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) {
    (void)h; (void)hp; (void)c; (void)n;
    tincle_start(app_load, "TinCLE babka", false, 1280, 720, TINCLE_MODE_2D_NORMAL);
    babka_shutdown();
    return 0;
}
#endif
```

---

## 1.3 Build & Deployment Pipelines

### Windows Native Build & Packaging
1. **Compile EXE (TinyCC via `tinclec`):**
   ```bat
   tinclec game.exe game.c babka.dll
   ```
2. **Pack Assets for Release (`asspack`):**
   Ensure `exsass.txt` lists `bas`, `json`, `png`, `ttf`, `ogg`, `wav` (and any extra read-only data extensions). Run `asspack` to generate `game.data`.
   * On Windows, `OPEN ... FOR INPUT` checks the working directory first (for mutable save files) and falls back to `game.data` via `tincle_load_asset()` **only when `game.data` exists**.
3. **Dependency Verification (`depurant`):**
   ```bat
   depurant.exe game.exe
   ```
   Verify `depurant.txt` is empty (zero missing DLLs).

### WebAssembly HTML5 Build & Packaging
1. **Check `exsass.txt` (CRITICAL):**
   * **MUST include:** `bas`, `json`, `png`, `ttf` (plus `ogg`/`wav` if used by `BGMPLAY`/`SEPLAY`).
   * **MUST NOT include:** `wasm` (`babka.wasm` is passed as an explicit side module argument to `emcass`), and **do NOT include `dat`** if your game generates local Windows save files like `BABKA_HI.DAT` in the project root (otherwise `emcass` will bake your local save file into `index.data`).
2. **Build Web Package (`emcass`):**
   ```bat
   emcass index.html "My ORB Game" 1280 720 game.c babka.wasm
   ```
   Requires `template.html` and `CREDITS.txt` in the project root. Produces `index.html`, `index.js`, `index.wasm`, and `index.data`.
3. **Local Browser Verification (`churro`):**
   Serve the directory over HTTP with `churro.exe` (never open `index.html` via `file://`) and verify visuals, input, WebAudio unlock on first key/click, and IndexedDB save persistence across browser reloads.

### Missing Script Diagnostic Boot Screen (ORB Easter Egg)
If `entry_script` (default `AUTOEXEC.BAS`) is not found at startup (e.g., forgotten from `exsass.txt` or `game.data`), `babka_init()` renders a nostalgic 32-column **ORB (Omnipotent Realizable BASIC)** boot screen showing `File Not Found: AUTOEXEC.BAS`, `OK`, and a blinking cursor. If you see this screen in a packaged build, check `exsass.txt` and `game.data` / `index.data`.

---

## 1.4 AI Best Practices & Critical Pitfalls

1. **Always End Your Main Loop with `VSYNC`:**
   `babka` runs a non-blocking VM inside TinCLE's frame loop. Always place `VSYNC` at the end of your main loop (`GOTO`) so each game tick renders cleanly and scales proportionally with `SPEED`.
2. **Rising-Edge Detection for `STRIG(0)` / Action Buttons:**
   `STRIG(0)` returns `-1` every frame while held. Track previous state (`PTRG`) to trigger single-shot actions (fire, jump, palette swap) on press only:
   ```basic
   510 TRG = STRIG(0)
   515 IF (TRG AND NOT PTRG) THEN GOSUB 800
   518 PTRG = TRG
   ```
3. **Bottom-Row HUD Without Accidental Scrolling (Deferred Wrap):**
   Text VRAM uses **Deferred Wrap**: printing exactly `grid_cols` characters (e.g., 32 chars in `SCREEN 1`) on the bottom row (`LOCATE 0, 23`) will **NOT** scroll the screen as long as you end the `PRINT` statement with a trailing semicolon `;`!
   ```basic
   660 LOCATE 0, 23 : PRINT USING "SCORE:#####  HI:#####  SPD:####"; SC, HI, SPEED;
   ```
4. **Coexisting `SOUND` (PSG SFX) with `PLAY` (PSG Ch. 3 Jingles):**
   PSG Channel 3 (`SOUND` registers `4`, `5`, `10`) is shared with `PLAY` argument 3. When silencing a continuous `SOUND` effect on Ch. 3, guard it with `PLAY(3) = 0` so you do not mute an active Ch. 3 MML jingle:
   ```basic
   630 IF HIT THEN SOUND 4, 220 : SOUND 5, 3 : SOUND 10, 13 ELSE IF PLAY(3) = 0 THEN SOUND 10, 0
   ```
5. **Gamepad 1P vs. Unconnected 2P:**
   TinCLE supports 1 gamepad. `STICK(1)` reads Gamepad 1 D-Pad + analog stick (`±0.4` threshold); `STRIG(1)` = Button A; `STRIG(3)` = Button B. Port 2 (`STICK(2)`, `STRIG(2)`, `STRIG(4)`) always returns `0`.
6. **Safe First-Run Save File Loading (`ON ERROR GOTO`):**
   On a fresh install (or cleared browser IndexedDB), save files do not exist yet and `OPEN ... FOR INPUT` raises Error `53` (`File not found`). Always wrap initial load in `ON ERROR GOTO` and restore `ON ERROR GOTO 0` immediately afterward:
   ```basic
   60 HI = 500 : ON ERROR GOTO 110
   70 OPEN "HISCORE.DAT" FOR INPUT AS #1
   80 INPUT #1, HI : CLOSE #1
   100 GOTO 120
   110 RESUME 120
   120 ON ERROR GOTO 0
   ```
7. **Do Not Use Trademarked Hardware Names on Screen:**
   Avoid displaying trademarked retro hardware brand names (such as 1980s home-computer brands) in in-game UI/titles; use `"ORB"` or `"TINCLE BABKA"`.
8. **Allocate Wide Line-Number Blocks to Prevent Exhaustion & Renumbering:**
   Because ORB uses classic line numbers (`0..65535`) with `GOTO`/`GOSUB` targets, inserting code later into tightly packed lines causes line-number exhaustion and expensive global renumbering bugs. Before writing a medium or large program, **plan wide section blocks upfront** (e.g., `1000-1999` = Init/Setup, `2000-2999` = Main Loop, `3000-3999` = Player/Enemy Logic, `4000-4999` = Map/Rooms, `5000+` = Subroutines, `9000+` = `DATA` tables). Within every section, **step line numbers by at least 10** (e.g., `1000, 1010, 1020...`) and never pack lines densely by 1.

---

# Part 2: ORB (Omnipotent Realizable BASIC) Complete Language & Command Reference

*(Standalone Language Reference — Single Source of Truth for `ORB.md`)*

## 2.1 Core Architecture & Virtual Hardware Model

### Execution & Real-Time `SPEED` Controller
* **Non-Blocking Bytecode VM:** Compiles line-numbered UTF-8 BASIC source once at startup into flat compiled statements.
* **Refresh-Rate Independent `SPEED` (`0..10000`, default `100`):**
  * **`SPEED 100` (Standard):** 1.0 virtual frame per 1/60 s real time; statement budget = **120 statements / virtual frame** (7,200 statements/sec).
  * **`SPEED 1..99` (Slow Motion):** Scales both statement budget and `VSYNC`/`WAIT` virtual frame progression proportionally (e.g., `SPEED 50` runs `VSYNC` loops cleanly at 0.5x speed).
  * **`SPEED 101..10000` (Turbo):** Scales both statement budget and `VSYNC`/`WAIT` virtual frames proportionally (e.g., `SPEED 300` executes 3 virtual frames per 1/60 s real frame).
  * **`SPEED 0` (Unlimited):** Removes statement limits (up to a **12 ms** per-frame time-slice safety cap) while keeping `VSYNC` / `WAIT` synchronized to real 60 Hz frames.
* **60 Hz System Clock (`TIME`):** Increments via a fractional accumulator (`dt * 60.0`), ensuring exact 60 Hz timing on 60 Hz, 120 Hz, and 144 Hz monitors. Wraps at `0..65535`.

### 4 Screen Modes & Integer Scaling
All screen modes render to a virtual pixel canvas and scale by the largest integer factor (`SDL_ScaleModeNearest`) centered inside the physical window, filling outer margins with the active `border` color.

| Mode (`SCREEN m`) | Virtual Resolution | Default Text Grid (8x8 USF) | Notes |
| :---: | :---: | :---: | :--- |
| `0` or `1` | `256 x 192` | `32 x 24` | Classic retro 4:3 (default at startup) |
| `2` | `256 x 240` | `32 x 30` | Extended vertical 4:3 |
| `3` | `320 x 180` | `40 x 22` | Crisp widescreen 16:9 (scales 4x to 1280x720) |
| `4` | `640 x 400` | `80 x 50` | High-resolution text / graphics mode |

* **Sprite Size Modes (`SCREEN , spr_size`):** `0` = 8x8 (8 px), `1` = 8x8 magnified 2x (16 px), `2` = 16x16 (16 px), `3` = 16x16 magnified 2x (32 px).
* **Overscan (`SCREEN , , overscan`):** `0` = maximum integer scale (default), `1` = reserves ~10% outer border margin (`90%` available area).

### 4-Layer Composite Pipeline & `LAYER` Control
Rendered back-to-front every frame:
1. **Layer 1 — Backdrop:** Solid fill using active `bg_color` (falls back to `border_color` if `bg_color = 0`).
2. **Layer 2 — Graphic VRAM:** Active display page (`0..3`) with hardware 4-quadrant wraparound scrolling (`SET SCROLL`). Palette index `0` is transparent.
3. **Layer 3 & 4 — Sprites (64 Planes) & Text VRAM (USF Grid):**
   * `LAYER 0` *(default)*: Graphic → **Sprites** → **Text** (HUD on top of sprites).
   * `LAYER 1`: Graphic → **Text** → **Sprites** (sprites pass in front of text tiles/pillars).
   * Sprites render from plane `63` (back) to plane `0` (front) with **no horizontal sprites-per-scanline limit**.

### Hybrid Color Model (256-Color Live Palette + Direct RGB/RGBA)
Every color parameter (`COLOR`, `PSET`, `LINE`, `CIRCLE`, `PAINT`, `GRPPRINT`, `PUT SPRITE`, `COLOR SPRITE`) accepts either:
* **Palette Index (`0..255`):**
  * `0`: Transparent.
  * `1..15`: Authentic 15-color retro palette (`1`=Black, `2`=Med Green, `3`=Lt Green, `4`=Dark Blue, `5`=Lt Blue, `6`=Dark Red, `7`=Cyan, `8`=Med Red, `9`=Lt Red, `10`=Dark Yellow, `11`=Lt Yellow, `12`=Dark Green, `13`=Magenta, `14`=Gray, `15`=White).
  * `16..255`: Default GRB332 color ramp.
  * **Live Palette Swapping:** Pixels drawn with palette indices store their `pal_idx`; modifying a palette entry via `COLOR=(i,r,g,b)` or `PALETTE i,r,g,b` **instantly updates all already-drawn Graphic VRAM pixels, Text, Sprites, Backdrop, and Border** using that index.
* **Direct Full-Color (`RGB(r,g,b)` / `RGBA(r,g,b,a)`):**
  * Encoded with bit 31 = `1` (`0x80000000 | (a7 << 24) | (r << 16) | (g << 8) | b`, where 7-bit alpha `0x7F` decodes to `255` opaque).
  * Immune to palette swaps; stored cleanly in `%` (`int32_t`) or `#` (`double`) variables.

### UTF-8 Codepoint Strings & Japanese IME
* All string indexing and length operations (`LEN`, `LEFT$`, `RIGHT$`, `MID$`, `INSTR`, `ASC`, `CHR$`, `PRINT USING`, `POS(0)`, `TAB()`) operate strictly in **Unicode codepoints** (1 character = 1 cell, e.g., `LEN("日本語") = 3`).
* `CHR$(0..255)` encodes seamlessly as single codepoints (`ASC(CHR$(255)) = 255`, `LEN(CHR$(255)) = 1`), preserving binary compatibility with `SPRITE$` and `COLOR SPRITE$`.
* `INPUT` and `LINE INPUT` are non-blocking, track the OS IME candidate window to the scaled text cursor, highlight active composition text, and support arrow keys, `Home`, `End`, `Backspace`, and `Delete`.

### Audio Engine (44.1 kHz Stereo, Real-Time)
* **PSG (`emu2149`, AY-3-8910, 1.789772 MHz clock):** Channels 1–3, authentic 16-step volume curve, tone + noise + hardware envelope.
* **YM2413 (OPLL) FM (`emu2413`, 3.579545 MHz clock):** Channels 4–12 (9 melodic FM channels with 15 built-in OPLL voices).
* **Independent Timing:** Audio synthesis runs in real time (SDL2 dedicated audio device on Windows; independent WebAudio `AudioContext` + `AudioBufferSourceNode` lookahead scheduler on Web, auto-unlocked on first click/tap/key) and is **unaffected by `SPEED`**.
* **TinCLE Audio Coexistence:** `BGMPLAY` / `BGMSTOP` / `SEPLAY` bridge directly to TinCLE's OGG/WAV mixer alongside live PSG+FM synthesis.

### Persistent File I/O (`#1..#16`)
* Supports up to 16 simultaneous sequential file handles (`#1` to `#16`).
* **Windows:** Reads from working directory first (mutable saves), falling back to `game.data` (`asspack`) only if `game.data` exists. Writes save directly to the working directory via `tincle_save_data()`.
* **WebAssembly:** TinCLE mounts IndexedDB (`IDBFS`) at `/save` and completes initial sync before `babka_init()`. Reads check `/save/<file>` first, then preloaded virtual root `/<file>`. Writes save via `tincle_save_data()` with a coalesced `FS.syncfs(false)` queue fallback so rapid consecutive saves never drop.

---

## 2.2 Language Fundamentals

### Program Structure & Crunching
* **Line Numbers:** Required integers `0..65535`. Lines are sorted in ascending order at compile time (duplicate line numbers overwrite earlier ones). UTF-8 BOM and blank or standalone `'` comment lines are tolerated.
* **Comments:** `REM ...` or `'` ignores the remainder of the line.
* **Multi-Statement Lines:** Separate statements with `:` (e.g., `10 A=1 : B=2 : PRINT A+B`).
* **Classic One-Liner Crunching:** Space-omitted classic retro BASIC one-liners such as `FORI=1TO10:PRINTI:NEXTI` and `IFX>0THEN100ELSE200` are supported while preserving multi-character variable names like `SCORE`, `TOTAL`, `FORMAT`, `NEXT_X`, and `AUTO`.

### Variables & Data Types
* **Names:** Up to **64 characters** significant (alphanumeric + `_`), **case-insensitive** (`score` == `SCORE`).
* **4 Data Types:**
  | Suffix | Type | C++ Backing | Default Value | `DEF*` Statement |
  | :---: | :--- | :--- | :---: | :--- |
  | `%` | Integer | `int32_t` (`-2,147,483,648` to `2,147,483,647`) | `0` | `DEFINT letter[-letter][, ...]` |
  | `!` | Single Precision | `float` | `0.0` | `DEFSNG letter[-letter][, ...]` |
  | `#` | Double Precision *(default)* | `double` | `0.0` | `DEFDBL letter[-letter][, ...]` |
  | `$` | UTF-8 String | `std::string` | `""` | `DEFSTR letter[-letter][, ...]` |
* Explicit suffix overrides `DEFINT`/`DEFSNG`/`DEFDBL`/`DEFSTR`. Different suffixes create distinct variables (`A%`, `A#`, `A$` are independent).
* Floating-point to `%` integer coercion rounds to nearest integer (`llround`) and raises Error `6` (`Overflow`) if out of 32-bit signed range.

### Numeric Literals
* **Decimal / Scientific:** `42`, `3.14`, `.5`, `1E5`, `2.5D-3` (optional suffix `%`, `!`, `#`).
* **Hexadecimal (`&H`), Octal (`&O` or `&0..7`), Binary (`&B`):**
  * Examples: `&HFF`, `&H1A0`, `&O77`, `&77`, `&B10110010` (optional trailing `%`).
  * **16-bit Base-Literal Sign-Extension Rule:** Base literals with `<= 4` digits in the range `0x8000..0xFFFF` sign-extend to `-32768..-1` (e.g., `&HFFFF` = `-1`, `&H8000` = `-32768`). Use 5+ digits (e.g., `&H0FFFF` = `65535`) for unsigned positive values.

### Arrays
* **Syntax:** `DIM name(d1[, d2...])[, ...]` and `ERASE name[, ...]`
* Both parentheses `A(i, j)` and brackets `A[i, j]` are accepted.
* **0-Based Inclusive:** `DIM A(10)` allocates 11 elements (`0` through `10`).
* **Auto-Dimensioning:** Using an undimensioned array auto-creates `0..10` per dimension. Redimensioning an existing array without `ERASE` raises Error `10` (`Redimensioned array`).

### Operators & Strict Precedence (Highest to Lowest)

| Prec. | Operators | Description & Notes |
| :---: | :--- | :--- |
| 1 | `( expr )`, Literals, Vars, Arrays, Functions | Primary expressions |
| 2 | `^` | Exponentiation (left-associative: `2^3^2 = 64`; binds tighter than unary `-`: `-2^2 = -4`, while `2^-2 = 0.25`) |
| 3 | `+`, `-` (unary) | Unary positive / negation |
| 4 | `*`, `/` | Multiplication, floating-point division (`/` by `0` → Error `11`) |
| 5 | `\`, `¥`, `￥`, `₩`, `＼` | Integer division (rounds operands to `int32`, truncates quotient toward zero) |
| 6 | `MOD` | Integer modulo (`a % b` on `int32`; divisor `0` → Error `11`) |
| 7 | `+`, `-` | Addition / Subtraction; `+` concatenates strings |
| 8 | `=`, `<>`, `><`, `<`, `>`, `<=`, `=<`, `>=`, `=>` | Numeric or lexicographical UTF-8 string comparison. **Returns `-1` (True) or `0` (False).** |
| 9 | `NOT` | Bitwise 32-bit NOT (`~a`). Lower precedence than comparisons (`NOT A = B` parses as `NOT (A = B)`). |
| 10 | `AND` | Bitwise 32-bit AND (`a & b`) |
| 11 | `OR` | Bitwise 32-bit OR (`a \| b`) |
| 12 | `XOR` | Bitwise 32-bit XOR (`a ^ b`) |
| 13 | `EQV` | Bitwise 32-bit equivalence (`~(a ^ b)`) |
| 14 | `IMP` | Bitwise 32-bit implication (`(~a) \| b`) |

---

## 2.3 Flow Control, Data & User Functions

| Statement | Syntax & Behavior |
| :--- | :--- |
| **`LET`** | `[LET] var = expr` / `[LET] arr(i1, ...) = expr` — Variable or array assignment (`LET` keyword is optional). |
| **`GOTO`** | `GOTO line` — Unconditional jump to `line` (Error `8` if undefined). |
| **`GOSUB`** | `GOSUB line` — Calls subroutine at `line`, pushing return PC onto call stack. |
| **`RETURN`** | `RETURN [line]` — Returns from `GOSUB` (or event interrupt) to caller, or jumps to `line` if specified (Error `3` if stack empty). |
| **`IF`** | `IF cond THEN stmt_or_line [: stmt...] [ELSE stmt_or_line [: stmt...]]` <br> `IF cond GOTO line [ELSE ...]` — True if `cond <> 0`. Supports nested `IF..THEN..ELSE`, multi-statement `:` chains, and bare line-number targets (`THEN 100 ELSE 200`). |
| **`FOR` / `NEXT`** | `FOR var = start TO limit [STEP step]` ... `NEXT [var1[, var2...]]` — Executes loop body at least once, increments `var` by `step` (default `1`), repeats while `var <= limit` (`step >= 0`) or `var >= limit` (`step < 0`). Comma-chained `NEXT J, I` supported. |
| **`ON..GOTO`** | `ON expr GOTO l1[, l2, ...]` — Evaluates `expr` (`0..255`; outside → Error `5`). If `1..N`, jumps to `l_expr`; if `0` or `> N`, falls through. |
| **`ON..GOSUB`** | `ON expr GOSUB l1[, l2, ...]` — Same selection rules as `ON..GOTO`, calling the target subroutine. |
| **`END` / `STOP`** | `END` closes all open files and halts VM (`status = 1`). `STOP` halts VM (`status = 1`). |
| **`SWAP`** | `SWAP a, b` or `SWAP(a, b)` — Swaps two variables or array elements of the **same type** (mismatch → Error `13`). |
| **`CLEAR`** | `CLEAR [str_space[, himem]]` — Closes all files, clears all variables, arrays, `DEF FN`, `DEF*` types (reset to `#`), stacks, event traps, and resets `DATA` pointer & `RND` seed. Optional arguments are evaluated and ignored. |
| **`DATA`** | `DATA item1[, item2, ...]` — Non-executable compile-time constant pool. Items may be quoted strings or unquoted text/numbers (including `&H`/`&O`/`&B`). |
| **`READ`** | `READ var1[, var2, ...]` — Reads next items from `DATA` pool into variables/arrays (Error `4` if exhausted). |
| **`RESTORE`** | `RESTORE [line]` — Resets `DATA` read pointer to start of program, or to first `DATA` at or after `line`. |
| **`DEF FN` / `FN`** | `DEF FNname[(p1[, p2...])] = expr` / `FNname[(a1[, a2...])]` (space after `FN` optional, e.g., `DEF FN SQ(X) = X*X`). Parameters bind in a **local scope** without clobbering global variables of the same name. Undefined call raises Error `18`. |

---

## 2.4 Timing, Speed Control & Event Interrupts

| Statement / Function | Syntax & Behavior |
| :--- | :--- |
| **`SPEED`** *(stmt)* | `SPEED n` (`0..10000`; outside → Error `5`) — Dynamically adjusts execution & virtual-frame speed (`0`=unlimited 12 ms slice, `50`=half speed, `100`=standard 60 fps, `300`=3x turbo). Mid-frame changes rescale the remaining frame budget immediately. |
| **`SPEED` / `SPEED()`** *(fn)* | Returns current `SPEED` setting (`0..10000`). |
| **`VSYNC`** | Yields the VM until the next virtual frame tick (1 real frame at `SPEED 0` or `100`). |
| **`WAIT`** | `WAIT [frames]` — Omitted, `0`, or `1` behaves like `VSYNC`. `frames >= 2` pauses execution for `frames` virtual frames (`< 0` → Error `5`). |
| **`TIME`** *(fn / stmt)* | `TIME` returns the 60 Hz tick counter (`0..65535`). `TIME = n` sets the counter (`n AND 65535`). |
| **`ON INTERVAL`** | `ON INTERVAL = ticks GOSUB line` (`ticks`: `0..65535`, 60 Hz ticks) — Registers periodic timer trap. |
| **`INTERVAL`** | `INTERVAL ON` (enable & start), `INTERVAL OFF` (disable & clear pending), `INTERVAL STOP` (suspend dispatch while latching pending events until `ON`). |
| **`ON SPRITE`** | `ON SPRITE GOSUB line` — Registers sprite collision trap (polled once per frame across all visible sprite pairs). |
| **`SPRITE` *(event)*** | `SPRITE ON` \| `SPRITE OFF` \| `SPRITE STOP` — Controls collision interrupt dispatch. |
| **`ON STRIG`** | `ON STRIG GOSUB [l0][, l1][, l2][, l3][, l4]` — Registers trigger rising-edge traps for ports `0..4`. |
| **`STRIG` *(event)*** | `STRIG[(port)] ON\|OFF\|STOP` — Controls trigger interrupt for `port` (`0..4`) or all 5 ports if omitted. |

*Interrupt traps are non-reentrant while inside their handler and re-arm automatically upon `RETURN`.*

---

## 2.5 Error Handling & Complete Error Codes Table

| Statement / Function | Syntax & Behavior |
| :--- | :--- |
| **`ON ERROR GOTO`** | `ON ERROR GOTO line` — Enables error trap (`line = 0` disables trapping; calling `ON ERROR GOTO 0` **inside** an error handler immediately re-raises the active error). |
| **`RESUME`** | `RESUME` or `RESUME 0` (retry faulting statement), `RESUME NEXT` (continue at next statement), `RESUME line` (jump to `line`). Calling outside a handler raises Error `22`. |
| **`ERROR`** | `ERROR code` (`1..255`) — Manually raises error `code`. |
| **`ERR` / `ERL`** | `ERR` returns last error code (`0` if none). `ERL` returns line number where the error occurred. |

### Error Code Table (`babka_core.h`)

| Code | Message | Code | Message | Code | Message |
| :---: | :--- | :---: | :--- | :---: | :--- |
| `1` | NEXT without FOR | `13` | Type mismatch | `25` | Line buffer overflow |
| `2` | Syntax error | `14` | Out of string space | `50` | Field overflow |
| `3` | RETURN without GOSUB | `15` | String too long | `51` | Internal error |
| `4` | Out of DATA | `16` | String formula too complex | `52` | Bad file number |
| `5` | Illegal function call | `17` | Can't continue | `53` | File not found |
| `6` | Overflow | `18` | Undefined user function | `54` | File already open |
| `7` | Out of memory | `19` | Device I/O error | `55` | Input past end |
| `8` | Undefined line number | `20` | Verify error | `56` | Bad file name |
| `9` | Subscript out of range | `21` | No RESUME | `57` | Direct statement in file |
| `10` | Redimensioned array | `22` | RESUME without error | `58` | Sequential I/O only |
| `11` | Division by zero | `23` | Unprintable error *(default)* | `59` | File not OPEN |
| `12` | Illegal direct | `24` | Missing operand | `61` | Bad file mode |

---

## 2.6 Text Console, Screen, Color & Font Commands

### Text Output & Cursor
* **`PRINT` / `?`:** `PRINT [expr][;|, expr...][;|,]`
  * `;` concatenates tightly and suppresses trailing newline when placed at end.
  * `,` advances to the next 14-column tab zone (or writes 14 spaces in `PRINT #n`).
  * Positive numbers print with a leading space and trailing space; negative numbers print `-` and trailing space.
* **`PRINT USING`:** `PRINT USING fmt$; expr[,|; expr...][;|,]`
  * Supported format specifiers:
    * `!` — First UTF-8 codepoint of string.
    * `@` — Entire string.
    * `& ... &` — Fixed-width string field (length = total chars including both `&`), truncated or right-padded with spaces by codepoints.
    * `#` — Numeric digit slot; `.` — Decimal point; leading `+` before `#` — Force explicit `+`/`-` sign.
    * Overflow prefixes the formatted number with `%`.
* **`SPC(n)`:** Returns `n` spaces (`0..255`; negative clamped to `0`, `> 255` → Error `5`).
* **`TAB(n)`:** Advances to column `n` (`0..255`) by returning spaces (`""` if already at or past `n`).
* **`CLS [mode]`:** `0` *(default)* = clear both Text VRAM & active Graphic page; `1` = Text VRAM only; `2` = active Graphic page only (`mode` `0` or `1` resets cursor to `0,0`).
* **`LOCATE [x][, y][, cursor_sw]`:** Moves text cursor to `(x, y)` (0-based, clamped to grid). Optional `cursor_sw`: `0` hides blinking cursor, `> 0` forces blinking cursor visible.
* **`WIDTH cols`:** Overrides text grid width (`1..255`, capped at `virt_w / cell_width`) and clears Text VRAM.
* **`POS(0)` / `CSRLIN`:** Returns current 0-based text cursor column (`POS(0)`, argument required) and row (`CSRLIN`).

### Console Input
* **`INPUT ["prompt";|,] var1[, var2...]`:** Non-blocking keyboard/IME line input. `;` prints `"? "` after prompt; `,` suppresses `"? "`. Multiple variables are comma-separated (quotes supported). Invalid numeric input prints `?Redo from start`; too few items prints `?? `.
* **`LINE INPUT ["prompt";|,] strvar$`:** Non-blocking single-line raw UTF-8 string input (preserves commas and quotes; no `"? "` appended; target must be string).
* **`INKEY$`:** Non-blocking; pops one queued keypress string (`""` if empty). Returns ASCII `32..126`, `CHR$(13)` Enter, `CHR$(27)` Esc, `CHR$(8)` Backspace, `CHR$(9)` Tab, `CHR$(28)` Right, `CHR$(29)` Left, `CHR$(30)` Up, `CHR$(31)` Down.
* **`INPUT$(n)`:** Waits non-blockingly until `n` (`1..65535`) keypress characters are accumulated, then returns them without echo.

### Screen, Color, Layer & USF Fonts
* **`SCREEN [mode][, spr_size][, overscan]`:** Sets mode (`0..4`), sprite size (`0..3`), and overscan (`0` or `1`). Changing `mode` clears all 4 graphic pages, resets pages/scroll/gcursor to `0`, resets `WIDTH` to auto, and clears Text VRAM.
* **`COLOR [fg][, bg][, border]`:** Sets active foreground, backdrop, and border colors (palette `0..255` or `RGB`/`RGBA`; omitted arguments stay unchanged). Bare `COLOR` resets the palette (same as `COLOR=NEW`).
* **`COLOR=(idx, r7, g7, b7)`:** Sets palette entry `idx` (`1..255`; `0` stays transparent) using 3-bit RGB (`0..7` per channel) and live-updates Graphic VRAM.
* **`COLOR=NEW` / `COLOR=RESTORE`:** Resets all 256 palette entries to default classic 15-color retro + GRB332 values and live-updates Graphic VRAM.
* **`PALETTE idx, r255, g255, b255`:** Sets palette entry `idx` (`1..255`) using full 8-bit RGB (`0..255` each) and live-updates Graphic VRAM.
* **`RGB(r, g, b)` / `RGBA(r, g, b, a)`:** Returns a 32-bit direct full-color `BabkaColor` (`r, g, b, a` clamped to `0..255`).
* **`LAYER mode`:** `0` = Text over Sprites (default), `1` = Sprites over Text.
* **`FONT slot, "file.json"`:** Loads a USF (Universal Sprite Font) manifest and its `_p0.png`..`_pN.png` pages into slot `0..15` (Error `53` if not found).
* **`FONT slot`:** Activates loaded font slot `0..15` (Error `5` if unloaded) and recalculates text grid dimensions without clearing Text VRAM.

---

## 2.7 Graphics VRAM & Drawing Commands

All drawing commands target the current `active_page` (`0..3`), preserve `pal_idx` for live palette swapping, and update the graphics cursor `(last_gx, last_gy)` used by `STEP`.

| Statement / Function | Syntax & Behavior |
| :--- | :--- |
| **`PSET`** | `PSET [STEP](x, y)[, color]` — Plots pixel at `(x, y)` (or relative offset with `STEP`). Default `color` = `fg_color`. |
| **`PRESET`** | `PRESET [STEP](x, y)[, color]` — Same as `PSET`, except default `color` = `bg_color`. |
| **`LINE`** | `LINE [[STEP](x1, y1)]-[STEP](x2, y2)[, color[, B\|BF]]` — Draws Bresenham line, box outline (`B`), or filled box (`BF`). Omitting start point starts from `(last_gx, last_gy)`. `STEP` on end point is relative to start point. |
| **`CIRCLE`** | `CIRCLE [STEP](x, y), r[, color[, start[, end[, aspect]]]]` — Draws circle/ellipse/arc/pie (`r >= 0`, `aspect > 0`, angles in radians; negative `start`/`end` draws radius line to center). |
| **`PAINT`** | `PAINT [STEP](x, y)[, fill_color[, border_color]]` — Non-recursive queue-BFS scanline flood fill (stack-safe). If `border_color` is omitted, fills contiguous pixels matching the seed pixel's color. |
| **`POINT(x, y)`** | Returns the `BabkaColor` (palette `0..255` or 32-bit direct color) at `(x, y)` on `active_page` (`0` if out of bounds). |
| **`COPY`** | `COPY (x1, y1)-(x2, y2)[, src_page] TO (dx, dy)[, dst_page]` — Copies rectangular pixel region safely (overlap-safe via temp buffer). Omitted `src_page` uses `active_page`; omitted `dst_page` uses `src_page`. |
| **`SET PAGE`** | `SET PAGE [disp_page][, active_page]` — Selects displayed page (`0..3`) and drawing target page (`0..3`) for double buffering. |
| **`SET SCROLL`** | `SET SCROLL [x][, y]` — Sets wraparound pixel scroll offset of the Graphic VRAM layer. Pass non-negative values (`>= 0`; negative values leave that axis unchanged). |
| **`GRPPRINT`** | `GRPPRINT [STEP](x, y), expr[, color]` — Rasterizes UTF-8 text (using active USF font) directly into Graphic VRAM pixels (palette-swap aware). Advances `last_gx` to end of string. |
| **`DRAW`** | `DRAW str$` — Executes the classic vector turtle-graphics macro language (max `X` macro nesting depth `16`). |

### `DRAW` Macro Language Reference

| Command | Action |
| :--- | :--- |
| `U[n]`, `D[n]`, `L[n]`, `R[n]` | Move/draw Up, Down, Left, Right by `n` (default `1`), scaled by `scale / 4` and rotated by `A`. |
| `E[n]`, `F[n]`, `G[n]`, `H[n]` | Diagonal moves: `E`=Up-Right, `F`=Down-Right, `G`=Down-Left, `H`=Up-Left. |
| `M[+\|-]x,y` | Move/draw to absolute `(x, y)`, or relative `(dx, dy)` scaled by `scale / 4` when prefixed with `+`/`-`. |
| `B` | Prefix: Blank (move graphics cursor without drawing next move command). |
| `N` | Prefix: No-update (draw next move command, then restore graphics cursor). |
| `C n` | Set active foreground drawing color (`0..255` or variable via `C=var;`). |
| `S n` | Set scale factor (`1..255`, default `4` = 1.0x; `n/4`). |
| `A n` | Set rotation angle (`0`=0°, `1`=90° CCW, `2`=180°, `3`=270° CCW). |
| `=var;` | Substitute integer value of numeric variable `var` for any argument (e.g., `R=LEN;`). |
| `Xvar$;` | Execute substring macro stored in string variable `var$` (recursive up to depth `16`). |

---

## 2.8 Sprites (64 Planes, 256 Patterns)

* **Planes:** `0..63` (Plane `0` has highest visual priority / drawn in front; Plane `63` is furthest back).
* **Patterns:** `0..255` 8x8 blocks (`1` bit per pixel, MSB `0x80` = leftmost pixel).
* **`SPRITE$(pat) = str$`:** *(Write-only statement)* Defines sprite pattern `pat` (`0..255`):
  * **8x8 Modes (`spr_size = 0, 1`):** 8 characters (`CHR$(b0)..CHR$(b7)`), 1 byte per row top-to-bottom.
  * **16x16 Modes (`spr_size = 2, 3`):** 32 characters (`pat` `0..63` maps to 4 consecutive 8-byte blocks `pat*4 .. pat*4+3` in a 4-quadrant 16x16 sprite layout):
    ```text
    +--------------+--------------+
    | Bytes  0.. 7 | Bytes 16..23 |  Rows  0.. 7
    | (Top-Left)   | (Top-Right)  |
    +--------------+--------------+
    | Bytes  8..15 | Bytes 24..31 |  Rows  8..15
    | (Bot-Left)   | (Bot-Right)  |
    +--------------+--------------+
    ```
* **`COLOR SPRITE(plane) = col`:** Sets solid color (`0..255` or `RGB`/`RGBA`) for `plane` (`0..63`) and disables per-row color mode.
* **`COLOR SPRITE$(plane) = str$`:** Sets per-row palette colors (up to 16 chars for rows `0..15`). Low nibble (`byte AND &H0F`) selects palette `0..15`; setting Early Clock bit `&H80` on row 0 shifts sprite X left by 32 pixels.
* **`PUT SPRITE plane, [STEP](x, y)[, col][, pat]`:**
  * Positions/updates `plane` (`0..63`). Coordinates, `col`, and `pat` are individually optional (`PUT SPRITE 0, , 8` changes only color).
  * Passing `col` disables per-row `COLOR SPRITE$` mode.
  * Setting `y = 208` or `y <= -256` hides the sprite; any other `y` makes it visible.
* **`SPRITE HIDE plane`:** Explicitly hides `plane` (`0..63`) and sets `y = 208`.
* **`SPRITEHIT(a, b)`:** Returns `-1` if visible sprite planes `a` and `b` (`0..63`, `a <> b`) have overlapping bounding boxes (using active sprite pixel size `8`, `16`, or `32`), else `0`.

---

## 2.9 Input Devices

### `STICK(port)` (`port`: `0..2`)
Returns an 8-way direction code `0..8`:

```text
   8   1   2        0 = Center (neutral)
    \  |  /         1 = Up       5 = Down
  7 -- 0 -- 3       2 = Up-Right 6 = Down-Left
    /  |  \         3 = Right    7 = Left
   6   5   4        4 = Dn-Right 8 = Up-Left
```

| Port | Input Source |
| :---: | :--- |
| `0` | Keyboard: Arrow keys, `WASD`, or Numpad `8/2/4/6` |
| `1` | Gamepad 1: D-Pad or left analog stick (`±0.4` deadzone) |
| `2` | Always returns `0` (TinCLE supports 1 gamepad) |

### `STRIG(port)` (`port`: `0..4`)
Returns `-1` while pressed, `0` when released.

| Port | Input Source |
| :---: | :--- |
| `0` | Keyboard: `Space`, `Z`, or `Enter` |
| `1` | Gamepad 1: Button A (button index `0`) |
| `3` | Gamepad 1: Button B (button index `1`) |
| `2`, `4` | Always returns `0` (Gamepad 2 unsupported) |

### Mouse & `PAD(n)` (`n`: `0..19`)
All mouse coordinates are automatically inverse-mapped from physical window coordinates into virtual canvas pixels (`0..virt_w-1`, `0..virt_h-1`).
* **`MOUSEX` / `MOUSEY`:** Current virtual X / Y pixel coordinates.
* **`MOUSEB`:** Button bitmask — bit 0 (`1`) = Left, bit 1 (`2`) = Right, bit 2 (`4`) = Middle.
* **`PAD(n)`:** Legacy PAD/mouse bridge (groups `0..3`, `4..7`, `8..11`, `12..15`, `16..19`): `n MOD 4 = 0` → `-1` (present), `1` → `MOUSEX`, `2` → `MOUSEY`, `3` → `-1` if Left button pressed else `0`.

---

## 2.10 Audio & 12-Channel MML Reference

### Direct PSG & BEEP
* **`BEEP`:** Triggers a classic ~1200 Hz (~62 ms) tone on PSG Ch. 1.
* **`SOUND reg, val`:** Writes `val` (`0..255`) directly to AY-3-8910 PSG register `reg` (`0..15`):

| Reg | Function | Reg | Function |
| :---: | :--- | :---: | :--- |
| `0, 1` | Ch. 1 Tone Period (12-bit: R0 low, R1[3:0] high) | `7` | Mixer Enable (`0`=ON, `1`=OFF; bits 0..2 Tone A..C, bits 3..5 Noise A..C; default `&HB8`) |
| `2, 3` | Ch. 2 Tone Period (12-bit) | `8, 9, 10` | Ch. 1..3 Volume (`0..15`, or `16` = Hardware Envelope) |
| `4, 5` | Ch. 3 Tone Period (12-bit) | `11, 12` | Hardware Envelope Period (16-bit) |
| `6` | Noise Period (5-bit: `0..31`) | `13` | Hardware Envelope Shape (`0..15`) |

*Period formula:* `period = INT(111861 / freq_hz)` (clamped `1..4095`).

### 12-Channel Background MML (`PLAY`)
* **`PLAY [#mode,] ch1$[, ch2$ ... , ch12$]`:** Starts asynchronous background MML playback on up to 12 channels simultaneously.
  * **Channels 1–3:** PSG (`emu2149`)
  * **Channels 4–12:** YM2413 (OPLL) FM (`emu2413`, 9 melodic channels)
  * Omitted / empty strings (`PLAY , , "O6L32CEG"`) leave other channels untouched!
  * Optional `#mode,` prefix (e.g., `PLAY #2, ...`) is accepted for legacy multi-channel syntax compatibility.
* **`PLAY(ch)`:** Returns `-1` if playing, `0` if finished (`ch = 0` checks if **any** of channels 1–12 is playing; `ch = 1..12` checks that specific channel).
* **`PLAY STOP`:** Immediately stops all 12 MML channels, silences PSG/FM key-on, and flushes queued WebAudio nodes.

### Supported MML Commands (Case-Insensitive)

| Command | Range / Default | Description |
| :--- | :--- | :--- |
| `A`..`G` [`#`\|`+`\|`-`][len][`.`...][`&`] | `len`: `1..64` | Play note (`#`/`+` sharp, `-` flat, `.` dot = 1.5x, `..` = 1.75x, `&` ties seamlessly into next note). |
| `R`[len][`.`...] / `P`[len][`.`...] | `len`: `1..64` | Rest (silences channel for duration). |
| `N`n | `0..96` | Absolute note number (`N0`=rest, `N1`=`O1C` .. `N96`=`O8B`, uses default `L`). |
| `L`n | `1..64` (def `4`) | Set default note/rest length (`1`=whole, `4`=quarter, `8`=eighth, `16`=sixteenth, etc.). |
| `O`n | `1..8` (def `4`) | Set base octave (`O4 A` = 440 Hz). |
| `>` / `<` | `O1..O8` | Shift base octave up (`>`) or down (`<`) by 1. *(Always balance `>` and `<`!)* |
| `T`n | `32..255` (def `120`) | Set channel tempo in BPM. |
| `V`n | `0..15` (def `12`) | Set channel volume (clears PSG envelope mode). |
| `@V`n | `0..127` | Fine volume alias (linearly scaled to `0..15`). |
| `@`n | `0..63` | Select FM OPLL voice (Ch. 4–12). `@1..15` select built-in patches; `@0` maps to `@3` (Piano); `@16..63` wrap via `(n MOD 15) + 1`. Defaults: Ch.4=`@3`, Ch.5=`@1`, Ch.6=`@13`, Ch.7–12=`@3`. |
| `Q`n | `1..8` (def `8` PSG, `7` FM) | Gate ratio (`n/8` of note duration sounded before key-off; `Q8` = legato, `Q4` = staccato). |
| `S`n | `0..15` | Enable PSG hardware envelope with shape `n` (writes PSG R13; Ch. 1–3 only). |
| `M`n | `1..65535` | Set PSG hardware envelope period (writes PSG R11/R12; Ch. 1–3 only). |
| `[ ... ]`n | `n >= 1` (def `2`) | Repeat enclosed MML phrase `n` times (supports nesting). |
| `Xvar$;` / `=var;` | Depth `<= 16` | Macro expansion: inserts string variable `var$` or integer value of `var` before playback. |

#### Built-in YM2413 (OPLL) FM Voices (`@1`..`@15`)

| `@` | Instrument | `@` | Instrument | `@` | Instrument |
| :---: | :--- | :---: | :--- | :---: | :--- |
| `@1` | Violin | `@6` | Oboe | `@11` | Harpsichord |
| `@2` | Guitar | `@7` | Trumpet | `@12` | Vibraphone |
| `@3` | Piano | `@8` | Organ | `@13` | Synth Bass |
| `@4` | Flute | `@9` | Horn | `@14` | Acoustic Bass |
| `@5` | Clarinet | `@10` | Synthesizer | `@15` | Electric Guitar |

### TinCLE Digital Audio Bridge
* **`BGMPLAY "file.ogg"`:** Loops streaming OGG/WAV BGM via TinCLE (`tincle_play_music`).
* **`BGMSTOP`:** Stops TinCLE streaming BGM (`tincle_stop_music`).
* **`SEPLAY "file.wav"`:** Loads (cached by filename) and plays a 44.1 kHz one-shot sound effect via TinCLE (`tincle_load_sound` / `tincle_play_sound`).

---

## 2.11 Sequential File I/O

| Statement / Function | Syntax & Behavior |
| :--- | :--- |
| **`OPEN`** | `OPEN "filename" [FOR INPUT\|OUTPUT\|APPEND] AS [#]n` (`n`: `1..16`). Defaults to `OUTPUT` if `FOR` omitted. Strips optional legacy drive prefixes (e.g., `"A:"`, `"MEM:"`). `INPUT` raises Error `53` if missing; `APPEND` creates a new file if missing. |
| **`PRINT #n`** | `PRINT #n, [USING fmt$;] expr...` — Writes formatted text to an `OUTPUT`/`APPEND` handle. |
| **`INPUT #n`** | `INPUT #n, var1[, var2...]` — Reads comma/newline-delimited items (supports quoted strings) from an `INPUT` handle (Error `55` at EOF). |
| **`LINE INPUT #n`** | `LINE INPUT #n, strvar$` — Reads one full line (stripping `\r\n` / `\n`) into a string variable. |
| **`INPUT$(cnt, #n)`** | Reads exactly `cnt` UTF-8 codepoints from an `INPUT` handle (Error `55` if fewer remain). |
| **`EOF(n)`** | Returns `-1` if `INPUT` handle `n` has reached end-of-file (ignoring trailing `\r`/`\n`), else `0`. |
| **`CLOSE`** | `CLOSE [[#]n[, [#]m...]]` — Flushes `OUTPUT`/`APPEND` handles to persistent storage (Windows disk / Web IndexedDB) and closes specified handles (or all open handles if omitted). `END` also auto-closes all open handles. |

---

## 2.12 Built-in Math, String & Conversion Functions

### Math & Numeric Conversion
| Function | Behavior & Notes |
| :--- | :--- |
| `ABS(x)` | Absolute value. |
| `INT(x)` | Floor (largest integer `<= x`, e.g., `INT(-1.2) = -2`). |
| `FIX(x)` | Truncate toward zero (e.g., `FIX(-1.2) = -1`). |
| `SGN(x)` | Sign: `1` (`x > 0`), `0` (`x = 0`), `-1` (`x < 0`). |
| `SQR(x)` | Square root (`x < 0` → Error `5`). |
| `RND(x)` | Pseudo-random in `[0, 1)`. `x > 0`: next random; `x = 0`: repeat last value; `x < 0`: deterministically reseed from `x`. |
| `SIN(x)`, `COS(x)`, `TAN(x)`, `ATN(x)` | Trigonometric functions in radians. |
| `EXP(x)`, `LOG(x)` | Natural exponential `e^x` (overflow → Error `6`) and natural logarithm `ln(x)` (`x <= 0` → Error `5`). |
| `CINT(x)` | Round to 32-bit signed integer `%` (out of `int32` range → Error `6`). |
| `CSNG(x)` / `CDBL(x)` | Convert to single precision `!` (`float`) or double precision `#` (`double`). |

### String & Base Conversion (All UTF-8 Codepoint Safe)
| Function / Statement | Behavior & Notes |
| :--- | :--- |
| `LEN(s$)` | Number of Unicode codepoints in `s$`. |
| `LEFT$(s$, n)` / `RIGHT$(s$, n)` | Leftmost / rightmost `n` codepoints (`n < 0` → Error `5`). |
| `MID$(s$, start[, n])` *(fn)* | Substring starting at 1-based codepoint `start` for `n` codepoints (or to end if `n` omitted; `start < 1` or `n < 0` → Error `5`). |
| `MID$(var$, start[, n]) = repl$` *(stmt)* | In-place codepoint replacement inside string variable or array element without changing total length (`start < 1` or `> LEN(var$)` → Error `5`). |
| `INSTR([start,] hay$, needle$)` | 1-based codepoint index of `needle$` in `hay$` starting at `start` (`1..65535`, default `1`), or `0` if not found. |
| `CHR$(cp)` | Encodes Unicode codepoint `cp` (`0..&H10FFFF`, outside → Error `5`) to UTF-8 string. |
| `ASC(s$)` | Returns Unicode codepoint of first character (`s$ = ""` → Error `5`). |
| `STR$(x)` | Converts number to string (leading space for non-negative, `-` for negative). |
| `VAL(s$)` | Parses decimal, scientific, `&H`, `&O`, or `&B` prefix string to number (`0` if non-numeric). |
| `HEX$(n)`, `OCT$(n)`, `BIN$(n)` | Converts integer `-32768..65535` to uppercase hexadecimal / octal / binary string without prefix (outside → Error `6`). |
| `SPACE$(n)` | Returns `n` spaces (`0..65535`). |
| `STRING$(n, ch$\|cp)` | Repeats first codepoint of `ch$` or codepoint `cp` `n` times (`0..65535`). |

---

## 2.13 Complete Minimal Game Example (`AUTOEXEC.BAS`)

```basic
10 REM === MINIMAL ORB ARCADE EXAMPLE ===
20 DEFINT A-Z
30 SCREEN 1, 1, 0 : COLOR 15, 1, 4 : CLS : LAYER 0
40 HI = 100 : ON ERROR GOTO 70
50 OPEN "STAR_HI.DAT" FOR INPUT AS #1 : INPUT #1, HI : CLOSE #1 : GOTO 80
70 RESUME 80
80 ON ERROR GOTO 0
90 LINE (4, 16)-(251, 175), 5, B : PAINT (128, 96), 4, 5
100 GRPPRINT (64, 24), "ORB STAR CATCHER", 15
110 RESTORE 500
120 P0$ = "" : FOR I = 0 TO 7 : READ B : P0$ = P0$ + CHR$(B) : NEXT I : SPRITE$(0) = P0$
130 P1$ = "" : FOR I = 0 TO 7 : READ B : P1$ = P1$ + CHR$(B) : NEXT I : SPRITE$(1) = P1$
140 PX = 120 : PY = 100 : SX = 60 : SY = 60 : SC = 0 : PTRG = 0
150 M1$ = "T150@3V13Q7O5L8 [C E G >C< G E]2"
160 M2$ = "T150@13V12Q6O3L4 [C G F G]2"
170 PLAY , , , M1$, M2$
200 REM === MAIN 60FPS GAME LOOP ===
210 IF PLAY(4) = 0 THEN PLAY , , , M1$, M2$
220 ST = STICK(0)
230 IF ST = 1 OR ST = 2 OR ST = 8 THEN PY = PY - 2
240 IF ST = 4 OR ST = 5 OR ST = 6 THEN PY = PY + 2
250 IF ST = 6 OR ST = 7 OR ST = 8 THEN PX = PX - 2
260 IF ST = 2 OR ST = 3 OR ST = 4 THEN PX = PX + 2
270 IF PX < 8 THEN PX = 8 ELSE IF PX > 232 THEN PX = 232
280 IF PY < 20 THEN PY = 20 ELSE IF PY > 156 THEN PY = 156
290 TRG = STRIG(0) : IF TRG AND NOT PTRG THEN COLOR=(4, 1, 4, 5)
295 PTRG = TRG
300 PUT SPRITE 0, (PX, PY), 11, 0
310 PUT SPRITE 1, (SX, SY), 10, 1
320 IF SPRITEHIT(0, 1) THEN PLAY , , "T240V14O6L32CEG>C<" : SC = SC + 50 : SX = 20 + INT(RND(1) * 200) : SY = 32 + INT(RND(1) * 116) : IF SC > HI THEN HI = SC : GOSUB 400
330 LOCATE 0, 0 : PRINT USING "SCORE:#####  HI:#####  SPD:####"; SC, HI, SPEED;
340 VSYNC
350 GOTO 210
400 OPEN "STAR_HI.DAT" FOR OUTPUT AS #1 : PRINT #1, HI : CLOSE #1 : RETURN
500 DATA &H18,&H3C,&H7E,&HDB,&HFF,&H7E,&H24,&H42
510 DATA &H18,&H18,&H7E,&HFF,&HFF,&H7E,&H18,&H18
```
