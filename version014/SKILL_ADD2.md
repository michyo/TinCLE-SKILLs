---
name: tincle-add2
description: Use when packaging production release builds for Windows/Web or using human developer tools (`cococake`, `popcorn`, `churro`, `lollipop`). Covers asset packing, credits, deployment pipelines (`asspack`, `emcass`, `wipee`), and GUI utilities. [TinCLE Additional Skill v0.14]
---

# SKILL_ADD2.md - TinCLE Additional Skills [Release Pipelines & Human Tools]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

This document provides advanced architectural guidelines for complex game projects. The instructions here override or extend the base `SKILL.md`.

## 1. Production Release Pipelines (Distribution Rules)

When generating final release builds or instructions, the AI **MUST** follow this 5-step pipeline and enforce documentation mandates.

### Step 1: Prep Assets & Hide Console & Credit Attribution Mandate

* **Enforce `CREDITS.txt` Attribution**:
  **Important:** `CREDITS.txt` is included as an attached file when distributing the Windows version of the game, and is embedded as credits in the web version of the game, which can be viewed by clicking the button at the bottom of the game screen.
  * **Agentic AIs**: Must inspect and update `CREDITS.txt` in the root directory, listing attributions for ALL third-party assets, fonts, audio, and libraries added to the project. If any asset details or license origins are missing, the AI **MUST explicitly ask the user** for details before finalizing the release build.
  * **Chat-based AIs**: Must **strongly urge the user** to add all third-party assets/libraries to `CREDITS.txt`. If the AI has information or context about the assets used (e.g., from prior conversation), it **MUST provide a ready-to-copy example snippet** for `CREDITS.txt`.
* Ensure `cursor.png` and `exsass.txt` are configured in the project root.
* Set the 3rd argument (`is_debug`) of `tincle_start` to **`false`** in `game.c` to hide the command console.

### Step 2: Windows Desktop Build Path (ZIP Pack)

1. **Compile:** `tinclec game.exe game.c [other_sources.c/DLL_files/TCC_options...]`
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
2. **Compile & Pack:** `emcass index.html "Game Title" [Width] [Height] game.c [other_sources.c/WASM_files/EMCC_options...] [-pb]`
  * **[CRITICAL] Always output exactly as `index.html`.** Name modification is strictly forbidden for itch.io/web platforms. Automatically outputs `index.js`, `index.wasm`, and `index.data`.
  * [Width] and [Height] refer to the actual dimensions of the game screen in the web version. Specify values that match the game screen dimensions.
  * **[-pb Option (Thumbnail Capture Support)]:** Append the `-pb` flag if the target hosting platform requires `preserveDrawingBuffer: true` for automatic screen capture or thumbnails (e.g., PLiCy). If omitted, `emcass` defaults to high-performance/low-memory mode without buffer preservation.
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

### Components Authorized for Redistribution

All components listed below are fully authorized for royalty-free inclusion and distribution within end-user game release packages, subject strictly to the condition that **`CREDITS.txt` is visibly included or embedded** so that players and end-users can easily view it. Any inclusion or distribution of files, tools, or components not explicitly listed below in end-user game release packages is strictly prohibited.

> **Mandatory Attribution Rule:**
> * **Web/WASM Target:** `CREDITS.txt` is automatically embedded into `index.html` during the standard `emcass` build process and can be viewed via the dedicated button at the bottom of the game screen.
> * **Windows Desktop Target:** `CREDITS.txt` must be explicitly attached alongside the executable package in a root-accessible location.

#### 1. Files Authorized for Direct Attachment (Distribution Bundle)
The following runtime binaries, dynamic libraries, and configuration files may be freely attached and shipped inside the distribution package:
* `.htaccess`
* `cannoli.wasm`
* `gatochoc.wasm`
* `vtrushka.wasm`
* `cannoli.dll`
* `gatochoc.dll`
* `vtrushka.dll`
* `SDL2.dll`
* `SDL2_gfx.dll`
* `SDL2_ttf.dll`
* `tincle.dll`
* `CREDITS.txt`

#### 2. Components Authorized for Embedding (Binary & Asset Packages)
The following core assets, static libraries, headers, and templates may be directly embedded into data archives (`game.data` via `asspack`) or compiled directly into binary targets:
* `cursor.png`
* `font.ttf`
* `template.html`
* `manifest.xml`
* `CREDITS.txt`
* `tincle.a`
* All C header and source files located within the `libs/` directory

## 2. Tools for Human Users

While TinCLE is optimized for autonomous AI operations, this suite of utilities provides human developers with seamless onboarding, pair-programming IDEs, local web testing environments, and physical archiving tools. AI agents should refer to this section when assisting human users with setup and GUI tool usage.

### 2.1 cococake (Human-AI Collaborative IDE)

* **Overview:** A specialized desktop IDE designed for human-AI pair-programming. It unifies a syntax-highlighted C code editor (top-left), a command-line build console (bottom-left), and an embedded web browser dedicated to an AI chat assistant (right pane).
* **Key Feature:** Allows human creators to chat naturally with their preferred AI, edit/save C code on the fly, and compile/execute binaries in a single window without context switching.
* **Execution Mode:** Desktop GUI application (double-click to launch).
* **Configuration File (`cococake.ini`):** Located in the tool directory to customize workspace defaults.
  ```ini
  [Settings]
  AI_URL=https://gemini.google.com/
  TCC_PATH=C:\tcc32
  EMSDK_PATH=C:\emsdk
  ```
* `AI_URL`: The URL of the specific AI chat page to auto-load in the right-pane browser (e.g., ChatGPT, Claude, Gemini).
* `TCC_PATH`: Absolute path to the directory containing `tcc.exe` (Windows desktop compiler).
* `EMSDK_PATH`: Absolute path to the directory containing `emsdk.bat` (Emscripten WebAssembly toolchain).

### 2.2 popcorn (Project Onboarding & Workspace Generator)

* **Overview:** The primary entry-point onboarding tool located at the root of the distribution package. It eliminates manually copying compiler toolchains or creating directory structures.
* **Key Feature:** Opens a simple folder selection dialog with 32-bit and 64-bit architecture radio buttons. Selecting or creating a folder automatically deploys the corresponding TinCLE compiler toolchain, runtime DLLs, and talent chip (`SKILL.md`) into the target directory, displaying a prompt instructing the user to pass `SKILL.md` to their AI agent to begin development.
* **Execution Mode:** Desktop GUI application (double-click to launch).

### 2.3 churro (Zero-Friction Local HTTP Web Server)

* **Overview:** A standalone, cross-origin isolated local HTTP server utility for instantly testing Emscripten WebAssembly builds (`emcass`).
* **Key Feature:** Automatically injects required COOP/COEP isolation headers (`Cross-Origin-Opener-Policy: same-origin` / `Cross-Origin-Embedder-Policy: require-corp`) and launches the default web browser upon startup. Shutdowns cleanly by pressing any single terminal key (no `Ctrl+C` required).
* **Execution Mode:** Command-line tool.
* **Usage:** `churro [port_number]` (Default port is `8000`).

### 2.4 lollipop (Physical Archive PDF Generator)

* **Overview:** A long-term physical code preservation utility that converts source files into continuous-form, line-printer zebra paper-styled landscape PDFs.
* **Key Feature:** Protects master code assets from digital bit-rot, cloud shutdowns, and disk failures by formatting code onto alternating white and light-gray horizontal bands with wide letter spacing, optimized for paper printing and real-world red-pen reviews.
* **Execution Mode:** Command-line tool.
* **Usage:** `lollipop.exe <input.txt> <output.pdf> [font.ttf]`
* Note: If `font.ttf` is omitted, `lollipop` automatically uses the default `font.ttf` in the TinCLE root folder.
