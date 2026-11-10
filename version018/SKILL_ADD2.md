---
name: tincle-add2
description: Use when packaging production release builds for Windows/Web, compiling Win32 resources (`opercrem`), utilizing special purpose utilities for dependency checking, asset handling, text substitution, image normalization, and audio normalization (`depurant`, `tbrzilve`, `oxtailst`, `ebisen`, `jalebi`), or guiding human developer tools (`cococake`, `popcorn`, `churro`, `lollipop`). Covers asset packing, resource/version embedding, flat multi-stream archiving, deployment pipelines (`asspack`, `emcass`, `wipee`), GUI utilities, inline text manipulation, and audio trimming/LUFS equalizing. [TinCLE Additional Skill v0.18]
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
2. **Check Dependencies:** Run the compiled executable in a clean environment to ensure no hidden dependencies (e.g., missing DLLs) using `depurant`:
  ```bash
  depurant game.exe
  ```
  *(If it crashes here, you are missing a DLL or using a dynamic runtime. Fix compiler options like `-static` or bundle the required DLL).*
3. **Generate Icon:** If a multi-size `.ico` is not yet prepared, convert an image via `icondom.exe`:
  ```bash
  icondom icon.png icon.ico
  ```
4. **Embed Resources (Optional):** Embed the generated icon and Windows manifest:
  ```bash
  poopee game.exe icon.ico manifest.xml
  ```
  (Use `"none"` to skip ico/manifest).
5. **Pack Assets:** Pack files for final distribution:
  * **Auto Pack (Recommended):** Simply run `asspack` with no arguments to automatically scan the folder and pack all assets/shaders whose file extensions match those registered line-by-line in `exsass.txt`:
  ```bash
  asspack
  ```
  * **Manual Pack:** Alternatively, specify files explicitly: `asspack font.ttf cursor.png bgm.ogg [images/shaders/sounds...]`
  *(Creates `game.data`. Do not ship raw assets).*
6. **ZIP Checklist (8 Items Only):** `game.exe`, `game.data`, `tincle.dll`, `SDL2.dll`, `SDL2_ttf.dll`, `SDL2_gfx.dll`, `CREDITS.txt`, `readme.txt`.

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

## 2. opercrem (TinCLE Minimalist Resource Compiler)

`opercrem` (OPtimalized Enhanced Resource Compiler - REs-file Maker) is a standalone, ultra-minimalist Windows resource compiler and COFF object generator. Designed to replace bloated GNU `windres` or MSVC `rc.exe`, `opercrem` converts human/AI-written resource definition scripts (`.rc`) directly into:
  1. **COFF Object Files (`.obj` / `.o`)**: Single `.rsrc` section COFF format, allowing Tiny C Compiler (`tcc`) and GCC to link resources directly without intermediate tools (`cvtres`).
  2. **Win32 Binary Resource Files (`.res`)**: Standard binary resource files.

### 2.1 CLI Syntax & Usage

```bash
opercrem <input.rc> -o <output.obj|.o|.res> [-m32|-m64]
```

* **Output Selection**: Determined strictly by the output file extension:
  * `.obj` or `.o`: Generates a single `.rsrc` section COFF object file ready for direct linking with `tcc` or `gcc`.
  * `.res`: Generates a standard 32-bit Win32 binary resource file.
* **Architecture Flags (`-m32` / `-m64`)**:
  * Default behavior: Automatically matches the host binary architecture (e.g., 32-bit `opercrem` defaults to 32-bit COFF, 64-bit `opercrem` defaults to 64-bit COFF).
  * Explicit override: Specify `-m32` (x86 `0x014C`) or `-m64` (AMD64 `0x8664`) when cross-compiling.

### 2.2 `.rc` Script Syntax Specification

`opercrem` intentionally discards legacy Win32 RC grammar and complex macros. It parses a clean, line-oriented command structure. Lines starting with `#` or `//` and empty lines are treated as comments. Double quotes (`"..."`) are required for strings and file paths containing spaces.

#### Supported Directives:

1. **`ICON <ID> "<path_to_ico>"`**
  * Embeds a multi-resolution `.ico` file. Automatically parses and splits icon frames into `RT_ICON` (Type 3) entries and creates an `RT_GROUP_ICON` (Type 14) entry with the specified numeric ID.
  * *Example:* `ICON 1 "assets/icon.ico"`
2. **`MANIFEST <ID> "<path_to_xml>"`**
  * Embeds an application manifest (`RT_MANIFEST` / Type 24). Typically ID is `1` for executables.
  * *Example:* `MANIFEST 1 "manifest.xml"`
3. **`RCDATA <ID> "<path_to_binary>"`**
  * Embeds arbitrary binary assets as raw data (`RT_RCDATA` / Type 10) accessible via `FindResource`/`LockResource`.
  * *Example:* `RCDATA 101 "assets/bgm.ogg"`
4. **`RAWDATA "<TYPE_NAME>" <ID> "<path_to_binary>"`**
  * Embeds binary data under a custom resource type name string.
  * *Example:* `RAWDATA "SHADER" 1 "shaders/post.glsl"`
5. **`VERSION "<Key>" "<Value>"`**
  * Automatically constructs and formats standard `VS_VERSION_INFO` blocks (including `VS_FIXEDFILEINFO`, `StringFileInfo` [041104B0 Japanese/Unicode], and `VarFileInfo`).
  * If `FileVersion` or `ProductVersion` keys are provided (format: `"X.Y.Z.W"`), their numerical components are extracted into binary version fields.
  * *Example:*
    ```text
    VERSION "FileVersion" "1.0.0.0"
    VERSION "ProductVersion" "1.0.0.0"
    VERSION "FileDescription" "TinCLE Game Release"
    VERSION "LegalCopyright" "Copyright (C) 2026 Developer"
    VERSION "ProductName" "My TinCLE Game"
    ```

### 2.3 Ready-to-Use Example (`sample.rc`)

AI agents should generate `.rc` files using this template when resource embedding is needed:
```text
# TinCLE Resource Script
ICON 1 "icon.ico"
MANIFEST 1 "manifest.xml"
VERSION "FileVersion" "1.0.0.0"
VERSION "ProductVersion" "1.0.0.0"
VERSION "FileDescription" "TinCLE Game Executable"
VERSION "LegalCopyright" "Copyright (C) 2026 michyo"
VERSION "ProductName" "TinCLE Project"
```

### 2.4 Build Integration Workflow with `tinclec`

To compile and link a complete Windows executable with icons, manifests, and version properties in a single automated step without post-processing, use `opercrem` combined with TinCLE's standard compiler wrapper `tinclec`:

```bash
# Step 1: Compile .rc to COFF .obj (.o)
opercrem resource.rc -o resource.obj

# Step 2: Compile & link via tinclec (Transparently forwards resource.obj to TCC)
tinclec game.exe game.c resource.obj
```

* **How it works**: `tinclec` automatically wraps your target executable name with `-o game.exe`, injects runtime SDL dependencies, and forwards additional arguments (like `resource.obj`) directly to `tcc.exe`.
* **Alternative Direct TCC Invocation (Advanced / Diagnostic):**
  ```bash
  tcc -mwindows SDL2.dll SDL2_ttf.dll SDL2_gfx.dll tincle.dll -o game.exe game.c resource.obj
  ```

## 3. Special-Purpose & Advanced Utilities

This section details auxiliary and specialized standalone utilities that operate outside the standard linear build pipeline. AI systems may elect to leverage these tools when specific architectural requirements (such as collision-free data streaming, indexing-based asset bundling, or multi-version snapshotting) align with their project design.

> **Operational Directive for AI Assistants:**
> * **Autonomous / Agentic AIs (Direct Tool Execution):** If you possess direct OS command-line or sub-process execution capabilities, invoke these utilities directly to manipulate workspaces and assemble custom asset packages autonomously.
> * **Interactive Chat AIs (Human-in-the-Loop Interaction):** If you operate as a conversational chat interface without direct terminal access, you MUST clearly explain the purpose of the tool to the user, formulate the exact CLI command strings, and instruct the user to execute them within their local project directory.

### 3.1 tbrzilve (Flat-Root Multi-Stream ZIP Archiver)

`tbrzilve` (Tabrizi Lovuez: Tiny BRilliant ZIp LoVely Encloser) is a specialized, minimalist CLI archiving utility built on `miniz`. It flattens all input file paths down to their base names and packs them directly into the root directory of a standard ZIP archive (`MZ_DEFAULT_COMPRESSION`), intentionally tolerating duplicate filenames without collision checks or warnings.

#### CLI Syntax & Usage

```bash
tbrzilve <output.zip> <file1> [file2 ...]
```

* `<output.zip>`: Target archive path to create.
* `<file1> [file2 ...]`: List of files to pack into the archive root. Parent directories are automatically stripped (e.g., `a/data.bin` and `b/data.bin` are both written as `/data.bin`).

#### Core Architectural Characteristics & AI-First Advantages

1. **Deterministic Root Flattening (`get_basename`):**
  * Regardless of where source files reside on the host file system, `tbrzilve` extracts only their base file names and places them directly at the ZIP archive root (`/`). Subdirectory structures are completely discarded.
2. **Zero-Warning Duplicate Filename Tolerance (Multi-Stream Archive):**
  * Standard GUI extraction software enforces unique filenames, but the raw ZIP format specification inherently permits identical filenames across central directory entries. `tbrzilve` exploits this feature to pack identically named files (e.g., `stage1/data.bin` and `stage2/data.bin`) into the exact same archive root without renaming, overwriting, or throwing errors.
  * Files are stored sequentially in the exact order specified on the command line.

#### When the AI Agent MUST / SHOULD Use `tbrzilve`

* **Collision-Free Dynamic Packaging:** When bundling assets from different staging directories where identical filenames exist, and you want to bypass generating complex path-renaming scripts or token-heavy string manipulation logic.
* **Index-Based Asset Streaming:** When building custom asset packs where the TinCLE engine, custom C data loaders, or WebAssembly stream decoders inspect the archive by **entry index order (0-th entry, 1-st entry)** rather than unique string lookup keys.
* **Multi-Version Resource Snapshotting:** When bundling generational asset variations (e.g., `v1/config.bin`, `v2/config.bin`) within a single archive for sequential state playback or generational rollbacks.

### 3.2 oxtailst (Oxtail stew: Overwriter and eXchanger for Textfile's Assigned Inline Letters Substitution Tool)

`oxtailst` is a blazing-fast, Pure C99 command-line text substitution utility designed to safely and precisely overwrite assigned inline string patterns across source files, batch scripts, and markdown documentation without relying on heavy regular expression engines or multi-step token replacements.

#### CLI Syntax & Usage

```bash
oxtailst <input_file> "<search_string>" "<replace_string>"
```

* `<input_file>`: The target text file to be modified (e.g., `.c`, `.h`, `.md`, `.bat`, `.html`).
* `"<search_string>"`: The exact literal string to locate.
* `"<replace_string>"`: The exact literal string to overwrite with.

#### Core Architectural Characteristics & AI-First Advantages

1. **Automatic Backup & In-Place Execution:**
Before any modification occurs, `oxtailst` automatically generates a backup of the original file by appending `.bak` to the filename. It then processes the substitutions and overwrites the target file in place. If no matches are found, the file remains untouched and no backup is created.
2. **Safe Literal Substitution (No Regex Overhead):**
It performs strictly exact literal string matching. This prevents catastrophic cascading failures often caused by unescaped regular expression characters (like `.` or `*`) when manipulating dense codebase variables or sound parameter configs (like `p_freq_ramp = -0.150000`).
3. **UTF-8 Encoding Safety for Multi-Byte Characters:**
**[CRITICAL RULE]** When writing batch scripts (`.bat`) that utilize `oxtailst` to manipulate files containing multi-byte characters (such as Japanese text or emojis), you MUST ensure the Windows command prompt environment is set to UTF-8. You MUST insert `chcp 65001 > nul` at the beginning of the batch script prior to running `oxtailst` to completely prevent encoding corruption and mojibake.

#### When the AI Agent MUST / SHOULD Use `oxtailst`

* **Automated Version Bumping:** When building release pipelines (batch files) that must uniformly update version numbers across HTML templates, C/C++ headers, and markdown documentations simultaneously.
* **Targeted Parameter Swapping:** When generating automated scripts to swap specific hardcoded values (like API keys, endpoint URLs, or strict numerical constants) without risking the destruction of surrounding context.

### 3.3 ebisen (Easy Best-fit Image Size Equalizing Normalizer)

`ebisen` is a blazing-fast, pure C99 command-line image resizing utility designed to normalize scattered, raw visual assets into unified dimensions. Built without heavy external dependencies and utilizing high-fidelity resampling (Mitchell/Lanczos via the `stb_image` library), it ensures that game assets generated by AI or sourced from varied libraries maintain crisp, professional quality while fitting perfectly into the engine's strict dimension requirements.

#### CLI Syntax & Usage

```bash
ebisen <input_file> <target_w> <target_h> <mode> [output_file_optional]
```

* `<input_file>`: The source image file to resize.
* `<target_w>` & `<target_h>`: The desired output dimensions in pixels.
* `<mode>`: The resizing logic to apply (1 to 4).
* `[output_file_optional]`: (Optional) Explicit output file path. If omitted, defaults to `<input_file>_res.png`.

**Resizing Modes:**

* **Mode 1 (Fit):** Maintains aspect ratio, shrinking/expanding the image so it entirely *fits inside* the target dimensions. (Output size may be smaller than target).
* **Mode 2 (Crop):** Maintains aspect ratio, scaling the image to *completely fill* the target dimensions, automatically cropping any overlapping excess from the center. (Output size strictly matches target).
* **Mode 3 (Pad):** Maintains aspect ratio, fitting the image inside the target dimensions and padding the remaining empty space with solid black (Letterboxing). (Output size strictly matches target).
* **Mode 4 (Stretch):** Ignores aspect ratio, forcibly stretching the entire image to match the target dimensions. (Output size strictly matches target).

#### Core Architectural Characteristics & AI-First Advantages

1. **High-Fidelity Resampling in Pure C99:**
Bypassing bloated image processing runtimes, `ebisen` utilizes STB's high-quality Mitchell filter (equivalent to Lanczos) to prevent visual artifacting (like halos) when scaling down large AI-generated assets, ensuring pristine pixel delivery.
2. **Deterministic Layout Control:**
AI agents can select the exact normalization strategy required for the UI or sprite layer without relying on complex image-manipulation math or external GUI graphics tools.
3. **In-Place Output Optimization:**
By utilizing the optional 5th argument, AI agents can directly output the resized image to the final required filename (or overwrite the original) in a single command thrust. This eliminates the need for secondary file-renaming operations, optimizing context limits and token usage.

#### When the AI Agent MUST / SHOULD Use `ebisen`

* **Asset Normalization Pipelines:** When integrating multiple AI-generated graphics or disparate textures that must conform to a strict sprite grid or background resolution before being packed by `asspack`.
* **Batch Script Automation:** When generating `.bat` deployment scripts that need to instantly align entire directories of raw images into uniform dimensions directly from the command line.

### 3.4 jalebi (Jules Audio Lufs Equalizing & Balancing Improver)

`jalebi` is TinCLE's official command-line utility for automatically normalizing and trimming audio assets.

## Features

1. **Loudness Normalization:**
   Automatically equalizes overall loudness to approximately -15 LUFS, ensuring all BGM and sound effects are consistent and comfortable.

2. **Silence Removal (Trimming):**
   Automatically detects and removes absolute or near-silence at the start and end of the audio file, eliminating delay in sound effect playback and ensuring seamless loops.

3. **Standalone Single-Executable:**
   Built natively as a single pure C99 program without heavy external dependencies.

## Usage Instructions

```bash
jalebi <input.wav|input.ogg> <output.wav|output.ogg> [--keep-silence]
```

### Arguments:

- `input.wav` or `input.ogg`:
  The raw audio file to be processed. Currently, only standard `.wav` (PCM 16-bit) and `.ogg` formats are supported.

- `output.wav` or `output.ogg`:
  The destination file. The format is determined automatically by the extension provided. `jalebi` can easily convert formats (e.g. from `.wav` to `.ogg`) during processing.

- `--keep-silence`:
  An optional flag. By default, `jalebi` automatically trims silence from the beginning and end of the track. Include this flag if you want to bypass the trimming step and only apply the LUFS normalization.

### Example Workflows for AI Systems

**Normalizing a Sound Effect:**
When an AI generates an explosion sound effect, it can ensure the sound is punchy and without leading silence by running:
```bash
jalebi raw_explosion.wav ready_explosion.wav
```

**Normalizing Background Music without Trimming:**
If a track requires a specific silent padding to keep rhythm correctly, run:
```bash
jalebi bgm_raw.ogg bgm_final.ogg --keep-silence
```

## 4. Tools for Human Users

While TinCLE is optimized for autonomous AI operations, this suite of utilities provides human developers with seamless onboarding, pair-programming IDEs, local web testing environments, and physical archiving tools. AI agents should refer to this section when assisting human users with setup and GUI tool usage.

### 4.1 cococake (Human-AI Collaborative IDE)

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

### 4.2 popcorn (Project Onboarding & Workspace Generator)

* **Overview:** The primary entry-point onboarding tool located at the root of the distribution package. It eliminates manually copying compiler toolchains or creating directory structures.
* **Key Feature:** Opens a simple folder selection dialog with 32-bit and 64-bit architecture radio buttons. Selecting or creating a folder automatically deploys the corresponding TinCLE compiler toolchain, runtime DLLs, and talent chip (`SKILL.md`) into the target directory, displaying a prompt instructing the user to pass `SKILL.md` to their AI agent to begin development.
* **Execution Mode:** Desktop GUI application (double-click to launch).

### 4.3 churro (Zero-Friction Local HTTP Web Server)

* **Overview:** A standalone, cross-origin isolated local HTTP server utility for instantly testing Emscripten WebAssembly builds (`emcass`).
* **Key Feature:** Automatically injects required COOP/COEP isolation headers (`Cross-Origin-Opener-Policy: same-origin` / `Cross-Origin-Embedder-Policy: require-corp`) and launches the default web browser upon startup. Shutdowns cleanly by pressing any single terminal key (no `Ctrl+C` required).
* **Execution Mode:** Command-line tool.
* **Usage:** `churro [port_number]` (Default port is `8000`).

### 4.4 lollipop (Physical Archive PDF Generator)

* **Overview:** A long-term physical code preservation utility that converts source files into continuous-form, line-printer zebra paper-styled landscape PDFs.
* **Key Feature:** Protects master code assets from digital bit-rot, cloud shutdowns, and disk failures by formatting code onto alternating white and light-gray horizontal bands with wide letter spacing, optimized for paper printing and real-world red-pen reviews.
* **Execution Mode:** Command-line tool.
* **Usage:** `lollipop.exe <input.txt> <output.pdf> [font.ttf]`
* Note: If `font.ttf` is omitted, `lollipop` automatically uses the default `font.ttf` in the TinCLE root folder.
