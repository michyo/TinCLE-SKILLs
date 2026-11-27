---
name: tincle-aon1
description: Use when integrating 2D/3D physics, Nuklear GUI elements, Local LLM inference, Artificial Chatterbots, or a Retro BASIC runtime in TinCLE using `cannoli` (Box2D/Box3D), `gatochoc` (HUD/UI/fonts), `gozinaki` (LLM/GGUF), `waffle` (Rule-based Chatbot), or `babka` (ORB BASIC — redirects to `SKILL_BK.md`). Covers API references, linkage, and boilerplate setup. [TinCLE Add-On Skill v0.19]
---

# SKILL_AON1.md - TinCLE Add-On Talent Chip [Physics, GUI, Local LLM, Chatbot & BASIC]

# SKILL_AON1.md - TinCLE Add-On Talent Chip [2D/3D Physics, GUI Toolkit & Local LLM]

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
| `const char* cannoli_get_version(void);` | Returns read-only string of cannoli version (e.g., `"0.19"`). |

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
| `const char* gatochoc_get_version(void);` | Returns read-only string of gatochoc version (e.g., `"0.19"`). |

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

### 4. Standard Integration Boilerplate (`game.c`)

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

## 3. gozinaki (Generative Output & Zero-shot Intelligence Node for Autonomous Knowledge Interaction)

**Module:** gozinaki (`gozinaki.dll` / `gozinaki.wasm`)
**Description:** Local LLM Inference Node based on llama.cpp (MIT License). Designed for real-time game loops via non-blocking step-by-step generation and chunked prompt evaluation.

* **Overview & Usage:**
  The distribution includes `gozinaki.dll` and its backend dependencies (`libllama.dll`, `ggml.dll`, `ggml-base.dll`, `ggml-cpu.dll`) for Windows, and `gozinaki.wasm` for Web/WASM. By including `#include "libs/gozinaki.h"`, AI agents can dynamically generate NPC dialogue, item descriptions, and contextual narratives.
* **AI Coding Rule:**
  Models (`.gguf` files) MUST NOT be embedded inside `index.data`. They must be fetched asynchronously using TinCLE's `tincle_fetch_file_async()` API. Inference and prompt evaluation are executed progressively by calling `gozinaki_step()` once per frame in the `update` loop to guarantee 60fps rendering without blocking the main thread.

### 1. Extension API Reference

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `bool gozinaki_init(const char* model_path, int n_ctx, int n_threads);` | **LLM Engine Init.** Loads the GGUF model from the path retrieved via `tincle_fetch_get_path()`. `n_ctx`: Context size (use 0 for model default). `n_threads`: Thread count (use 0 for auto). Returns `true` on success. |
| `void gozinaki_free(void);` | **Cleanup.** Completely unloads the model and frees all internal contexts. |
| `bool gozinaki_is_initialized(void);` | **Status Check.** Returns `true` if the model is currently loaded and ready. |
| `bool gozinaki_set_prompt(const char* system_prompt, const char* user_prompt, int max_tokens);` | **Prompt Injection.** Starts a new generation session. `system_prompt` can be NULL/empty. Automatically tokenizes and sets status to `GOZINAKI_STATUS_EVALUATING`. Returns `true` if successfully started. |
| `GozinakiStatus gozinaki_step(void);` | **Non-blocking Step Engine.** **[CRITICAL]** Call this exactly once per frame inside your `update_cb` while the status is `GOZINAKI_STATUS_EVALUATING` or `GOZINAKI_STATUS_GENERATING`. It processes prompt chunks and generates tokens to maintain frame rate. |
| `void gozinaki_abort(void);` | **Force Cancel.** Interrupts active evaluation/generation and returns the engine to the IDLE state. |
| `const char* gozinaki_get_text(void);` | **Full Text Accessor.** Returns the complete generated UTF-8 text so far. Pointer is managed internally; do not free. |
| `const char* gozinaki_get_delta_text(void);` | **Delta Text Accessor.** Returns only the new token string generated in the very last `gozinaki_step()`. Ideal for triggering typing sound effects. Returns `""` if no new characters were formed. |
| `GozinakiStatus gozinaki_get_status(void);` | **State Polling.** Returns the current `GozinakiStatus` enum. |

### 2. Core Types & Enums

```c
typedef enum {
    GOZINAKI_STATUS_IDLE       = 0,  // Ready to accept a new prompt
    GOZINAKI_STATUS_GENERATING = 1,  // Currently generating text (call gozinaki_step)
    GOZINAKI_STATUS_FINISHED   = 2,  // Generation complete (EOS reached or max_tokens hit)
    GOZINAKI_STATUS_EVALUATING = 3,  // Reading prompt in chunks to prevent freezes (call gozinaki_step)
    GOZINAKI_STATUS_ERROR      = -1  // Internal error occurred
} GozinakiStatus;
```

### 3. Integration Pipeline & Architecture Notes

#### Model Loading & Fetching (CRITICAL RULE)

Large `.gguf` files (e.g., SmolLM2-135M or Qwen2.5-0.5B) must be stored alongside the executable/HTML, **not** inside `exsass.txt` data packs. They must be loaded using TinCLE's asynchronous fetch API to prevent browser freezing during WASM initialization.

#### WASM Compilation Flags (CRITICAL RULE)

When compiling a web build using `gozinaki.wasm`, the AI agent MUST instruct the user to append the following memory and module flags to their `emcass` or `emcc` command. Failure to do so will result in a `Stack overflow` or `memory access out of bounds` crash:

```bash
-s MAIN_MODULE=2 -s INITIAL_MEMORY=1073741824 -s ALLOW_MEMORY_GROWTH=1 -s MAXIMUM_MEMORY=2147483648 -s STACK_SIZE=16777216
```

#### Event Edge-Detection Requirement

When triggering `gozinaki_set_prompt` via user input (e.g., keyboard or gamepad), the AI agent MUST implement edge-detection (checking if the key was *just* pressed this frame). Do not evaluate continuous key-down states, as 60fps loops will repeatedly reset the LLM context and cause freezes.

#### Distribution

When using gozinaki, you must include the respective dynamic modules and the external `.gguf` model file in your distribution.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`, `SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `gozinaki.dll`, `libllama.dll`, `ggml.dll`, `ggml-base.dll`, `ggml-cpu.dll`, `model.gguf` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `gozinaki.wasm`, `model.gguf` |

### 4. Standard Integration Boilerplate

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include "libs/gozinaki.h"
#include <stdio.h>

static TinCLE_AsyncFile* g_model_file = NULL;
static bool g_llm_ready = false;
static bool g_prev_space = false;

void main_update(float dt) {
    // 1. Handle Asynchronous Model Loading
    if (!g_llm_ready) {
        float progress = 0.0f;
        if (tincle_fetch_get_status(g_model_file, &progress) == TINCLE_ASYNC_READY) {
            // Context size 1024 is recommended for lightweight NPC chat
            if (gozinaki_init(tincle_fetch_get_path(g_model_file), 1024, 0)) {
                g_llm_ready = true;
                gozinaki_set_prompt("You are a helpful NPC.", "Welcome to TinCLE!", 128);
            }
        }
        return;
    }

    // 2. Step-by-Step Non-blocking Engine (Handles both Evaluating & Generating)
    GozinakiStatus status = gozinaki_get_status();
    if (status == GOZINAKI_STATUS_EVALUATING || status == GOZINAKI_STATUS_GENERATING) {
        gozinaki_step();

        if (status == GOZINAKI_STATUS_GENERATING) {
            const char* delta = gozinaki_get_delta_text();
            if (delta && delta[0] != '\0') {
                // Optional: Play typing sound using tincle_play_sound() here
            }
        }
    }

    // 3. Trigger new prompt using Edge-Detection
    if (status == GOZINAKI_STATUS_FINISHED) {
        bool curr_space = tincle_key_pressed(SDL_SCANCODE_SPACE);
        if (curr_space && !g_prev_space) {
            gozinaki_set_prompt("You are an evil knight.", "Show me your power!", 128);
        }
        g_prev_space = curr_space;
    }
}

void main_draw(void) {
    tincle_clear((TinCLE_Color){0, 0, 40, 255});

    if (!g_llm_ready) {
        tincle_draw_text("Loading AI Model...", 20, 20, (TinCLE_Color){150, 150, 150, 255});
        return;
    }

    GozinakiStatus status = gozinaki_get_status();
    if (status == GOZINAKI_STATUS_EVALUATING) {
        tincle_draw_text("AI is thinking...", 20, 20, (TinCLE_Color){255, 255, 100, 255});
    } else {
        tincle_draw_text(gozinaki_get_text(), 20, 20, (TinCLE_Color){255, 255, 255, 255});
    }
}

void game_load(void) {
    // Initiate background download of the model
    g_model_file = tincle_fetch_file_async("model.gguf");

    tincle_add_state(0, main_update, main_draw);
    tincle_change_state(0);
}
// Note: Entry point (tincle_start) omitted for brevity. Follow standard SKILL.md template.
```

## 4. waffle (Word Arranger & Faux-Fluid Language Emulator)

**Module:** waffle (`waffle.dll` / `waffle.wasm`)
**Description:** Lightweight, zero-dependency, rule-based artificial chatterbot addon.

* **Overview & Usage:**
  The distribution includes `waffle.dll` for Windows and `waffle.wasm` for Web/WASM. By including `#include "waffle.h"`, AI agents can easily embed responsive, faux-fluid NPC conversations without the massive overhead of generative LLMs.
* **AI Coding Rule:**
  Unlike `gozinaki`, `waffle` does not require gigabytes of external `.gguf` weights. It operates on ultra-fast, memory-direct Pure C99 parsing using TSV dictionary files (`dict_base.tsv`, `user_dict.tsv`) loaded via TinCLE's native `tincle_load_asset`. It features dynamic learning capabilities (`waffle_learn`) and automatic particle-based noun extraction (助詞デリミタ) for Japanese, allowing it to echo user inputs seamlessly.

### 1. Extension API Reference

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `WaffleHandle waffle_create(void);` | **Chatterbot Init.** Allocates and returns a new Waffle context. |
| `void waffle_destroy(WaffleHandle handle);` | **Cleanup.** Frees the Waffle context and all dynamically allocated rules. |
| `void waffle_set_seed(WaffleHandle handle, unsigned int seed);` | **Seed Setter.** Sets the PRNG seed for deterministic random response selection. |
| `int waffle_load_dictionaries(WaffleHandle handle, const char* base_asset, const char* user_asset);` | **Asset Loader.** Loads TSV rule dictionaries via `tincle_load_asset`. `base_asset` is mandatory (e.g., `"dict_base.tsv"`). `user_asset` is optional (pass `NULL` if unused). Returns `1` on success, `0` on failure. |
| `int waffle_query(WaffleHandle handle, const char* lang_hint, const char* input_text, char* out_buffer, int out_buffer_size);` | **Dialogue Query.** The core chat function. `lang_hint` filters rules (e.g., `"ja"`, `"en"`, or `"all"`). Writes the NPC's response to `out_buffer`. Returns `1` if a keyword was matched, `0` if a fallback response (`*`) was triggered. |
| `int waffle_learn(WaffleHandle handle, const char* lang, const char* keyword, const char* response);` | **Dynamic Learning.** Explicitly teaches the bot a new response for a keyword in real-time. The rule is stored in memory and marked as "learned". Returns `1` on success. |
| `int waffle_save_learned(WaffleHandle handle, const char* user_filename);` | **Persistent Save.** Writes all dynamically "learned" rules to a TSV file (e.g., `"user_dict.tsv"`) using standard C file I/O, allowing knowledge to persist across game sessions. Returns `1` on success. |
| `const char* waffle_get_version(void);` | Returns read-only string of waffle version and prints creator credits to the console. |

### 2. Dictionary Format & Mechanics (TSV)

Waffle relies on line-based TSV (Tab-Separated Values) format: `<lang>\t<keyword>\t<response>\n`

* **Fallback (`*`):** If `<keyword>` is an asterisk (`*`), it serves as a random fallback response when no user keywords match.
* **Slot Extraction (`%s`):** If `<response>` contains `%s`, Waffle automatically extracts the relevant noun from the user's input and substitutes it.
  * *Japanese:* Automatically scans backwards from the matched keyword to find Japanese particles (e.g., が, を, は, も, なんか). Extracts the preceding noun (e.g., input: "リンゴが好き" -> Extracts "リンゴ" -> Response: "リンゴが好きなんだ！").
  * *English:* Extracts the space-delimited word immediately following or preceding the keyword.

### 3. Distribution

When using waffle, you must include either waffle.dll or waffle.wasm—whichever is appropriate for the target platform—along with its dictionary assets in your distribution.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`, `SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `waffle.dll`, `dict_base.tsv`, `user_dict.tsv` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `waffle.wasm`, `dict_base.tsv`, `user_dict.tsv` |

### 4. Standard Integration Boilerplate

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include "waffle.h"
#include <stdio.h>

static WaffleHandle g_waffle = NULL;
static char g_response[512] = "Talk to me!";

void main_update(float dt) {
    // Example: Query the bot with Space key
    if (tincle_key_pressed(SDL_SCANCODE_SPACE)) {
        // Query in Japanese mode
        waffle_query(g_waffle, "ja", "私はリンゴが好きなんだ", g_response, sizeof(g_response));
    }

    // Example: Teach the bot a new word with L key
    if (tincle_key_pressed(SDL_SCANCODE_L)) {
        waffle_learn(g_waffle, "ja", "みっちょ", "大天才だよ！");
        waffle_save_learned(g_waffle, "user_dict.tsv");
    }
}

void main_draw(void) {
    tincle_clear((TinCLE_Color){20, 20, 40, 255});
    tincle_draw_text(g_response, 50, 100, (TinCLE_Color){255, 255, 255, 255});
}

void game_load(void) {
    g_waffle = waffle_create();
    if (g_waffle) {
        waffle_set_seed(g_waffle, 12345);
        // Load base dictionary and existing learned user dictionary
        waffle_load_dictionaries(g_waffle, "dict_base.tsv", "user_dict.tsv");
    }
    tincle_add_state(0, main_update, main_draw);
    tincle_change_state(0);
}
```

## 5. babka (BASIC Ancient Bytecode Kernel Actuator)

**Module:** babka (`babka.dll` / `babka.wasm`)
**Description:** Non-blocking Retro BASIC Virtual Machine (**ORB: Omnipotent Realizable BASIC**) featuring 4 screen modes, hybrid 256-color live palette + direct 24/32-bit `RGB`/`RGBA`, UTF-8/IME console input, USF sprite fonts, 64 sprites, a real-time `SPEED` controller, sequential persistent file I/O, and 12-channel PSG (`emu2149`) + YM2413 (OPLL) FM (`emu2413`) MML audio.

* **Dedicated Talent Chip Required:** **`SKILL_BK.md`**
* **Overview & Usage:**
  The distribution includes `babka.dll` (for Windows) and `babka.wasm` (Emscripten dynamic side module for Web/WASM), paired with `#include "libs/babka.h"`. Developers and AI agents write games or interactive apps as line-numbered UTF-8 BASIC scripts (`AUTOEXEC.BAS`) hosted by a minimal fixed C99 `game.c` wrapper alongside a default USF font (`font.json`, `font_p0.png`).
* **AI Coding Rule (CRITICAL — MUST READ `SKILL_BK.md`):**
  The complete ORB language specification, C99 host API (`libs/babka.h`), `game.c` template, `exsass.txt` / `emcass` packaging rules, all built-in statements/functions, 12-channel MML syntax, and error codes are maintained in the dedicated skill sheet **`SKILL_BK.md`**.
  Whenever a user requests building a game or application in BASIC (ORB) with `babka`, **DO NOT guess legacy BASIC syntax or host boilerplate from memory—immediately load and strictly follow `SKILL_BK.md`** as the Single Source of Truth. *(For human-readable language manuals, `ORB.md` and `ORB_JP.md` are also provided.)*

### Distribution

When using `babka`, you must include either `babka.dll` or `babka.wasm`—whichever is appropriate for the target platform—in your distribution (with `AUTOEXEC.BAS`, `font.json`, and `font_p0.png` packed into `game.data` / `index.data`). An example of the minimum set of distribution files is as follows.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`, `SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `babka.dll` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `babka.wasm` |
