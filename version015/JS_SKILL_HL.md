---
name: tincle-js-hl
description: Use when building, creating, or packaging 2D web and standalone desktop games using TinCLE JS ecosystem. Pure Vanilla JS Canvas game generation with jgrscnzl, rjasplns, churro, and audio tools. [TinCLE Additional Skill v0.15]
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

## 7. Libraries available when creating `game.js`.

You can use the following libraries when creating `game.js`.

### 7.1 Three.js (JavaScript 3D library) (Version: r186)

When building 3D games or features using Three.js, follow these strict integration rules:

* **Template Importmap**: The host HTML (`index.html` / `tinclejs.html`) provides the following `<script type="importmap">`:
  ```json
  {
    "imports": {
      "three": "./libs/threejs/three.module.js",
      "three/addons/": "./libs/threejs/addons/"
    }
  }
  ```
* **Execution Context & Dynamic Imports (Mandatory)**:
  * `game.js` is loaded via a classic non-module `<script>` tag. **NEVER** use top-level static import statements (`import * as THREE from 'three';` at line 2 is strictly prohibited and will cause fatal syntax errors).
  * Wrap the entire game logic inside an asynchronous IIFE: `(async () => { /* Game Logic */ })();`.
  * Always import Three.js core and addons dynamically using `await import(...)`:
    ```javascript
    const THREE = await import('three');
    // Any official addon from ./libs/threejs/addons/ can be imported via 'three/addons/...':
    const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');
    ```
  * **Note:** All official add-ons for this version of three.js are included by default in `./libs/threejs/addons/`.
* **Canvas Binding & Sizing (Strict Constraint)**:
  * Bind the WebGL renderer directly to the existing `#tinclecanvas` element:
  `const canvasElement = document.getElementById('tinclecanvas');`
  `const renderer = new THREE.WebGLRenderer({ canvas: canvasElement, antialias: true });`
  * **NEVER append the renderer's DOM element** (`document.body.appendChild(renderer.domElement)` is prohibited).
  * **Preserve Canvas Resolution**: Always call `renderer.setSize(width, height, false)` with the third parameter set to `false`. This prevents Three.js from setting inline style attributes that distort TinCLE's fixed container layout.
  * Set camera aspect ratio strictly to the canvas dimensions (e.g., `WIDTH / HEIGHT`). Do NOT use `window.innerWidth / window.innerHeight`.
* **3D Model Loaders (GLTF / VRML)**:
  Official Three.js loaders are pre-installed in `./libs/threejs/addons/loaders/`. You can dynamically import and instantiate them as follows:
  ```javascript
  // For standard modern 3D models (.gltf / .glb):
  const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  const gltfLoader = new GLTFLoader();
  gltfLoader.load('model.glb', (gltf) => {
    scene.add(gltf.scene);
  });

  // For classic VRML 2.0 / 97 models (.wrl):
  const { VRMLLoader } = await import('three/addons/loaders/VRMLLoader.js');
  const vrmlLoader = new VRMLLoader();
  vrmlLoader.load('model.wrl', (vrmlScene) => {
    scene.add(vrmlScene);
  });
  ```
  *(Note: Any external model files, textures, and `.bin` buffers MUST have their file extensions registered line-by-line in `exsass.txt` to ensure they are packed for Windows desktop builds).*

### Standard Boilerplate Pattern using Three.js

```javascript
// "Game Title" (640, 480)
(async () => {
  const THREE = await import('three');
  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');

  const WIDTH = 640;
  const HEIGHT = 480;

  const canvasElement = document.getElementById('tinclecanvas');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, WIDTH / HEIGHT, 0.1, 1000);
  camera.position.set(0, 2, 4);

  const renderer = new THREE.WebGLRenderer({ canvas: canvasElement, antialias: true });
  renderer.setSize(WIDTH, HEIGHT, false);

  const controls = new OrbitControls(camera, canvasElement);
  controls.enableDamping = true;

  // ... Game Objects, State Machine, and Scene Flow ...

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }
  animate();
})();
```

### 7.2 Planck.js (2D Physics Engine: Box2D for JavaScript) (Version: v1.3.0)

Planck.js is pre-loaded globally via `<script src="./libs/planck.min.js">` in the host HTML templates. You can use it directly via the global `planck` object for high-performance 2D rigid-body simulations (equivalent to Box2D / cannoli in native TinCLE).

* **Global Access**: Access the engine directly without imports: `const pl = window.planck || planck; const Vec2 = pl.Vec2;`.
* **Physics World & Coordinate Scaling**:
  Planck.js operates in real-world metric units (meters, seconds), whereas the canvas operates in screen pixels. Always define a coordinate scaling factor (e.g., `SCALE = 30` pixels per meter):
  * Physical Coordinate to Screen: `screenX = bodyPos.x * SCALE; screenY = bodyPos.y * SCALE;`
  * Gravity: Set natural gravity downward, e.g., `const world = pl.World(Vec2(0, 10));`.
* **Simulation Step & Rendering**:
  In your main animation loop, advance the simulation before drawing:
  ```javascript
  world.step(1 / 60);
  // Retrieve body transform and render to 2D Canvas:
  const pos = myBody.getPosition();
  const angle = myBody.getAngle();
  ctx.save();
  ctx.translate(pos.x * SCALE, pos.y * SCALE);
  ctx.rotate(angle);
  // ... Draw shape primitives ...
  ctx.restore();
  ```

#### Standard Boilerplate Pattern using Planck.js

```javascript
// "2D Physics Demo" (640, 480)
const canvas = document.getElementById('tinclecanvas');
const ctx = canvas.getContext('2d');
const WIDTH = 640;
const HEIGHT = 480;
const SCALE = 30; // 30 pixels = 1 meter

const pl = planck;
const Vec2 = pl.Vec2;
const world = pl.World(Vec2(0, 10));

// Ground
const ground = world.createBody();
ground.createFixture(pl.Edge(Vec2(-10, HEIGHT / SCALE - 0.5), Vec2(WIDTH / SCALE + 10, HEIGHT / SCALE - 0.5)));

// Dynamic Box
const box = world.createDynamicBody(Vec2(WIDTH / 2 / SCALE, 2));
box.createFixture(pl.Box(0.8, 0.8), { density: 1.0, restitution: 0.6 });

function gameLoop() {
  world.step(1 / 60);

  ctx.fillStyle = '#222';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // Render Ground
  ctx.strokeStyle = '#4ade80';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, HEIGHT - 15);
  ctx.lineTo(WIDTH, HEIGHT - 15);
  ctx.stroke();

  // Render Box
  const pos = box.getPosition();
  const angle = box.getAngle();
  ctx.save();
  ctx.translate(pos.x * SCALE, pos.y * SCALE);
  ctx.rotate(angle);
  ctx.fillStyle = '#f43f5e';
  ctx.fillRect(-0.8 * SCALE, -0.8 * SCALE, 1.6 * SCALE, 1.8 * SCALE);
  ctx.restore();

  requestAnimationFrame(gameLoop);
}
gameLoop();
```

### 7.3 cannon-es (3D Physics Engine: Box3D for JavaScript) (Version: v0.20.0)

`cannon-es` (v0.20.0) provides robust, lightweight 3D rigid-body physics simulation seamlessly integrated with Three.js.

* **Template Importmap**:
  The host HTML provides the import mapping for `cannon-es`:
  ```json
  {
    "imports": {
      "cannon-es": "./libs/cannon-es/cannon-es.js"
    }
  }
  ```
* **Dynamic Import**:
  Import dynamically inside your async IIFE:
  ```javascript
  const CANNON = await import('cannon-es');
  ```
* **Simulation Loop & Mesh Synchronization**:
  In your main animation loop, step the physics world (fixed time step e.g. `1 / 60`) and copy the physics body's position and quaternion directly to the Three.js mesh:
  ```javascript
  world.fixedStep();
  mesh.position.copy(body.position);
  mesh.quaternion.copy(body.quaternion);
  ```

#### Standard Boilerplate Pattern (Three.js + cannon-es)

```javascript
// "3D Physics Demo" (640, 480)
(async () => {
  const THREE = await import('three');
  const CANNON = await import('cannon-es');

  const WIDTH = 640;
  const HEIGHT = 480;

  const canvas = document.getElementById('tinclecanvas');
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
  renderer.setSize(WIDTH, HEIGHT, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, WIDTH / HEIGHT, 0.1, 100);
  camera.position.set(0, 5, 10);
  camera.lookAt(0, 0, 0);

  // 1. Setup Physics World
  const world = new CANNON.World({
    gravity: new CANNON.Vec3(0, -9.82, 0)
  });

  // 2. Physics & Visual Ground
  const groundBody = new CANNON.Body({
    type: CANNON.Body.STATIC,
    shape: new CANNON.Plane()
  });
  groundBody.quaternion.setFromEuler(-Math.PI / 2, 0, 0); // Flat on XZ
  world.addBody(groundBody);

  const groundMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(20, 20),
    new THREE.MeshBasicMaterial({ color: 0x334155, wireframe: true })
  );
  groundMesh.rotation.x = -Math.PI / 2;
  scene.add(groundMesh);

  // 3. Falling Dynamic Box
  const boxBody = new CANNON.Body({
    mass: 1,
    shape: new CANNON.Box(new CANNON.Vec3(0.5, 0.5, 0.5)), // Half-extents
    position: new CANNON.Vec3(0, 5, 0)
  });
  world.addBody(boxBody);

  const boxMesh = new THREE.Mesh(
    new THREE.BoxGeometry(1, 1, 1),
    new THREE.MeshNormalMaterial()
  );
  scene.add(boxMesh);

  // Game Loop
  function animate() {
    requestAnimationFrame(animate);

    world.fixedStep();
    boxMesh.position.copy(boxBody.position);
    boxMesh.quaternion.copy(boxBody.quaternion);

    renderer.render(scene, camera);
  }
  animate();
})();
```

### 7.4 Howler.js (Audio Library: Standard Audio & 3D Spatial Sound) (Version: v2.2.4)

Howler.js (v2.2.4) is pre-loaded globally via `<script src="./libs/howler.min.js">` in the host HTML templates. It provides robust cross-browser audio playback, automated Web Audio unlock upon first user gesture, seamless looping, and volume control.

* **Global Access**: Access directly via `Howl` or `Howler` without imports.
* **Basic Sound & BGM Instantiation**:
  ```javascript
  // 1. Looping BGM (OGG recommended)
  const bgm = new Howl({
    src: ['bgm.ogg'],
    loop: true,
    volume: 0.6
  });

  // 2. Sound Effect (WAV/OGG)
  const seExplosion = new Howl({
    src: ['explosion.wav'],
    volume: 0.8
  });

  // Playback:
  // Note: Modern browsers require a user interaction (click/keypress) before audio can play.
  bgm.play();
  seExplosion.play();
  ```
* **Global Master Volume**: Control all sounds globally via `Howler.volume(0.5);`.
* **Asset Packaging Requirement**: Always ensure all audio extensions (`.ogg`, `.wav`) are registered in `exsass.txt` so `rjasplns` packs them into desktop builds.

#### Standard Integration Example

```javascript
// Start audio on first user input to satisfy browser autoplay policies:
window.addEventListener('keydown', () => {
  if (!bgm.playing()) {
    bgm.play();
  }
}, { once: true });
```
