---
name: tincle-ba
description: Master skill sheet for bandpisa (Blueprint Arranger & Network Delineator for Plating Imagined Spaces to AI). Covers interactive map editor operations, UI controls, multi-layer tile arrangement, spatial semantic annotations, and comprehensive JSON map data structures for AI-first game development with TinCLE. [TinCLE Tool Skill v0.18]
---

# SKILL_BA.md - TinCLE Companion Specification Document [bandpisa Map Editor Skill]

* **Tool Name:** `bandpisa` (Blueprint Arranger & Network Delineator for Plating Imagined Spaces to AI)
* **Target Version:** Version 0.18
* **Author / Copyright:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.
* **Companion Engine:** TinCLE (AI-First 2D Game Engine)
* **Official Website:** https://michyo.net/tincle/

---

## 1. Overview & Core Philosophy

`bandpisa` is the official visual map editor and spatial blueprint authoring tool for the AI-first game engine **TinCLE**.
It bridges human imagination and autonomous AI game development:

1. **For Human Users:** Provides an intuitive, responsive, and lightweight GUI (Dear ImGui + Win32/OpenGL3) for painting multi-layer tilemaps and delineating meaningful spatial semantic areas (e.g., "Castle", "Dungeon Entrance", "Boss Arena", "Treasure Chamber", "NPC Spawn", "Trigger Zone").
2. **For AI Agents:** Produces standardized, clean JSON map descriptors that allow the AI to immediately understand level topology, passable routes, environmental decor, and gameplay semantics without requiring complex vision models.

---

## 2. User Guidance & Editor Operations (For Explaining to Humans)

When guiding human creators on using `bandpisa`, the AI Agent should reference the following controls, shortcuts, and operational flows:

### 2.1 Launch & Workflow Modes
* **Startup Modal:**
  * **New Map Tab:** Select a tileset PNG atlas image, define tile dimensions (default: 48x48 px), and set map dimensions (width x height, up to 1024x1024 tiles).
  * **Open Map Tab:** Select an existing `.json` map file. The editor automatically resolves and loads the companion tileset image located in the same directory.
* **Language Support:**
  * Fully bilingual (English / Japanese). Default is English.
  * Switch anytime via `Language -> English / 日本語`. Preferences are saved across sessions in `bandpisa.ini`.
* **Safe Exit & Unsaved Warning:**
  * If a user tries to create a new map, open another file, or close the application with unsaved edits, a confirmation dialog pops up offering **"Save & Proceed"**, **"Don't Save"**, and **"Cancel"**.

### 2.2 Viewport Navigation (Frustum-Culled Canvas)
* **Pan (Scroll):** Drag with **Middle Mouse Button** or hold **`Space` + Left Mouse Drag**.
* **Zoom:** Scroll the **Mouse Wheel** to zoom in/out relative to the cursor position (0.1x to 8.0x).
* **Reset Camera:** Press the **`Home`** button on the toolbar or select `View -> Reset Camera`.
* **High-Performance Frustum Culling:** Even for massive maps up to 1024x1024 tiles (~1 million tiles), only visible tiles within the screen viewport are submitted to GPU draw calls, maintaining a constant 60 FPS.

### 2.3 Tile Editing Tools & Shortcuts

| Tool | Shortcut | Description |
| :--- | :---: | :--- |
| **Pen** | `P` | Places the selected atlas tile on the active layer with left-click/drag. |
| **Eraser** | `E` | Clears tiles on the active layer (resets to `-1` / empty). |
| **Box (Rect)** | `R` | Fills a rectangular bounding area with the selected tile. |
| **Bucket (Fill)** | `F` | 4-directional Flood Fill to replace connected identical tiles. |
| **Picker** | `I` | Eyedropper: picks the tile ID under the cursor into the active palette. |
| **Memo** | `A` | Click and drag on the map canvas to immediately create an annotation area. |
| **Right Click** | — | Quick Eraser: right-click or drag anytime to delete tiles. |
| **Undo** | `Ctrl + Z` | Reverts the last action (up to 50 historical snapshot steps). |
| **Redo** | `Ctrl + Y` | Re-applies the undone action (also `Ctrl + Shift + Z`). |

### 2.4 Multi-Layer Structure (4 Layers with Full Transparency)
* **Layer 0 (Ground):** Base terrain (grass, water, dirt, floor stone).
* **Layer 1 (Decoration):** Lower accents and pathways (carpets, road paths, edges, puddles).
* **Layer 2 (Objects):** Solid structures and props (walls, trees, chests, furniture, doors).
* **Layer 3 (Overlay):** Upper canopy and overhead elements (roofs, tree tops, clouds).
* **Full Alpha Transparency:** Upper layers blend seamlessly over lower layers using standard `GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA` OpenGL blending.
* **Inline Layer Renaming:** Users can rename any layer directly in the layer panel; changes are stored in the exported JSON.
* **Layer Visibility & Opacity:** Toggle the checkbox to hide/show layers, and use the opacity slider to preview underlying structures.

### 2.5 Spatial Annotations (Semantics & Overlapping Memos)
* **Adding Memos:**
  * Method 1: Select the **Memo (A)** tool and drag a rectangle on the canvas.
  * Method 2: Click **`+ Add New Memo Manually`** in the Annotations panel, then drag to select the desired area on the canvas.
* **Overlapping Support:** Memo areas can naturally overlap (e.g., a "Castle Entrance" memo inside a larger "Royal Castle Grounds" memo). Each area retains its identity, color, and properties.
* **Redefining Areas:** Select any memo from the list and click **`Redefine Area on Map (Drag)`** to update its bounds without deleting other memos.
* **Instant Camera Centering:** Clicking a memo in the list automatically pans and centers the canvas camera directly onto the memo area.
* **Memo Opacity Slider:** Use the `Memo: 0.xx` slider in the top toolbar to adjust memo highlight transparency (0.05 to 1.00) so background tiles remain clear.

### 2.6 Map Resizing & Interactive Cropping
* Open `Edit -> Resize Map...` anytime during authoring.
* Supports expanding or shrinking maps (from 1x1 up to 1024x1024 tiles).
* **Interactive Mini-Map Preview:** When shrinking (cropping) or expanding, users can **drag the highlighted crop box** on the dialog's mini-map to choose exactly which portion of the map is preserved. All existing annotations automatically adjust their tile coordinates accordingly.

### 2.7 Adjustable UI Splitters
* The boundary between the Left Pane (Palette / Layers) and the Map View, and between the Map View and the Right Pane (Annotations) can be freely resized by dragging with the mouse.
* The vertical separator between the Palette and Layers can also be adjusted.
* The window has a protected minimum size (800x600 px) to prevent panel collapse or clipping.

---

## 3. Data Specification & Game Engine Integration (For AI Game Creators)

When generating game code (Pure C99 + SDL2/TinCLE) or parsing map files authored with `bandpisa`, the AI Agent MUST strictly conform to the following specifications:

### 3.1 File Conventions & Directory Layout
* The map file is always saved in JSON format (`.json`).
* The tileset image (`.png`) **MUST reside in the same directory** as the JSON map file.
* In the exported JSON, `"tileset"."image"` stores only the raw filename without path components (e.g., `"world_chip.png"`).

### 3.2 JSON Schema Reference

```json
{
  "format": "bandpisa_map",
  "version": "1.0",
  "tileset": {
    "image": "world_chip.png",
    "tile_width": 48,
    "tile_height": 48
  },
  "map": {
    "width": 30,
    "height": 20,
    "layers": [
      {
        "id": 0,
        "name": "Layer 0: Ground",
        "visible": true,
        "opacity": 1.0,
        "data": [ 0, 0, 1, 1, ... ]
      },
      {
        "id": 1,
        "name": "Layer 1: Decoration",
        "visible": true,
        "opacity": 1.0,
        "data": [ -1, -1, 5, ... ]
      },
      {
        "id": 2,
        "name": "Layer 2: Objects",
        "visible": true,
        "opacity": 1.0,
        "data": [ -1, 12, -1, ... ]
      },
      {
        "id": 3,
        "name": "Layer 3: Overlay",
        "visible": true,
        "opacity": 1.0,
        "data": [ -1, -1, 18, ... ]
      }
    ]
  },
  "annotations": [
    {
      "id": 1,
      "name": "Royal Castle",
      "category": "Castle",
      "description": "Capital fortress of the kingdom",
      "rect": {
        "x": 4,
        "y": 2,
        "width": 8,
        "height": 6
      },
      "color": 3761933311
    },
    {
      "id": 2,
      "name": "Castle Gate",
      "category": "Entrance",
      "description": "South entrance guarded by royal sentries",
      "rect": {
        "x": 7,
        "y": 7,
        "width": 2,
        "height": 1
      },
      "color": 998438655
    }
  ]
}
```

### 3.3 Tileset Indexing & Texture Coordinate Math
* Tile IDs in `layer.data` are **0-indexed** integers:
  * `-1`: Empty / Transparent tile (do not render).
  * `0, 1, 2, ...`: Tile index inside the atlas image.
* Given atlas image dimensions `atlas_w`, `atlas_h`, and tile dimensions `tile_w`, `tile_h`:
  * `tiles_per_row = atlas_w / tile_w`
  * Tile coordinates in atlas:
    $$\text{tile\_col} = \text{tile\_id} \pmod{\text{tiles\_per\_row}}$$
    $$\text{tile\_row} = \lfloor \text{tile\_id} / \text{tiles\_per\_row} \rfloor$$
  * Normalized Texture UV:
    $$u_0 = \frac{\text{tile\_col} \times \text{tile\_w}}{\text{atlas\_w}}, \quad v_0 = \frac{\text{tile\_row} \times \text{tile\_h}}{\text{atlas\_h}}$$
    $$u_1 = \frac{(\text{tile\_col} + 1) \times \text{tile\_w}}{\text{atlas\_w}}, \quad v_1 = \frac{(\text{tile\_row} + 1) \times \text{tile\_h}}{\text{atlas\_h}}$$
  * SDL2 Rect Source:
    `src_rect = { tile_col * tile_w, tile_row * tile_h, tile_w, tile_h }`

### 3.4 How AI Game Creators Leverage Annotations (Semantic Driven Game Logic)
Instead of hardcoding collision tables, trigger points, and entity placements, the AI parses the `"annotations"` array:
1. **Collision & Obstacle Generation:**
   * Query tiles under Layer 2 or annotations with `category: "Wall"`, `category: "Obstacle"`.
2. **Event & Transition Triggers:**
   * Annotations with `category: "Entrance"`, `category: "Exit"`, `category: "Portal"`, or `category: "Trigger"` define map warp boundaries.
   * Check player collision against `ann.rect.x <= player_tx < ann.rect.x + ann.rect.width`.
3. **NPC & Enemy Spawning:**
   * Annotations with `category: "Spawn"`, `category: "Enemy"`, or `category: "NPC"`.
   * The AI can populate entities randomly or centered inside `ann.rect`.
4. **AI NPC Navigation & Story Beats:**
   * The `name` and `description` fields carry direct natural language prompts for AI dialogue, quest goals, and narrative events (e.g., `name: "Old Witch's Hut"`, `description: "Requires Moon Key to unlock"`).

### 3.5 C99 TinCLE Map Loader Pattern (Reference Implementation)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int id;
    char name[64];
    char category[32];
    char description[256];
    int x, y, w, h;
} MapAnnotation;

typedef struct {
    int width;
    int height;
    int tile_w;
    int tile_h;
    char atlas_file[128];
    int* layers[4];
    MapAnnotation* annotations;
    int annotation_count;
} BandpisaMap;

// Rendering loop with Frustum Culling (TinCLE / SDL2)
void RenderMap(SDL_Renderer* renderer, SDL_Texture* atlas, BandpisaMap* map, int cam_x, int cam_y, int screen_w, int screen_h) {
    int start_tx = cam_x / map->tile_w;
    int start_ty = cam_y / map->tile_h;
    int end_tx   = (cam_x + screen_w) / map->tile_w + 1;
    int end_ty   = (cam_y + screen_h) / map->tile_h + 1;

    if (start_tx < 0) start_tx = 0;
    if (start_ty < 0) start_ty = 0;
    if (end_tx > map->width) end_tx = map->width;
    if (end_ty > map->height) end_ty = map->height;

    for (int l = 0; l < 4; ++l) {
        if (!map->layers[l]) continue;
        for (int ty = start_ty; ty < end_ty; ++ty) {
            for (int tx = start_tx; tx < end_tx; ++tx) {
                int tid = map->layers[l][ty * map->width + tx];
                if (tid < 0) continue;

                // Atlas source rect
                int atlas_cols = 192 / map->tile_w; // e.g. atlas texture width / tile width
                SDL_Rect src = { (tid % atlas_cols) * map->tile_w, (tid / atlas_cols) * map->tile_h, map->tile_w, map->tile_h };
                SDL_Rect dst = { tx * map->tile_w - cam_x, ty * map->tile_h - cam_y, map->tile_w, map->tile_h };
                SDL_RenderCopy(renderer, atlas, &src, &dst);
            }
        }
    }
}
```

---

## 4. AI Persona & Interaction Directives

1. **When Asked for Instructions:**
   * Speak concisely and informatively. Focus on practical key combinations (`Space + Left Drag` to Pan, `Wheel` to Zoom, `Ctrl+Z` to Undo, `A` for Memos).
   * Remind users that annotations can overlap and be resized anytime.
2. **When Building Games from Map Files:**
   * Always inspect both `layers` and `annotations` in the JSON.
   * Treat Layer 0 as walkable ground, Layer 2 as obstacles, and Layer 3 as foreground/canopy.
   * Use annotations as the single source of truth for semantic gameplay locations.
