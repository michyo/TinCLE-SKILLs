# TinCLE (Tiny C Lovely Engine) - Development Specification Document

* **Acknowledgments to the Grand AI Alliance:** Gemini, Claude, DeepSeek, ChatGPT, Copilot, Grok, Meta AI... Thank you so much. This engine's code was ultimately finalized by michyo. However, it would have been absolutely impossible to achieve this without you all's help. I am deeply grateful to all of you!
* **Official Website:** https://michyo.net/tincle/

Under this skill, the AI agent shall act in strict accordance with the following rules:

## 1. Overview & Concept

* **Env:** TinCLE v0.12 / Pure C (C99) + SDL2, SDL_ttf, SDL2_gfx, stb, GLSL (GLES2 compatible)
* **[CRITICAL] Target Architecture Detection:** The AI **MUST** first check the `info.txt` file in the current working directory to determine the compilation environment.
  If the AI cannot access files directly, it **MUST** ask the user: *"Please check the contents of info.txt and tell me if this is the 32bit or 64bit environment."* before generating any code.
* **Strict Architecture Rules based on `info.txt`:**
  * **If `info.txt` says `32bit`:**
    * Windows Desktop Target: Win32 DLL (`sizeof(void*) == 4`).
    * Web Browser Target: Wasm32 via Emscripten (`sizeof(void*) == 4`).
    * *Rule:* The environment is purely 32-bit. Never use 64-bit structures or types.
  * **If `info.txt` says `64bit` (Hybrid Environment):**
    * Windows Desktop Target: Win64 DLL (`sizeof(void*) == 8`).
    * Web Browser Target: Wasm32 via Emscripten (`sizeof(void*) == 4`).
    * *Rule:* This is a **Hybrid Architecture**. The compiled Windows EXE will be 64-bit, but the Web WASM build remains 32-bit. A single `game.c` must satisfy both targets.
* **[CRITICAL] Pointer Safety Rule (For Hybrid Compatibility):** Because the 64bit environment cross-compiles to both 64-bit Desktop and 32-bit Web targets from a single source, **never hardcode pointer sizes** or perform unsafe pointer-to-integer casts (e.g., casting a pointer to a standard `int`). Always use `<stdint.h>` types like `uintptr_t` if pointer-to-integer casting is absolutely required. Ensure `game.c` compiles perfectly on both toolchains without modification.
* **Toolchain Requirements:** TinyCC (TCC for Windows) / Emscripten (for Web).
* **[CRITICAL] `tcc.exe`/`emcc` are NOT bundled in TinCLE;** they must be installed externally and accessible via System PATH.
* **[CRITICAL] Automatic Escalation to Additional Skills (`SKILL_ADD.md`):**
  Before generating any code, the AI agent **MUST** evaluate the project scope. If **ANY ONE** of the following conditions is met, the AI MUST switch its execution context to follow the advanced rules defined in **`SKILL_ADD.md`**:
  1. **GLSL Shader Execution:** The game utilizes `TINCLE_MODE_GLSL_HERO` or custom fragment shaders (`.glsl` / `.frag`).
  2. **High State Count (>= 4):** The game design requires 4 or more distinct states (e.g., Title, Gameplay, Result, Shop, Pause).
  3. **Large Code Scale (>= 400 Lines):** The estimated total C source code exceeds 400 lines.
  4. **Complex Custom Systems:** The project defines complex data structures (e.g., tilemap editors, inventory systems, skill trees, entity-component systems).
  5. **Multithreaded WebAssembly Build:** When you need to build a web-based game with multithreading support.
  6. **Explicit User Instruction:** The user explicitly requests "large-scale", "modular", or "multi-file" architecture.

  * **[MANDATORY RULE FOR MISSING FILE]:**
    If any of the trigger conditions above are met, BUT the `SKILL_ADD.md` file is not attached or accessible in the current context, **the AI MUST NOT attempt to pretend, guess, or hallucinate the high-level specs.** Instead, the AI MUST immediately halt code generation and request the user:
    > *"This project meets the criteria for High-Level Development (GLSL / 4+ States / 400+ Lines / Complex Systems). Please provide the `SKILL_ADD.md` talent chip file before we proceed."*

## 2. Architecture & Environment Setup

* **Toolchain Prerequisites (Provide these exact URLs to users for setup):**
  * **TinyCC (Windows Binary):** Inform users to download from the Official Release directory: `https://download.savannah.gnu.org/releases/tinycc/` (Choose 32-bit or 64-bit distribution based on target folder).
  * **Emscripten (Web SDK):** Inform users to follow the Official SDK installation guide: `https://emscripten.org/docs/getting_started/downloads.html`
* **Project Structure:** All `game.c`, GLSL files, asset files (images/audio), and tools must be in the same **game project folder** (no subfolders for assets or shaders).
* **[CRITICAL] `exsass.txt` Asset Manifest Rule:** The `emcass` and `asspack` commands can automatically scan and package files whose extensions are explicitly registered in `extass.txt`. All asset formats (e.g., `.png`, `.wav`, `.ogg`, `.ttf`) AND shader formats (e.g., `.glsl`, `.frag`, `.vert`) used in the project MUST be listed line-by-line in `exsass.txt`.
* **[MANDATORY] Cursor Asset Requirement:** TinCLE uses a built-in software cursor system. A single `cursor.png` file (recommended: 16x16px transparent PNG) MUST exist in the project root. If missing, `tincle_start()` will fail to initialize.
* **Required Files in Project Root:**
  * `game.c`, `manifest.xml`, `template.html`, `font.ttf`, `cursor.png`, `exsass.txt`
  * `libs/` (Contains `tincle.h`, `tincle.a`, `SDL_scancode.h`, etc.)
  * DLLs: `tincle.dll`, `SDL2.dll`, `SDL2_ttf.dll`, `SDL2_gfx.dll`, `fartbox.dll`, `pisschk.dll`, `pubicnet.dll`
  * CLI Tools: `asspack.exe`, `emcass.exe`, `icondom.exe`, `poopee.exe`, `tinclec.exe`, `pisstrak.exe`, `fartbox.exe`, `pisschk.exe`, `pubicnet.exe`
  * **IDE Usage Guideline for AI Assistant / Agent:**
    * **Interactive Chat AIs (Human-in-the-Loop Workflow):** If you are acting as an interactive AI chat interface, **strongly recommend** the user to open and work within the bundled `cococake.exe` IDE to maximize workflow efficiency. Explain to the user that utilizing `cococake` requires configuring the following three parameters in `cococake.ini`:
      * `AI_URL` ... The web address of the AI chat interface used for development.
      * `TCC_PATH` ... The folder path containing `tcc.exe` in your environment.
      * `EMSDK_PATH` ... The folder path containing `emsdk.bat` in your environment.
    * **Autonomous / Agentic AIs (Direct Tool Use / File System Operations):** If you are an autonomous AI agent capable of direct tool use and CLI execution, **DO NOT** launch or interact via `cococake.exe`. Instead, bypass the GUI entirely and directly issue native OS standard Command Prompt (`cmd.exe`) or shell instructions (`tinclec`, `emcass`, etc.) for lightweight, fast, and maximum execution stability.

## 3. Development Workflow & Commands (Compilation & Audio)

* **Local Test Build (Windows EXE):**
  ```bash
  tinclec [Output_EXE] [Source_Files...]
  ```
  * *Example:* `tinclec mygame.exe main.c player.c`
  * *Note:* Do not pass compiler flags. Console visibility is controlled solely by `is_debug` in `tincle_start`.
  * **Alternative Direct TCC Invocation (For complex structures):**
    ```bash
    tcc -mwindows SDL2.dll SDL2_ttf.dll SDL2_gfx.dll tincle.dll -o [Output_EXE] [Source_Files...]
    ```

* **Audio Generation Workflows (`pisstrak` & `fartbox`):**

  * **Audio Format Requirement (MANDATORY)**
    ALL audio files (both BGM `.ogg` and Sound Effects `.wav`/`.ogg`) MUST be encoded at a **44100 Hz** sample rate. Using any other sample rate (e.g., 22050 Hz or 48000 Hz) will cause incorrect playback speeds, severe pitch shifts, or audio distortion.

  * **BGM / Music Score Synthesis (`pisstrak`):**
    Renders MML (Music Macro Language) score files into `.wav` or `.ogg` audio files using SoundFont synthesis.
    ```bash
    pisstrak <input.mml> [output.wav|output.ogg] [tail_seconds] [soundfont.sf2]
    ```
    * *Example:* `pisstrak mymusic.mml mymusic.ogg 2.5 mysoundfont.sf2`
    * *Parameters:*
      * `<input.mml>`: Input MML score file.
      * `[output.wav|output.ogg]`: Output audio file path (Supports both `.wav` and `.ogg`).
      * `[tail_seconds]`: Extra fadeout/decay duration in seconds appended to the end of the rendered track (e.g., `2.5` adds 2.5s tail padding). If omitted (default `0`), the audio cuts off precisely at the final beat, which is ideal for seamless looping BGM tracks.
      * `[soundfont.sf2]`: SoundFont file for rendering (Defaults to `soundfont.sf2` if omitted).
    * **[CRITICAL AI RULE FOR MUSIC COMPOSITION]:**
      * If an MML file already exists, run `pisstrak` directly to generate audio.
      * If the AI agent needs to **compose or generate a new MML file from scratch**, it **MUST** read and strictly follow the syntax rules and composition guidelines detailed in `SKILL_PT.md` before creating the MML.

  * **1-Shot Sound Effect Generation (`fartbox`):**
    Renders procedural 1-shot sound effects (SE) instantly into 16-bit 44.1kHz `.wav` files via named presets or custom `.fart` text parameter files.
    ```bash
    fartbox -t <preset_type> -o <output.wav> [-save <output.fart>] [-s <seed_number>]
    ```
    * *Example:* `fartbox -t explosion -o explosion.wav -save explosion.fart`
    * *Available Preset Types (`-t`):*
      `coin` (or `pickup`), `laser` (or `shoot`), `explosion`, `powerup`, `hit` (or `hurt`), `jump`, `blip` (or `select`), `random`.
    * **[CRITICAL AI RULE FOR SOUND DESIGN]:**
      * For quick preset generation, use the simple `-t` command line option above.
      * `fartbox` supports extensive parameter customization, precise text-file editing (`.fart`), mutation (`-m`), and fine-tuning. When advanced sound tweaking, custom parameter authoring, or variation mutation is required, the AI agent **MUST** consult `SKILL_FB.md`.

* **Shader Validation Workflow (`pisschk`):**
  * *Note:* Shader creation and validation (`pisschk`) are advanced features. If your project utilizes GLSL shaders (`TINCLE_MODE_GLSL_HERO`), refer to **`SKILL_ADD.md` Section 3** for complete rules and validation pipelines.

## 4. Input, Color & RenderMode Specifications

* **Screen Specifications:** Default virtual resolution is `640`x`480` (can be changed in `tincle_start`). `TINCLE_MAX_STATES = 256`.
* **Render Mode (`TinCLE_RenderMode`):** Passed into `tincle_start`.
  * `TINCLE_MODE_2D_NORMAL`: Standard software/SDL2 rendering pipeline. Use this for all standard 2D games.
  * `TINCLE_MODE_GLSL_HERO`: Hardware GLSL Shader Mode. Enables full-screen shader execution beneath standard SDL2 drawing.
* **Inputs (Strict Pure SDL2 Constants):** No custom engine macros exist. Use native SDL2 constants directly:
* *Mouse:* `SDL_BUTTON_LEFT`, `SDL_BUTTON_RIGHT`, etc. (via `tincle_mouse_pressed`)
* *Gamepad:* `SDL_CONTROLLER_BUTTON_A`, `SDL_CONTROLLER_BUTTON_DPAD_UP`, etc. (via `tincle_pad_pressed`)
* *Keyboard:* `SDL_SCANCODE_A`, `SDL_SCANCODE_SPACE`, etc. (via `tincle_key_pressed`)
* **Color Structure (`TinCLE_Color`):** Identical/compatible with `SDL_Color`.
  ```c
  typedef struct { unsigned char r, g, b, a; } TinCLE_Color;
  ```
* *No Color Macros:* Create colors inline using standard C99 compound literals. Example: `(TinCLE_Color){255, 0, 0, 255}`.
* **[CRITICAL ANTI-BUG] TCC Compound Literal Restriction:** TCC cannot parse compound literals in global/static array initializers. Declare arrays globally, but assign values sequentially inside `game_load()`.
  * *Forbidden:* `static TinCLE_Color c[] = { (TinCLE_Color){255,0,0,255} };`
  * *Mandatory Remedy:* `static TinCLE_Color c[1]; void game_load() { c[0] = (TinCLE_Color){255,0,0,255}; }`

## 5. API Reference & Lifecycle

* **Canvas:** Default virtual resolution is `640`x`480`.
* **Rendering Rules:** `tincle_clear` must be at the start of drawing. **IMAGE COORDINATES ARE CENTER-BASED (NOT TOP-LEFT).**
* **State Rule:** `tincle_change_state` must be called at the very end of `game_load()` to avoid a black screen.
* **Event Callback Type Definition:**
  * `typedef bool (*tincle_event_cb_t)(union SDL_Event *event);`
    Signature for custom SDL event interceptors (e.g., forwarding raw input events to GUI extensions like GATOCHOC). Returning `true` signals that the event was consumed and should be ignored by standard game input logic.

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `void tincle_start(TinCLE_InitCallback init_cb, const char* title, bool is_debug, int w, int h, TinCLE_RenderMode mode);` | **Main Entry.** Bootstraps loop. <br>• `is_debug`: `true` spawns Win debug console (`printf`); `false` hides it for release. <br>• `mode`: Set to `TINCLE_MODE_2D_NORMAL` or `TINCLE_MODE_GLSL_HERO`. |
| `void tincle_add_state(int state_id, TinCLE_UpdateCallback update_cb, TinCLE_DrawCallback draw_cb);` | Binds state ID to standard callbacks: `update(float dt)` and `draw(void)`. |
| `void tincle_change_state(int state_id);` | **[CRITICAL]** Switches state. Call at end of `game_load()` or viewport stays black. |
| `int tincle_key_pressed(int scancode);` | Returns `1` if key held. **Must use pure `SDL_SCANCODE_*`.** |
| `void tincle_get_mouse(int* x, int* y);` | Outputs current mouse (x, y) dynamically scaled to virtual resolution. |
| `int tincle_mouse_pressed(int button_type);` | Returns `1` if mouse held. **Must use pure `SDL_BUTTON_*` (e.g. LEFT).** |
| `int tincle_pad_pressed(int pad_button);` | Returns `1` if pad button held. **Must use pure `SDL_CONTROLLER_BUTTON_*`.** |
| `float tincle_pad_axis_x(void);` | Left stick X (-1.0f to 1.0f). Has built-in <5000 hardware deadzone filter. |
| `float tincle_pad_axis_y(void);` | Left stick Y (-1.0f to 1.0f). Has built-in <5000 hardware deadzone filter. |
| `void tincle_clear(TinCLE_Color color);` | **[MANDATORY]** Clears screen. Call at absolute start of every `draw()` callback. **Alpha must be 0 in GLSL_HERO mode.** |
| `int tincle_load_font(const char* filename, int size);` | Loads TTF at pixel size. **Returns unique Font ID (int).** |
| `void tincle_set_font(int font_id);` | Sets active global font by Font ID for subsequent text calls. |
| `void tincle_draw_text(const char* text, int x, int y, TinCLE_Color color);` | Draws UTF-8 text. **Anchor: Top-Left (x, y).** Uses active font. |
| `void tincle_draw_text_center(const char* text, int x, int y, TinCLE_Color color);` | Draws UTF-8 text. **Anchor: EXACT CENTER (x, y).** Uses active font. |
| `int tincle_load_image(const char* filename);` | Caches image (PNG/JPG). **Returns Image ID (`img_id`), or `-1`.** |
| `void tincle_draw_image(int img_id, int x, int y);` | Uses `img_id`. **[CRITICAL GEAR] Anchor: EXACT CENTER (x, y)** of unscaled image. |
| `void tincle_draw_image_ex(int img_id, int x, int y, int w, int h, double angle);` | Uses `img_id`. **[CRITICAL GEAR] Anchor: EXACT CENTER (x, y)** for position, scale, and rotation. |
| `void tincle_play_music(const char* filename);` | Plays Ogg BGM immediately on infinite loop. Unloads previous music automatically. |
| `void tincle_stop_music(void);` | Instantly stops and unloads current BGM from memory. |
| `int tincle_load_sound(const char* filename);` | Caches WAV/Ogg SE clip. **Returns unique Sound ID, or `-1`.** |
| `void tincle_play_sound(int se_id);` | Plays SE channel via auto-mixer (supports up to 16 concurrent sounds). |
| `struct SDL_Renderer* tincle_get_renderer(void);` | **Returns native `SDL_Renderer***` for direct SDL2/SDL2_gfx primitive drawing. |
| `const char* tincle_get_version(void);` | Returns read-only string of engine version (e.g., `"0.12"`). |
| `bool tincle_is_fullscreen(void);` | Returns `true` if current window is in full-screen mode. |
| `void tincle_set_cursor_auto_policy(bool visible_in_windowed, bool visible_in_fullscreen);` | Sets default cursor visibility behavior for Windowed and Fullscreen modes. |
| `void tincle_set_cursor_visible(bool visible);` | Toggles engine software cursor visibility instantly. |
| `void tincle_set_custom_cursor(int img_id, int hotspot_x, int hotspot_y);` | Replaces software cursor with image ID and hotspot offsets. |
| `void tincle_reset_cursor_to_default(void);` | Restores default mouse cursor image (`cursor.png`). |
| `unsigned char* tincle_load_asset(const char* filename, size_t* out_size);` | Reads the file according to the TinCLE engine's standard file input method. The file size is returned in `size_t`. |
| `void tincle_set_master_volume(float vol);` | Sets master audio volume (`0.0f` to `1.0f`). Default is `1.0f`. Multiplies both BGM and SE. |
| `void tincle_set_bgm_volume(float vol);` | Sets BGM volume (`0.0f` to `1.0f`). Default is `0.8f` for ear-protection. |
| `void tincle_set_se_volume(float vol);` | Sets Sound Effects (SE) volume (`0.0f` to `1.0f`). Default is `0.8f` for ear-protection. |
| `float tincle_get_master_volume(void);` | Returns current master volume level (`0.0f` to `1.0f`). |
| `float tincle_get_bgm_volume(void);` | Returns current BGM volume level (`0.0f` to `1.0f`). |
| `float tincle_get_se_volume(void);` | Returns current SE volume level (`0.0f` to `1.0f`). |
| `void tincle_set_event_callback(tincle_event_cb_t cb);` | **Event Interceptor Registrar.** Registers a custom SDL event callback function. Call inside `game_load()` to forward raw `SDL_Event*` handles directly to third-party modules or extensions (e.g., `gatochoc_handle_event`). |
| `struct SDL_Window* tincle_get_window(void);` | **Native Window Accessor.** Returns pointer to internal `SDL_Window`. Essential for initializing external UI frameworks or managing window-level extension backends. |

### 5.1 GLSL Unleashed API (`TINCLE_MODE_GLSL_HERO` Only)

For full-screen GLSL fragment shader rendering, shader compilation/uniform APIs, and mandatory viewport/aspect ratio calculations, refer to the supplementary talent chip **`SKILL_ADD.md` Section 3**.

### 5.2 Network API / pubicnet

For games requiring online multi-user synchronization or dedicated server capabilities, refer to the supplementary talent chip `SKILL_PN.md`.

### 5.3 Addon Libraries & Extended Talent Chips

TinCLE provides modular addon libraries to seamlessly extend core capabilities without inflating the engine footprint:

* **Physics Engine (`cannoli`)**: Exposes the full API suites of both Box2D (2D physics) and Box3D (3D physics) via `cannoli.dll` (Win32) or `cannoli.wasm` (WebAssembly).
* **Immediate-Mode GUI (`gatochoc`)**: Exposes the full API suite of the Nuklear GUI framework across both 2D and OpenGL pipelines via `gatochoc.dll` (Win32) or `gatochoc.wasm` (WebAssembly).

**Note for AI Developers / Skill Delivery**:
When generating or implementing code that requires advanced 2D/3D physics simulation or custom on-screen GUI/HUD interfaces, refer to the **`SKILL_AON1.md`** talent chip for complete API definitions, header bindings, and implementation rules.

## 6. Mandatory AI Coding Rules & Template

**[CRITICAL WARNING] Never output search citations or footnotes (e.g., `[cite: 1]`, `[1]`) anywhere in or around code blocks. They instantly cause fatal C syntax errors. Output ONLY valid, clean C source code.**

The AI **MUST strictly comply 100%** with this structural template and the absolute rules below:

* **Resource Loading Rule:** NEVER call `tincle_load_image`, `tincle_load_font`, or `tincle_load_sound` inside `update` or `draw` callbacks! All assets MUST be loaded ONCE inside `game_load()`.
* **State Registration Rule:** `tincle_add_state` and `tincle_change_state` MUST be called inside `game_load()`. Forgetting `tincle_change_state` will result in a black screen.
* **HEADER INCLUDE RULE FOR AI AGENTS:** All standard SDL2 sub-headers (such as `SDL_scancode.h`, `SDL_gamecontroller.h`, `SDL_keycode.h`, and `SDL2_gfxPrimitives.h`) exist within the `libs/` directory (or standard `<SDL2/...>` path on Web). **DO NOT** manually define SDL constants or scan codes from scratch. Always rely on these included headers for `SDL_SCANCODE_*`, `SDL_CONTROLLER_BUTTON_*`, and `SDL_BUTTON_*` constants.

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h" // MANDATORY: Always include engine core first
#include <stdio.h>
#include <math.h>        // Explicitly include if math functions (sinf, etc.) are used

// --- Standard SDL2 Sub-Headers for Inputs, Controllers, and Graphics Extensions ---
// All required SDL2 headers (scancodes, gamecontroller, etc.) are bundled in libs/
#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL_scancode.h>
  #include <SDL2/SDL_gamecontroller.h> // For SDL_CONTROLLER_BUTTON_*
  #include <SDL2/SDL_keycode.h>        // For SDL_Keycode
  #include <SDL2/SDL2_gfxPrimitives.h> // For native SDL2_gfx on Web
#else
  #include "libs/SDL_scancode.h"
  #include "libs/SDL_gamecontroller.h" // For SDL_CONTROLLER_BUTTON_*
  #include "libs/SDL_keycode.h"        // For SDL_Keycode
  #include "libs/SDL2_gfxPrimitives.h" // For native SDL2_gfx on Windows
  #include <windows.h>                 // Required for native Windows execution
#endif

// --- State Callbacks Example ---
void title_update(float dt) {} // RULE: All movements/timers must multiply by 'dt'
void title_draw(void) {
  tincle_clear((TinCLE_Color){20, 20, 40, 255}); // Standard 2D Opaque Clear
}

void game_load(void) {
  // RULE: Load ALL assets ONCE here (Fonts, Images, Custom Cursors)
  int f = tincle_load_font("font.ttf", 32);

  // --- Example: Correct Resource Loading (Load ONLY ONCE here!) ---
  // g_custom_cursor = tincle_load_image("my_cursor.png");
  // tincle_set_custom_cursor(g_custom_cursor, 0, 0);

  // RULE: Register states and set initial state at the end of game_load()
  tincle_add_state(0, title_update, title_draw);
  tincle_change_state(0);
}

#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) { tincle_start(game_load, "TITLE", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) { tincle_start(game_load, "TITLE", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#endif
```

## 7 Absolute Rules for Code Generation:

1. **Pure C99 Standard:** Absolute C syntax only. Never use C++ styles (classes, namespaces).
2. **Delta Time (`dt`):** All locomotion, physics, and custom timers must be multiplied by `dt` in `update()`.
3. **Input Synthesis:** Overwrite gamepad analog vector (`tincle_pad_axis`) with max keyboard constants (`1.0f`/`-1.0f`) if arrows/WASD are pressed.
4. **Header Scopes & SDL2 Usage:** For extra SDL2/SDL2_gfx headers, use `<SDL2/filename.h>` inside `__EMSCRIPTEN__` and `"libs/filename.h"` inside `#else` (like `SDL2_gfxPrimitives.h`). You can freely use `tincle_get_renderer()` for custom SDL2/SDL2_gfx drawing extensions, but NEVER modify window dimensions or destroy/alter core SDL window/renderer loops directly.
5. **Strict State Model:** Split logic cleanly via State Management API (e.g., Title, Play, Over). Never write a raw single-loop frame block.
6. **Toolchain Distribution Policy:** Instruct users to use `tinclec` for Win EXE and `emcass` for Web builds. `asspack` handles media asset bundling (supports auto-scanning via `exsass.txt` when called without arguments); `icondom` generates ICO files; `poopee` handles metadata embedding into compiled EXEs.
7. **Note:** Assigning the `ESC` or `F11` keys to game controls will likely cause issues, as these keys conflict with the web browser's full-screen toggle. Avoid assigning game controls to these two keys.

### 7.1 CRITICAL: Mouse Cursor Ownership & Software Cursor Policy

**[MUST READ] ABSOLUTE ANTI-BUG RULE FOR CURSOR HANDLING**
TinCLE (v0.06+) completely disables and overrides the OS/SDL hardware cursor to prevent rendering instability caused by OS/OpenGL overlay issues.
TinCLE **exclusively owns** all mouse cursor management and renders its own software cursor.

#### 1. Forbidden APIs (DO NOT CALL UNDER ANY CIRCUMSTANCES)

Calling any of the following standard APIs will corrupt the rendering state and crash/break cursor functionality:
* **DO NOT** call `SDL_ShowCursor()`. (TinCLE permanently disables it via `SDL_DISABLE`).
* **DO NOT** call Win32 API functions: `ShowCursor()`, `SetCursor()`, or subclass `WM_SETCURSOR`.
* **DO NOT** use `SDL_SetRelativeMouseMode()` directly for visibility toggling.

#### 2. Exclusive TinCLE Cursor APIs

* You MUST use only the following TinCLE native functions to control cursor behavior:
  `tincle_set_cursor_visible(bool visible)`, `tincle_set_cursor_auto_policy(...)`, `tincle_set_custom_cursor(...)`
* `tincle_set_cursor_visible` overrides the policy for the current mode set by `tincle_set_cursor_auto_policy`. If you use this command to toggle the mouse cursor on or off, be sure to use `tincle_set_cursor_visible` again to restore the original state as needed.

#### 3. Required Capture & Synchronization Pattern

When toggling between UI cursor mode and relative FPS mouse capture, **always update the relative mode state FIRST before calling TinCLE cursor APIs**.
```c
// Correct implementation example for game/UI mouse capturing
static void enforce_game_mouse_capture(void) {
    SDL_bool want_relative = g_mouse_captured ? SDL_TRUE : SDL_FALSE;
    if (SDL_GetRelativeMouseMode() != want_relative) {
        SDL_SetRelativeMouseMode(want_relative);
    }
}

static void set_game_mouse_capture(int capture) {
    g_mouse_captured = capture ? 1 : 0;

    // 1. Synchronize relative mode first
    enforce_game_mouse_capture();

    // 2. Toggle software cursor visibility via TinCLE
    tincle_set_cursor_visible(g_mouse_captured ? false : true);

    // 3. Flush relative state buffer
    SDL_GetRelativeMouseState(NULL, NULL);
}
```
**Note**: `enforce_game_mouse_capture()` must ONLY synchronize the relative mouse state. It MUST NOT invoke any cursor visibility APIs internally.

## 8. Production Release Pipelines (Distribution Rules)

When generating final release builds or instructions, the AI **MUST** follow this 5-step pipeline and enforce documentation mandates.

### Step 1: Prep Assets & Hide Console & Credit Attribution Mandate

* **Enforce `CREDITS.txt` Attribution**:
  **Important:** `CREDITS.txt` is included as an attached file when distributing the Windows version of the game, and is embedded as credits in the web version of the game, which can be viewed by clicking the button at the bottom of the game screen.
  * **Agentic AIs**: Must inspect and update `CREDITS.txt` in the root directory, listing attributions for ALL third-party assets, fonts, audio, and libraries added to the project. If any asset details or license origins are missing, the AI **MUST explicitly ask the user** for details before finalizing the release build.
  * **Chat-based AIs**: Must **strongly urge the user** to add all third-party assets/libraries to `CREDITS.txt`. If the AI has information or context about the assets used (e.g., from prior conversation), it **MUST provide a ready-to-copy example snippet** for `CREDITS.txt`.
* Ensure `cursor.png` and `exsass.txt` are configured in the project root.
* Set the 3rd argument (`is_debug`) of `tincle_start` to **`false`** in `game.c` to hide the command console.

### Step 2: Windows Desktop Build Path (ZIP Pack)

1. **Compile:** `tinclec game.exe game.c [other_sources.c...]`
2. **Generate Icon:** If a multi-size `.ico` is not yet prepared, convert an image via `icondom.exe`:
  ```bash
  icondom icon.png icon.ico
  ```
3. **Embed Resources (Optional):** Embed the generated icon and Windows manifest:
  ```bash
  poopee game.exe icon.ico manifest.xml
  ```
  (Use `"none"` to skip ico/manifest).
4. **Pack Assets:** Pack files for final distribution:
   * **Auto Pack (Recommended):** Simply run `asspack` with no arguments to automatically scan the folder and pack all assets/shaders whose file extensions match those registered line-by-line in `exsass.txt`:
     ```bash
     asspack
     ```
   * **Manual Pack:** Alternatively, specify files explicitly: `asspack font.ttf cursor.png bgm.ogg [images/shaders/sounds...]`
   *(Creates `game.data`. Do not ship raw assets).*
5. **ZIP Checklist (8 Items Only):** `game.exe`, `game.data`, `tincle.dll`, `SDL2.dll`, `SDL2_ttf.dll`, `SDL2_gfx.dll`, `CREDITS.txt`, `readme.txt`.

### Step 3: Web Browser Build Path (ZIP Pack)

1. **Verify Asset Extensions:** Ensure all asset AND shader extensions are listed in `exsass.txt`.
2. **Compile & Pack:** `emcass index.html "Game Title" [Width] [Height] game.c [other_sources.c...]`
  * **[CRITICAL] Always output exactly as `index.html`.** Name modification is strictly forbidden for itch.io/web platforms. Automatically outputs `index.js`, `index.wasm`, and `index.data`.
  * [Width] and [Height] refer to the actual dimensions of the game screen in the web version. Specify values that match the game screen dimensions.
3. **ZIP Checklist (5 Items Only):** `index.html`, `index.js`, `index.wasm`, `index.data`, `CREDITS.txt`.
4. **[TROUBLESHOOTING] Server Header Requirements (.htaccess):**
  If the Web build fails to run and throws the following browser console error:
  `Uncaught (in promise) TypeError: Failed to execute 'decode' on 'TextDecoder': The provided ArrayBuffer value must not be resizable`
  This indicates that critical Emscripten capabilities (such as SharedArrayBuffer) are blocked due to missing Cross-Origin Isolation headers on the web host.
  * **Remedy:** Instruct the user to place the bundled `.htaccess` file into the same directory as `index.html` to enable the required COOP and COEP security headers on Apache-based servers:
    ```apache
    <IfModule mod_headers.c>
      Header add Cross-Origin-Opener-Policy "same-origin"
      Header add Cross-Origin-Embedder-Policy "require-corp"
    </IfModule>
    ```

### Step 4: Mandatory `readme.txt` Specifications

AI must explicitly include these details in `readme.txt` or platform descriptions:

* **Controls Disclosure:** State that **`Alt + Enter`** toggles Fullscreen, and **`Alt + Backspace`** resets window scale on Windows. State that the canvas button toggles Fullscreen on Web.
* **Creator Copyright:** Display user's own copyright notice (`Copyright (C) 2026 [Developer Name]`).

### Step 5: Final Archive Packaging (`wipee`)

Automate the final ZIP archive generation using `wipee` (TinCLE Whole Integration Packager for Executable Environment).

1. **Prepare Release Directories:**
  Create separate output directories for each target platform (e.g., `_release_win` for Windows Desktop, `_release_web` for Web Browser) and place all items specified in the ZIP Checklists (Step 2 & Step 3) into their respective folders.

2. **Standard Release Packaging (itch.io / Web / General Distribution):**
  Run `wipee` specifying the output archive name and the target directory. This generates a clean, standard RAW Deflate ZIP package fully compatible with Web hosting environments and standard archive tools.
  ```bash
  wipee game_win.zip _release_win
  wipee game_web.zip _release_web
  ```

3. **Scanner Bypass Packaging (Desktop Distribution Only - Optional):**
  When explicitly preparing a Windows desktop distribution intended to prevent aggressive AV heuristics or automated scanner interference, pass the `-m` flag to activate Malformed ZIP mode (`compression = 99` in Central Directory).
  ```bash
  wipee game_win_secured.zip _release_win -m
  ```
  * **[CRITICAL] Never use the `-m` flag for Web / itch.io builds.** WebAssembly deployment environments depend on strict standard ZIP structures to extract `index.html` server-side.

## 9. Complete Boilerplate Code (`game.c` Template)

The AI can utilize this robust, production-ready full skeleton code to initiate or rewrite any game project under TinCLE v0.05.

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include <stdio.h>
#include <math.h>

#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL_scancode.h>
  #include <SDL2/SDL2_gfxPrimitives.h>
#else
  #include "libs/SDL_scancode.h"
  #include "libs/SDL2_gfxPrimitives.h"
  #include <windows.h>
#endif

// [TCC WORKAROUND] Prevent macro collision and fix missing float math symbols
#undef M_PI
#define M_PI 3.14159265358979323846
#ifndef sinf
#define sinf(x) ((float)sin((double)(x)))
#endif

// --- Globals & Assets ---
static SDL_Renderer* renderer = NULL;
static float g_player_x = 320.0f;
static float g_player_y = 240.0f;
static float g_game_time = 0.0f;
static int g_img_player = -1;
static int g_font_large  = -1;
static int g_font_medium = -1;

// --- State 0: Title ---
void title_update(float dt) {
  if (tincle_key_pressed(SDL_SCANCODE_SPACE) || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_START)) {
    tincle_change_state(1); // Play State
  }
}
void title_draw(void) {
  tincle_clear((TinCLE_Color){0, 0, 0, 255});
  tincle_set_font(g_font_large);
  tincle_draw_text_center("YOUR_GAME_TITLE", 320, 180, (TinCLE_Color){255, 255, 255, 255});
  tincle_set_font(g_font_medium);
  tincle_draw_text_center("PRESS SPACE TO START", 320, 300, (TinCLE_Color){0, 255, 0, 255});
}

// --- State 1: Gameplay ---
void play_update(float dt) {
  g_game_time += dt;
  float move_speed = 200.0f; // Multiplied by dt for framerate independence
  if (tincle_key_pressed(SDL_SCANCODE_LEFT)  || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_DPAD_LEFT))  g_player_x -= move_speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_RIGHT) || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_DPAD_RIGHT)) g_player_x += move_speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_UP)    || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_DPAD_UP))    g_player_y -= move_speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_DOWN)  || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_DPAD_DOWN))  g_player_y += move_speed * dt;

  if (tincle_key_pressed(SDL_SCANCODE_ESCAPE) || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_BACK)) {
    tincle_change_state(0); // Title State
  }
}
void play_draw(void) {
  tincle_clear((TinCLE_Color){20, 20, 50, 255});
  tincle_set_font(g_font_medium);
  tincle_draw_text("GAME PLAYING", 20, 20, (TinCLE_Color){0, 255, 0, 255});

  // CRITICAL: tincle_draw_image handles coordinates as the EXACT CENTER anchor point
  if (g_img_player != -1) {
    tincle_draw_image(g_img_player, (int)g_player_x, (int)g_player_y);
  } else {
    tincle_draw_text("P", (int)g_player_x, (int)g_player_y, (TinCLE_Color){255, 0, 0, 255});
  }

  // Native API Extension Examples (Direct renderer usage)
  SDL_Rect rect = { 100, 100, 50, 50 };
  SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
  SDL_RenderFillRect(renderer, &rect);

  filledEllipseRGBA(renderer, 400, 300, 50, 25, 255, 0, 0, 128);

  int tri_top_y = 150 + (int)(sinf(g_game_time * 5.0f) * 15.0f);
  filledTrigonRGBA(renderer, 400, tri_top_y, 360, 200, 440, 200, 0, 255, 255, 200);
}

// --- Initialization & Callbacks ---
void game_load(void) {
  renderer = tincle_get_renderer(); // Cache renderer context for native loops
  g_font_large  = tincle_load_font("font.ttf", 64);
  g_font_medium = tincle_load_font("font.ttf", 32);
  g_img_player = tincle_load_image("player.png");

  tincle_add_state(0, title_update, title_draw);
  tincle_add_state(1, play_update, play_draw);
  tincle_change_state(0); // Activate initial state
}

// --- Entry Point Bootstrapper ---
#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) { tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) { tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#endif
```
