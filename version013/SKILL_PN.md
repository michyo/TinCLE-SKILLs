# TinCLE (Tiny C Lovely Engine) - Networking Talent Chip Version 0.13

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

~ Multi-User Dedicated Server Generator & Asynchronous Network API ~

## 1. Overview & Architecture

The TinCLE networking pipeline consists of three core components:

1. **`pubicnet` (CLI Tool)**
   - Generates/reads `uuid.txt` (36-byte UUID) in the project directory.
   - Binary-patches the template dynamic binary with the 36-character GAME_ID (UUID) and Game Title.
   - Outputs a standalone dedicated server executable: `my_server.exe`.
2. **`my_server.exe` (Dedicated Server)**
   - Listens on TCP port `8080` (default) for non-blocking packet broadcasting.
   - Validates client header MAGIC (`"PNET"`) and GAME_ID (UUID).
   - Automatically assigns unique `peer_id` (1~65535) to connected clients upon handshake.
   - Broadcasts incoming payload data to all clients residing in the same `room_id`.
3. **`tincle_net_*` API (Client Integration via `tincle.dll`)**
   - Non-blocking socket communication layer embedded inside TinCLE.
   - Cross-platform support (Win32 / WASM via Emscripten).

---

## 2. Server Generation Workflow (Step-by-Step)

Before invoking network APIs in client code (`game.c`), the AI Agent or developer must generate the dedicated game server executable.

### Step 1: Execute `pubicnet`
Run the `pubicnet` tool from the project directory with the game title as a required argument. You may optionally specify a custom output executable name (defaults to `my_server.exe` if omitted):

```bash
# Default output (my_server.exe)
pubicnet "My Game Title"

# Custom output name
pubicnet "My Game Title" custom_server.exe
```

### Step 2: Automatic UUID & Server Output

* If `uuid.txt` does NOT exist in the working directory, `pubicnet` generates a new UUID (e.g., `a1b2c3d4-5678-90ab-cdef-1234567890ab`) and saves it as `uuid.txt`.
* `pubicnet` reads the template library (`pubicnet.dll`), injects the target full 36-character GAME_ID (UUID) and Game Title into internal memory placeholders, and outputs the patched server binary (`my_server.exe` or specified name).

### Step 3: Launch Dedicated Server

Run `my_server.exe` to start listening for client connections:

```bash
my_server -p 8080
```

*Console Output:*

```plaintext
======================================================================
 [TinCLE Version 0.11] My Game Title Server Started!
 [Port] 8080
======================================================================
```

### Step 4: Server Packaging & Release Preparation

The generated server executable is unique to your game build and **MUST be distributed alongside the game client**.

To ensure safety, stability, and ease of use, follow these distribution guidelines:

1. **Apply `poopee` Post-Processing (CRITICAL):**
  * Before distributing the server executable, you **MUST** run `poopee` on the generated server EXE to embed the application icon and OS manifest.
  * This step is strongly recommended to prevent false-positive antivirus flags (such as Windows Defender) on user machines.
    ```bash
    poopee my_server.exe icon.ico manifest.xml
    ```

2. **Standalone Server ZIP Distribution:**
  * For maximum user convenience, create a separate standalone ZIP archive specifically for host players/server admins (e.g., `MyGame_Dedicated_Server.zip`).
  * The archive should contain the following 3 files:
    1. `my_server.exe` (The `poopee`-processed server executable)
    2. `CREDITS.txt` (License and attribution credits)
    3. `readme.txt` (Clear documentation explaining what the server is, how to open ports, and how to launch it)

---

## 3. Client API Reference

All networking functions are exposed via `libs/tincle.h`.

| Function | Return Type | Description |
| --- | --- | --- |
| `tincle_net_set_game_id(const char* game_id_or_uuid)` | `void` | Configures full 36-character GAME_ID (UUID) used for server authentication. **Must be called before `tincle_net_connect**`. |
| `tincle_net_connect(const char* ip, int port, uint16_t room_id)` | `int` | Initiates asynchronous TCP connection to the server and triggers automatic Peer ID handshake. Returns `1` on socket creation success, `0` on failure. |
| `tincle_net_disconnect()` | `void` | Closes network socket and resets client Peer ID state. |
| `tincle_net_send(const uint8_t* data, uint16_t size)` | `int` | Broadcasts raw binary payload to all clients in the current `room_id`. Returns `1` on success, `0` on failure. |
| `tincle_net_poll(uint16_t* out_sender_peer_id, uint8_t* out_buffer, uint16_t max_size)` | `int` | Non-blocking receive function. Must be called repeatedly in the game update loop. Returns received payload byte count (`0` if no data). **If `out_sender_peer_id` is `0`, `out_buffer` contains the `uint16_t` Peer ID of a disconnected client sent by the server.** |
| `tincle_net_get_peer_id()` | `uint16_t` | Returns the assigned unique Client Peer ID (`1`~`65535`). Returns `0` if not yet connected/handshaken. |

### Disconnect & Timeout Handling Mechanism

To maintain a responsive multiplayer state, clients must handle disconnection using a two-stage approach inside the `tincle_net_poll` loop:

1. **Visual Hide Timeout (Local Client Side - 2 Seconds):**
   - If a peer's position data has not arrived for more than 2 seconds (`PEER_TIMEOUT_SEC`), the client temporarily hides the player from the screen (e.g., `active = false`). This prevents dead/lagging players from lingering on the screen.
2. **Server Logout Notification (System Event - 0s or 30s):**
   - When `tincle_net_poll` returns `out_sender_peer_id == 0`, it indicates a system event directly sent from the server.
   - The payload contains a `uint16_t` representing the `disconnected_peer_id`.
   - **Immediate Disconnect (0s):** Sent instantly when a client performs a graceful close/disconnect.
   - **Timeout Disconnect (30s):** Sent after 30 seconds if a client suffers a hard crash or network disruption without sending a WebSocket close frame.
   - Upon receiving `out_sender_peer_id == 0`, the client must completely clean up and release the specified peer's state, regardless of whether the player was already visually hidden by the 2-second local check.

---

## 4. Minimal Network Implementation Boilerplate

### Critical Architecture Rules for AI Agents

When designing a TinCLE multiplayer game, AI Agents **MUST** strictly adhere to the following architecture rules:

1. **Do NOT Rely on `uuid.txt` in the Distributed Game:**
   - The `uuid.txt` file is **ONLY** used locally during the server generation build process with `pubicnet`.
   - Never assume `uuid.txt` will exist on the player's machine. The client code (`game.c`) **MUST** embed or hardcode the full 36-character GAME_ID (UUID) directly in C variables and pass it to `tincle_net_set_game_id()`.

2. **Always Provide a Server IP / Port Configuration UI:**
   - **NEVER** hardcode the destination IP address to `127.0.0.1` (localhost) or a fixed IP inside the client code.
   - Hardcoding `127.0.0.1` completely breaks real online multiplayer across different machines.
   - You **MUST** implement an in-game UI screen (or input prompt/config file loader) that allows players to freely enter and save the target Server IP address and Port number before attempting to call `tincle_net_connect()`.

3. **UUID Acquisition Rule by AI Agent Type (CRITICAL):**
   - The 36-character GAME_ID (UUID) passed to `tincle_net_set_game_id()` MUST strictly match the 36-characters UUID embedded inside the generated server (`my_server.exe`). Never invent or hallucinate a random dummy UUID!
   - **For Autonomous / Agentic AIs (Tools & CLI execution enabled):**
     You MUST execute `pubicnet "<Game Title>"` FIRST in the terminal to generate `uuid.txt` and `my_server.exe`. Then, read the generated UUID from `uuid.txt` and embed the full 36-characters directly into the client C code (`game.c`).
   - **For Conversational / Chat AIs (No direct terminal execution):**
     You CANNOT run `pubicnet` by yourself. If the user has NOT provided the target UUID or `uuid.txt` content yet, you **MUST explicitly ask the user to provide the UUID** (or run `pubicnet` first) BEFORE writing the `tincle_net_set_game_id()` code. NEVER invent a placeholder UUID, as mismatched GAME_IDs will permanently block all network connections!

### Boilerplate

This boilerplate demonstrates how an AI Agent should write client code (`game.c`) within the official TinCLE state lifecycle to establish connections, send player state, and poll incoming broadcast data without blocking the render thread.

**CRITICAL Note:** Always call `tincle_net_set_game_id()` before `tincle_net_connect()` to ensure the full 36-character GAME_ID (UUID) matches the server.

```c
#define SDL_MAIN_HANDLED
#include "libs/tincle.h"
#include <stdio.h>
#include <stdint.h>

#ifdef __EMSCRIPTEN__
    #include <SDL2/SDL_scancode.h>
#else
    #include "libs/SDL_scancode.h"
    #include <windows.h>
#endif

// Network Packet Structure
typedef struct {
    float x;
    float y;
} PlayerNetworkPacket;

// Global States & Storage
static int g_font_medium = -1;
static float g_my_x = 320.0f;
static float g_my_y = 240.0f;

// Table for other players' positions (Supports up to 16 peers)
static float g_other_x[16] = {0};
static float g_other_y[16] = {0};
static bool  g_other_active[16] = {false};
static float g_other_last_seen[16] = {0};

// Timeout threshold for peer disconnections (seconds)
#define PEER_TIMEOUT_SEC 2.0f

// State 0: Gameplay Logic Updates
void play_update(float dt) {
    static float s_total_time = 0.0f;
    s_total_time += dt;

    // 1. Network Receive Polling (Process all incoming packets)
    uint16_t sender_peer_id = 0;
    uint8_t recv_buf[128]; // Receive via buffer to also catch system notifications (leave events)
    int recv_len = 0;

    // 1. Network Receive Polling
    while ((recv_len = tincle_net_poll(&sender_peer_id, recv_buf, sizeof(recv_buf))) > 0) {

        // sender_peer_id == 0 indicates a system notification from the server (immediate disconnect or 30-sec timeout disconnect)
        if (sender_peer_id == 0) {
            if (recv_len >= (int)sizeof(uint16_t)) {
                uint16_t left_peer_id = *(uint16_t*)recv_buf;
                if (left_peer_id > 0 && left_peer_id < 16) {
                    // Output a "completely logged out" log, regardless of whether the player was already visually hidden by the 2-sec timeout!
                    printf("[Net] Peer %d completely logged out (Server Notification)!\n", left_peer_id);

                    g_other_active[left_peer_id] = false; // Completely release and reset the player state
                }
            }
        }
        // Normal position synchronization packets from other players
        else if (sender_peer_id != tincle_net_get_peer_id() && sender_peer_id < 16) {
            if (recv_len >= (int)sizeof(PlayerNetworkPacket)) {
                PlayerNetworkPacket* recv_packet = (PlayerNetworkPacket*)recv_buf;
                g_other_x[sender_peer_id] = recv_packet->x;
                g_other_y[sender_peer_id] = recv_packet->y;

                g_other_active[sender_peer_id] = true;
                g_other_last_seen[sender_peer_id] = s_total_time;
            }
        }
    }

    // 2. Visual Timeout Check (Emergency visual hide processing)
    for (int i = 1; i < 16; i++) {
        if (i != tincle_net_get_peer_id() && g_other_active[i]) {
            // Temporarily hide the player from the screen if packets stop arriving for 2 seconds
            if (s_total_time - g_other_last_seen[i] > PEER_TIMEOUT_SEC) {
                printf("[Net] Peer %d position data paused (Visual Hide)\n", i);
                g_other_active[i] = false;
            }
        }
    }

    // 3. Local Player Input Handling
    float move_speed = 200.0f;
    if (tincle_key_pressed(SDL_SCANCODE_LEFT))  g_my_x -= move_speed * dt;
    if (tincle_key_pressed(SDL_SCANCODE_RIGHT)) g_my_x += move_speed * dt;
    if (tincle_key_pressed(SDL_SCANCODE_UP))    g_my_y -= move_speed * dt;
    if (tincle_key_pressed(SDL_SCANCODE_DOWN))  g_my_y += move_speed * dt;

    // 4. Send Local Position to Server (Only after Peer ID is assigned)
    uint16_t my_id = tincle_net_get_peer_id();
    if (my_id != 0) {
        PlayerNetworkPacket my_packet;
        my_packet.x = g_my_x;
        my_packet.y = g_my_y;

        tincle_net_send((const uint8_t*)&my_packet, sizeof(PlayerNetworkPacket));
    }
}

// State 0: Gameplay Rendering
void play_draw(void) {
    // Clear background (Dark Navy)
    tincle_clear((TinCLE_Color){20, 20, 50, 255});

    if (g_font_medium != -1) {
        tincle_set_font(g_font_medium);
    }

    uint16_t my_id = tincle_net_get_peer_id();
    char buf[64];

    // Render assigned Peer ID
    sprintf(buf, "MY PEER ID: %d", my_id);
    tincle_draw_text(buf, 20, 20, (TinCLE_Color){0, 255, 0, 255});

    // Render Local Player (Yellow)
    sprintf(buf, "P%d", my_id);
    tincle_draw_text_center(buf, (int)g_my_x, (int)g_my_y, (TinCLE_Color){255, 255, 0, 255});

    // Render Remote Peers (Magenta)
    for (int i = 1; i < 16; i++) {
        if (i != my_id && g_other_active[i]) {
            sprintf(buf, "P%d", i);
            tincle_draw_text_center(buf, (int)g_other_x[i], (int)g_other_y[i], (TinCLE_Color){255, 0, 255, 255});
        }
    }
}

// Engine & Network Initialization
void game_load(void) {
    // Load default font asset
    g_font_medium = tincle_load_font("font.ttf", 24);

    // Set full 36-character Game UUID (Must match server config)
    tincle_net_set_game_id("406230b1-ae94-05b7-e9af-541d23f313c7");

    // Establish connection to pubicnet server (IP, Port, RoomID)
    if (tincle_net_connect("127.0.0.1", 8080, 1)) { // Server IP Address & Port
        printf("[Net] Connecting to pubicnet server...\n");
    }

    tincle_add_state(0, play_update, play_draw);
    tincle_change_state(0);
}

// Application Entry Point
#ifdef __EMSCRIPTEN__
int main(int argc, char* argv[]) {
    tincle_start(game_load, "My Net Game", true, 640, 480, TINCLE_MODE_2D_NORMAL);
    return 0;
}
#else
int WINAPI WinMain(HINSTANCE h, HINSTANCE hp, LPSTR c, int n) {
    tincle_start(game_load, "My Net Game", true, 640, 480, TINCLE_MODE_2D_NORMAL);
    return 0;
}
#endif
```
