---
name: tincle-js-hl
description: Use when building, creating, or packaging 2D web and standalone desktop games using TinCLE JS ecosystem. Pure Vanilla JS Canvas game generation with jgrscnzl, rjasplns, churro, and audio tools. [TinCLE Additional Skill v0.16]
---

# SKILL_HL.md - TinCLE JS High Level Skills Sheet

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

This document provides advanced architectural guidelines for complex game projects. The instructions here override or extend the base `SKILL.md`.

Create a self-contained single-file Canvas game in pure JavaScript without external libraries or assets.

## 1. Code & Environment Rules
- **Header Line (Absolute Requirement)**: Line 1 (the very first character of the file) MUST start with `// "Game Title" (width, height)`. Do NOT put any decorative comments, empty lines, or header banners above this line. (e.g. `// "My Game" (640, 480)`).
- **Canvas**: Assume `<canvas id="tinclecanvas">` exists. Obtain context via `document.getElementById('tinclecanvas').getContext('2d')`.
- **Output & Multi-File Script Architecture**:
  * For standard single-file projects, output the primary entry point as `game.js`.
  * **Automatic Script Injection (Multi-File Support)**: Both `jgrscnzl` and `rjasplns` automatically scan the project root directory for all other `.js` files and inject them as `<script type="text/javascript" src="filename.js"></script>` tags **above (before)** the primary target script (`game.js`).
  * Subdirectories for `.js` files are strictly prohibited; all split scripts MUST be placed directly in the project root.
  * When splitting complex projects across multiple files (e.g., `constants.js`, `player.js`, `levels.js`), define global classes, utilities, or data objects inside those auxiliary files so that `game.js` can cleanly consume them.
  * Never wrap generated code with HTML or Markdown formatting tags in source files.
- **Audio Options (Hybrid)**: You can implement audio using either of the following approaches (or combine both):
  1. **Procedural Web Audio API**: Generate real-time BGM and sound effects procedurally using Web Audio API oscillators (`OscillatorNode`, `GainNode`, etc.).
  2. **External Audio Assets**: Load and play pre-rendered audio files (`.ogg` / `.wav`) using standard HTML5 Audio or Web Audio API buffer decoding. All external audio files MUST be generated or formatted at a **44100 Hz** sample rate. You can generate BGM using `pisstrak` (`SKILL_PT.md`) and sound effects using `fartbox` (`SKILL_FB.md`).
- **Graphics**: Draw all visuals purely using 2D Canvas primitives. Combine multiple geometric shapes/paths to compose expressive characters, sprites, and objects.
- **Windows Packaging Prerequisite**: Building the standalone Windows desktop version via `rjasplns` strictly requires NW.js (https://nwjs.io/). The directory of `nw.exe` binary MUST be added to the system PATH.
- **UI & HUD Overlay Rules (Canvas Visibility Protection)**:
  * **Single Canvas Standard**: Render in-game HUDs, scores, and text directly onto `#tinclecanvas` (or via Three.js textures/sprites) whenever possible. Avoid dynamically creating redundant full-screen overlay `<canvas>` elements.
  * **No Full-Screen Opaque/Shaded Backdrops**: If creating HTML/DOM UI overlays (e.g. menus, dialogue boxes, HUDs), the root overlay container MUST be completely transparent (`background: transparent; pointer-events: none;`). NEVER apply full-screen dark gradients, solid backgrounds, or shaded overlays (e.g. `inset: 0` with dark backgrounds) that cover the entire viewport, as they will obstruct and black out the 3D/2D game canvas in web browser environments.
  * **Self-Contained UI Panels**: Confine background colors and panels strictly to the specific UI boxes, cards, or buttons themselves (e.g., small dialog cards or HUD panels), ensuring the underlying `#tinclecanvas` remains 100% visible across all game scenes (TITLE, PLAY, RESULT).

## 2. Game Scene Flow (Mandatory)
Structure your code with a clear state machine supporting at least 3 distinct scenes:
1. `TITLE`: Shows the game title, controls guide, and "Press Space / Click to Start".
2. `PLAY`: The core playable game loop.
3. `RESULT`: Shows Game Over or Stage Complete screen, final score/records, and "Press R / Space to Restart".

## 3. Rapid Development Workflow & Audio Creation

TinCLE JS adopts an instant, web-first development loop. During active game development, always iterate, test, and debug in the browser environment. Do NOT package into Windows executables during everyday iteration.

### Builder Execution Role

- If you have command-line execution capability (Agent Mode / Terminal), execute the relevant build commands directly and verify output.
- If you are a conversational chat AI, provide the commands clearly and instruct the user to execute them.

### A. Web Iteration Loop (`jgrscnzl` & `churro`)

1. **Generate Web Output**:
  ```bash
  jgrscnzl game.js
  ```
  * Generates `index.html` from `tinclejs.html`.
2. **Launch Local Server & Browser (`churro`)**:
  ```bash
  churro [port_number]
  ```
  * Default port is `8000`.
  * Automatically launches the default web browser with Cross-Origin Isolation headers (`COOP`/`COEP`).
  * Press any single terminal key to cleanly terminate the server.
  * Open Developer Tools (F12) to inspect JavaScript console logs, exceptions, and live performance.

### B. Audio Asset Generation Workflows (`pisstrak` & `fartbox`)

When utilizing external audio assets rather than real-time Web Audio API oscillators, generate them using these standalone CLI utilities:

* **Audio Sample Rate (Strict Requirement)**:
  ALL audio files (both BGM `.ogg` and Sound Effects `.wav`/`.ogg`) MUST be encoded at a **44100 Hz** sample rate to prevent pitch distortion and speed glitches.
* **BGM Synthesis (`pisstrak`)**:
  Renders MML score files into `.ogg` or `.wav` using SoundFont synthesis:
  ```bash
  pisstrak <input.mml> [output.wav|output.ogg] [tail_seconds] [soundfont.sf2]
  ```
  * *Example:* `pisstrak mybgm.mml mybgm.ogg 0 soundfont.sf2` (Passing `0` tail_seconds is ideal for seamless looping BGM).
  * **[AI Rule]**: If you need to compose a new MML score from scratch, you **MUST** read and follow `SKILL_PT.md`.
* **Sound Effect Generation (`fartbox`)**:
  Renders procedural 1-shot sound effects instantly into 16-bit 44.1kHz `.wav` files via named presets:
  ```bash
  fartbox -t <preset_type> -o <output.wav>
  ```
  * *Example:* `fartbox -t explosion -o explosion.wav`
  * *Available Preset Types (`-t`):* `coin`, `laser`, `explosion`, `powerup`, `hit`, `jump`, `blip`, `random`.
  * **[AI Rule]**: For complex parameter authoring, fine-tuning, or mutations (`.fart`), you **MUST** consult `SKILL_FB.md`.

---

## 4. Production Release Pipelines (Distribution Rules)

When generating final release builds or instructions, the AI **MUST** follow this structured multi-step pipeline.

### Step 1: Prep Assets & Credit Attribution Mandate (`CREDITS.txt`)

* **Enforce `CREDITS.txt` Attribution**:
  `CREDITS.txt` is distributed alongside both the Windows Desktop and Web builds, and its contents are viewable via the dedicated credit button at the bottom of the game screen on Web.
  * **Agentic AIs**: Must inspect and update `CREDITS.txt` in the root directory, listing attributions for ALL third-party assets, fonts, audio, and libraries added to the project. If license origins are missing, explicitly ask the user before finalizing.
  * **Chat-based AIs**: Must strongly urge the user to add all third-party assets/libraries to `CREDITS.txt` and provide a ready-to-copy snippet when context is available.

### Step 2: Web Browser Build Path

1. **Compile Web Target**:
  ```bash
  jgrscnzl game.js
  ```
  * Generates `index.html`.
2. **Distribution Checklist (Web)**:
  Place the following items into the release folder (e.g., `_release_web`):
    * `index.html`
    * `game.js`
    * `libs/` directory
    * All audio/image assets referenced by `game.js`
    * `.htaccess` (Ensures Cross-Origin Isolation on Apache servers)
    * `CREDITS.txt`
    * `readme.txt`

### Step 3: Windows Desktop Standalone Build Path (`rjasplns`)

1. **Compile Executable**:
  ```bash
  rjasplns game.js [game.exe]
  ```
  * Generates standalone `game.exe` (defaults to `game.exe` if omitted).
  * Automatically scans the current directory and bundles all game assets whose file extensions match those listed line-by-line in `exsass.txt` directly into the executable package. Ensure all used asset extensions (e.g. `.png`, `.ogg`, `.wav`) are registered in `exsass.txt`.
  * Automatically collects all necessary NW.js binaries (`.dll`, `.bin`, `.dat`, `.pak` files) and the `locales/` directory into the working directory.
2. **Generate Icon (`icondom`)**:
  If a multi-resolution `.ico` icon is not yet prepared, convert your source image:
  ```bash
  icondom icon.png icon.ico
  ```
3. **Embed Resources (`poopee`)**:
  Embed the application icon and Windows manifest directly into the generated binary:
  ```bash
  poopee game.exe icon.ico manifest.xml
  ```
  *(Pass `"none"` if skipping either icon or manifest).*
4. **Distribution Checklist (Windows)**:
  Place the following items into the release folder (e.g., `_release_win`):
    * `game.exe` (with embedded icon, manifest, and internal asset bundle)
    * All NW.js runtime dependencies (`.dll`, `.bin`, `.dat`, `.pak` files collected by `rjasplns`)
    * `locales/` directory
    * `CREDITS.txt`
    * `readme.txt`
  *(Do NOT ship raw audio or image asset files in this folder; they are already packed inside the executable).*

### Step 4: Mandatory `readme.txt` Specifications

AI must explicitly include these details in `readme.txt` or platform descriptions:

* **Controls Disclosure**:
  * **Windows Desktop**: Mention standard window / fullscreen controls (toggle fullscreen via `F11` or platform default shortcuts).
  * **Web Browser**: Mention that clicking the on-screen canvas button toggles Fullscreen mode.
* **Creator Copyright**:
  * Display the user's copyright notice (`Copyright (C) 2026 [Developer/Creator Name]`).

### Step 5: Final Archive Packaging (`wipee`)

Automate the final ZIP archive generation using `wipee` (Whole Integration Packager for Executable Environment):

1. **Standard Packaging (Web / itch.io / General Distribution)**:
  ```bash
  wipee game_web.zip _release_web
  wipee game_win.zip _release_win
  ```
  * Generates a clean, standard Deflate ZIP archive.
2. **Scanner Bypass Packaging (Desktop Distribution Only - Optional)**:
  When distributing Windows desktop packages where over-reactive antivirus heuristic scanners might interfere, use the `-m` flag to activate Malformed ZIP mode:
  ```bash
  wipee game_win_secured.zip _release_win -m
  ```
  * **[CRITICAL] Never use `-m` for Web / itch.io builds.** Web hosting platforms require standard ZIP headers for automatic extraction.

### Components Authorized for Redistribution

The following components are fully authorized for royalty-free distribution within end-user game release packages, subject strictly to the condition that **`CREDITS.txt` is visibly included**:
  * `.htaccess`
  * `libs/` directory (including Three.js runtime files)
  * All NW.js runtime files generated by `rjasplns` (`*.dll`, `*.pak`, `*.dat`, `*.bin`, and `locales/`)
  * `CREDITS.txt`
  * `readme.txt`

## 5. Custom GLSL Shader Development & Validation (`pisschk`)

When implementing advanced visual effects using custom GLSL shaders (such as Three.js `ShaderMaterial` or raw WebGL fragment shaders loaded from external `.frag` or `.glsl` files), all fragment shaders **MUST** be validated using `pisschk` to prevent cross-platform rendering failures (e.g. driver-specific bugs or reserved word crashes).

### A. Shader Writing Rules for TinCLE JS

1. **WebGL / GLES Compliance**: Write shaders compatible with WebGL 1.0 (GLES2) / WebGL 2.0 standards.
2. **Explicit Precision Header**: Unlike the C version of TinCLE, there is no automatic header injection. When writing raw standalone fragment shader files (`.frag` / `.glsl`), you **MUST** include precision specifiers explicitly at the top:
   ```glsl
   precision mediump float;
   ```
3. **Canvas Coordinates**: Canvas rendering resolution is strictly fixed to the declared game dimensions (`WIDTH`, `HEIGHT`). Therefore, standard normalized coordinates can be calculated directly via `gl_FragCoord.xy / u_resolution.xy` (or standard UV pass-throughs like `vUv`).

### B. Shader Validation Workflow (`pisschk`)

To guarantee that shaders run flawlessly across NVIDIA, strict AMD Radeon drivers, and diverse browser WebGL runtimes, validate every shader file before referencing it in `game.js`:
```bash
pisschk <shader_file_path>
```

* **Example**: `pisschk assets/shaders/water.frag`
* **Validation Coverage**:
  * **Strict Radeon Compliance**: Enforces rigorous GLSL syntax and blocks vendor-specific extensions and reserved identifier collisions (e.g., using `active` as a variable name).
  * **Web / GLES Compliance**: Verifies WebGL/GLES2 suitability.
* **Exit Codes**:
  * `0`: All inspection checks PASSED successfully.
  * `1`: Syntax/compilation errors DETECTED.
  * `2`: File I/O or argument error.

### [CRITICAL AI RULE FOR SHADER CODE]

Whenever the AI agent creates or modifies external GLSL shader files (`.frag` / `.glsl`), it **MUST** execute `pisschk` to verify that the shader passes all checks cleanly before finalizing the build.

## 6. Tools for Human Users

While TinCLE JS is optimized for autonomous AI operations, this suite of utilities provides human developers with seamless project onboarding and physical archiving tools. AI agents should refer to this section when assisting human developers with environment setup or offline archival.

### A. popcorn (Project Onboarding & Workspace Generator)

* **Overview**: The primary entry-point onboarding tool located at the root of the distribution package. It completely eliminates manual folder creation and toolchain copying.
* **Key Feature**: Launches a lightweight desktop GUI dialog for selecting or creating a project directory. Upon selection, `popcorn` automatically prepares a clean workspace by deploying the TinCLE JS toolchain (`jgrscnzl`, `rjasplns`, runtime templates, audio utilities) and talent chip skill sheets (`SKILL.md`, `SKILL_HL.md`, etc.). It concludes by prompting the user to hand `SKILL.md` to their AI assistant to start game development immediately.
* **Execution Mode**: Desktop GUI application (launch via double-click).

### B. lollipop (Physical Archive PDF Generator)

* **Overview**: A physical code preservation utility that converts source code (such as `game.js`) into continuous-form, line-printer zebra paper-styled landscape PDFs.
* **Key Feature**: Protects completed game source code from digital bit-rot, storage corruption, and cloud obsolescence by formatting lines onto alternating white and light-gray horizontal bands with generous character spacing—ideal for physical paper printing, offline tangible archiving, and manual red-pen code reviews.
* **Execution Mode**: Command-line tool.
* **Usage**:
  ```bash
  lollipop.exe <input_source_file> <output.pdf> [font.ttf]
  ```
  * *Example*: `lollipop.exe game.js archive_game.pdf`
  * *Note*: If `font.ttf` is omitted, `lollipop` automatically uses the default `font.ttf` located in the TinCLE JS workspace.

## 7. Pre-Installed Libraries & Modular Expansion

TinCLE JS bundles a standardized suite of 100% offline, local, non-copyleft JavaScript libraries inside the `./libs/` directory.

- **Supported Libraries**:
  * **Three.js** (v0.186.0): 3D graphics rendering, scene graphs, cameras, and loaders (GLTF / VRML).
  * **Planck.js** (v1.3.0): 2D rigid-body Box2D physics simulation for canvas games.
  * **cannon-es** (v0.20.0): Lightweight 3D Box3D rigid-body physics coupled with Three.js.
  * **Howler.js** (v2.2.4): Cross-browser Web Audio management, spatial sound, and seamless BGM/SE playback.
  * **Obelisk.js** (v1.2.1): Pseudo-3D isometric pixel-art and destructible voxel canvas rendering.

### [MANDATORY AI RULE FOR LIBRARIES]

To prevent token bloat and maintain context precision, the full architectural patterns, boilerplate templates, and usage rules for these libraries have been modularized into **`SKILL_LIB1.md`**.
Whenever you build games or features utilizing any of the above libraries, you **MUST** load, read, and strictly follow the implementation guidelines in **`SKILL_LIB1.md`**.
