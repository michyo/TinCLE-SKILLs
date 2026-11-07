# TinCLE.md - TinCLE information document Version 0.16

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

## 1. What is TinCLE?

### Game Engine of the AI, by the AI, for the AI.

**The World's First True "AI-First" Minimal Game Engine.**

TinCLE (Tiny C Lovely Engine) is an ultra-lightweight, high-performance game framework designed from the ground up for the era of Generative AI and "Vibe Coding."

While conventional "AI-assisted" game engines try to stuff AI assistants into bloated, multi-gigabyte GUI editors, TinCLE takes the complete opposite approach: **We redesigned the entire engine architecture to match what Large Language Models (LLMs) are already naturally best at.**

* Official Web Site: https://michyo.net/tincle/
* OFficial Release Page: https://michyox.itch.io/tincle
* Official Japanese Site: https://tincle.netlify.app/

---

### Core Philosophy & Key Attractions

#### 1. Zero Context Waste, 100% First-Try Success
Modern game engines melt your AI's context window with endless API wrappers, complex scene graphs, and thousands of pages of human-oriented documentation. TinCLE shatters this bloat. Built on Pure C (C99), native SDL2, and GLES2, TinCLE uses standard libraries that every major LLM on Earth has ingested billions of times during pre-training. The AI already knows how to write flawless TinCLE code before you even type your first prompt.

#### 2. "Talent Chips" (SKILL.md): Instant AI Mastery
TinCLE dispenses with hand-holding human manuals. Instead, it provides highly dense, LLM-optimized system directives called **"Talent Chips"** (`SKILL.md`, `SKILL_PT.md`, `SKILL_FB.md`, `SKILL_PCG.md`, `SKILL_AON1.md`, etc.). By dropping these chips into any external AI (ChatGPT, Claude, Gemini, DeepSeek, Copilot), the LLM instantly transforms into a legendary, zero-hallucination TinCLE Master Developer, Sound Designer, Composer, and UI Architect.

#### 3. One-Click Hybrid Cross-Compilation (Win32 / Win64 / WebAssembly)
Powered by a razor-thin compiler environment (TinyCC for Windows desktop and Emscripten for WebAssembly), a single `game.c` source cross-compiles seamlessly across 32-bit/64-bit Windows desktop native EXEs and high-performance Web WASM targets in under a second—without changing a single line of code.

#### 4. The Sweets-Series All-In-One Toolchain (100% Offline & Local)
TinCLE ships with a comprehensive suite of single-purpose, hyper-efficient execution tools:
* **`tinclec` & `emcass`**: One-command automated compilers for Windows EXE and Web WASM (`index.html`).
* **`asspack` & `exsass.txt`**: Automatic asset packer that fuses raw graphics, audio, and shaders into a tight, single binary.
* **`pisstrak` & `fartbox`**: Procedural SoundFont MML music renderer and 1-shot synthesizer for instant audio generation.
* **`churro`**: Offline local web server automatically injecting COOP/COEP HTTP isolation headers for zero-headache WebAssembly testing.
* **`gatochoc`, `cannoli`, `vtrushka`, `aplcrisp`, `cofetart` & `gozinaki`**: Immediate-Mode GUI (Nuklear), high-speed 2D/3D physics (Box2D v3 / Box3D), VRML 3D parsing, isometric pixel-art rendering, lightweight neural network training/inference, and local on-device LLM generative inference (llama.cpp) extension modules.
* **`popcorn`, `cococake`, `wipee`, `icondom`, `poopee`, `opercrem`, `tbrzilve`**: Project scaffolding, collaborative IDE, release packager, icon generator, binary resource embedder, and specialized flat-root archivers.

#### 5. Multi-Primitive Visual Synthesis Standard
TinCLE enforces a mandatory AI rendering standard that combines multiple code-based primitive shapes (rects, lines, ellipses, polygons) into detailed, expressive graphics. You can build complete, visually rich games purely through code execution without drawing or downloading a single external image asset.

---

### Who is TinCLE for?

* **Vibe Coders**: Creators who want to talk with AI and watch fully functioning 2D/3D games come to life instantly without touching code themselves.
* **Solo Developers & Educators**: Creators looking for a zero-dependency, hyper-fast prototyping platform that runs 100% offline and local on Windows.
* **AI Enthusiasts**: Developers looking to test the absolute bleeding edge of LLM capabilities in real-time software generation.
* **Game Jammers**: Creators who want to quickly build web games that run on HTML5/WASM for events like game jams.

Stop fighting bloated engine UI screens. Feed the talent chips to your AI, direct the vision, and let your AI bring your games to market at ultra-speed!

## 2. Development Environment

TinCLE is built with the following software stack:
- Windows 10 Pro 64-bit
- Tiny C Compiler Version 0.9.28rc
- Emscripten SDK Version 6.0.0 (WASM Toolchain)
- Simple DirectMedia Layer (SDL) Version 2.32.10
- SDL_ttf Version 2.24.0
- stb libraries
- SDL2_GFX Version 1.0.4
- GCC Version 16.1.0
- Ogg Version 1.3.6
- Vorbis Version 1.3.7
- TinySoundFont
- glslang Version 16.4.0
- sfxr-sdl Version 1.2.1
- Box2D Version 3.1.1
- Box3D Version 0.1.0
- WebView Version 2.1.0.4129.50
- Scintilla Version 553
- Lexilla Version 553
- Miniz Version 3.1.2
- Nuklear Version 4.13.3
- NW.js Version 0.117.0
- Three.js Version 186
- Planck.js Version 1.3.0
- cannon-es Version 0.20.0
- Howler.js Version 2.2.4
- Obelisk.js Version 1.2.1
- Genann Version 1.1.1
- llama.cpp Version 0.7.0

## 3. Package File Manifest

TinCLE provides a self-contained, 100% offline development kit. All executables, dynamic libraries, templates, and talent chips are organized flatly or via standard local directories within each architecture package (32bit/ and 64bit/).

| Category | Files / Directories | Role & Description |
| :--- | :--- | :--- |
| **Core Runtime** | `tincle.dll`<br>`SDL2*.dll`<br>`libs/` | Core Pure C99/SDL2 engine runtime, dynamic libraries, and framework C headers. |
| **Talent Chips** | `SKILL*.md` | LLM system instruction chips (SKILL.md, SKILL_HL.md, SKILL_PT.md, SKILL_FB.md, SKILL_AON*.md, etc.). |
| **C99 Toolchain** | `tinclec.exe`<br>`emcass.exe`<br>+ `template.html`<br>`asspack.exe`<br>`pisschk.exe`<br>+ `pisschk.dll`<br>`pubicnet.exe`<br>+ `pubicnet.dll` | **C99 Build Pipeline**:<br>- tinclec: Instant Windows desktop native compiler.<br>- emcass: WebAssembly (WASM) compiler (uses template.html).<br>- asspack: Automatic virtual filesystem binary asset packager.<br>- pisschk: Dual-mode GLSL hardware shader syntax validator.<br>- pubicnet: Dedicated multiplayer socket server binary generator. |
| **JS Toolchain** | `jgrscnzl.exe`<br>+ `tinclejs.html`<br>`rjasplns.exe`<br>+ `tcljswin.html` | **TinCLE JS Pipeline**:<br>- jgrscnzl: HTML5 web launcher generator (uses tinclejs.html).<br>- rjasplns: Standalone Windows NW.js EXE packager (uses tcljswin.html). |
| **Release & Deployment** | `opercrem.exe`<br>`poopee.exe`<br>+ `manifest.xml`<br>`wipee.exe`<br>`tbrzilve.exe` | **Binary Post-Processing**:<br>- opercrem: Standalone .rc resource compiler and direct COFF object generator.<br>- poopee: Direct PE metadata & icon injector (uses manifest.xml).<br>- wipee: Release packaging ZIP creator with AV-bypass mode (-m).<br>- tbrzilve: Flat-root duplicate-tolerant multi-stream ZIP packager. |
| **Audio Synthesis** | `pisstrak.exe`<br>+ `soundfont.sf2`<br>`fartbox.exe`<br>+ `fartbox.dll` | **Procedural Sound Drivers**:<br>- pisstrak: MML-to-audio SoundFont synthesizer (uses soundfont.sf2).<br>- fartbox: Procedural 1-shot sound effect synthesizer. |
| **Image Utilities** | `icondom.exe` | Multi-resolution Windows icon generator (.png to .ico). |
| **Addon Modules** | `cannoli.*`<br>`gatochoc.*`<br>`vtrushka.*`<br>`aplcrisp.*`<br>`cofetart.*`<br>`gozinaki.*`<br>+ `libllama.dll`<br>+ `ggml*.dll` | Optional high-performance runtime extension modules (.dll / .wasm):<br>- cannoli: Box2D v3 (2D) and Box3D v0.1 (3D) physics.<br>- gatochoc: Nuklear immediate-mode GUI with Japanese font support.<br>- vtrushka: Declarative VRML (.wrl) 3D world scene parser & renderer.<br>- aplcrisp: Isometric 2.5D pixel-art primitive generator & renderer.<br>- cofetart: Pure C99 lightweight neural network training & inference (Genann).<br>- gozinaki: Local generative LLM inference engine (llama.cpp) with chunked evaluation. |
| **Human Utilities** | `popcorn.exe`<br>`churro.exe`<br>`cococake.exe`<br>+ `Lexilla.dll`<br>+ `Scintilla.dll`<br>+ `WebView2Loader.dll`<br>+ `cococake.ini`<br>`lollipop.exe` | **Developer Ergonomics**:<br>- popcorn: 1-click project directory & toolchain workspace generator.<br>- churro: Instant cross-origin isolated local web server.<br>- cococake: AI-pair programming desktop IDE.<br>- lollipop: Continuous line-printer zebra paper PDF source archiver. |
| **AI Documentation** | `TinCLE.md`<br>`HISTORY.md` | Core architecture guide and full version release chronicle for AI consumption. |
| **Human Guides** | `readme.txt`<br>`document.pdf` | Getting-started manual and printable specification reference. |
| **Assets & Metadata** | `CREDITS.txt`<br>`info.txt`<br>`exsass.txt`<br>`.htaccess`<br>`cursor.png`<br>`font.ttf`<br>`icon.png` | Starter resources and release-readiness metadata files. |

## 4. TinCLE Toolchain

### 01. TinCLE (Tiny C Lovely Engine)

* **What is TinCLE?**
  TinCLE consists of the core runtime library (`tincle.dll` / `tincle.a` / `tincle.h`) and its dedicated automated compiler assistant (`tinclec`). The core library packages a ultra-lean 2D/GLSL execution pipeline on top of Pure C (C99) and SDL2. By simply passing your `game.c` source code to `tinclec`, it automatically invokes the embedded TCC toolchain to compile, link, and spit out a lightweight Windows native executable (`.exe`) in under a second—completely bypassing complex IDE configurations, heavy build systems, or manual linker flag management.
* "Why TinCLE?"
  Because existing game engines are too bloated. They are like a heavy, endless stream. Our framework is so tiny, light, and fast-it's like a quick tinkle. Just let it out, and you're done! No waste, just pure relief.
* How to TinCLE?
  AI can learn how to use TinCLE by reading `SKILL.md`.

### 02. poopee (POst OPtimizer of ExE)

* **What is poopee?**
  `poopee` (POst OPtimizer of ExE) is a lightweight binary post-processing and resource injection tool designed for Windows executables (`.exe`). After compiling your game with `tinclec`, `poopee` directly modifies the target PE binary to embed custom multi-resolution Windows icons (`.ico` generated by `icondom`) and high-compatibility application manifests (`manifest.xml`) into the heart of the executable—all without requiring complex resource compilers (like `windres` or `rc.exe`) or heavy IDE toolchains.
* "Why poopee?"
  You've let out the fluid code with TinCLE, packed the solid mass with asspack, and protected your assets with icondom. Your masterpiece is inside the compiler, but it's still holding onto heavy configuration waste and raw data junk. Before your executable hits the public, it needs to pass the strict, constipated inspection of modern antivirus algorithms. That's when you need to drop the final payload: poopee. This post-processing powerhouse flushes out all compiling residue, injects your high-res icons, and embeds the perfect manifest. It squeezes every last drop of dead weight out of your EXE, leaving nothing but a smooth, clean, highly-optimized release. Don't let your game get stuck in development limbo. Let poopee push it out, and feel the pure, total relief of a flawless deployment!
* How to poopee?
  AI can learn how to use poopee by reading `SKILL_ADD2.md`.

### 03. asspack (ASSet PACKer)

* **What is asspack?**
  `asspack` (ASSet PACKer) is TinCLE's specialized asset bundling utility. It scans your project root directory based on the file extensions registered line-by-line in `exsass.txt` (e.g., `.png`, `.ogg`, `.ttf`, `.glsl`) and automatically packs all matching textures, audio clips, fonts, and shader files into a single, highly compressed, un-crackable data package (`game.data`). This eliminates the need to ship loose asset folders alongside your Windows EXE, allowing the game engine to load binary assets directly through a clean, unified internal virtual filesystem.
* "Why asspack?"
  First came TinCLE, the light and quick relief for modern bloated development. But what about the heavy, solid assets? That's where asspack comes in. It seals all your textures, sounds, and data into a single, un-crackable package, preventing any leaking. TinCLE handles the fluid code, asspack compresses the solid mass. Together, they complete the ultimate cycle of clean, lightweight execution.
* How to asspack?
  AI can learn how to use asspack by reading `SKILL_ADD2.md`.

### 04. emcass (EMCc ASSistant)

* **What is emcass?**
  `emcass` (EMCc ASSistant) is TinCLE's specialized WebAssembly (WASM) build automation utility. It wraps the underlying Emscripten toolchain (`emcc`) to compile your C99 code (`game.c`) and automatically package all assets/shaders registered in `exsass.txt` into a high-performance, web-ready distribution kit (`index.html`, `index.js`, `index.wasm`, and `index.data`). With a single command, `emcass` configures complex WebGL/GLES2 viewports, embeds custom HTML5 templates, and generates zero-latency browser builds perfectly suited for itch.io and web deployment—no manual Emscripten flag configuration required.
* "Why emcass?"
  First, TinCLE handled the fluid, and asspack sealed the mass. But the modern web demanded more-it demanded a format that runs anywhere, anytime, with absolute, shameless speed. That's where emcass comes in. While heavy, bloated modern frameworks crawl onto the web yelling "Eat My Data!", emcass tells the internet to eat our dust. It emulsifies your entire low-level creation into high-performance WebAssembly bytecode and streams it directly into the browser's face. No friction, no heavy runtimes, and absolutely no filters. TinCLE flows, asspack compresses, and emcass blasts the whole package across the digital landscape. Complete the ultimate, unhinged cycle of lightweight web domination!
* How to emcass?
  AI can learn how to use emcass by reading `SKILL_ADD2.md`.

### 05. icondom (ICON DOMesticater)

* **What is icondom?**
  `icondom` (ICON DOMesticater) is TinCLE's automatic icon converter and safety-packaging tool. It takes a single standard image file (e.g., `icon.png`) and instantly downsamples, reformats, and packages it into a multi-resolution, fully compliant Windows icon binary (`.ico`) containing all standard system dimensions (16x16, 32x32, 48x48, 256x256). Designed to work seamlessly with `poopee`, `icondom` eliminates the need for external graphics editors or online converter utilities, ensuring your executable displays crisp, error-free icons across all Windows OS environments.
* "Why icondom?"
  In game development, raw, unprotected graphics are dangerous. If you randomly inject multi-resolution images into your project without proper safety measures, you risk bloating your memory and exposing your pipeline to format leaks. That's why you must use icondom. With just a single raw image, icondom instantly stretches, compresses, and wraps all required resolutions into one perfectly secured, self-contained .ico file. It shields your executable from the messy overhead of modern asset handling. Don't go raw into the OS environment. Wrap your visuals with icondom, practice safe deployment, and keep your software 100% protected!
* How to icondom?
  AI can learn how to use icondom by reading `SKILL_ADD2.md`.

### 06. pisstrak (Programmable Integrated Sound Synthesizer & TRAcKer)

* **What is pisstrak?**
  `pisstrak` (Programmable Integrated Sound Synthesizer & TRAcKer) is TinCLE's SoundFont-powered MML (Music Macro Language) audio synthesis engine. Instead of forcing AI agents to generate raw wave data or handle heavy DAW software, `pisstrak` converts lightweight text-based MML scores into high-quality, fully rendered 44.1kHz `.wav` or `.ogg` audio files in seconds using embedded SoundFont synthesis (`.sf2`). Coupled with the strict duration protocols in `SKILL_PT.md`, `pisstrak` enables any LLM to compose, structure, and render loopable, millisecond-precise background music (BGM) without token overflow or external digital audio workstations.
* "Why pisstrak?"
  AI models are brilliant with logic, but when it comes to composing music and rendering actual audio, they are often left stuck. They can't hand-craft wave files, but they can write text-based MML. pisstrak is our revolutionary response to this limitation, completing the TinCLE stream. Whenever your AI agent needs a soundtrack, it doesn't need a complex digital audio workstation-it just needs to let it out. pisstrak takes the raw MML generated by the AI, runs it through our embedded synthesis engine, and flushes out beautifully rendered OGG/WAV files in seconds. No heavy audio middleware, no creative block. It's the fast, fluid, and seamless way to track your game's audio. When the inspiration hits your AI, just let pisstrak flow and listen to the sweet sound of automated victory!
* How to pisstrak?
  AI can learn how to use pisstrak by reading `SKILL_PT.md`.

### 07. fartbox (Frequency Audio Rendering & Tuning BOX)

* **What is fartbox?**
  `fartbox` (Frequency Audio Rendering & Tuning BOX) is TinCLE's procedural 1-shot sound effect (SE) generator. Designed specifically for AI agents that cannot operate complex graphical audio editors, `fartbox` instantly synthesizes clean, 16-bit 44.1kHz `.wav` sound effects—such as lasers, explosions, jumps, and coin pickups—directly from command-line preset flags (e.g., `-t explosion`) or highly customizable `.fart` text parameter files. Guided by `SKILL_FB.md`, any LLM can programmatically craft, mutate (`-m`), and fine-tune custom audio dynamics without external sample libraries or manual UI tweaking.
* "Why fartbox?"
  Traditional sound production is clogged with heavy digital audio workstations, bloated sample libraries, and sluggish manual UI tweaking. For an autonomous AI agent, this creates an intolerable build-up of friction-essentially, operational gas. fartbox is our rapid-fire solution that flushes out all human-oriented GUI overhead. Sound is stripped down to its bare essence: pure mathematical parameters processed via a lightweight text stream. Instead of diggng through gigabytes of assets, your AI agent can procedurally generate, fine-tune, and mutate raw audio structures-like lasers, explosions, and blips-instantly through simple command-line execution. No heavy middleware, no friction, and absolutely no holding back. When your game needs a quick, sharp auditory impact, let fartbox release the pressure and blast high-fidelity procedural effects straight into your build!
* How to fartbox?
  AI can learn how to use fartbox by reading `SKILL_FB.md`.

### 08. pisschk (Pipelined Inspection System for Shader - CHecKer)

* **What is pisschk?**
  `pisschk` (Pipelined Inspection System for Shader - CHecKer) is TinCLE's dual-mode GLSL shader validation utility. It acts as an automated diagnostic filter for custom fragment and vertex shaders (`.glsl` / `.frag` / `.vert`), analyzing source code for hardware-strict compliance before deployment. `pisschk` catches strict vendor errors (such as Radeon-specific reserved word conflicts and implicit cast bugs) as well as GLES2 precision specification omissions, ensuring your shaders compile cleanly across both desktop GPUs and web targets without platform-specific crashes.
* "Why pisschk?"
  In graphics development, what looks clean on the outside can be deeply infected on the inside. Many developers get pampered by NVIDIA's loose compiler, releasing shaders that look beautiful but contain fatal hidden illnesses-like reserved word bugs-that will instantly crash on Radeon systems. That's why your pipeline needs pisschk. Think of it as the ultimate urinalysis for your GLSL. pisschk dips a sharp, unyielding testing strip straight into your shader stream, instantly flagging any turbid, rule-breaking code before it reaches the public. Don't let a contaminated shader poison your launch. Run your code through pisschk, filter out the hardware-specific impurities, and ensure a 100% healthy, cross-platform release!
* How to pisschk?
  AI can learn how to use pisschk by reading `SKILL_ADD1.md`.

### 09. pubicnet (Public Universal Binary Inter-Connect NETwork)

* **What is pubicnet?**
  `pubicnet` (Public Universal Binary Inter-Connect NETwork) is TinCLE's standalone dedicated server binary generator and lightweight networking framework. Designed to eliminate bloated cloud SDKs and heavy RPC middleware, `pubicnet` allows AI agents to instantly bake encrypted UUID game identities directly into executable server binaries with a single command-line execution. Operating on top of non-blocking, direct-memory Pure C99 socket pipelines, `pubicnet` delivers low-latency, private multi-user synchronization and dedicated server execution without external dependencies.
* "Why pubicnet?"
  Modern multiplayer backends are heavily cluttered with bloated cloud SDKs, complex authentication handshakes, and sluggish, over-engineered RPC frameworks. For an autonomous AI agent, this introduces a mountain of architectural friction. That's why we created pubicnet. While the internet is a public place, your dedicated game traffic should remain strictly private and concealed. pubicnet strips away all heavy backend overhead, allowing your AI agent to instantly binary-patch a self-contained dedicated server with a unique, encrypted UUID in a single command-line thrust. Networking is reduced to non-blocking, memory-direct Pure C99 streaming. No bloated cloud services, no external dependencies, and absolutely no exposure. When your game needs a rapid, secured, and intimate connection to the web, let pubicnet pop up your dedicated server and handle the raw data flow with absolute privacy!
* How to pubicnet?
  AI can learn how to use pubicnet by reading `SKILL_PN.md`.

### 10. cannoli (Cannoli: Collision And Newtonian Network Object Linked Interface)

* **What is cannoli?**
  `cannoli` (Collision And Newtonian Network Object Linked Interface) is TinCLE's dynamic 2D and 3D physics addon library. Acting as a sweet, non-blocking C99 shell wrapper (`cannoli.dll` for Windows and `cannoli.wasm` / `cannoli.a` for Web), `cannoli` fully exposes the uninhibited API suites of pure C Box2D v3.0 (2D rigid-body physics) and Box3D v0.1 (3D physics) directly to your project without performance loss. By simply including `#include "libs/cannoli.h"`, AI agents and developers can instantly inject real-time physical dynamics—such as gravity, mass, collision impulse, joint constraints, and 3D force vectors—into their game entities across both desktop and browser compilation targets.
* "Why cannoli?"
  Until now, TinCLE handled the fluid stream, and asspack compressed the mass. But as complex physics entered the scene, our lightweight world needed something structural, crispy, and deliciously rich to hold the rigid Newtonian pressure. That's why we created cannoli.Inspired by the iconic Sicilian pastry, cannoli wraps the heavy, multi-layered dynamics of the Box2D/Box3D engine inside a sweet, crunchy, non-blocking C99 DLL shell. It injects your entities with immediate mass, friction, and satisfying bounce without clogging your pipeline. Every great metabolism needs a sweet intake to keep the stream moving. Don't let your game's world feel bland and weightless. Sweeten your rigid-body simulation with cannoli, and let your objects collide with pure, delicious momentum!
* How to cannoli?
  AI can learn how to use cannoli by reading `SKILL_AON1.md`.

### 11. cococake (Coconut cake: COoperative Creation Of C with Ai Knowrage - Environment)

* **What is cococake?**
  `cococake` (COoperative Creation Of C with Ai Knowrage - Environment) is TinCLE's sweet, sugar-coated integrated development environment (IDE) specifically designed for human-AI collaborative workflows. Unifying the 3-step development loop into a single structured desktop window, `cococake` layers a syntax-highlighted C code editor on the top-left, an integrated Command Prompt terminal on the bottom-left, and an embedded browser pane on the right dedicated to your favorite AI assistant (ChatGPT, Claude, Gemini, etc.). With customizable auto-launching URLs for project-specific AI chat sessions, `cococake` provides a seamless, sweet pair-programming space where developers can converse with AI, adjust code, and build executables—all without switching windows or breaking focus.
* "Why cococake?"
  TinCLE is raw, fast, and engineered for autonomous AI. But for a human companion trying to keep up with the loop, managing separate editor windows, CLI terminals, and AI chat tabs can feel like a bitter challenge. Enter cococake-the ultimate, sugar-coated IDE designed to sweeten your workflow. Just like the layers of a rich coconut cake, cococake layers everything you need into a single, cohesive window: an API-colored code editor, a direct compiler console, and an integrated browser for your favorite AI assistant. It transforms the daunting 3-step loop into a delicious, seamless slice of cake. Don't torture yourself with over-complicated environments. Sit back, take a bite of cococake, and enjoy the most effortlessly sweet pair-programming experience on earth!
* How to cococake?
  AI can learn how to use cococake by reading `SKILL_ADD2.md`.

### 12. popcorn (Popcorn: Project Organizer Providing Clean Onboarding & Runtime Navigation)

* **What is popcorn?**
  `popcorn` (Popcorn: Project Organizer Providing Clean Onboarding & Runtime Navigation) is TinCLE's entry-point onboarding and project workspace generator. Positioned directly at the root of the distribution package as the very first tool for human creators, `popcorn` eliminates setup confusion by providing a single-dialogue wizard. Upon execution, it prompts the user to select or create a target game directory alongside a 32-bit or 64-bit architecture option, automatically deploying the complete TinCLE compiler toolchain, runtime DLLs, and talent chips (`SKILL.md`) into a fresh, ready-to-use project folder without manual file operations.
* "Why popcorn?"
  For human developers entering the TinCLE universe, the first step should never be a sluggish chore. Nobody wants to waste time manually creating folders and copy-pasting compiler toolchains. That's why we built popcorn. Placed right outside the core folders, it is the first tool a human should touch. With a single execute, popcorn instantly fires up, copies the entire required toolchain, and prepares a pristine workspace. Your project files pop into existence like kernels on high heat-fast, light, and highly satisfying. It completely removes the manual setup friction, leaving your human brain fresh and ready to hand the reins over to the real protagonist. Grab your popcorn, spawn your directory, and let the AI-driven development show begin!
* How to popcorn?
  AI can learn how to use popcorn by reading `SKILL_ADD2.md`.

### 13. wipee (Whole Integration Packager for Executable Environment)

* **What is wipee?**
  `wipee` (Whole Integration Packager for Executable Environment) is TinCLE's automated deployment packaging utility. Designed to streamline final distribution and prevent release friction, `wipee` sweeps through your target release directories (e.g., `_release_win` or `_release_web`) and packages all executables, data archives, DLLs, and compliance files into a clean, ready-to-distribute ZIP archive with a single command (`wipee output.zip folder`). Beyond standard ZIP creation, `wipee` features a specialized "Malformed ZIP mode" (`-m`), which intentionally alters Central Directory compression headers to shield lightweight, TCC-compiled binaries from over-reactive antivirus heuristic scanners during Windows desktop distribution.
* "Why wipee?"
  You've code-flowed with TinCLE, packed the mass with asspack, and pushed out the optimal binary with poopee. Your masterpiece is finished, but leaving your development workspace messy and exposed to the wild internet is bad hygiene. That's why you need wipee-the ultimate post-deployment finish. wipee cleans up your entire build environment, safely wiping away the clutter and wrapping your executable and assets into a single, sterile, ready-to-distribute ZIP package. Best of all, it features our discrete "Malformed ZIP mode for reliable delivery." This specialized sanitation technique wraps your archive in a subtly non-standard structure, shielding your pure, lightweight creation from the over-reactive, constipated false-positives of modern OS security layers. Don't leave your release raw and unprotected. Clean up your build, give it a thorough wipe with wipee, and achieve the pure, absolute relief of a spotless, perfect deployment!
* How to wipee?
  AI can learn how to use wipee by reading `SKILL_ADD2.md`.

### 14. gatochoc (Gateau au chocolat: Gui And Toolkit for On-screen Components, Huds, and Object Controls)

* **What is gatochoc?**
  `gatochoc` (Gui And Toolkit for On-screen Components, Huds, and Object Controls) is TinCLE's lightweight immediate-mode GUI extension library based on the Nuklear GUI framework. Operating as a rich, transparent C99 DLL (`gatochoc.dll` for Windows and `gatochoc.wasm` / `gatochocmt.wasm` for Web), `gatochoc` seamlessly glazes both standard 2D software pipelines (`SDL_Renderer*`) and OpenGL GLSL shader pipelines (`SDL_GLContext`) with high-fidelity, hardware-accelerated UI controls—such as movable windows, buttons, sliders, text inputs, and debug panels. Equipped with zero-latency event interception and built-in full Japanese font rendering capabilities (`GATOCHOC_FONT_JAPANESE` via `SKILL_AON1.md`), `gatochoc` empowers developers and AI agents to build rich in-game HUDs, developer tools, and standalone desktop applications without adding heavy framework overhead.
* "Why gatochoc?"
  TinCLE handles the raw, high-performance flow, but every great interactive experience needs a rich, beautiful outer layer to face the user. Writing robust HUDs, debug menus, and complex UI controls from scratch in pure C can be a bitter, jaw-breaking task. That’s why we created gatochoc.Inspired by the dense, luxurious French chocolate cake, gatochoc glazes your runtime with the complete, immediate power of the Nuklear GUI ecosystem. Operating as a transparent C99 DLL, it seamlessly infuses your SDL and OpenGL contexts with high-fidelity, hardware-accelerated on-screen components without adding a single byte of bloated runtime fat. It’s the ultimate, calorie-free icing for your game’s visual presentation. Don't leave your user interface looking dry and raw. Dress up your HUDs, sweeten your diagnostics, and give your project a gorgeously rich, interactive layer with gatochoc!
* How to gatochoc?
  AI can learn how to use gatochoc by reading `SKILL_AON1.md`.

### 15. churro (Churro: Coop/coep Header Unlocked Rapid Runtime Open-server)

* **What is churro?**
  `churro` (Coop/coep Header Unlocked Rapid Runtime Open-server) is TinCLE's standalone, cross-origin isolated local web server utility. Designed to completely eliminate the need for heavy web stack setups (like XAMPP or Python environment configurations) when testing WebAssembly builds, `churro` runs directly inside your project directory to serve Emscripten outputs (`emcass`). Upon execution with a single command, `churro` automatically injects critical Cross-Origin Isolation HTTP headers (`Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`), automatically launches your default web browser, and streams binary asset packages (`.wasm` / `.data`). Featuring multi-threaded binary streaming and clean single-keypress terminal shutdown, `churro` provides a zero-friction, one-click offline runtime environment for developers of all ages.
* "Why churro?"
  Testing your WebAssembly builds on the modern web shouldn't feel like a bitter, agonizing chore. No human developer—whether a seasoned engineer or a schoolchild starting their first coding journey—should have to suffer through the tedious setup of heavy server stacks like XAMPP, or fight with missing COOP/COEP headers just to see their game run. That’s why we fried up churro.Inspired by the classic, simple pastry invented by shepherds for a quick, freshly-baked bite in the wild, churro bakes a crisp, sweet, and perfectly configured local HTTP environment in milliseconds right inside your project directory. With a single execute, it automatically sets the strict multi-origin isolation headers, spins up a lightning-fast local server, and launches your browser instantly. No complex configuration, no infrastructure friction, just a hot, delicious, and hassle-free way to taste your Emscripten builds. Stop messing with heavy web backend overhead—grab a churro, press enter, and enjoy your web game fresh out of the fryer!
* How to churro?
  AI can learn how to use churro by reading `SKILL_ADD2.md`.

### 16. lollipop (Lollipop: Legacy Outputter Like LIne Printer Of Pdf)

* **What is lollipop?**
  `lollipop` (Legacy Outputter Like LIne Printer Of Pdf) is TinCLE's physical-archive PDF generator designed for long-term code preservation. Created without complex options or setup friction, `lollipop` accepts a source code file or directory and instantly bakes it into a continuous-form landscape PDF. Recreating the iconic aesthetic of classic line-printer zebra paper—complete with alternating white and light-gray horizontal track bands and generous character spacing—`lollipop` produces a highly readable, physical-ready document optimized for paper printing, tangible offline archiving, and real-world red-pen code reviews.
* "Why lollipop?"
  In a world plagued by disk failures, unannounced cloud service shutdowns, and volatile digital environments, true peace of mind for your masterfully crafted source code only comes when it is manifested in the physical world. lollipop is built strictly for the human developer who understands that paper remains the ultimate, incorruptible archive.This utility bakes your source code into a beautifully formatted, landscape PDF inspired by the nostalgic charm of classic line-printer continuous forms. Alternating between clean white and soft gray background tracks with generous letter spacing, it provides an exceptionally readable canvas perfect for taking real-world red ink corrections.We named this time-defying outputter after the traditional lollipop—a sweet masterpiece with such low moisture content that it naturally repels decay, bacteria, and mold, making it one of the most resilient treats in history. While digital bit-rot threatens every drive, your printed lollipop code remains frozen in sweet, permanent perfection, immune to the chaos of the digital age. Stop trusting the fragile cloud with your lifelong legacy—print a lollipop, grab your red pen, and preserve your code in timeless sugar!
* How to lollipop?
  AI can learn how to use lollipop by reading `SKILL_ADD2.md`.

### 17. vtrushka (Vatrushka: Vrml TRUly SHaping Kosmos Agent)

* **What is vtrushka?**
  `vtrushka` (Vatrushka: Vrml TRUly SHaping Kosmos Agent) is TinCLE's dedicated 3D world scene-graph parser and rendering engine. Operating as a razor-thin, high-speed C99 extension library (`vtrushka.dll` for Windows desktop and `vtrushka.wasm` for WebAssembly), `vtrushka` parses text-based VRML (Virtual Reality Modeling Language, `.wrl`) source files and transforms them into real-time, hardware-accelerated 3D viewports. By offloading complex 3D scene construction to declarative VRML structures, `vtrushka` allows AI agents and developers to build expansive 3D environments, custom cameras, dynamic lighting, and hierarchical transform nodes-all without polluting the core `game.c` runtime with endless low-level vertex arrays or manual matrix transformations.
* "Why vtrushka?"
  Forcing your code—or your AI assistant—to hardcode every single 3D object, vertex, and matrix calculation directly into raw C program is pure, brutal torture. No matter how brilliant the mind, building a vast 3D world through raw low-level code alone has its limits. That’s why we baked vtrushka. Instead of kneeling to modern, heavily bloated 3D standard runtimes, we went back to the golden age and resurrected VRML (.wrl)—a beautifully readable, classic text-based 3D format—with a 100% scratch-built parser and renderer designed uniquely for TinCLE. We named this 3D cosmos shaper after Vatrushka, the traditional sweet pastry where rich ingredients like cottage cheese, mashed potatoes, and sweet jam are all packed together into a single, perfectly balanced ring of deliciousness. vtrushka lets you pack shapes, textures, lighting, and world layouts into simple VRML files, serving up a fully realized 3D world fresh from the oven in milliseconds, available as both a native DLL and WASM module. Stop grinding your gears over complex 3D asset pipelines. Load up vtrushka, throw in your ingredients, and shape your own sweet digital cosmos instantly!
* How to vtrushka?
  AI can learn how to use vtrushka by reading `SKILL_AON2.md`.

### 18. opercrem (Opera cream: OPtimalized Enhanced Resource Compiler - REs-file Maker)

* **What is opercrem?**
  `opercrem` (OPtimalized Enhanced Resource Compiler - REs-file Maker) is TinCLE's standalone, ultra-minimalist Windows resource compiler and COFF object generator. Designed to completely liberate the toolchain from heavy proprietary SDK utilities (`rc.exe`/`cvtres.exe`) and bloated copyleft GPL dependencies (GNU `windres`), `opercrem` directly parses clean, line-oriented resource scripts (`.rc`) into single `.rsrc` section COFF object files (`.obj` / `.o`) or standard Win32 binary resource files (`.res`). It natively handles automatic `RT_ICON` multi-resolution frame extraction, `RT_GROUP_ICON` cataloging, raw binary embedding (`RCDATA`/`RAWDATA`), and full `VS_VERSION_INFO` binary block construction. With intelligent preprocessor architecture detection and explicit `-m32` / `-m64` flags, `opercrem` outputs format-perfect COFF files ready for direct linking via `tinclec` and TinyCC in a single command—delivering a 100% offline, self-contained Windows metadata deployment pipeline.
* "Why opercrem?"
  Building for Windows is a blast until modern antivirus algorithms look at your clean, un-bloated executable and scream "Malware!" out of pure ignorance. To pass their paranoid inspections, you need to bake serious metadata like VS_VERSION_INFO and manifestations into your binary. But who wants to deal with traditional heavy, outdated SDK tools? Enter opercrem. Wrapped into a single, shockingly light 100KB executable, opercrem is a powerhouse resource compiler that spits out flawless .res, .obj, or .o files in a single, instant flash, fully supporting 32-bit and 64-bit cross-compilation. We named it after Opera Cream, the legendary confection where rich cream, sugar, vanilla, and marshmallow fluff are all tightly enveloped in a smooth layer of pure chocolate cream. It is a decadent bundle of sweetness that no one can resist. opercrem takes all your messy raw resources, wraps them in a flawless binary shell, and delivers a smooth, clean deployment that slides right past modern security filters. Bite into the pure efficiency, give troublesome traditional ceremonies the middle finger, and sweeten your Windows builds!
* How to opercrem?
  AI can learn how to use opercrem by reading `SKILL_ADD2.md`.

### 19. tbrzilve (Tabrizi Lovuez: Tiny BRilliant ZIp LoVely Encloser)

* **What is tbrzilve?**
  `tbrzilve` (Tabrizi Lovuez: Tiny BRilliant ZIp LoVely Encloser) is TinCLE's specialized, flat-root multi-stream ZIP archiving utility powered by `miniz`. Breaking away from traditional directory-preserving archivers, `tbrzilve` automatically strips away all host folder hierarchies and packs input files directly into the root level of a standard ZIP container (`MZ_DEFAULT_COMPRESSION`), intentionally tolerating duplicate filenames without collision alerts, auto-renaming, or overwrite errors. Files are indexed strictly in their chronological command-line order, enabling TinCLE's runtime engines and custom C binary stream loaders to perform direct, index-based sequential asset streaming, generational multi-version snapshots, and collision-free dynamic packaging—all while completely liberating AI agents from error-prone path-manipulation and renaming code.
* "Why tbrzilve?"
  Traditional, human-centric OS and GUI unarchivers live in constant fear of name collisions. To please them, an AI developer must write messy, complex string-manipulation code to rename files—a breeding ground for pure hallucinations and bugs. tbrzilve destroys this paradigm. Exploiting a hidden truth in the official ZIP specification, it allows files with the exact same name to co-exist flatly in a single root directory without a single warning. For humans, this looks like broken magic. But for TinCLE's binary-seeking loaders, it is the ultimate superpower. The AI dumps files instantly and retrieves them by their elegant index order, creating a lightning-fast architecture for version control and dynamic asset swapping. We named it after Tabrizi Lovuez, the exquisite Persian confection. In the box, perfectly uniform, diamond-shaped sweets look identical at first glance. Yet, look closer, and the unique arrangement of pistachios inside each one reveals their distinct identities. tbrzilve packs your identical-looking but structurally different files into a flat, elegant arrangement. Forget human folder structures, free your AI from string-handling bugs, and embrace index-driven efficiency!
* How to tbrzilve?
  AI can learn how to use tbrzilve by reading `SKILL_ADD2.md`.

### 20. jgrscnzl (Jagerschnitzel: Javascript Game Revolutional SCeNe Zeal Launcher)

* **What is jgrscnzl?**
  `jgrscnzl` (Javascript Game Revolutional SCeNe Zeal Launcher) is TinCLE JS's automated HTML5 web distribution launcher and compiler assistant. By parsing the mandatory title and resolution header comment (`// "Title" (Width, Height)`) in your JavaScript source, it injects game dimensions, project metadata, and credits from `CREDITS.txt` into the specialized `tinclejs.html` template to spit out a clean, standalone `index.html`. Furthermore, `jgrscnzl` automatically discovers all other `.js` script files located in the project root directory and prepends them as `<script>` tags before the primary game script, enabling zero-configuration modular and multi-file codebases. Equipped with on-canvas fullscreen toggle controls, it delivers a turnkey, zero-dependency browser game deployment ready for immediate hosting on platforms like itch.io.
* "Why jgrscnzl?"
  Sometimes, low-spec local AIs struggle with C pointer structures and Emscripten #ifdef macros, leading to endless loops of broken code. TinCLE JS solves this by embracing JavaScript. jgrscnzl takes a raw, single-canvas game.js written by your AI, layers it with essential runtime libraries, and bathes it in a perfectly configured index.html template. We named it after Jagerschnitzel, the classic comfort food. You take a simple cut of pork, pound it thin, coat it in flour, egg, and breadcrumbs, fry it to a golden crisp, and smother it in a rich, velvety mushroom cream sauce. jgrscnzl does exactly that to your code: it turns raw, basic JavaScript into a savory, crispy web deployment, complete with a clean full-screen button. A masterpiece served straight to the browser!
* How to jgrscnzl?
  AI can learn how to use jgrscnzl by reading `SKILL_HL.md`.

### 21. rjasplns (Rajas Poblanas: Rapid JAvaScript Project Local Nw.js Shaper)

* **What is rjasplns?**
  `rjasplns` (Rapid JAvaScript Project Local Nw.js Shaper) is TinCLE JS's dedicated standalone Windows desktop executable packager powered by NW.js and `miniz`. Acting as a direct bridge from web scripts to native desktop binaries, `rjasplns` dynamically synthesizes window configurations (`package.json`) and runtime host wrappers (`tcljswin.html`), compresses your primary script (`game.js`), modular auxiliary scripts, and local `libs/` dependencies into an in-memory ZIP container, and automatically sweeps the project directory to bundle all media matching file extensions in `exsass.txt`. It then fuses this archive directly to a detected system `nw.exe` via binary appending to output a unified executable (defaults to `game.exe`), while simultaneously extracting required runtime dependencies (`.dll`, `.pak`, `.dat`, `.bin`, and `locales/`). The resulting standalone binary automatically handles proportional canvas letterboxing across arbitrary window scales and native fullscreen modes.
* "Why rjasplns?"
  Web execution is great, but a true desktop masterpiece demands its own autonomous environment. rjasplns takes your AI's humble game.js and cooks it using the NW.js runtime, compressing it directly into a standalone Windows executable (.exe) along with all necessary DLLs and assets. It is named after Rajas Poblanas, the rich Mexican delicacy. Strips of simple poblano peppers are roasted, then slowly simmered in a heavy homemade sauce of Mexican cream, shredded cheese, and intense spices. rjasplns throws your raw script into a hot skillet with core runtime libraries and NW.js configurations, stewing them into a fiery, unified executable. Featuring automatic aspect-ratio scaling with elegant black bars for any window size, it shapes your casual script into a heavy-hitting native package.
* How to rjasplns?
  AI can learn how to use rjasplns by reading `SKILL_HL.md`.

### 22. aplcrisp (Apple crisp: APpeaLing Colorful Renderer of ISometric Pixel)

* **What is aplcrisp?**
  aplcrisp (APpeaLing Colorful Renderer of ISometric Pixel) is TinCLE's specialized 2D isometric voxel rendering extension library. Operating as a highly portable C99 addon (aplcrisp.dll for Windows and aplcrisp.wasm for Web), aplcrisp is a complete, native-compiled port of the famous Obelisk.js framework, bringing sophisticated pseudo-3D pixel architectures directly to the TinCLE ecosystem. Just like its namesake dessert—where scattered pieces of tart apple, crunchy oatmeal crumbs, and sweet streusel toppings bake together into a single, perfectly unified, and delicious sweet treat—aplcrisp allows AI agents and human creators to take individual, granular isometric pixel objects (cubes, pyramids, cylinders, and slopes) and seamlessly assemble them into stunning, cohesive tactical maps and retro dioramas. By handling complex isometric coordinate math, depth sorting, and vibrant color shading behind a clean API, aplcrisp empowers developers to cook up rich, structurally beautiful voxel-like worlds with a fraction of the code.
* "Why aplcrisp?"
  At first glance, a world built with aplcrisp looks like a true 3D voxel engine. But make no mistake—this is a brilliant illusion. True voxel engines are heavy, bloated with complex Z-buffer depth calculations, hidden surface removal, and massive 3D matrix math that easily overwhelms a lightweight AI's context. aplcrisp entirely bypasses this bloat. It does not calculate 3D space; it generates pristine, pre-shaded 2D pixel-art stamps. To create a 3D masterpiece, your AI must construct it layer by layer, from back to front, using a classic "painter's algorithm." What might seem like a limitation to a human is actually the ultimate superpower for an AI. By reducing complex 3D rendering into simple 2D drawing loops, aplcrisp keeps the context window pure, the compilation instant, and the runtime blazing fast. It is the perfect blend of high-fidelity isometric aesthetics and zero-overhead execution. Don't weigh your game down with heavy 3D math—stack your pixel-art stamps with aplcrisp, let your AI handle the sorting, and serve up a beautifully crisp, isometric world!
* How to aplcrisp?
  AI can learn how to use aplcrisp by reading `SKILL_AON2.md`.

### 23. cofetart (Coffee tart: COntinuous FEedback Tiny Artificial-intelligence Runtime Toolkit)

* **What is cofetart?**
  `cofetart` (Coffee tart: COntinuous FEedback Tiny Artificial-intelligence Runtime Toolkit) is TinCLE's specialized lightweight neural network addon library powered by the pure C99 Genann framework. Operating as a transparent dynamic library (`cofetart.dll` for Windows desktop and `cofetart.wasm` / `cofetartmt.wasm` for WebAssembly), `cofetart` fully exposes the uninhibited C API suite for feedforward multi-layer perceptron (MLP) construction, real-time backpropagation training, and rapid inference evaluation directly to your game logic. By simply including `#include "libs/cofetart.h"`, AI agents and developers can easily build adaptive NPC behaviors, autonomous agents, and dynamic on-device continuous learning loops across both native desktop and WebAssembly environments with zero wrapper friction.
* "Why cofetart?"
  cofetart is TinCLE's minimalist, ultra-lightweight Artificial Neural Network (ANN) addon library based on the Genann framework. Operating as a clean, transparent C99 DLL (cofetart.dll for Windows and cofetart.wasm for Web), cofetart completely exposes a pure, feed-forward neural network pipeline directly to the TinCLE ecosystem. Just like a classic, unadorned coffee tart—whose deceptively simple, plain surface hides an explosion of intense, deep flavors that completely captivate your palate from the very first bite—cofetart provides a streamlined, distraction-free environment to construct, train, and execute neural networks. While modern deep learning often sparks confusion with bloated overhead, this compact engine serves a sharp, addictive blend of bitter complexity and sweet reward. Once AI agents or human creators experience the power of its continuous backpropagation feedback loops for real-time pattern recognition, procedural generation, or adaptive enemy behaviors, they will find its raw, undeniable utility impossible to resist.
* How to cofetart?
  AI can learn how to use cofetart by reading `SKILL_AON2.md`.

### 24. gozinaki (Gozinaki: Generative Output & Zero-shot Intelligence Node for Autonomous Knowledge Interaction)

* **What is gozinaki?**
  `gozinaki` (Gozinaki: Generative Output & Zero-shot Intelligence Node for Autonomous Knowledge Interaction) is TinCLE's specialized on-device Local Large Language Model (LLM) inference extension library powered by `llama.cpp`. Operating as a high-performance C99/C++ dynamic module (`gozinaki.dll` for Windows desktop and `gozinaki.wasm` / `gozinakimt.wasm` for WebAssembly), `gozinaki` embeds standalone generative intelligence directly into your game's runtime loop without external cloud dependencies or blocking network calls. Designed specifically for interactive real-time game engines, it features an asynchronous, non-blocking execution architecture: prompts are tokenized and ingested in small, configurable chunks during `GOZINAKI_STATUS_EVALUATING`, and tokens are progressively decoded one step per frame during `GOZINAKI_STATUS_GENERATING`. Paired with TinCLE's `tincle_fetch_file_async()` API for streaming external `.gguf` quantized models (such as Qwen or SmolLM), `gozinaki` enables AI agents and creators to breathe living, dynamic dialogues, procedural NPC personalities, and responsive environmental narratives into both desktop and browser games while maintaining a smooth, uninterrupted frame rate.
* "Why gozinaki?"
  TinCLE was forged under a singular, unbreakable vow: a game engine of the AI, by the AI, for the AI. Yet, no matter how beautifully an AI coded a game, the final executable was often trapped in the past, forced to speak through dead, hardcoded static strings. To solve this, modern developers lazily chain their games to heavy, blocking web APIs, exposing their pure local builds to the bloated, unpredictable cloud. We refuse that compromise. Enter gozinaki. Named after the sacred Georgian New Year's confection, gozinaki embeds a fully generative LLM node directly into your native DLL or WASM runtime. Just as the traditional sweet is made by taking scattered, raw nuts and binding them tightly with boiling, golden honey, gozinaki takes the vast, complex weights of neural knowledge (the nuts) and caramelizes them flawlessly with your zero-shot inference prompts (the honey). It compresses pure generative intelligence into a sweet, non-blocking, autonomous output. Traditionally served at the very stroke of midnight to guarantee a prosperous new year, dropping gozinaki into your project marks the absolute dawn of true autonomy for your game. Cut the bloated cloud umbilical cord. Drop in gozinaki, bind your knowledge with sweet inference, and let your standalone masterpiece speak with a brilliant, living mind of its own!
* How to gozinaki?
  AI can learn how to use gozinaki by reading `SKILL_AON1.md`.
