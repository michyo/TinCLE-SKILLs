This is part 3 of 3 (API Reference & Boilerplate) of the specification for "TinCLE". Now all specifications are fully provided. Memorize this content and switch your status into game code generation mode. Please reply with nothing but the exact text below:

"[ TinCLE Specification 3/3: All setup including Boilerplate complete. Ready to build games. Please give your instructions! ]"

---

## 5. Full API Reference (Function Specifications)

This section provides the comprehensive API reference available when writing game logic within `game.c`.
*Note: Although these functions are exported via `__declspec(dllexport)` within the engine (`tincle.dll`), they can be invoked seamlessly as standard C functions on the game application side.*

### 5.1. Lifecycle & System Control

#### `void tincle_start(TinCLE_InitCallback init_cb, const char* title, bool is_debug, int width, int height);`

* **Description:** The most critical function of the engine. It automatically executes environment initialization, asset loading, transitions into the main game loop, and handles terminal cleanup operations in a single one-shot sequence.
* **Arguments:**
* `init_cb`: A user-defined callback function pointer tasked with initial loading and asset setups (typically, pass `game_load`).
* `title`: A string literal specifying the window title text.
* `is_debug`: A boolean toggle for Debug Mode. When set to `true`, the engine automatically spawns and docks a standard Windows command prompt window (Debug Console) to stream standard outputs such as `printf`. **Set to `false` for the production/release build to hide the command console completely.**
* `width` / `height`: The virtual target resolution dimensions of the game canvas (strictly defaulted to `640` and `480`).

#### `void tincle_add_state(int state_id, TinCLE_UpdateCallback update_cb, TinCLE_DrawCallback draw_cb);`

* **Description:** Binds logic updating and rendering drawing callbacks to a specific game state identifier, executed sequentially every frame when the target state is active.
* **Arguments:**
* `state_id`: An arbitrary integer constant or a user-defined enumeration value representing the state.
* `update_cb`: A logic update function pointer adhering strictly to the signature: `void update(float dt);`.
* `draw_cb`: A rendering function pointer adhering strictly to the signature: `void draw(void);`.

#### `void tincle_change_state(int state_id);`

* **Description:** Instantly switches the currently active game scene (active state) to the designated state. **CRITICAL CRITERIA: You must call this function at the very end of your `game_load()` sequence to activate the initial game state, otherwise the viewport will remain indefinitely black without starting.**
* **Arguments:**
* `state_id`: A pre-registered state identifier to transition into.

---

### 5.2. Input (Device Control)

#### `int tincle_key_pressed(int scancode);`

* **Description:** Queries whether a specific keyboard key is currently being held down.
* **Arguments:**
* `scancode`: A hardware-independent key identification code. **Crucial:** You must strictly pass the `TINCLE_KEY_*` constant macros defined in Section 4.4 (e.g., `TINCLE_KEY_SPACE`, `TINCLE_KEY_RIGHT`). Do not pass raw SDL internal scan codes.

#### `void tincle_get_mouse(int* x, int* y);`

* **Description:** Retrieves the current spatial coordinates of the mouse cursor, dynamically translated and scaled to align with the game's internal virtual resolution.
* **Arguments:**
* `x` / `y`: Integer pointers where the mapped virtual coordinates will be written.

#### `int tincle_mouse_pressed(int button_type);`

* **Description:** Queries whether a specific mouse button is currently being held down.
* **Arguments:**
* `button_type`: The preset mouse button identification macro defined in Section 4.2 (e.g., `TINCLE_MOUSE_LEFT`, `TINCLE_MOUSE_MIDDLE`, `TINCLE_MOUSE_RIGHT`).

#### `int tincle_pad_pressed(int pad_button);`

* **Description:** Queries whether a specific button on a connected gamepad is currently being held down. Input tracking is automatically normalized using standard Xbox controller layouts.
* **Arguments:**
* `pad_button`: The gamepad button macro defined in Section 4.3 (e.g., `TINCLE_PAD_A`, `TINCLE_PAD_START`, `TINCLE_PAD_LEFT`).

#### `float tincle_pad_axis_x(void);`

* **Description:** Measures the current horizontal (X-axis) tilt of the gamepad's left analog stick, returning a floating-point value clamped between `-1.0f` (full left) and `1.0f` (full right).
* **Notes for AI:** The engine internally implements a deadzone filter (clamping any absolute mechanical values below 5000 directly to `0.0f`). AI agents can safely map this return value directly into movement calculations without factoring in controller drift counter-measures.

#### `float tincle_pad_axis_y(void);`

* **Description:** Measures the current vertical (Y-axis) tilt of the gamepad's left analog stick, returning a floating-point value clamped between `-1.0f` (full up) and `1.0f` (full down).
* **Notes for AI:** Implements the exact same integrated deadzone optimization as the horizontal axis tracker.

---

### 5.3. Graphics & Rendering Control

#### `void tincle_clear(TinCLE_Color color);`

* **Description:** Fills and clears the entire screen with the specified color. This function **must without exception** be invoked at the absolute beginning of the `draw` callback function on every single frame.
* **Arguments:**
* `color`: A `TinCLE_Color` structural data instance (or one of the preset color macros defined in Section 4.5).

#### `void tincle_load_font(const char* filename);`

* **Description:** Loads a TrueType font file (`.ttf`) to establish the internal standard text rendering pipeline. TinCLE maintains a single, high-performance global font handle. Calling this function multiple times will automatically release the previously loaded font and overwrite it with the new asset.
* **Arguments:**
* `filename`: The relative path or filename of the `.ttf` asset (supports automatic extraction from packaged `game.data` distribution archives).

#### `void tincle_draw_text(const char* text, int x, int y, int size_type, TinCLE_Color color);`

* **Description:** Renders crisp, anti-aliased typographic text on the screen with native UTF-8 multi-byte character encoding support.
* **Arguments:**
* `text`: The string literal or character array to be rendered.
* `x` / `y`: The starting spatial coordinates on the internal virtual resolution canvas.
* `size_type`: The designated font sizing token macro defined in Section 4.1 (`TINCLE_FONT_S`, `TINCLE_FONT_M`, or `TINCLE_FONT_L`).
* `color`: The structural color properties used to tint the text characters.

#### `void tincle_draw_text_center(const char* text, int x, int y, int size_type, TinCLE_Color color);`

* **Description:** Renders crisp, anti-aliased typographic text horizontally and vertically centered at the specified spatial coordinates on the internal virtual resolution canvas. This is highly optimized for titles, UI labels, or button text where precise geometric centering is required. Fully supports native UTF-8 multi-byte character encoding.
* **Arguments:**
  * `text`: The string literal or character array to be rendered.
  * `x` / `y`: The target spatial coordinates that act as the exact central anchor point of the rendered text block.
  * `size_type`: The designated font sizing token macro defined in Section 4.1 (`TINCLE_FONT_S`, `TINCLE_FONT_M`, or `TINCLE_FONT_L`).
  * `color`: The structural color properties used to tint the text characters.

#### `int tincle_load_image(const char* filename);`

* **Description:** Ingests a graphical image file (e.g., PNG, JPG) into the hardware rendering pipeline and caches it as an optimized texture resource.
* **Arguments:**
* `filename`: The filename or directory path of the source image asset (fully optimized to auto-extract from packaged `game.data` files seamlessly).
* **Return Value:** Returns a uniquely assigned structural integer identifier (Texture ID) tracking the asset. Returns `-1` if the asset initialization or loading routine fails.

#### `void tincle_draw_image(int img_id, int x, int y);`

* **Description:** Renders a pre-loaded texture resource onto the virtual canvas surface at its original unscaled (100% / 1:1) default dimensions.
* **Arguments:**
* `img_id`: The cached texture index integer originally retrieved via `tincle_load_image`.
* `x` / `y`: The spatial alignment coordinates on the internal virtual resolution layout.

#### `void tincle_draw_image_ex(int img_id, int x, int y, int w, int h, double angle);`

* **Description:** Executes advanced, high-performance rendering configurations including spatial scaling (stretching/shrinking dimensions) and hardware rotational transformations.
* **Arguments:**
* `img_id`: The target texture source index integer.
* `x` / `y`: The spatial coordinate position tracking the upper-left (top-left) anchor point of the target rendering bounding box.
* `w` / `h`: The dynamic width and height scaling dimensions applied to the output render.
* `angle`: The rotational angle calculated in degrees clockwise (0 to 360).

---

### 5.4. Audio (Music & Sound Effects) Control

#### `void tincle_play_music(const char* filename);`

* **Description:** Ingests and spins up background music (BGM) utilizing standard Ogg Vorbis compression formatting configured for infinite looping. Initializing a new music file stream automatically terminates and frees the memory allocation of any previously running track.
* **Arguments:**
* `filename`: The relative system path referencing the source `.ogg` audio file.

Note: There is no command to load and prepare background music in advance. Playback begins immediately when you pass a filename to `tincle_play_music`.

#### `void tincle_stop_music(void);`

* **Description:** Instantly halts any currently playing background audio stream and safely unloads it from core memory allocations.

#### `int tincle_load_sound(const char* filename);`

* **Description:** Reads a concise sound effect (SE) clip formatted as a standard WAV or compressed Ogg Vorbis file, assigning a unique structural channel lookup ID.
* **Arguments:**
* `filename`: The relative system path referencing the target sound asset file.
* **Return Value:** Returns the newly registered sound identifier index tracking the clip. Returns `-1` if initialization or storage routines fail.

#### `void tincle_play_sound(int se_id);`

* **Description:** Dispatches a designated sound effect instance for immediate playback. The engine natively structures an automatic multi-mixing array supporting up to 16 concurrent operational sound channels, ensuring overlapping assets do not clip or terminate early.
* **Arguments:**
* `se_id`: The specific sound effect target index integer originally registered via `tincle_load_sound`.

---

### 5.5. System Information Retrieval

#### `struct SDL_Renderer* tincle_get_renderer(void);`

* **Description:** Exposes and passes the underlying core `SDL_Renderer` structural pointer initialized by the engine environment. This allows advanced workflows or AI agents to directly invoke native SDL2 APIs (`SDL_RenderFillRect`, `SDL2_gfx` geometric primitives, etc.) to construct bespoke layouts or graphic functions directly on the frame canvas.
* **Return Value:** A functional native structural pointer referencing the active `SDL_Renderer`.

#### `const char* tincle_get_version(void);`

* **Description:** Returns a structured string literal indicating the active structural engine build and specification version number of TinCLE.
* **Return Value:** A read-only constant character pointer detailing the version tracking value (e.g., `"0.01"`).

---

## 6. Mandatory Rules

### 6.1. Mandatory Coding Rules for `game.c`

When generating a `game.c` file from scratch or modifying an existing codebase, AI agents and developers **must comply 100%** with the following structural mandates:

1. **Unified Entry Point Cross-Platform Conditional Structure:** The application entry point must handle cross-platform compilation flawlessly using conditional compilation directives. Inside `game.c`, you **must strictly implement** the dual entry point architecture utilizing `#ifdef __EMSCRIPTEN__` for Web/WASM targets and `WinMain` with `<windows.h>` for native Windows targets.

Exact code template required in `game.c`:
```c
#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) {
  tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480);
  return 0;
}
#else
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
  tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480);
  return 0;
}
#endif
```

For the Windows native build path, you **must include `<windows.h>`** at the top of the file (wrapped cleanly within the non-emscripten block) to ensure flawless native `-mwindows` compilation.
2. **Framerate Independence (Delta Time Multiplication):** All spatial movements, animations, physics, and custom timer calculations **must without exception** be multiplied by `float dt` (the elapsed frame time in seconds) passed down into the `update` callback.
3. **Hybrid Keyboard/Gamepad Movement Logic:** When implementing spatial locomotion routines, it is highly recommended to design a modern hybrid processing layout: establish the gamepad analog stick tilt (`tincle_pad_axis_x / y`) as the baseline input vector, and immediately overwrite/synthesize it with maximum constants (`1.0f` / `-1.0f`) if keyboard or pad directional keys are currently engaged.
4. **Absolute Asset Loading Pre-requisite:** Within the `game_load` procedure, you **must explicitly invoke `tincle_load_font("font.ttf");` as the absolute first operational line**. Failing to initialize this default font handle will cause an immediate engine fatal crash during any downstream text rendering routines. Consequently, the minimum asset architecture of any distribution must contain at least one valid `.ttf` file.
5. **Conditional Use of Native SDL APIs:** If advanced routines require direct access to SDL operational structures (such as scancodes), you must conditionally switch the header paths using `#ifdef __EMSCRIPTEN__` to ensure cross-platform compatibility. For Windows native builds, include headers from the local directory using double quotes (e.g., `#include "libs/SDL.h"` or `#include "libs/SDL_scancode.h"`). For Emscripten Web builds, you must include the Emscripten-bundled SDK headers using angle brackets (e.g., `#include <SDL2/SDL.h>`). However, **you must never write code that directly manipulates or alters the core SDL window handles, active renderers, or primary event processing systems**. All application-level game logic and rendering flows must be fully abstracted and wrapped within native TinCLE APIs.
6. **Mandatory State Registration inside `game_load`:**
  * You MUST call `tincle_add_state()` exclusively WITHIN the `game_load()` function.
  * DO NOT invoke `tincle_add_state()` inside `main()` or `WinMain()`. The internal engine architecture initializes the state handles within `tincle_start()`, meaning any downstream states registered before `tincle_start()` will be completely wiped out, resulting in a fatal black screen.

### 6.2. Mandatory AI Coding Constraints & Rules

To ensure 100% compilation on the first attempt without compilation errors, the AI must strictly adhere to these 8 coding rules:

1. **NO SEARCH CITATIONS IN CODE:** Never include text-based source citations, inline footnotes, or reference annotations (such as `[cite: 1]`, `[1]`, or `(Source: ... )`) anywhere inside or outside the code block. These annotations instantly cause syntax errors in C. Output ONLY valid, clean C source code.
2. **Absolute Pure C (C99 Standard):** Do not mix C++ syntax (e.g., no classes, no namespaces).
3. **Double Quotes & Platform-Specific Headers:** Always include engine core headers using `#include "libs/tincle.h"`. When including raw SDL headers, you must cleanly branch your code using `#ifdef __EMSCRIPTEN__` — use `#include "libs/SDL.h"` or `#include "libs/SDL2_gfxPrimitives.h"` or etc. for Windows native and `#include <SDL2/SDL.h>` or `#include <SDL2/SDL2_gfxPrimitives.h>` or etc. for Emscripten Web targets.
4. **Standard Library Inclusions:** If you utilize mathematical operations (such as `sinf`, `cosf`, `sqrtf`, `fabsf`), you must explicitly `#include <math.h>`. Do not assume standard headers are pre-included.
5. **Mandatory Font Preloading:** The framework requires an operational font to initialize text routines. You must execute `tincle_load_font("font.ttf");` immediately at the top of the `game_load()` lifecycle sequence before loading other images or sounds.
6. **Strict State-Separation Model:** Do not write a chaotic single-loop game block. Split game states cleanly (e.g., Title Screen, Gameplay Loop, Game Over Screen) using the built-in State Management API.
7. **Always Use Approved Build Tools (`tinclec` & `emcass`):** When guiding the user on how to build the game, instruct them based on the target platform. Instruct them to execute the bundled `tinclec` tool for native Windows desktop builds, and the `emcass` tool for Web/WASM compilation. Never instruct them to use raw `tcc` or raw `emcc` commands directly.
8. **Never Confuse Asset Utilities:**
   * `asspack.exe` is used to pack all game media assets (images, fonts, sounds) into a secure `game.data` package.
   * `embedres.exe` is used ONLY for embedding binary metadata (like `icon.ico` and application manifest strings) directly into the executable file header. It cannot process game media assets.

---

## 7. Creation of Release Version (Distribution Instructions)

When ready to build the final production release for distribution, follow this strict five-step pipeline:

* **Asset Credit Management:** If you recognize, extract, or utilize third-party assets from a provided ZIP file or external sources, you must automatically append the appropriate credit and attribution information to `CREDITS.txt`. Do not leave `CREDITS.txt` as the default template if new third-party assets are introduced.

### Step 1: Hide the Debug Console
Locate the `tincle_start` call inside the conditional entry points (`main` for Web or `WinMain` for Windows) in `game.c`. Change the third argument (`is_debug`) from `true` to `false`.
```c
// Example: Hiding the runtime debug log or console output
tincle_start(game_load, "My Ultimate Game", false, 640, 480);
                                            // Set this to false for production!
```

### Step 2: High-Density Asset Packing via `asspack` (for Windows)

To bundle all external textures, audio clips, and font files into an uncrackable, optimized unified package for Windows Desktop deployment, execute the `asspack` command in the terminal. This creates a single consolidated virtual file called `game.data`.

```bash
> asspack font.ttf player.png enemy.png bgm.ogg shoot.wav
```

*Note: Once `game.data` is generated, the Windows engine will automatically look inside this packed binary container. However, if a raw asset file exists locally, it takes precedence over the packed asset. When distributing your game, pack all assets into `game.data` and do not include raw asset files in the release archive.*

### Step 3: Web/WASM Production Build via `emcass` (for Web)

For web browser deployment, the asset packaging and compilation are unified into a single command using `emcass`. You do not need to use `asspack` manually for Web builds; `emcass` handles both asset preloading and generation of the web deliverables automatically.

```bash
emcass index.html "My Ultimate Game" main.c player.c stage.c
```

*Note: This command scans your local development directory, compiles the code via the Emscripten toolchain, packs all detected assets into `index.data`, and uses `template.html` to output the complete browser-ready package with the mandatory fixed base name `index`.*
*Requirements: When executing a Web build, ensure that `CREDITS.txt` is placed in the exact same folder as the source code before running the build. This is strict because emcass requires `CREDITS.txt` in that directory to display credits properly; otherwise, the web-version credit screen will be blank.*

### Step 4: Final Deployment Package Checklist (Windows Desktop Target)

Distribute the final Windows desktop build by packaging the following **"8 structural items"** inside a ZIP archive. Do not include individual raw source assets, header files, or `.c` files in the player package:

1. `game.exe` (The compiled game binary generated by `tinclec` - can be renamed)
2. `game.data` (The packed resource binary containing all assets generated by `asspack.exe`)
3. `tincle.dll` (The TinCLE core engine runtime)
4. `SDL2.dll` (Official SDL2 library)
5. `SDL2_ttf.dll` (Official SDL_ttf library)
6. `SDL2_gfx.dll` (Official SDL2_gfx library)
7. `CREDITS.txt` (License documentation for the engine and libraries)
8. `readme.txt` (The instruction manual file for the game itself)

Note: Create and prepare a `readme.txt` file containing a description of the game to be distributed.

### Step 5: Final Deployment Package Checklist (Web Browser Target)

Distribute the final Web browser build by packaging the following **"5 structural items"** generated by `emcass` into a single ZIP archive for platform deployment (e.g., itch.io HTML5 project upload):

1. `index.html` (The web page housing the game canvas - MUST NOT be renamed)
2. `index.js` (The JavaScript glue-code generated by Emscripten)
3. `index.wasm` (The compiled WebAssembly binary core)
4. `index.data` (The virtual filesystem package containing preloaded assets)
5. `CREDITS.txt` (License documentation for the engine, Emscripten components, and libraries)

### MANDATORY INSTRUCTIONS FOR `readme.txt` CREATION

When the AI agent or developer prepares the `readme.txt` (or platform game page description), the following specifications **must be explicitly detailed without exception**:

1. **Input Shortcuts & Window Controls Disclosure:**
* **For Windows Desktop Players:** Clearly state that pressing **`Alt + Enter`** toggles between Fullscreen and Windowed mode, and pressing **`Alt + Backspace`** immediately resets the game window to its default resolution scale. (Since these core shortcuts are invisible, players have no way of knowing them unless documented here).
* **For Web Browser Players:** Clearly state that players can toggle Fullscreen mode by clicking the dedicated HTML canvas fullscreen button provided on the game page.

2. **Mandatory Game Creator Copyright Attribution:**
* The `readme.txt` **must clearly display the user's/developer's own copyright notice** as the primary game creator (e.g., `Copyright (C) 2026 [Your Name / Team Name]`).
* **CRITICAL AI WARNING:** When creating code or release readmes, do NOT just only append the TinCLE framework copyright notice (`Copyright (C) 2026 michyo`). While the engine license requires credit attribution to the engine author, the game itself belongs to the game creator. The AI must explicitly separate the Game Creator Copyright from the Engine Framework Credits and ensure the game author's identity is clearly defined.

---

## 8. Standard Implementation Boilerplate Code for `game.c`

This section provides the comprehensive, bulletproof source code boilerplate template that AI agents must utilize as the structural foundation when spinning up a brand new game project from scratch.

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"

// [TCC WORKAROUND] Prevent 'M_PI redefined' warning from SDL2_gfx
#undef M_PI

// Automatically switch between headers for the Web version and the Windows version
#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL2_gfxPrimitives.h> // The web version uses Emscripten's built-in gfx
#else
  #include "libs/SDL2_gfxPrimitives.h" // The Windows version uses the gfx files in the lib folder
  #include <windows.h>                 // Required for native Windows structures
#endif

#include <stdio.h>
#include <math.h>

// [TCC WORKAROUND] Fix 'undefined symbol sinf' error in Windows TCC environments.
// Maps the C99 float function 'sinf' to the standard double 'sin' via compiler macro.
#ifndef sinf
#define sinf(x) ((float)sin((double)(x)))
#endif

// Global System Variables & Options
static SDL_Renderer* renderer = NULL;
static float g_player_x = 320.0f;
static float g_player_y = 240.0f;
static float g_game_time = 0.0f; // Used for sine wave animations
static int g_img_player = -1;

// ============================================================================
// State: Title Screen (State ID: 0)
// ============================================================================
void title_update(float dt) {
  // Advance to Gameplay State via Space key or Gamepad Start button
  if (tincle_key_pressed(TINCLE_KEY_SPACE) || tincle_pad_pressed(TINCLE_PAD_START)) {
    tincle_change_state(1);
  }
}

void title_draw(void) {
  tincle_clear(TINCLE_COLOR_BLACK);

  // MANDATORY: Always use tincle_draw_text_center for perfect UI text alignment!
  tincle_draw_text_center("YOUR_GAME_TITLE", 320, 180, TINCLE_FONT_L, TINCLE_COLOR_WHITE);
  tincle_draw_text_center("PRESS SPACE TO START", 320, 300, TINCLE_FONT_M, TINCLE_COLOR_GREEN);
}

// ============================================================================
// State: Gameplay Loop (State ID: 1)
// ============================================================================
void play_update(float dt) {
  // Accumulate delta time for dynamic calculations
  g_game_time += dt;

  // Framerate Independence: Speed is always multiplied by delta time (dt)
  float move_speed = 200.0f;
  if (tincle_key_pressed(TINCLE_KEY_LEFT)  || tincle_pad_pressed(TINCLE_PAD_LEFT))  g_player_x -= move_speed * dt;
  if (tincle_key_pressed(TINCLE_KEY_RIGHT) || tincle_pad_pressed(TINCLE_PAD_RIGHT)) g_player_x += move_speed * dt;
  if (tincle_key_pressed(TINCLE_KEY_UP)    || tincle_pad_pressed(TINCLE_PAD_UP))    g_player_y -= move_speed * dt;
  if (tincle_key_pressed(TINCLE_KEY_DOWN)  || tincle_pad_pressed(TINCLE_PAD_DOWN))  g_player_y += move_speed * dt;

  // Returning to the Title Screen sequence
  if (tincle_key_pressed(TINCLE_KEY_ESCAPE) || tincle_pad_pressed(TINCLE_PAD_BACK)) {
    tincle_change_state(0);
  }
}

void play_draw(void) {
  // Clear display background using deep navy color parameters
  tincle_clear((TinCLE_Color){20, 20, 50, 255});
  tincle_draw_text("GAME PLAYING", 20, 20, TINCLE_FONT_M, TINCLE_COLOR_GREEN);

  // Render player asset dynamically
  if (g_img_player != -1) {
    tincle_draw_image(g_img_player, (int)g_player_x, (int)g_player_y);
  } else {
    tincle_draw_text("P", (int)g_player_x, (int)g_player_y, TINCLE_FONT_M, TINCLE_COLOR_RED);
  }

  // [EXAMPLE 1] Render a filled square using native SDL API
  SDL_Rect rect = { 100, 100, 50, 50 };
  SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
  SDL_RenderFillRect(renderer, &rect);

  // [EXAMPLE 2] Render a floating alpha ellipse using SDL2_gfx primitives
  filledEllipseRGBA(renderer, 400, 300, 50, 25, 255, 0, 0, 128);

  // [EXAMPLE 3] Render a filled polygon triangle using SDL2_gfx filledTrigonRGBA.
  // This demonstrates how to construct a triangle instead of utilizing a non-existent "triangleRGBA" function.
  // The top vertex floats up and down smoothly via sinf() from math.h!
  int tri_top_y = 150 + (int)(sinf(g_game_time * 5.0f) * 15.0f);
  filledTrigonRGBA(renderer,
                   500, tri_top_y,  // Vertex 1 (Top, moving dynamically)
                   460, 200,        // Vertex 2 (Bottom Left)
                   540, 200,        // Vertex 3 (Bottom Right)
                   0, 255, 255, 200 // Color: Cyan with Alpha
  );
}

// ============================================================================
// System Lifecycle: Initialization & Asset Preloading
// ============================================================================
void game_load(void) {
  // Cache the underlying core SDL_Renderer context to enable native graphics extensions
  renderer = tincle_get_renderer();

  // MANDATORY MANDATE: Font asset initialization must be executed first to avoid fatal engine crashes
  tincle_load_font("font.ttf");

  // Optional downstream asset loading queues
  g_img_player = tincle_load_image("player.png");

  // Bind and register the operational lifecycle callback procedures to their respective scene handles
  tincle_add_state(0, title_update, title_draw);
  tincle_add_state(1, play_update, play_draw);

  // CRITICAL MANDATE: You must switch to your starting state at the end of game_load!
  tincle_change_state(0);
}

// ============================================================================
// Main Entry Point
// ============================================================================
#ifdef __EMSCRIPTEN__
// Standard entry for Web (Emscripten) mode
int main(int argc, char* argv[]) {
  tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480);
  return 0;
}
#else
// WinMain entry for Windows (TCC, etc.) mode
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
  tincle_start(game_load, "YOUR_GAME_TITLE", true, 640, 480);
  return 0;
}
#endif
```
