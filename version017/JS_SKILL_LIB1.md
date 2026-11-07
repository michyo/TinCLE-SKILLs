---
name: tincle-js-lib1
description: Use when implementing, integrating, or configuring external 3D/2D physics, graphics, or audio libraries in TinCLE JS (Three.js, Planck.js, cannon-es, Howler.js, Obelisk.js). [TinCLE Library Skill v0.17]
---

# SKILL_LIB1.md - TinCLE JS Pre-Installed Libraries Reference

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

This document provides technical integration guidelines, API boundaries, and standard boilerplate code for third-party libraries pre-installed in the `./libs/` directory of the TinCLE JS environment.

## 1. Libraries available when creating `game.js`.

You can use the following libraries when creating `game.js`.

### 1.1 Three.js (JavaScript 3D library) (Version: r186)

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

### 1.2 Planck.js (2D Physics Engine: Box2D for JavaScript) (Version: v1.3.0)

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

### 1.3 cannon-es (3D Physics Engine: Box3D for JavaScript) (Version: v0.20.0)

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

### 1.4 Howler.js (Audio Library: Standard Audio & 3D Spatial Sound) (Version: v2.2.4)

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

### 1.5 Obelisk.js (JavaScript library for building isometric pixel objects) (Version: v1.2.1)

Obelisk.js (v1.2.1) is pre-loaded globally via `<script src="./libs/obelisk.min.js">` in the host HTML templates. It provides an intuitive, high-performance pixel-engine to construct pseudo-3D isometric and voxel graphics directly onto HTML5 2D Canvas without 3D WebGL overhead.

* **Global Access**:
  Access the namespace directly through `obelisk` without import statements (e.g. `const ob = window.obelisk || obelisk;`).
* **Canvas Binding & Pixel View**:
  Always bind the `PixelView` directly to `#tinclecanvas` using a custom `Point` as the coordinate origin (center of the canvas):
  ```javascript
  const canvas = document.getElementById('tinclecanvas');
  const point = new obelisk.Point(WIDTH / 2, HEIGHT / 2);
  const pixelView = new obelisk.PixelView(canvas, point);
  ```
* **Coordinate System & Core Primitives**:
  * Coordinates use 3D grid vectors via `obelisk.Point3D(x, y, z)`. The isometric plane spans across X and Y, while Z represents vertical height.
  * **Bricks & Primitives**: Construct dimensional primitives using dimension objects and render them through `pixelView.renderObject(primitive, point3D)`:
    * `Cube`: `new obelisk.Cube(dimension, color, border)`
    * `Brick`: `new obelisk.Brick(dimension, color, border)`
    * `Pyramid`: `new obelisk.Pyramid(dimension, color, border)`
    * `SideX / SideY`: Planar surfaces for walls and custom geometry.
* **Palette & Color Shading**:
  Colors automatically compute realistic isometric shading across top, horizontal, and vertical facets:
  ```javascript
  // Base color (hex) with optional highlight/shadow configuration:
  const cubeColor = new obelisk.CubeColor().getByHorizontalColor(0x38bdf8);
  ```
* **Interactive Voxel Destruction & Dynamic Re-Rendering**:
  Because Obelisk.js rasterizes directly into the 2D canvas pixel buffer, maintain game actors and destructible terrain as logical grid arrays (e.g., `grid[x][y][z]`). On each animation frame, clear the canvas (`pixelView.clear()` or standard `ctx.fillRect`) and render voxels sorted from back-to-front (`x + y + z` depth sorting) to guarantee accurate isometric occlusion.

#### Standard Boilerplate Pattern using Obelisk.js

```javascript
// "Isometric Voxel Arena" (640, 480)
(() => {
  const WIDTH = 640;
  const HEIGHT = 480;
  const canvas = document.getElementById('tinclecanvas');
  const ctx = canvas.getContext('2d');

  // 1. Initialize Isometric Viewport centered on screen
  const origin = new obelisk.Point(WIDTH / 2, 160);
  const pixelView = new obelisk.PixelView(canvas, origin);

  // 2. Define Shared Voxel Dimensions & Colors
  const UNIT_SIZE = 16;
  const cubeDim = new obelisk.CubeDimension(UNIT_SIZE, UNIT_SIZE, UNIT_SIZE);
  const floorDim = new obelisk.BrickDimension(UNIT_SIZE, UNIT_SIZE);

  const floorColor = new obelisk.BrickColor().getByHorizontalColor(0x334155);
  const crateColor = new obelisk.CubeColor().getByHorizontalColor(0xf59e0b);
  const heroColor = new obelisk.CubeColor().getByHorizontalColor(0x06b6d4);

  const floorBrick = new obelisk.Brick(floorDim, floorColor);
  const crateCube = new obelisk.Cube(cubeDim, crateColor);
  const heroCube = new obelisk.Cube(cubeDim, heroColor);

  // 3. Simple Game State
  const player = { x: 0, y: 0, z: 0 };
  const crates = [
    { x: 32, y: 32, z: 0 },
    { x: 32, y: 32, z: UNIT_SIZE },
    { x: -32, y: 48, z: 0 }
  ];

  // Input Handling
  const keys = {};
  window.addEventListener('keydown', (e) => { keys[e.code] = true; });
  window.addEventListener('keyup', (e) => { keys[e.code] = false; });

  function gameLoop() {
    // Movement on isometric grid
    const speed = 2;
    if (keys['ArrowUp'] || keys['KeyW']) { player.x -= speed; player.y -= speed; }
    if (keys['ArrowDown'] || keys['KeyS']) { player.x += speed; player.y += speed; }
    if (keys['ArrowLeft'] || keys['KeyA']) { player.x -= speed; player.y += speed; }
    if (keys['ArrowRight'] || keys['KeyD']) { player.x += speed; player.y -= speed; }

    // Clear canvas
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Render Grid Floor (Back to Front)
    for (let x = -4; x <= 4; x++) {
      for (let y = -4; y <= 4; y++) {
        pixelView.renderObject(floorBrick, new obelisk.Point3D(x * UNIT_SIZE, y * UNIT_SIZE, 0));
      }
    }

    // Render Destructible Crates
    crates.forEach(c => {
      pixelView.renderObject(crateCube, new obelisk.Point3D(c.x, c.y, c.z));
    });

    // Render Player
    pixelView.renderObject(heroCube, new obelisk.Point3D(player.x, player.y, player.z));

    requestAnimationFrame(gameLoop);
  }
  gameLoop();
})();
```
