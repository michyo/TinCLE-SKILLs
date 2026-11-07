---
name: tincle-aon2
description: Use when loading, rendering, or manipulating VRML 2.0 (.wrl) 3D worlds, cameras, or interactive node scripts in TinCLE. Provides vtrushka C API specifications and limitations. [TinCLE Add-On Skill v0.14]
---

# SKILL_AON2.md - TinCLE Add-On Talent Chip [VRML 3D World Creation]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

## 1. Overview

* **Purpose & Value:** High-level 3D world loader and software renderer pipeline for TinCLE. Completely eliminates the need to manually manage 3D vertex buffers, transformation matrices, camera projections, or custom sorting in pure C.
* **Declarative 3D World Creation:** Enables developers to build complex 3D environments, animated models, materials, and textures using standard **VRML 2.0 (`.wrl`)** files exported from 3D DCC tools (e.g. Blender).
* **Zero-Friction Engine Integration:** Seamlessly plugs into TinCLE's runtime loop via `vtrushka_update(dt)` and `vtrushka_draw()`, leveraging TinCLE's internal `SDL_RenderGeometry` backend for both Windows (Desktop EXE) and WebAssembly (Emscripten HTML5).
* **C-Driven Interactive Logic:** Replaces JavaScript inside VRML `Script` nodes with high-performance C callback handlers (`vtrushka_script_set_handler`), allowing direct manipulation of 3D transforms, switches, and touch sensor events.
* **Distribution & Runtime:** Simply `#include "libs/vtrushka.h"` in your C source, and ship `vtrushka.dll` (Windows) or `vtrushka.wasm` (WebAssembly) alongside your game executable/bundle.
* **Requirements:** vtrushka requires latest version of TinCLE, which must expose: `tincle_load_asset()`, `tincle_load_image()`, `tincle_get_texture()`, `tincle_create_image_from_pixels()`, `tincle_get_renderer()`

## 2. Distribution

When using vtrushka, you must include either vtrushka.dll or vtrushka.wasm-whichever is appropriate for the target platform-in your distribution. An example of the minimum set of distribution files, including these, is as follows.

| Platform | Required files |
| --- | --- |
| Windows | `game.exe`, `tincle.dll`, `SDL2.dll`,`SDL2_gfx.dll`, `SDL2_ttf.dll`, `game.data`, `CREDITS.txt`, `vtrushka.dll` |
| WebAssembly | `index.html`, `index.js`, `index.wasm`, `index.data`, `vtrushka.wasm` |

## 2. API Reference

### 2.1. System Management

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `void vtrushka_init(SDL_Renderer* renderer);` | **Main entry.** Call once at game startup. Pass `tincle_get_renderer()`. Initializes all 64 model slots. Must be called before any other vtrushka API. |
| `void vtrushka_shutdown(void);` | Frees all loaded models, script handlers, and internal scratch buffers. Call at game shutdown. Safe to call if not initialized. |
| `int vtrushka_load_wrl(const char* filename);` | **Loads a .wrl file via `tincle_load_asset()`.** Auto-detects header. **VRML 2.0 only** - returns `VTRUSHKA_INVALID_ID` (-1) for VRML 1.0. On success returns a slot ID (0-63). Returns -1 on parse error, missing file, or no free slot. |
| `void vtrushka_unload(int vrml_id);` | Frees the model and all associated resources. Also clears any script handlers registered for this slot. Safe to call with invalid ID. |
| `const char* vtrushka_get_version(void);` | Returns read-only string of vtrushka version (e.g., `"0.14"`). |

### 2.2. Camera

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `void vtrushka_camera_default(VtrushkaCamera* cam);` | Fills the struct with defaults: position (0,0,10), yaw=0, pitch=0, fov_y=45 deg, near=0.1, far=1000. |
| `void vtrushka_set_camera(int vrml_id, const VtrushkaCamera* cam);` | Replaces the entire camera state. |
| `void vtrushka_get_camera(int vrml_id, VtrushkaCamera* out_cam);` | Reads current camera state. |
| `void vtrushka_camera_move(int vrml_id, float forward, float right, float up);` | **FPS-style translation.** `forward` moves along the view direction, `right` is strafe, `up` is world-Y offset. Units are world units. Combine with `dt` in your game loop. |
| `void vtrushka_camera_rotate(int vrml_id, float dyaw, float dpitch);` | **FPS-style rotation.** `dyaw` rotates around world Y (positive = turn right). `dpitch` tilts up/down, **auto-clamped to +/- 89 deg** to prevent gimbal flip. |
| `void vtrushka_camera_bind_viewpoint(int vrml_id, int viewpoint_node_id);` | Alias for `vtrushka_viewpoint_bind`. |

**Related struct:**
```c
typedef struct {
    float position[3];  /* World coordinates */
    float yaw;          /* Radians. 0 = looking down -Z. */
    float pitch;        /* Radians. Positive = looking up. */
    float fov_y;        /* Vertical FOV in radians. Default 45 deg. */
    float near_z, far_z;
} VtrushkaCamera;
```

### 2.3. Viewpoint (Scene-Defined Camera Positions)

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `int vtrushka_viewpoint_count(int vrml_id);` | Number of `Viewpoint` nodes in the loaded world. Returns 0 on error. |
| `int vtrushka_viewpoint_get_info(int vrml_id, int index, VtrushkaViewpointInfo* out);` | Fills info for the index-th viewpoint. **Returns 0 on success, -1 on bad index or error.** Fields: `node_id`, `def_name`, `description`, `position[3]`, `yaw`, `pitch`. |
| `int vtrushka_viewpoint_find_by_name(int vrml_id, const char* def_name);` | Finds a viewpoint by its DEF name. **Returns node_id, or -1 if not found.** |
| `int vtrushka_viewpoint_find_by_description(int vrml_id, const char* description);` | Finds a viewpoint by its `description` field. **Exact match, case-sensitive.** Returns node_id or -1. |
| `void vtrushka_viewpoint_bind(int vrml_id, int viewpoint_node_id);` | **Teleports the camera to the viewpoint's world position and orientation.** `node_id = -1` unbinds (camera stays in place). **Note:** Unlike VRML's spec, vtrushka copies the transform once - the camera does NOT follow subsequent animations of the viewpoint. |
| `int vtrushka_viewpoint_get_current(int vrml_id);` | Returns the currently bound viewpoint's node_id, or -1. |

**Related struct:**
```c
typedef struct {
    int         node_id;
    const char* def_name;
    const char* description;
    float       position[3];
    float       yaw;
    float       pitch;
} VtrushkaViewpointInfo;
```

### 2.4. Rendering & Animation

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `void vtrushka_draw(int vrml_id, float x, float y, float z, float rx, float ry, float rz, float scale);` | **Call every frame** inside your draw callback. Applies root transform (Z->Y->X Euler angles in degrees, uniform scale), then projects all meshes via the current camera. Triangles are depth-sorted (painter's algorithm) before submission to `SDL_RenderGeometry`. **Backface culling is active** - meshes must have CCW winding when viewed from outside. |
| `void vtrushka_update(int vrml_id, float dt);` | **Call every frame** with elapsed seconds. Advances `TimeSensor` fractions, evaluates `Interpolator` nodes, and propagates `value_changed` events to `Transform` targets via ROUTE. |

* **Important:** `rx, ry, rz` are Euler angles in **degrees** (not radians, unlike VRML's rotation field). Applied in Z→Y→X order.

### 2.5. Picking & Interaction

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `int vtrushka_pick_node(int vrml_id, float screen_x, float screen_y);` | **Ray-cast from 2D screen pixel to 3D world.** Returns the node_id of the nearest mesh hit, or -1. Invisible nodes (e.g. inactive `Switch` children) are skipped. Cost: O(total triangles). Suitable for click/tap events only. |
| `int vtrushka_find_touch_sensor(int vrml_id, int node_id);` | Returns the `sensor_id` of a `TouchSensor`/`PlaneSensor`/etc. whose target is the given node_id. Returns -1 if none. |
| `void vtrushka_trigger_sensor(int vrml_id, int sensor_id, bool active);` | Fires a sensor as if the user clicked/released. Propagates `isActive` and (on FALSE->TRUE) `touchTime` through ROUTE, invoking script handlers or transform updates. |

### 2.6. Script - Basic (Low-Level)

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `const char* vtrushka_get_script_code(int vrml_id, int script_id);` | Returns the raw `url[0]` string of the `Script` node (including the `javascript:` prefix if present). **For reading only** - vtrushka does not execute JavaScript. |
| `void vtrushka_set_script_executor(VtrushkaScriptExecutor fn, void* user_data);` | Registers a **global fallback executor** invoked for `Script.eventIn` events that have no per-event handler registered (see Section 2.7). |
| `void vtrushka_dispatch_script(int vrml_id, int script_id, const char* event_in_name, const char* value_repr);` | Manually invokes the global executor. Rarely needed - prefer per-event handlers in Section 2.7. |

**Executor signature:**
```c
typedef void (*VtrushkaScriptExecutor)(int vrml_id, int script_id,
                                       const char* event_in_name,
                                       const char* value_repr,
                                       float timestamp, void* user_data);
```

### 2.7. Script - Handlers (Recommended)

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `int vtrushka_script_count(int vrml_id);` | Number of `Script` nodes in the world. |
| `int vtrushka_script_get_info(int vrml_id, int index, VtrushkaScriptInfo* out);` | Fills `script_id`, `script_name`, and port counts (eventIn/eventOut/field). Returns 0 on success. |
| `int vtrushka_script_find_by_name(int vrml_id, const char* def_name);` | Returns script_id by DEF name, or -1. |
| `const char* vtrushka_script_get_port_name(int vrml_id, int script_id, int kind, int index);` | Enumerates port names. `kind`: **0=eventIn, 1=eventOut, 2=field**. Returns NULL on invalid arguments. |
| `void vtrushka_script_set_handler(int vrml_id, int script_id, const char* event_in_name, VtrushkaScriptHandler fn, void* user_data);` | **Registers a C function to be invoked whenever the named eventIn fires** (via ROUTE or `vtrushka_trigger_sensor`). This is the primary way to implement Script behavior in vtrushka. |
| `void vtrushka_script_clear_handler(int vrml_id, int script_id, const char* event_in_name);` | Removes a previously registered handler. |
| `void vtrushka_script_send_event(int vrml_id, int script_id, const char* event_out_name, const char* value_repr);` | **Fires an eventOut from C code.** Propagates through ROUTE to all downstream nodes. Use inside a handler to signal completion or drive animations. |
| `const char* vtrushka_script_get_field(int vrml_id, int script_id, const char* field_name);` | Reads a `field` value as a VRML-syntax string (e.g. `"TRUE"`, `"3.14"`, `"1 2 3"`). Persistent across calls. Returns NULL if not found. |
| `int vtrushka_script_set_field(int vrml_id, int script_id, const char* field_name, const char* value_repr);` | Writes a `field` value. Returns 0 on success. |

**Related struct:**
```c
typedef struct {
    int         script_id;
    const char* script_name;
    int         event_in_count;
    int         event_out_count;
    int         field_count;
} VtrushkaScriptInfo;
```

**Handler signature:**
```c
typedef void (*VtrushkaScriptHandler)(int vrml_id, int script_id,
                                      const char* event_in_name,
                                      const char* value_repr, void* user_data);
```

### 2.8. Node Direct Manipulation

| Function Signature | Description & Critical Notes [Args / Return] |
| --- | --- |
| `int vtrushka_find_node_by_name(int vrml_id, const char* def_name);` | Returns the node_id of a DEF-named node, or -1. Works for any node type (`Transform`, `Switch`, `Script`, etc.). |
| `int vtrushka_node_set_field_string(int vrml_id, int node_id, const char* field_name, const char* value_repr);` | **Sets a node field from C.** Supported fields: <br>* `Switch.whichChoice` (integer string) <br>* `Transform.translation` / `rotation` / `scale` / `center` (space-separated floats) <br>Returns 0 on success. |
| `int vtrushka_node_get_which_choice(int vrml_id, int node_id);` | Reads `Switch.whichChoice`. Returns the value, or **-2 if the node is not a Switch**. |

---

## 3. Value Representation Format (`value_repr`)

All string-based event/field values follow VRML syntax:

| VRML Type | C String Example |
| --- | --- |
| `SFBool` | `"TRUE"`, `"FALSE"` |
| `SFFloat` / `SFTime` | `"3.14"`, `"0.5"`, `"1234567890.0"` |
| `SFInt32` | `"42"`, `"-1"` |
| `SFVec2f` | `"1.0 2.0"` |
| `SFVec3f` / `SFColor` | `"1.0 0.5 0.0"` |
| `SFRotation` | `"0 1 0 1.5708"` (axis x y z, angle in radians) |
| `SFString` | `"hello"` |

**Parsing:** vtrushka uses `strtod` / `sscanf` internally. Whitespace-separated tokens. No brackets or commas needed.

---

## 4. Coverage and Limitations

### 4.1. Supported VRML 2.0 Nodes

| Category | Nodes |
| --- | --- |
| **Grouping** | `Anchor` (partial), `Billboard`, `Collision` (parsed, no collision), `Group`, `Transform` |
| **Special Groups** | `Inline` (parsed, not fetched), `LOD` (parsed, not active), `Switch` (FULLY SUPPORTED) |
| **Common** | `AudioClip` (parsed only), `DirectionalLight`, `PointLight`, `Script` (FULLY SUPPORTED) (C handlers), `Shape`, `Sound` (parsed only), `SpotLight`, `WorldInfo` |
| **Sensors** | `CylinderSensor`, `PlaneSensor`, `ProximitySensor`, `SphereSensor`, `TimeSensor` (FULLY SUPPORTED), `TouchSensor` (FULLY SUPPORTED), `VisibilitySensor` |
| **Geometry** | `Box`, `Cone`, `Cylinder`, `ElevationGrid`, `Extrusion`, `IndexedFaceSet`, `IndexedLineSet`, `PointSet`, `Sphere`, `Text` (rectangle placeholder) |
| **Geometric Properties** | `Color`, `Coordinate`, `Normal`, `TextureCoordinate` |
| **Appearance** | `Appearance`, `FontStyle` (parsed only), `ImageTexture` (FULLY SUPPORTED), `Material` (FULLY SUPPORTED), `MovieTexture` (static only), `PixelTexture` (FULLY SUPPORTED), `TextureTransform` (parsed, not applied) |
| **Interpolators** | `ColorInterpolator`, `CoordinateInterpolator`, `NormalInterpolator`, `OrientationInterpolator`, `PositionInterpolator`, `ScalarInterpolator` |
| **Bindable** | `Background` (parsed only), `Fog` (parsed only), `NavigationInfo` (parsed only), `Viewpoint` (FULLY SUPPORTED) |

### 4.2. Constraints & Known Limitations

| Feature | Status | Notes |
| --- | --- | --- |
| **VRML 1.0** | NOT SUPPORTED | `vtrushka_load_wrl` returns -1. **Use VRML 2.0.** |
| **JavaScript / Java execution** | NOT SUPPORTED | `Script.url` is stored but not executed. Use C handlers (Section 2.7). |
| **Texture repeat (tile)** | NOT SUPPORTED | `repeatS`/`repeatT` are read but not applied. UVs are clamped to [0,1]. **Workaround:** tile geometry manually via `USE`d shapes. |
| **`TextureTransform`** | NOT SUPPORTED | Parsed but not applied. |
| **`MovieTexture` animation** | NOT SUPPORTED | Static texture only. |
| **`Background` skybox** | NOT SUPPORTED | Parsed but not rendered. **Workaround:** use `tincle_draw_image_ex` as fullscreen backdrop. |
| **`Fog`** | NOT SUPPORTED | Parsed but not applied. **Workaround:** author pre-tinted textures. |
| **`NavigationInfo`** | NOT SUPPORTED | Parsed but not applied (use `vtrushka_camera_*` instead). |
| **`Collision` detection** | NOT SUPPORTED | Node parsed but no collision response. |
| **`Anchor` URL navigation** | NOT SUPPORTED | Node parsed, but clicking does not navigate. |
| **`Inline.url` fetching** | NOT SUPPORTED | Node parsed, but external file not loaded. |
| **`LOD` distance-based switching** | NOT SUPPORTED | Node parsed; all levels rendered. |
| **Viewpoint follows animated parent** | NOT SUPPORTED | Bind copies transform once; camera does not track subsequent animation. |
| **Viewpoint stack (`set_bind` push/pop)** | NOT SUPPORTED | Only a single "currently bound" slot. |
| **`PROTO` body multi-node expansion** | PARTIALLY SUPPORTED | Only `body_root` (first node) is expanded. Routes inside PROTO body are ignored. |
| **`EXTERNPROTO` URL fetch** | NOT SUPPORTED | Not fetched; instance renders empty. |
| **`Text` font rendering** | PARTIALLY SUPPORTED | Renders as a flat rectangle placeholder. **Workaround:** use `tincle_draw_text` overlaid on the scene. |
| **Multi-texture-per-face** | NOT SUPPORTED | Only one texture per `Appearance`. |
| **Perspective-correct texturing** | PARTIALLY SUPPORTED | Affine interpolation via `SDL_RenderGeometry`. Distortion visible on steep angles. |
| **Backface culling** | CAUTION | Active; meshes must have CCW winding viewed from outside. |

---

## 5. Minimal Bootstrap Example

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include "libs/vtrushka.h"

#ifdef __EMSCRIPTEN__
  #include <SDL2/SDL_scancode.h>
  #include <SDL2/SDL2_gfxPrimitives.h>
#else
  #include "libs/SDL_scancode.h"
  #include "libs/SDL2_gfxPrimitives.h"
  #include <windows.h>
#endif

static int g_world;

void game_update(float dt) {
  vtrushka_update(g_world, dt);

  float fwd = (tincle_key_pressed(SDL_SCANCODE_W) ? 1.0f : 0.0f)
            - (tincle_key_pressed(SDL_SCANCODE_S) ? 1.0f : 0.0f);
  float rgt = (tincle_key_pressed(SDL_SCANCODE_D) ? 1.0f : 0.0f)
            - (tincle_key_pressed(SDL_SCANCODE_A) ? 1.0f : 0.0f);
  vtrushka_camera_move(g_world, fwd * 5.0f * dt, rgt * 5.0f * dt, 0.0f);
}

void game_draw(void) {
  tincle_clear((TinCLE_Color){0, 0, 0, 255});
  vtrushka_draw(g_world, 0, 0, 0, 0, 0, 0, 1.0f);
}

void game_load(void) {
  vtrushka_init(tincle_get_renderer());
  g_world = vtrushka_load_wrl("world.wrl");
  tincle_add_state(0, game_update, game_draw);
  tincle_change_state(0);
}

// --- Entry Point Bootstrapper ---
#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) { tincle_start(game_load, "BOX", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) { tincle_start(game_load, "BOX", true, 640, 480, TINCLE_MODE_2D_NORMAL); return 0; }
#endif
```

```vrml
#VRML V2.0 utf8
Group {
  children [
    Shape {
      appearance Appearance {
        material Material {
          diffuseColor 1.0 0.0 0.0
        }
      }
      geometry Box {
        size 2.0 2.0 2.0
      }
    }
  ]
}
```

### Typical Uses of TouchSensor + Script

```c
/* Script handler example: combination lock */
static void on_combination(int id, int sid, const char* ev,
                           const char* val, void* ud) {
    if (strcmp(val, "TRUE") == 0) {
        vtrushka_script_set_field(id, sid, "unlocked", "TRUE");
    }
}

/* In game_load() */
int sid = vtrushka_script_find_by_name(g_world, "OpenVault");
vtrushka_script_set_handler(g_world, sid, "combinationEntered",
                            on_combination, NULL);
```
