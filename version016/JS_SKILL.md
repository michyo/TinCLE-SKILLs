---
name: tincle-js-core
description: Use when building, creating, or packaging 2D web and standalone desktop games using TinCLE JS ecosystem. Pure Vanilla JS Canvas game generation with jgrscnzl, rjasplns tools. [TinCLE Core Skill v0.16]
---

# SKILL.md - TinCLE JS Skills Sheet [Core Skills]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

Create a game using the JavaScript canvas.

* Assume the canvas has been given the ID "tinclecanvas".
* **Required**: You must include a comment on the first line in the format `// "Game Title" (canvas-width, canvas-height)`.
* Write your code so that it runs as JavaScript in a standard web browser.
* Use the Web Audio API to implement simple background music and sound effects.
* Do not output any HTML; output only the JavaScript file `game.js`.
* When creating objects to be drawn on the screen without using assets, do not use a single primitive; instead, combine multiple primitives to reproduce the desired appearance.
* **Mouse/Touch Coordinates Handling**: When handling mouse clicks or touch events, always account for CSS scaling and fullscreen modes by converting screen coordinates to internal canvas coordinates using scaling factors: `const scaleX = canvas.width / rect.width; const mouseX = (e.clientX - rect.left) * scaleX;` (same for Y).
* If additional skill documents (such as `SKILL_HL.md`, `SKILL_FB.md`, `SKILL_PT.md`, etc.) are available in your context or workspace, read and strictly prioritize their guidelines; otherwise, create the game entirely within the constraints of this document alone.
* After creating the file, instruct the user to build it as `jgrscnzl game.js` (Web Version) and `rjasplns game.js [game.exe]` (Windows Version).
* **Windows Build Prerequisite**: NW.js (https://nwjs.io/) must be installed on the user's host environment, and `nw.exe` must be accessible via system PATH to run `rjasplns`.
