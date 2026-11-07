---
name: tincle-aon1
description: Use when integrating 2D/3D physics or Nuklear GUI elements in TinCLE using `cannoli` (Box2D/Box3D) or `gatochoc` (HUD/UI/fonts). Covers API references, linkage, and boilerplate setup. [TinCLE Add-On Skill v0.14]
---

# SKILL_AON1.md - TinCLE Add-On Talent Chip [2D/3D Physics & GUI Toolkit]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

## 1. cannoli (Collision And Newtonian Network Object Linked Interface)

**Module:** cannoli (`cannoli.dll` / `cannoli.wasm`)
**Description:** 2D & 3D Physics Extension (Box2D & Box3D Full Export)

* **Overview & Usage:**
  The distribution includes `cannoli.dll` (for Windows) and `libs/cannoli.a` (for Web/WASM). By adding `#include "libs/cannoli.h"` at the top of your source code, the complete, uninhibited set of Pure C Box2D v3.0 (2D physics) and Box3D v0.1 (3D physics) APIs becomes fully available across both Windows (`tinclec`) and Web (`emcass`) build targets. If you use this feature, you must include `cannoli.dll` in the distribution package for Windows.
* **AI Coding Rule:**
  You can directly invoke any official Box2D (e.g., `b2CreateWorld`, `b2CreateBody`, `b2Body_GetPosition`) and Box3D C functions without external wrappers. Treat `cannoli.h` as a native, unified 2D/3D physics extension of the TinCLE environment.

### Additional API Reference

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `const char* cannoli_get_version(void);` | Returns read-only string of cannoli version (e.g., `"0.14"`). |

### Distribution

When using cannoli, you must include either cannoli.dll or cannoli.wasm-whichever is appropriate for the target platform-in your distribution. An example of the minimum set of distribution files, including these, is as follows.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`,`SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `cannoli.dll` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `cannoli.wasm` |

## 2. gatochoc (Gui And Toolkit for On-screen Components, Huds, and Object Controls)

**Module:** gatochoc (`gatochoc.dll` / `gatochoc.wasm`)
**Description:** Lightweight Nuklear-based GUI extension for TinCLE (Supports SDL_Renderer & OpenGL GL2/GLES2 backends).

### 1. Extension API Reference

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `bool gatochoc_init(gatochoc_mode_t mode, SDL_Window *win, void *target);` | **UI Engine Init.** Call inside `game_load`. <br>* `mode`: `GATOCHOC_MODE_SDL_RENDERER` or `GATOCHOC_MODE_GLSL`. <br>* `win`: Pointer to `SDL_Window` (via `tincle_get_window()`). <br>* `target`: `SDL_Renderer*` (SDL mode via `tincle_get_renderer()`) or `SDL_GLContext` (GLSL mode). <br>* **Return:** `true` if success, `false` on failure. |
| `bool gatochoc_handle_event(SDL_Event *event);` | **Input Forwarder.** Pass raw `SDL_Event*` here inside the event callback (`tincle_set_event_callback`). Automatically triggers `nk_input_begin` on first event. <br>* **Return:** `true` if UI consumed the event, `false` otherwise. |
| `struct nk_context* gatochoc_get_context(void);` | **Nuklear Context Accessor.** Returns pointer to internal `struct nk_context*`. Use this to call standard Nuklear GUI functions (e.g., `nk_begin`, `nk_layout_row_dynamic`, `nk_button_label`, `nk_end`). |
| `void gatochoc_input_begin(void);` | **Input Frame Flush.** Call at the very top of `update_cb` before building any Nuklear UI. Flushes and finalizes pending input events (`nk_input_end`) for the current frame. |
| `void gatochoc_input_end(void);` | **Input Cleanup.** Frame input close handler (reserved / optional for explicit multi-pass input states). |
| `GatoChocFont gatochoc_load_font_from_memory(const void* data, size_t size, float font_size, GatoChocFontRange range_type);` | **Standard Font Loader.** Loads TrueType font (`.ttf`) from memory buffer. <br>* `range_type`: `GATOCHOC_FONT_DEFAULT` (ASCII) or `GATOCHOC_FONT_JAPANESE` (Full Japanese including full-width symbols `0xFF00-0xFFEF`). |
| `GatoChocFont gatochoc_load_font_from_memory_ex(const void* data, size_t size, float font_size, GatoChocFontRange range_type, const unsigned long *custom_ranges);` | **Extended Font Loader.** Custom glyph range font loader. Set `range_type` to `GATOCHOC_FONT_CUSTOM` and pass a zero-terminated `nk_rune` array to `custom_ranges` for multilingual support (e.g., Chinese, Korean). |
| `void gatochoc_set_default_font(GatoChocFont font);` | **Default Font Setter.** Sets the loaded `GatoChocFont` as the global default font for all Nuklear UI elements. |
| `void gatochoc_render(void);` | **UI Draw Pass.** Renders generated Nuklear geometry. Call inside `draw_cb`, right after `tincle_clear` and game rendering. Auto-finalizes font atlas on first frame if required. |
| `void gatochoc_shutdown(void);` | **Cleanup.** Frees all Nuklear contexts, font atlases, and backend resources. Call on game exit. |
| `const char* gatochoc_get_version(void);` | Returns read-only string of gatochoc version (e.g., `"0.14"`). |

---

### 2. Core Types & Enums

```c
// Backend Rendering Mode
typedef enum gatochoc_mode {
    GATOCHOC_MODE_SDL_RENDERER = 0, // 2D SDL_Renderer Pipeline
    GATOCHOC_MODE_GLSL         = 1  // OpenGL GL2 / GLES2 Pipeline
} gatochoc_mode_t;

// Font Handle Type
typedef struct nk_font* GatoChocFont;

// Unicode Glyph Range Preset
typedef enum {
    GATOCHOC_FONT_DEFAULT  = 0, // Basic ASCII only
    GATOCHOC_FONT_JAPANESE = 1, // Full Japanese (Hiragana, Katakana, Kanji & Full-width Symbols)
    GATOCHOC_FONT_CUSTOM   = 2  // User-defined custom Unicode range array
} GatoChocFontRange;
```

---

### 3. Integration Pipeline & Architecture Notes

#### Load & Link Blueprint

1. **Direct Linkage (No Special Loader Needed):**
  * Link `gatochoc.dll` (Desktop) or `gatochoc.wasm` / `gatochocmt.wasm` (WebAssembly Side Module) directly during compilation with `tcc` or `emcc`.
  * Bind `on_sdl_event` using `tincle_set_event_callback(on_sdl_event)` to pass raw SDL inputs straight to `gatochoc_handle_event`.

2. **Flexible Backend Selection (TinCLE Dual Rendering Engine):**
  * **`GATOCHOC_MODE_SDL_RENDERER`**: Use when running TinCLE with `TINCLE_MODE_2D_NORMAL`. Standard 2D GUI overlay using `SDL_Renderer*`.
  * **`GATOCHOC_MODE_GLSL`**: Use when running TinCLE with `TINCLE_MODE_GLSL_HERO`. Renders directly using OpenGL / GLES2 shaders via native `SDL_GLContext`.

3. **Frame Execution Sequence (CRITICAL RULE):**
  * **Event Pass:** Inputs are forwarded via `tincle_set_event_callback` -> `gatochoc_handle_event`.
  * **Update Pass (`update_cb`):**
    1. Call `gatochoc_input_begin()` at the **very first line**.
    2. Build Nuklear UI controls (`nk_begin` ... `nk_end`).
    3. Call `gatochoc_input_end()` at the **very last line** (required for future frame-state extensions).
  * **Draw Pass (`draw_cb`):** Call `gatochoc_render()` right after `tincle_clear` to draw UI on top.

#### Distribution

When using gatochoc, you must include either gatochoc.dll or gatochoc.wasm-whichever is appropriate for the target platform-in your distribution. An example of the minimum set of distribution files, including these, is as follows.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`,`SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `gatochoc.dll` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `gatochoc.wasm` |

---

### 2. Standard Integration Boilerplate (`game.c`)

* **Required:** To use `gatochoc`, you must include the dedicated header file by adding `#include “libs/gatochoc.h”`.

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include "libs/gatochoc.h"
#include <stdio.h>

#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL.h>
  #include <SDL2/SDL_scancode.h>
#else
  #include "libs/SDL_scancode.h"
  #include <windows.h>
#endif

// --- Global Variables ---
static int g_counter = 0;
static GatoChocFont g_jp_font = NULL;

// --- SDL Event Forwarder Callback ---
bool on_sdl_event(SDL_Event *event) {
    // Forward raw event to GATOCHOC. Returns true if consumed by UI.
    return gatochoc_handle_event(event);
}

// --- Frame Update Callback ---
void main_update(float dt) {
    // 1. Flush & Lock frame input state (MUST BE FIRST)
    gatochoc_input_begin();

    // 2. Build Nuklear GUI Controls
    struct nk_context *ctx = gatochoc_get_context();
    if (ctx) {
        nk_flags flags = NK_WINDOW_BORDER | NK_WINDOW_MOVABLE | NK_WINDOW_SCALABLE | NK_WINDOW_TITLE;
        if (nk_begin(ctx, "TinCLE x Nuklear GUI", nk_rect(50, 50, 280, 200), flags)) {

            nk_layout_row_dynamic(ctx, 30, 1);
            nk_label(ctx, "Hello Michyo! Nuklear Active!", NK_TEXT_LEFT);

            char buf[64];
            snprintf(buf, sizeof(buf), "Count: %d", g_counter);
            nk_label(ctx, buf, NK_TEXT_LEFT);

            if (nk_button_label(ctx, "Push Me!")) {
                g_counter++;
            }
        }
        nk_end(ctx);
    }

    // 3. Close frame input state (MUST BE LAST in update)
    gatochoc_input_end();
}

// --- Frame Render Callback ---
void main_draw(void) {
    // 1. Clear background
    tincle_clear((TinCLE_Color){255, 40, 60, 255});

    // 2. Render Nuklear GUI overlay on top
    gatochoc_render();
}

// --- Engine Load & Initialization ---
void game_load(void) {
    // 1. Initialize GATOCHOC with TinCLE rendering target
    gatochoc_init(GATOCHOC_MODE_SDL_RENDERER, tincle_get_window(), tincle_get_renderer());

    // 2. Bind event callback to forward inputs
    tincle_set_event_callback(on_sdl_event);

    // 3. Load Japanese Font Asset
    size_t font_size = 0;
    unsigned char* font_data = tincle_load_asset("font.ttf", &font_size);
    if (font_data) {
        g_jp_font = gatochoc_load_font_from_memory(font_data, font_size, 18.0f, GATOCHOC_FONT_JAPANESE);
        if (g_jp_font) {
            gatochoc_set_default_font(g_jp_font);
        }
        free(font_data);
    }

    // 4. Register State 0 & Transition
    tincle_add_state(0, main_update, main_draw);
    tincle_change_state(0);
}

// --- Entry Point ---
#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) {
    tincle_start(game_load, "TinCLE Nuklear Demo", true, 640, 480, TINCLE_MODE_2D_NORMAL);
    gatochoc_shutdown();
    return 0;
}
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) {
    tincle_start(game_load, "TinCLE Nuklear Demo", true, 640, 480, TINCLE_MODE_2D_NORMAL);
    gatochoc_shutdown();
    return 0;
}
#endif
```
