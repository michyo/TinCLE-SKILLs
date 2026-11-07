# TinCLE (Tiny C Lovely Engine) - Additional High Level Skills Version 0.10

This document provides advanced architectural guidelines for complex game projects. The instructions here override or extend the base `SKILL.md`.

---

## 1. Multi-File Code Generation & Modular Architecture

### Auto-Trigger Criteria (When to use Multi-File Mode)

The AI Agent MUST automatically switch from single-file `game.c` to this Multi-File Modular Architecture if **ANY** of the following conditions are met:

1. **State Count (>= 4):** The game design requires 4 or more distinct states (e.g., Title, Gameplay, Result, Shop, Pause).
2. **Code Scale (>= 400 Lines):** The estimated total C source code exceeds 400 lines.
3. **Complex Custom Systems:** The project defines complex data structures (e.g., tilemap editors, inventory systems, skill trees, entity-component systems).
4. **Explicit User Instruction:** The user explicitly requests modular, multi-file, or large-scale generation.

### Architecture Overview

To prevent LLM context degradation and syntax hallucinations, separate the code into distinct, single-responsibility C source files:
* `game_shared.h`: Global asset structs, shared state variables (`extern`), and common headers (`tincle.h`, math, SDL2).
* `main.c`: Global variable definitions, asset loading inside `game_load()`, state registrations, and the entry point (`tincle_start`).
* `state_*.c`: Implementation of `update` and `draw` callbacks for each specific state. Include `game_shared.h` at the top of every state file.

### Compilation Rules

Pass all `.c` files simultaneously to `tinclec` (Windows) or `emcass` (Web):
```bash
# Windows Desktop Build
tinclec mygame.exe main.c state_title.c state_play.c

# Web WASM Build
emcass index.html "My Game" main.c state_title.c state_play.c
```

### CRITICAL: Single File Hard Limit Policy (Anti-Bloat Rule)

* **[ABSOLUTE LIMIT] Max 400 Lines Per File:**
  Even when split by State (e.g., `state_game.c`), **NO SINGLE `.c` FILE MAY EVER EXCEED 400 LINES OF CODE.**
* **Sub-module Splitting Required:**
  If a single state (such as Main Gameplay) grows complex, the AI **MUST NOT** stuff all logic into a single `state_game.c`.
  The AI **MUST** aggressively sub-split the state into distinct system modules!

  * **Example of Correct Sub-module Breakdown for a Large State:**
    * `state_game.c` -> State entry/exit, state-level `update` / `draw` callbacks ONLY.
    * `game_player.c` / `.h` -> Player movement, input, and state logic.
    * `game_enemy.c` / `.h` -> Enemy AI, spawning, and bullet patterns.
    * `game_ui.c` / `.h` -> HUD, score rendering, and UI popups.

* **[STRICT BAN]** Generating a single file over 400 lines under the excuse of "it's just one state" is STRICTLY FORBIDDEN. If any single C file approaches 400 lines, extract its systems into dedicated sub-modules immediately.

### Minimal Multi-File Boilerplate Template

#### File 1: `game_shared.h`

```c
#ifndef GAME_SHARED_H
#define GAME_SHARED_H

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

// Math workarounds
#undef M_PI
#define M_PI 3.14159265358979323846
#ifndef sinf
#define sinf(x) ((float)sin((double)(x)))
#endif

// --- Shared Global Asset Context ---
typedef struct {
  SDL_Renderer* renderer;
  int font_large;
  int font_medium;
  int img_player;
  float player_x;
  float player_y;
} GameContext;

extern GameContext g_ctx; // Global context declaration

// --- State Function Declarations ---
void title_update(float dt);
void title_draw(void);

void play_update(float dt);
void play_draw(void);

#endif // GAME_SHARED_H
```

#### File 2: `main.c`

```c
#define SDL_MAIN_HANDLED
#include "game_shared.h"

// Definition of shared context
GameContext g_ctx;

void game_load(void) {
  g_ctx.renderer = tincle_get_renderer();
  g_ctx.font_large  = tincle_load_font("font.ttf", 64);
  g_ctx.font_medium = tincle_load_font("font.ttf", 32);
  g_ctx.img_player  = tincle_load_image("player.png");
  g_ctx.player_x    = 320.0f;
  g_ctx.player_y    = 240.0f;

  // Register states
  tincle_add_state(0, title_update, title_draw);
  tincle_add_state(1, play_update, play_draw);

  tincle_change_state(0); // Set initial state
}

#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) { tincle_start(game_load, "TINCLE_GAME", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) { tincle_start(game_load, "TINCLE_GAME", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#endif
```

#### File 3: `state_title.c`

```c
#include "game_shared.h"

void title_update(float dt) {
  if (tincle_key_pressed(SDL_SCANCODE_SPACE) || tincle_pad_pressed(SDL_CONTROLLER_BUTTON_START)) {
    tincle_change_state(1); // Change to Play State
  }
}

void title_draw(void) {
  tincle_clear((TinCLE_Color){0, 0, 0, 255});
  tincle_set_font(g_ctx.font_large);
  tincle_draw_text_center("TITLE STATE", 320, 180, (TinCLE_Color){255, 255, 255, 255});
  tincle_set_font(g_ctx.font_medium);
  tincle_draw_text_center("PRESS SPACE TO PLAY", 320, 300, (TinCLE_Color){0, 255, 0, 255});
}
```

#### File 4: `state_play.c`

```c
#include "game_shared.h"

void play_update(float dt) {
  float speed = 200.0f;
  if (tincle_key_pressed(SDL_SCANCODE_LEFT))  g_ctx.player_x -= speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_RIGHT)) g_ctx.player_x += speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_UP))    g_ctx.player_y -= speed * dt;
  if (tincle_key_pressed(SDL_SCANCODE_DOWN))  g_ctx.player_y += speed * dt;

  if (tincle_key_pressed(SDL_SCANCODE_ESCAPE)) {
    tincle_change_state(0); // Return to Title State
  }
}

void play_draw(void) {
  tincle_clear((TinCLE_Color){20, 20, 50, 255});
  tincle_set_font(g_ctx.font_medium);
  tincle_draw_text("PLAY STATE", 20, 20, (TinCLE_Color){0, 255, 0, 255});

  if (g_ctx.img_player != -1) {
    tincle_draw_image(g_ctx.img_player, (int)g_ctx.player_x, (int)g_ctx.player_y);
  } else {
    tincle_draw_text("P", (int)g_ctx.player_x, (int)g_ctx.player_y, (TinCLE_Color){255, 0, 0, 255});
  }
}
```

---

## 2. Emscripten Web Multithreaded Build (`libs/tinclemt.a`)

### Overview & Capabilities

For standard WebAssembly (HTML5) exports, the base prebuilt static library `libs/tincle.a` is compiled for single-threaded execution, fully compatible with the automated `emcass` CLI workflow.

However, if a complex game requires WebAssembly multithreading (utilizing `SharedArrayBuffer` and `pthreads`), TinCLE provides an optional prebuilt multithreaded library: **`libs/tinclemt.a`**. This variant is precompiled with `-pthread`, `atomics`, and `bulk-memory` features enabled.

### Mandatory Usage Rules & Manual Workflow

1. **Toolchain Limit & Self-Responsibility**:
  * The default `emcass` CLI assistant tool does **NOT** support `tinclemt.a` or automated multithreaded builds natively.
  * Enabling multithreading requires manual execution of the native `emcc` toolchain and is considered an advanced, high-level developer action.

2. **Recommended Build Pipeline**:
  * **Step 1:** Execute standard `emcass` once to let it output its default WebAssembly build files.
  * **Step 2:** Inspect and copy the underlying, complete `emcc` command string constructed internally by `emcass`.
  * **Step 3:** Manually modify the copied `emcc` command line:
    * Replace `libs/tincle.a` with `libs/tinclemt.a`.
    * Append the `-pthread` flag along with your required memory and thread allocation limits (e.g., `-s ALLOW_MEMORY_GROWTH=0`, `-s INITIAL_MEMORY=<bytes>`, `-s PTHREAD_POOL_SIZE=<num>`).

3. **Required HTTP Server Headers & Bundled `.htaccess`**:
  * WebAssembly multithreading strictly mandates Cross-Origin Isolation in modern web browsers. The web server MUST serve the deployed game with the following HTTP response headers:
    ```http
    Cross-Origin-Opener-Policy: same-origin
    Cross-Origin-Embedder-Policy: require-corp
    ```
  * **Pre-bundled Solution:** TinCLE includes a pre-configured `.htaccess` file in the package. If hosting on an Apache-based web server (or custom server with `.htaccess` support), simply place the bundled `.htaccess` file directly into your game's root web deployment directory.
  * **`.htaccess` Content Example:**
    ```apache
    <IfModule mod_headers.c>
       Header add Cross-Origin-Opener-Policy "same-origin"
       Header add Cross-Origin-Embedder-Policy "require-corp"
    </IfModule>
    ```

---

## 3. Custom GLSL Shader Development & Validation (`TINCLE_MODE_GLSL_HERO`)

### Overview & Engine Mode

When building high-end visual effects, post-processing filters, or procedural graphics, TinCLE provides the **`TINCLE_MODE_GLSL_HERO`** execution mode.

To activate custom GLSL shader support, set the final argument of `tincle_start()` as follows in `main.c`:
```c
tincle_start(game_load, "My GLSL Game", true, 640, 480, TINCLE_MODE_GLSL_HERO);
```

### [CRITICAL] Clear Color & Screen Tinting Rules in GLSL_HERO Mode

When running under `TINCLE_MODE_GLSL_HERO`, the custom GLSL fragment shader executes on the background hardware layer directly beneath the standard SDL2 2D rendering layer.

1. **Basic Visibility (Alpha = 0):**
  To let the background GLSL shader render normally without obstruction, clear the screen using **Alpha = 0** in your `draw` callback:
  ```c
  // Standard clear for GLSL_HERO (Background shader fully visible)
  tincle_clear((TinCLE_Color){0, 0, 0, 0});
  ```

2. **Advanced Feature — Screen Tinting / Color Overlay (0 < Alpha < 255):**
  By passing a semi-transparent alpha value to `tincle_clear`, you can apply a dynamic color tint or overlay fade directly on top of the GLSL background shader!
  * **Night / Ambient Lighting Effect:** `tincle_clear((TinCLE_Color){10, 15, 50, 128});` (Applies a semi-transparent dark blue tint)
  * **Damage / Red Flash Effect:** `tincle_clear((TinCLE_Color){255, 0, 0, 100});` (Applies a temporary red overlay)
  * **Fade Out Effect:** Increase Alpha over time up to 255 to smoothly fade out to a solid color.

3. **Opaque Warning (Alpha = 255):**
  * Calling `tincle_clear` with a completely opaque alpha (`Alpha = 255`) will draw a solid color over the entire screen, completely hiding/erasing the hardware GLSL shader layer beneath it.

### Shader Code & Viewport Rules

1. **GLES2 Compliance:** Shaders **MUST** be 100% GLES2 compliant to run on WebAssembly.
2. **Header Injection Warning:** **NEVER write `precision mediump float;` in your `.glsl` file!** TinCLE automatically injects this header during the Emscripten build. Writing it manually causes syntax errors on Windows OpenGL.
3. **[MANDATORY] Viewport & Aspect Ratio Correction for Fullscreen / Letterboxing:**
  * **NEVER** calculate UV coordinates using `gl_FragCoord.xy / u_resolution` directly. When entering fullscreen mode or letterboxing, `u_resolution` represents physical window dimensions, causing critical position shifts.
  * **ALWAYS** calculate UV coordinates using `u_viewport` to strictly lock rendering to the actual game viewport:
    ```glsl
    vec2 uv = (gl_FragCoord.xy - u_viewport.xy) / u_viewport.zw;
    ```
  * When normalizing mouse coordinates received from C (`u_custom_mouse.xy`), apply a fixed aspect ratio matching virtual game resolution (e.g., `640.0 / 480.0`) to both `p.x` and `m.x` to prevent horizontal distortion across different screen sizes.

### Built-in Shader Uniforms

* `uniform float u_time;` -> In-game time in seconds (`SDL_GetTicks() / 1000.0f`).
* `uniform vec2 u_resolution;` -> Physical window/screen resolution (`width`, `height`).
* `uniform vec4 u_viewport;` -> Actual rendering viewport rect (`x`, `y`, `w`, `h`).

### GLSL API Reference Table

| Function Signature | Description & Critical Notes |
| --- | --- |
| `void tincle_render_shader(const char* filename);` | Call inside `game_load()` to keep a background shader running continuously. |
| `int tincle_load_shader(const char* filename);` | Call inside `game_load()`. Compiles shader and returns Shader ID (`int`). |
| `void tincle_set_shader(int shader_id);` | Sets active background shader ID (`-1` to disable). |
| `void tincle_shader_use(int shader_id);` | Activates shader for uniform updates. **Has overhead (`glUseProgram`). Call only when switching scenes or updating values.** |
| `void tincle_shader_send_vec3(int shader_id, const char* name, float x, float y, float z);` | Binds a `vec3` uniform value to the target shader. |
| `void tincle_shader_send_float(int shader_id, const char* name, float value);` | Binds a `float` uniform value to the target shader. |

### Shader Validation Workflow (`pisschk`)

To prevent cross-platform rendering failures—such as desktop NVIDIA leniency vs. AMD Radeon strictness vs. WebGL/GLES2 specifications—all fragment shaders (`.frag` / `.glsl`) **MUST** be validated using `pisschk` before deployment.

```bash
pisschk <shader_file_path>
```

* **Example:** `pisschk assets/shaders/water.frag`
* **Validation Coverage:**
  * **Mode 0 (Desktop / Radeon Compliance):** Equivalent to `glslang -S frag -d --no-link --error-column`. Enforces strict desktop GLSL syntax and blocks driver-specific extensions/reserved words (e.g., `active`).
  * **Mode 1 (Web / GLES2 Compliance):** Automatically prepends `precision mediump float;` header to verify strict WebGL/GLES2 compatibility for Emscripten web builds.

* **Exit Codes:**
  * `0`: All inspection checks PASSED successfully.
  * `1`: Syntax/compilation errors DETECTED.
  * `2`: File I/O or argument error.

### [CRITICAL AI RULE FOR SHADER DEVELOPMENT]

Whenever the AI agent writes, edits, or modifies ANY GLSL shader code for TinCLE, it **MUST** automatically execute `pisschk` on the target shader file to guarantee 100% cross-platform compatibility across NVIDIA, AMD Radeon, and WebGL/GLES2 targets before delivering the final code to the user.

### Mandatory GLSL Template & Anti-Crash Rules

* **[FATAL BUG PREVENTATIVE] One-Time Shader Load Rule:**
  * **NEVER** call `tincle_load_shader()` or `tincle_render_shader()` inside `update()` or `draw()` callbacks! Loading shaders every frame will immediately exhaust internal shader tables and crash the engine.
  * Shaders **MUST** be loaded and rendered ONCE inside `game_load()`.

```c
#define SDL_MAIN_HANDLED
#include "game_shared.h" // or "libs/tincle.h" (and the libraries needed)

void title_update(float dt) {}

void title_draw(void) {
  // MANDATORY: Alpha MUST be 0 to keep the GLSL hardware shader layer visible beneath 2D elements!
  tincle_clear((TinCLE_Color){0, 0, 0, 0});

  // Draw 2D UI elements on top of shader...
}

void game_load(void) {
  // Example GLSL Setup
  int shader_id = tincle_load_shader("bg.glsl");
  tincle_render_shader("bg.glsl");

  tincle_add_state(0, title_update, title_draw);
  tincle_change_state(0);
}

#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) { tincle_start(game_load, "GLSL_GAME", true, 640, 480, TINCLE_MODE_GLSL_HERO); return 0; }
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) { tincle_start(game_load, "GLSL_GAME", true, 640, 480, TINCLE_MODE_GLSL_HERO); return 0; }
#endif
```

### Advanced Rules for GLSL Shader & Asset Management

1. **Normalized Shader Mouse Coordinates (`GLSL_HERO` Mode):**
  * Mouse coordinates returned by `tincle_get_mouse()` are automatically scaled to the virtual resolution (e.g., 640x480).
  * When passing mouse positions to custom GLSL shaders, C code **MUST** normalize values strictly using the virtual game resolution and invert the Y-axis for OpenGL space:
    ```c
    s_mouse_nx = (float)mx / VIRTUAL_WIDTH;
    s_mouse_ny = 1.0f - ((float)my / VIRTUAL_HEIGHT);
    ```
  * Do NOT pass raw screen pixel coordinates directly to the shader if `u_viewport` is used for screen-space UV calculation.

2. **Shader Asset Manifest Rule (`exsass.txt`):**
  * All shader files (e.g., `.glsl`, `.frag`, `.vert`) MUST be placed in the project root folder.
  * Ensure their file extensions (e.g., `.glsl`, `.frag`) are explicitly registered line-by-line in `exsass.txt` so that `emcass` and `asspack` can automatically package them for release.
