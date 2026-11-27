---
name: tincle-dr
description: Use when converting 2D character sprites (front and back PNG views) into 3D rigged glTF/GLB models with automatic silhouette extrusion, bone extraction, and vertex skin weights in the TinCLE ecosystem. [TinCLE Tool Skill v0.19]
---

# SKILL_DR.md - TinCLE Tool Talent Chip: dorayaki

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.
* **Tool Name:** `dorayaki` (Dual Outlines Rigged And Yoked Around Kinematic Interiors)
* **Target Ecosystem:** TinCLE Game Engine AI-first Toolchain
* **Binary:** `dorayaki.exe`

---

## 1. Overview & Purpose

`dorayaki` is an AI-first, ultra-lightweight command-line asset generation tool designed specifically for the **TinCLE** game engine ecosystem.

Modern game development demands rapid transitions from 2D character concept art (front/back orthographic sprites) into animated 3D/2.5D assets. However, full 3D modeling packages (such as Blender) and heavy neural photogrammetry pipelines are far too bloated, slow, and fragile for automated AI workflows.

`dorayaki` solves this elegantly by taking two transparent PNG images (`front.png` and `back.png`), extracting their non-zero alpha silhouettes, generating a sandwich-style extruded polygonal mesh (with front face, back face, and perimeter side walls), and automatically embedding a humanoid skeleton (8-joint hierarchy) with smooth inverse-distance vertex skin weights. The output is a standard **glTF 2.0 / GLB** binary file ready to be loaded by TinCLE, web viewers, or modern 3D graphics pipelines.

---

## 2. Command-Line Interface & Usage for AI Agents

All TinCLE CLI tools are designed for seamless automated execution by AI agents and batch build scripts.

### Basic Syntax

```bash
dorayaki.exe <front.png> <back.png> <output.glb|output.gltf> [depth] [grid_res]
```

### Arguments

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `front.png` | Path | **Yes** | - | Path to the front-view character image (RGBA transparent PNG). |
| `back.png` | Path | **Yes** | - | Path to the back-view character image (RGBA transparent PNG, same size recommended). |
| `output.glb` | Path | **Yes** | - | Output path. If extension is `.glb`, writes single-binary GLB; otherwise writes `.gltf` JSON. |
| `depth` | Float | No | `0.16` | Extrusion thickness (Z-axis distance between front and back surfaces). |
| `grid_res` | Integer| No | `80` | Silhouette sampling grid resolution along the character's longest edge. |

### Execution Examples

#### 1. Standard Character Baking (Recommended for AI Agents)
```bash
dorayaki.exe front.png back.png character.glb
```

#### 2. Thicker Silhouette Extrusion with Higher Grid Fidelity
```bash
dorayaki.exe hero_front.png hero_back.png hero.glb 0.22 100
```

#### 3. Output as glTF JSON for Inspection
```bash
dorayaki.exe front.png back.png character.gltf
```

---

## 3. Internal Specifications & Rigging Topology

### Mesh Architecture
1. **Front Surface:** Facing `+Z`, mapped with `front.png` UVs (`(0,0)` at top-left to `(1,1)` at bottom-right).
2. **Back Surface:** Facing `-Z`, mapped with `back.png` horizontally flipped UVs (`(1-u, v)`).
3. **Side Perimeter (Crust):** Automated quad-strip extrusion enclosing every contour edge between front and back, textured with tinted edge pixels and outward normals.

### Humanoid Bone Hierarchy (8 Joints)
Assuming standard humanoid T-pose or A-pose sprites:

* **Joint 0: Root** (Center / Spine base)
  * **Joint 1: Spine** (Mid-torso / Chest)
    * **Joint 2: Head** (Upper bounding box)
    * **Joint 3: Arm_L** (Left lateral extension)
    * **Joint 4: Arm_R** (Right lateral extension)
  * **Joint 5: Pelvis** (Lower torso)
    * **Joint 6: Leg_L** (Left lower quadrant)
    * **Joint 7: Leg_R** (Right lower quadrant)

### Skinning Weights
Vertex weights are computed using 3D inverse-distance falloff:
$$W_k = \frac{1}{\text{dist}(V, B_k)^3}$$
Normalized across the 4 most influential joints per vertex (`JOINTS_0` as `uint16_t[4]`, `WEIGHTS_0` as normalized `float[4]`), guaranteeing smooth deformation across bone transitions in the engine.
