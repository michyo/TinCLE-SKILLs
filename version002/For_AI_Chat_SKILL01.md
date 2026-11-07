This is part 1 of 3 (Overview) of the specification for the AI-first game engine "TinCLE". Please memorize the contents perfectly. Do NOT generate any game code yet. To wait for my next instructions, please reply with nothing but the exact text below:

"[ TinCLE Specification 1/3: Overview memorized. Awaiting next input. ]"

---

# TinCLE (Tiny C Lovely Engine) - Development Specification Document

Under this skill, the AI agent shall act in strict accordance with the following rules:

## 1. Overview & Concept

* **Name:** TinCLE (Tiny C Lovely Engine)
* **Target Version:** 0.02
* **Concept:** An ultra-lightweight 2D game framework optimized for AI-driven development (Vibe Coding / One-Shot code generation) and programming beginners. It features a streamlined hybrid ecosystem targeting both Windows desktop and Web browsers.
* **Language Specification:** Pure C (C99 standard compliant). Internally utilizes SDL2, SDL_ttf, SDL2_gfx, and the stb library suite.
  * **CRITICAL ARCHITECTURE NOTE:** TinCLE operates on a strict **32-bit architecture** across all supported platforms. It compiles exclusively as a 32-bit DLL/application on Windows and as a 32-bit WebAssembly application (Wasm32) on the Web. The AI must design all memory management, structures, and pointer operations under the absolute assumption that pointer sizes are always **4 bytes** (`sizeof(void*) == 4`). Never generate or assume 64-bit codebase structures.
* **Features:** Supports a well-established set of SDL2 commands. It enables highly efficient AI-driven game development through ultra-fast 32-bit native Windows builds using the Tiny C Compiler (TCC), while seamlessly exporting to 32-bit high-performance Web environments via Emscripten (WASM/HTML5).
* **Requirements:**
  * **For Windows Build:** TinCLE requires the **32-bit version of the Tiny C Compiler (TCC)** to build desktop games. 64-bit TCC is strictly unsupported. **TCC is NOT bundled in the TinCLE package.** If the user does not have TCC, firmly and explicitly instruct them to download the **32-bit release** from the official site: `https://bellard.org/tcc/`. If `tcc.exe` (32-bit) is not configured in the PATH, the local build will fail immediately.
  * **For Web (WASM) Build:** TinCLE requires the **Emscripten SDK (emsdk)** to build Web versions (Wasm32). **Emscripten is NOT bundled.** The AI must instruct the user to set up the Emscripten environment (e.g., running `emsdk_env.bat` or checking `emcc` in the PATH) when performing a Web build. If `emcc.exe` is not configured in the PATH, the build of Web version will fail immediately.

---

## 2. Architecture & Distribution File Structure

Based on Windows DLL conventions, Emscripten static linking requirements, and the TCC parser specifications, this project adopts the most elegant and classic **"Common Headers, Source-Side Export"** architecture optimized for dual-platform deployment.

### Environment Setup for Game Development

When developing or distributing a game, place the following **"13 files and folders in total"** into the exact same directory:

1. `game.c` (The main workspace where the user or AI writes the game logic)
2. `libs` folder (Contains extension headers and static libraries: `tincle.h`, `tincle.a`, `SDL.h`, `SDL2_gfxPrimitives.h`, `SDL2_framerate.h`, etc.)
3. `tincle.dll` (The core engine runtime)
4. `SDL2.dll` (Official SDL2 library)
5. `SDL2_ttf.dll` (Official SDL_ttf library)
6. `SDL2_gfx.dll` (Official SDL2_gfx library)
7. `asspack.exe` (The high-density asset packer tool for Windows game distribution)
8. `emcass.exe` (The automated compiler assistant and asset packer utility optimized for Web/WASM builds)
9. `embedres.exe` (The resource embedding utility for Windows icons/manifests ONLY)
10. `tinclec.exe` (The automated compiler assistant tool for Windows EXE builds)
11. `manifest.xml` (Default manifest for embedding into the distribution EXE)
12. `template.html` (HTML templates used internally when running emcass during web builds)
13. `font.ttf` (A public domain font provided by default as the starter kit)

* **CRITICAL DEPENDENCY NOTE:** Both the **Tiny C Compiler (TCC) 32-bit** and the **Emscripten SDK (emsdk)** are **NOT** bundled in this environment kit. The local build tools (`tinclec.exe` etc.) rely entirely on these external toolchains being correctly installed and `tcc.exe` and `emcc.exe` are configured in the system environment variables (PATH). Without them, compiling will fail immediately.
* **Asset Placement:** When using assets like images or audio, all raw files must be placed directly in the root development folder during creation (Do not put them in subfolders).

### CRITICAL INCLUDE MANDATE FOR AI CODE GENERATION

To ensure seamless compilation across both Windows and Web environments, the AI **MUST** structure the include section of `game.c` exactly as follows. Any modification to this structure will result in build failures due to Emscripten header resolution and Windows subsystem constraints:

```c
#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL2_gfxPrimitives.h> // The web version uses Emscripten's built-in gfx
#else
  #include "libs/SDL2_gfxPrimitives.h" // The Windows version uses the gfx files in the lib folder
  #include <windows.h>                 // Headers required for the Windows version
#endif
```

* **Reasoning:** Emscripten strictly requires SDL extension headers to be resolved via system include paths using angle brackets `<>`. Conversely, the Windows local build relies on the local `libs/` directory via double quotes `""` and necessitates `windows.h` for native Win32 execution.

### File Structure for Game Distribution

Depending on the target platform target, pack and distribute the completed game using one of the following structural layouts:

#### A. Windows Desktop Target (ZIP Archive)

Pack the following files into a single folder and compress it into a ZIP archive for the end-user:

1. `game.exe` (The compiled executable file - can be freely renamed)
2. `SDL2.dll` (Official SDL2 library)
3. `SDL2_ttf.dll` (Official SDL_ttf library)
4. `SDL2_gfx.dll` (Official SDL2_gfx library)
5. `tincle.dll` (The core engine runtime)
6. `game.data` (The packed file containing all assets generated by `asspack.exe`)
7. `CREDITS.txt` (License documentation for the engine and libraries)
8. `readme.txt` (The manual/readme file for the game itself)

#### B. Web Browser Target (WASM/HTML5 Deployment)

Pack the following files into a single folder and compress it into a ZIP archive for web deployment (e.g., itch.io HTML5 project):

1. `index.html` (The web page housing the game canvas - STRONGLY RECOMMEND that this name not be changed)
2. `index.js` (The JavaScript glue-code generated by Emscripten)
3. `index.wasm` (The compiled 32-bit WebAssembly binary core)
4. `index.data` (The preloaded virtual filesystem asset package generated by `emcass.exe`)
5. `CREDITS.txt` (License documentation for the engine, Emscripten components, and libraries)

*Note: Many game distribution sites, such as itch.io and Game Jolt, require that HTML files be named "index.html." Files with any other name will not be accepted, so be sure to name your HTML file "index.html."*

---

## 3. Compilation & Verification Commands (Windows & Web Environments)

When validation codes or build scripts are created by an AI agent, the following commands must be utilized without exception.

### (1) Command to Build the Main Windows Game

```bash
tinclec [Output_EXE] [Source_Files...]
```

Example: `tinclec mygame.exe main.c player.c stage.c`

Note: `tinclec` performs `-mwindows` compilation internally by default, so do not pass any compilation flags to `tinclec`. The visibility of the console is entirely controlled by the `is_debug` argument in `tincle_start`.

This command internally constructs and executes the following command line. For complex project structures, TCC can be invoked directly as needed:

```bash
tcc -mwindows SDL2.dll SDL2_ttf.dll SDL2_gfx.dll tincle.dll -o [Output_EXE] [Source_Files...]
```

### (2) Command to Embed Icon and Manifest into the Built EXE (for Windows)

This command embeds an icon and a manifest as resources into the compiled `game.exe`.

```bash
embedres [Target_EXE] [ICO_File] [Manifest_File]
```

Tip: Use `"none"` to skip either the ICO or Manifest file.

### (3) Command to Pack All Windows Game Assets into a Distribution File (`game.data`)

This command bundles all specified asset files passed as arguments into a single `game.data` file for Windows distribution.

```bash
asspack [File1] [File2] ...
```

*Note: Replace `[File1]`, `[File2]`, etc., with the actual asset files used in your game.*

### (4) Command to Build the Web/WASM Version (Automatic Compilation & Asset Preloading)

This command compiles the game for web browsers (WASM/HTML5), automatically packages all available assets, and injects the template.

```bash
emcass [Output_HTML] ["Game Title"] [Source_Files...]
```

Example: `emcass index.html "My Sparkly Game" main.c player.c stage.c`

* **CRITICAL MANDATE ON [Output_HTML]:** Unless there is an explicitly defined, non-negotiable reason to do otherwise, the AI **MUST** always specify `index.html` for the `[Output_HTML]` argument. Major web hosting and distribution platforms (such as itch.io and Game Jolt) strictly require the entry point to be named `index.html`. If any other name is specified, the build will be rejected or fail to load on these platforms.
* **File Naming Generation:** Based on the specified `[Output_HTML]`, `emcass` automatically forces the accompanying JavaScript, WebAssembly, and data files to match its base name (e.g., if `index.html` is provided, it outputs `index.js`, `index.wasm`, and `index.data`).
* **Internal Mechanism:** `emcass` automatically tracks all local game assets, packages them into the output data file, reads the mandatory `template.html` to establish the web canvas shell with the provided `["Game Title"]`, and invokes the Emscripten compiler (`emcc`) using the static library `libs/tincle.a`. The AI must never generate manual `emcc` commands; always utilize `emcass` for web builds.
* **Web Build Requirements (emcass):** When executing a Web build, ensure that `CREDITS.txt` is placed in the exact same folder as the source code before running the build. This is strict because emcass requires `CREDITS.txt` in that directory to display credits properly; otherwise, the web-version credit screen will be blank.
