This is part 2 of 3 (Constants) of the specification for "TinCLE". Please merge this with your previous memory and update your knowledge base. Do NOT generate any game code yet. Please reply with nothing but the exact text below:

"[ TinCLE Specification 2/3: Constants memorized. Awaiting next input. ]"

---

## 4. Constant Macros & Structure Definitions

The following definitions are readily available when writing `game.c`. These are all predefined within `tincle.h`.

### 4.1. Screen Size & Specifications

TinCLE features an automatic logical scaling system that preserves the aspect ratio. While the window size is fully resizable, all in-game coordinate calculations must be based on the virtual resolution specifications.

* **Default Virtual Resolution**: `640` (Width) x `480` (Height)
* *Note: These dimensions are specified as arguments when calling `tincle_start` within the `WinMain` function (detailed in Section 5.1). All rendering calculations must strictly baseline against these virtual dimensions.*

* `TINCLE_FONT_S`: 16 (For small-sized fonts)
* `TINCLE_FONT_M`: 32 (For medium-sized fonts)
* `TINCLE_FONT_L`: 64 (For large-sized fonts)
* `TINCLE_MAX_STATES`: 256 (Maximum number of manageable states)

### 4.2. Mouse Button Definitions

* `TINCLE_MOUSE_LEFT`  : 1 (Left button)
* `TINCLE_MOUSE_MIDDLE`: 2 (Middle wheel button)
* `TINCLE_MOUSE_RIGHT` : 3 (Right button)

### 4.3. Gamepad Definitions (Xbox Layout Standard)

* `TINCLE_PAD_A`    : 0
* `TINCLE_PAD_B`    : 1
* `TINCLE_PAD_X`    : 2
* `TINCLE_PAD_Y`    : 3
* `TINCLE_PAD_START`: 4
* `TINCLE_PAD_BACK` : 5
* `TINCLE_PAD_UP`   : 6
* `TINCLE_PAD_DOWN` : 7
* `TINCLE_PAD_LEFT` : 8
* `TINCLE_PAD_RIGHT`: 9

### 4.4. Keyboard Scan Codes (SDL_scancode Compliant)

This section details the comprehensive list of hardware-independent scan codes utilized within TinCLE for keyboard input detection. These identifiers strictly align with standard standard `SDL_scancode` mapping values.

#### Alphabet Keys

| Constant Name | Scan Code |
| --- | --- |
| `TINCLE_KEY_A` | 4 |
| `TINCLE_KEY_B` | 5 |
| `TINCLE_KEY_C` | 6 |
| `TINCLE_KEY_D` | 7 |
| `TINCLE_KEY_E` | 8 |
| `TINCLE_KEY_F` | 9 |
| `TINCLE_KEY_G` | 10 |
| `TINCLE_KEY_H` | 11 |
| `TINCLE_KEY_I` | 12 |
| `TINCLE_KEY_J` | 13 |
| `TINCLE_KEY_K` | 14 |
| `TINCLE_KEY_L` | 15 |
| `TINCLE_KEY_M` | 16 |
| `TINCLE_KEY_N` | 17 |
| `TINCLE_KEY_O` | 18 |
| `TINCLE_KEY_P` | 19 |
| `TINCLE_KEY_Q` | 20 |
| `TINCLE_KEY_R` | 21 |
| `TINCLE_KEY_S` | 22 |
| `TINCLE_KEY_T` | 23 |
| `TINCLE_KEY_U` | 24 |
| `TINCLE_KEY_V` | 25 |
| `TINCLE_KEY_W` | 26 |
| `TINCLE_KEY_X` | 27 |
| `TINCLE_KEY_Y` | 28 |
| `TINCLE_KEY_Z` | 29 |

#### Numeric Keys (Top Row)

| Constant Name | Scan Code |
| --- | --- |
| `TINCLE_KEY_1` | 30 |
| `TINCLE_KEY_2` | 31 |
| `TINCLE_KEY_3` | 32 |
| `TINCLE_KEY_4` | 33 |
| `TINCLE_KEY_5` | 34 |
| `TINCLE_KEY_6` | 35 |
| `TINCLE_KEY_7` | 36 |
| `TINCLE_KEY_8` | 37 |
| `TINCLE_KEY_9` | 38 |
| `TINCLE_KEY_0` | 39 |

#### Core Control & Space Keys

| Constant Name | Scan Code | Description |
| --- | --- | --- |
| `TINCLE_KEY_RETURN` | 40 | Enter / Return |
| `TINCLE_KEY_ESCAPE` | 41 | Esc |
| `TINCLE_KEY_BACKSPACE` | 42 | Backspace |
| `TINCLE_KEY_TAB` | 43 | Tab |
| `TINCLE_KEY_SPACE` | 44 | Spacebar |
| `TINCLE_KEY_CAPSLOCK` | 57 | Caps Lock |

#### Symbol Keys

| Constant Name | Scan Code |
| --- | --- |
| `TINCLE_KEY_MINUS` | 45 |
| `TINCLE_KEY_EQUALS` | 46 |
| `TINCLE_KEY_LEFTBRACKET` | 47 |
| `TINCLE_KEY_RIGHTBRACKET` | 48 |
| `TINCLE_KEY_BACKSLASH` | 49 |
| `TINCLE_KEY_NONUSHASH` | 50 |
| `TINCLE_KEY_SEMICOLON` | 51 |
| `TINCLE_KEY_APOSTROPHE` | 52 |
| `TINCLE_KEY_GRAVE` | 53 |
| `TINCLE_KEY_COMMA` | 54 |
| `TINCLE_KEY_PERIOD` | 55 |
| `TINCLE_KEY_SLASH` | 56 |

#### Navigation & Editing Keys

| Constant Name | Scan Code |
| --- | --- |
| `TINCLE_KEY_PRINTSCREEN` | 70 |
| `TINCLE_KEY_SCROLLLOCK` | 71 |
| `TINCLE_KEY_PAUSE` | 72 |
| `TINCLE_KEY_INSERT` | 73 |
| `TINCLE_KEY_HOME` | 74 |
| `TINCLE_KEY_PAGEUP` | 75 |
| `TINCLE_KEY_DELETE` | 76 |
| `TINCLE_KEY_END` | 77 |
| `TINCLE_KEY_PAGEDOWN` | 78 |

#### Arrow Keys

| Constant Name | Scan Code |
| --- | --- |
| `TINCLE_KEY_RIGHT` | 79 |
| `TINCLE_KEY_LEFT` | 80 |
| `TINCLE_KEY_DOWN` | 81 |
| `TINCLE_KEY_UP` | 82 |

#### Function Keys (F1 - F24)

| Constant Name | Scan Code | Constant Name | Scan Code |
| --- | --- | --- | --- |
| `TINCLE_KEY_F1` | 58 | `TINCLE_KEY_F13` | 104 |
| `TINCLE_KEY_F2` | 59 | `TINCLE_KEY_F14` | 105 |
| `TINCLE_KEY_F3` | 60 | `TINCLE_KEY_F15` | 106 |
| `TINCLE_KEY_F4` | 61 | `TINCLE_KEY_F16` | 107 |
| `TINCLE_KEY_F5` | 62 | `TINCLE_KEY_F17` | 108 |
| `TINCLE_KEY_F6` | 63 | `TINCLE_KEY_F18` | 109 |
| `TINCLE_KEY_F7` | 64 | `TINCLE_KEY_F19` | 110 |
| `TINCLE_KEY_F8` | 65 | `TINCLE_KEY_F20` | 111 |
| `TINCLE_KEY_F9` | 66 | `TINCLE_KEY_F21` | 112 |
| `TINCLE_KEY_F10` | 67 | `TINCLE_KEY_F22` | 113 |
| `TINCLE_KEY_F11` | 68 | `TINCLE_KEY_F23` | 114 |
| `TINCLE_KEY_F12` | 69 | `TINCLE_KEY_F24` | 115 |

#### Numeric Pad (Keypad) Keys

| Constant Name | Scan Code | Description / Character |
| --- | --- | --- |
| `TINCLE_KEY_NUMLOCKCLEAR` | 83 | Num Lock / Clear |
| `TINCLE_KEY_KP_DIVIDE` | 84 | Keypad `/` |
| `TINCLE_KEY_KP_MULTIPLY` | 85 | Keypad `*` |
| `TINCLE_KEY_KP_MINUS` | 86 | Keypad `-` |
| `TINCLE_KEY_KP_PLUS` | 87 | Keypad `+` |
| `TINCLE_KEY_KP_ENTER` | 88 | Keypad Enter |
| `TINCLE_KEY_KP_1` | 89 | Keypad `1` |
| `TINCLE_KEY_KP_2` | 90 | Keypad `2` |
| `TINCLE_KEY_KP_3` | 91 | Keypad `3` |
| `TINCLE_KEY_KP_4` | 92 | Keypad `4` |
| `TINCLE_KEY_KP_5` | 93 | Keypad `5` |
| `TINCLE_KEY_KP_6` | 94 | Keypad `6` |
| `TINCLE_KEY_KP_7` | 95 | Keypad `7` |
| `TINCLE_KEY_KP_8` | 96 | Keypad `8` |
| `TINCLE_KEY_KP_9` | 97 | Keypad `9` |
| `TINCLE_KEY_KP_0` | 98 | Keypad `0` |
| `TINCLE_KEY_KP_PERIOD` | 99 | Keypad `.` |
| `TINCLE_KEY_KP_EQUALS` | 103 | Keypad `=` |
| `TINCLE_KEY_KP_COMMA` | 133 | Keypad `,` |
| `TINCLE_KEY_KP_EQUALSAS400` | 134 | AS400 Keypad `=` |
| `TINCLE_KEY_KP_00` | 176 | Keypad `00` |
| `TINCLE_KEY_KP_000` | 177 | Keypad `000` |
| `TINCLE_KEY_THOUSANDSSEPARATOR` | 178 | Keypad Thousands Separator |
| `TINCLE_KEY_DECIMALSEPARATOR` | 179 | Keypad Decimal Separator |
| `TINCLE_KEY_CURRENCYUNIT` | 180 | Keypad Currency Unit |
| `TINCLE_KEY_CURRENCYSUBUNIT` | 181 | Keypad Currency Sub-unit |
| `TINCLE_KEY_KP_LEFTPAREN` | 182 | Keypad `(` |
| `TINCLE_KEY_KP_RIGHTPAREN` | 183 | Keypad `)` |
| `TINCLE_KEY_KP_LEFTBRACE` | 184 | Keypad `{` |
| `TINCLE_KEY_KP_RIGHTBRACE` | 185 | Keypad `}` |
| `TINCLE_KEY_KP_TAB` | 186 | Keypad Tab |
| `TINCLE_KEY_KP_BACKSPACE` | 187 | Keypad Backspace |
| `TINCLE_KEY_KP_A` | 188 | Keypad Hex `A` |
| `TINCLE_KEY_KP_B` | 189 | Keypad Hex `B` |
| `TINCLE_KEY_KP_C` | 190 | Keypad Hex `C` |
| `TINCLE_KEY_KP_D` | 191 | Keypad Hex `D` |
| `TINCLE_KEY_KP_E` | 192 | Keypad Hex `E` |
| `TINCLE_KEY_KP_F` | 193 | Keypad Hex `F` |
| `TINCLE_KEY_KP_XOR` | 194 | Keypad `XOR` |
| `TINCLE_KEY_KP_POWER` | 195 | Keypad `^` (Power) |
| `TINCLE_KEY_KP_PERCENT` | 196 | Keypad `%` |
| `TINCLE_KEY_KP_LESS` | 197 | Keypad `<` |
| `TINCLE_KEY_KP_GREATER` | 198 | Keypad `>` |
| `TINCLE_KEY_KP_AMPERSAND` | 199 | Keypad `&` |
| `TINCLE_KEY_KP_DBLAMPERSAND` | 200 | Keypad `&&` |
| `TINCLE_KEY_KP_VERTICALBAR` | 201 | Keypad `|` |
| `TINCLE_KEY_KP_DBLVERTICALBAR` | 202 | Keypad `||` |
| `TINCLE_KEY_KP_COLON` | 203 | Keypad `:` |
| `TINCLE_KEY_KP_HASH` | 204 | Keypad `#` |
| `TINCLE_KEY_KP_SPACE` | 205 | Keypad Space |
| `TINCLE_KEY_KP_AT` | 206 | Keypad `@` |
| `TINCLE_KEY_KP_EXCLAM` | 207 | Keypad `!` |
| `TINCLE_KEY_KP_MEMSTORE` | 208 | Keypad Memory Store |
| `TINCLE_KEY_KP_MEMRECALL` | 209 | Keypad Memory Recall |
| `TINCLE_KEY_KP_MEMCLEAR` | 210 | Keypad Memory Clear |
| `TINCLE_KEY_KP_MEMADD` | 211 | Keypad Memory Add |
| `TINCLE_KEY_KP_MEMSUBTRACT` | 212 | Keypad Memory Subtract |
| `TINCLE_KEY_KP_MEMMULTIPLY` | 213 | Keypad Memory Multiply |
| `TINCLE_KEY_KP_MEMDIVIDE` | 214 | Keypad Memory Divide |
| `TINCLE_KEY_KP_PLUSMINUS` | 215 | Keypad `+/-` |
| `TINCLE_KEY_KP_CLEAR` | 216 | Keypad Clear |
| `TINCLE_KEY_KP_CLEARENTRY` | 217 | Keypad Clear Entry |
| `TINCLE_KEY_KP_BINARY` | 218 | Keypad Binary Mode |
| `TINCLE_KEY_KP_OCTAL` | 219 | Keypad Octal Mode |
| `TINCLE_KEY_KP_DECIMAL` | 220 | Keypad Decimal Mode |
| `TINCLE_KEY_KP_HEXADECIMAL` | 221 | Keypad Hexadecimal Mode |

#### Modifier Keys

| Constant Name | Scan Code | Description |
| --- | --- | --- |
| `TINCLE_KEY_LCTRL` | 224 | Left Control |
| `TINCLE_KEY_LSHIFT` | 225 | Left Shift |
| `TINCLE_KEY_LALT` | 226 | Left Alt / Option |
| `TINCLE_KEY_LGUI` | 227 | Left GUI (Windows / Command) |
| `TINCLE_KEY_RCTRL` | 228 | Right Control |
| `TINCLE_KEY_RSHIFT` | 229 | Right Shift |
| `TINCLE_KEY_RALT` | 230 | Right Alt / Option |
| `TINCLE_KEY_RGUI` | 231 | Right GUI (Windows / Command) |

#### International & Language Keys

| Constant Name | Scan Code | Constant Name | Scan Code |
| --- | --- | --- | --- |
| `TINCLE_KEY_INTERNATIONAL1` | 135 | `TINCLE_KEY_LANG1` | 144 |
| `TINCLE_KEY_INTERNATIONAL2` | 136 | `TINCLE_KEY_LANG2` | 145 |
| `TINCLE_KEY_INTERNATIONAL3` | 137 | `TINCLE_KEY_LANG3` | 146 |
| `TINCLE_KEY_INTERNATIONAL4` | 138 | `TINCLE_KEY_LANG4` | 147 |
| `TINCLE_KEY_INTERNATIONAL5` | 139 | `TINCLE_KEY_LANG5` | 148 |
| `TINCLE_KEY_INTERNATIONAL6` | 140 | `TINCLE_KEY_LANG6` | 149 |
| `TINCLE_KEY_INTERNATIONAL7` | 141 | `TINCLE_KEY_LANG7` | 150 |
| `TINCLE_KEY_INTERNATIONAL8` | 142 | `TINCLE_KEY_LANG8` | 151 |
| `TINCLE_KEY_INTERNATIONAL9` | 143 | `TINCLE_KEY_LANG9` | 152 |

#### System, Media & Application Keys

| Constant Name | Scan Code | Description / Use Case |
| --- | --- | --- |
| `TINCLE_KEY_UNKNOWN` | 0 | Unrecognized / Edge cases |
| `TINCLE_KEY_NONUSBACKSLASH` | 100 | Non-US Backslash |
| `TINCLE_KEY_APPLICATION` | 101 | Context Menu Key |
| `TINCLE_KEY_POWER` | 102 | System Power Status |
| `TINCLE_KEY_EXECUTE` | 116 | Execute Command |
| `TINCLE_KEY_HELP` | 117 | Help Menu Trigger |
| `TINCLE_KEY_MENU` | 118 | Menu Key |
| `TINCLE_KEY_SELECT` | 119 | Select Command |
| `TINCLE_KEY_STOP` | 120 | Stop Operation |
| `TINCLE_KEY_AGAIN` | 121 | Redo / Repeat |
| `TINCLE_KEY_UNDO` | 122 | Undo Action |
| `TINCLE_KEY_CUT` | 123 | Clipboard Cut |
| `TINCLE_KEY_COPY` | 124 | Clipboard Copy |
| `TINCLE_KEY_PASTE` | 125 | Clipboard Paste |
| `TINCLE_KEY_FIND` | 126 | Search / Find |
| `TINCLE_KEY_MUTE` | 127 | Master Audio Mute (Legacy) |
| `TINCLE_KEY_VOLUMEUP` | 128 | System Volume Up |
| `TINCLE_KEY_VOLUMEDOWN` | 129 | System Volume Down |
| `TINCLE_KEY_ALTERASE` | 153 | Alt Erase |
| `TINCLE_KEY_SYSREQ` | 154 | Sys Req / Print Screen |
| `TINCLE_KEY_CANCEL` | 155 | Cancel Action |
| `TINCLE_KEY_CLEAR` | 156 | Clear Display / State |
| `TINCLE_KEY_PRIOR` | 157 | Prior Page / Selection |
| `TINCLE_KEY_RETURN2` | 158 | Alternative Return |
| `TINCLE_KEY_SEPARATOR` | 159 | Separator |
| `TINCLE_KEY_OUT` | 160 | Out |
| `TINCLE_KEY_OPER` | 161 | Operational Mode |
| `TINCLE_KEY_CLEARAGAIN` | 162 | Clear / Reset Again |
| `TINCLE_KEY_CRSEL` | 163 | CR Sel |
| `TINCLE_KEY_EXSEL` | 164 | EX Sel |
| `TINCLE_KEY_MODE` | 257 | Mode Switch |
| `TINCLE_KEY_AUDIONEXT` | 258 | Media Track Next |
| `TINCLE_KEY_AUDIOPREV` | 259 | Media Track Previous |
| `TINCLE_KEY_AUDIOSTOP` | 260 | Media Audio Stop |
| `TINCLE_KEY_AUDIOPLAY` | 261 | Media Audio Play / Pause |
| `TINCLE_KEY_AUDIOMUTE` | 262 | System Audio Mute |
| `TINCLE_KEY_MEDIASELECT` | 263 | Launch Media Player |
| `TINCLE_KEY_WWW` | 264 | Launch Web Browser |
| `TINCLE_KEY_MAIL` | 265 | Launch Mail Application |
| `TINCLE_KEY_CALCULATOR` | 266 | Launch Calculator |
| `TINCLE_KEY_COMPUTER` | 267 | Open My Computer / Files |
| `TINCLE_KEY_AC_SEARCH` | 268 | AC Search |
| `TINCLE_KEY_AC_HOME` | 269 | AC Home |
| `TINCLE_KEY_AC_BACK` | 270 | AC Back |
| `TINCLE_KEY_AC_FORWARD` | 271 | AC Forward |
| `TINCLE_KEY_AC_STOP` | 272 | AC Stop |
| `TINCLE_KEY_AC_REFRESH` | 273 | AC Refresh |
| `TINCLE_KEY_AC_BOOKMARKS` | 274 | AC Bookmarks |
| `TINCLE_KEY_BRIGHTNESSDOWN` | 275 | Monitor Brightness Down |
| `TINCLE_KEY_BRIGHTNESSUP` | 276 | Monitor Brightness Up |
| `TINCLE_KEY_DISPLAYSWITCH` | 277 | Display Output Toggle |
| `TINCLE_KEY_KBDILLUMTOGGLE` | 278 | Keyboard Backlight Toggle |
| `TINCLE_KEY_KBDILLUMDOWN` | 279 | Keyboard Backlight Down |
| `TINCLE_KEY_KBDILLUMUP` | 280 | Keyboard Backlight Up |
| `TINCLE_KEY_EJECT` | 281 | Optical Drive Eject |
| `TINCLE_KEY_SLEEP` | 282 | System Sleep Trigger |
| `TINCLE_KEY_APP1` | 283 | Launch Custom App 1 |
| `TINCLE_KEY_APP2` | 284 | Launch Custom App 2 |
| `TINCLE_KEY_AUDIOREWIND` | 285 | Media Audio Rewind |
| `TINCLE_KEY_AUDIOFASTFORWARD` | 286 | Media Audio Fast Forward |
| `TINCLE_KEY_SOFTLEFT` | 287 | Soft Left Control |
| `TINCLE_KEY_SOFTRIGHT` | 288 | Soft Right Control |
| `TINCLE_KEY_CALL` | 289 | Initiate Call / Accept |
| `TINCLE_KEY_ENDCALL` | 290 | Terminate Call / Decline |

## 4.5. Color Structure & Preset Definitions

This section defines a custom color structure that stores RGBA channels in 1-byte integers, alongside handy preset macros for rapid color selection.

```c
typedef struct {
    unsigned char r, g, b, a;
} TinCLE_Color;
```

### 【Quick-Use Macros (Compound Literals)】

These convenient preset macros can be injected inline directly into function arguments.

#### 1. PERFECT MONOTONE SYSTEM (19 Steps Gray Scale)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_BLACK` | `(TinCLE_Color){0, 0, 0, 255}` | `TINCLE_COLOR_GRAY_1` | `(TinCLE_Color){13, 13, 13, 255}` |
| `TINCLE_COLOR_GRAY_2` | `(TinCLE_Color){26, 26, 26, 255}` | `TINCLE_COLOR_GRAY_3` | `(TinCLE_Color){39, 39, 39, 255}` |
| `TINCLE_COLOR_GRAY_4` | `(TinCLE_Color){51, 51, 51, 255}` | `TINCLE_COLOR_GRAY_5` | `(TinCLE_Color){64, 64, 64, 255}` |
| `TINCLE_COLOR_GRAY_6` | `(TinCLE_Color){77, 77, 77, 255}` | `TINCLE_COLOR_GRAY_7` | `(TinCLE_Color){90, 90, 90, 255}` |
| `TINCLE_COLOR_GRAY_8` | `(TinCLE_Color){102, 102, 102, 255}` | `TINCLE_COLOR_GRAY_9` | `(TinCLE_Color){115, 115, 115, 255}` |
| `TINCLE_COLOR_GRAY` | `(TinCLE_Color){128, 128, 128, 255}` | `TINCLE_COLOR_GRAY_10` | `(TinCLE_Color){140, 140, 140, 255}` |
| `TINCLE_COLOR_GRAY_11` | `(TinCLE_Color){153, 153, 153, 255}` | `TINCLE_COLOR_GRAY_12` | `(TinCLE_Color){166, 166, 166, 255}` |
| `TINCLE_COLOR_GRAY_13` | `(TinCLE_Color){179, 179, 179, 255}` | `TINCLE_COLOR_GRAY_14` | `(TinCLE_Color){204, 204, 204, 255}` |
| `TINCLE_COLOR_GRAY_15` | `(TinCLE_Color){217, 217, 217, 255}` | `TINCLE_COLOR_GRAY_16` | `(TinCLE_Color){230, 230, 230, 255}` |
| `TINCLE_COLOR_GRAY_17` | `(TinCLE_Color){243, 243, 243, 255}` | `TINCLE_COLOR_WHITE` | `(TinCLE_Color){255, 255, 255, 255}` |

#### 2. REGULAR RETRO 16 COLORS

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_NAVY` | `(TinCLE_Color){0, 0, 128, 255}` | `TINCLE_COLOR_DARK_BLUE` | `(TinCLE_Color){0, 0, 139, 255}` |
| `TINCLE_COLOR_GREEN` | `(TinCLE_Color){0, 128, 0, 255}` | `TINCLE_COLOR_TEAL` | `(TinCLE_Color){0, 128, 128, 255}` |
| `TINCLE_COLOR_MAROON` | `(TinCLE_Color){128, 0, 0, 255}` | `TINCLE_COLOR_PURPLE` | `(TinCLE_Color){128, 0, 128, 255}` |
| `TINCLE_COLOR_OLIVE` | `(TinCLE_Color){128, 128, 0, 255}` | `TINCLE_COLOR_LIGHT_GRAY` | `(TinCLE_Color){211, 211, 211, 255}` |
| `TINCLE_COLOR_DARK_GRAY` | `(TinCLE_Color){169, 169, 169, 255}` | `TINCLE_COLOR_BLUE` | `(TinCLE_Color){0, 0, 255, 255}` |
| `TINCLE_COLOR_LIME` | `(TinCLE_Color){0, 255, 0, 255}` | `TINCLE_COLOR_CYAN` | `(TinCLE_Color){0, 255, 255, 255}` |
| `TINCLE_COLOR_RED` | `(TinCLE_Color){255, 0, 0, 255}` | `TINCLE_COLOR_MAGENTA` | `(TinCLE_Color){255, 0, 255, 255}` |
| `TINCLE_COLOR_YELLOW` | `(TinCLE_Color){255, 255, 0, 255}` |  |  |

#### 3. RED / ORANGE / BROWN SYSTEMS (35 Colors)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_DARK_RED` | `(TinCLE_Color){139, 0, 0, 255}` | `TINCLE_COLOR_BROWN` | `(TinCLE_Color){165, 42,  42, 255}` |
| `TINCLE_COLOR_FIREBRICK` | `(TinCLE_Color){178, 34, 34, 255}` | `TINCLE_COLOR_CRIMSON` | `(TinCLE_Color){220, 20, 60, 255}` |
| `TINCLE_COLOR_TOMATO` | `(TinCLE_Color){255, 99, 71, 255}` | `TINCLE_COLOR_CORAL` | `(TinCLE_Color){255, 127, 80, 255}` |
| `TINCLE_COLOR_INDIAN_RED` | `(TinCLE_Color){205, 92, 92, 255}` | `TINCLE_COLOR_LIGHT_CORAL` | `(TinCLE_Color){240, 128, 128, 255}` |
| `TINCLE_COLOR_DARK_SALMON` | `(TinCLE_Color){233, 150, 122, 255}` | `TINCLE_COLOR_SALMON` | `(TinCLE_Color){250, 128, 114, 255}` |
| `TINCLE_COLOR_LIGHT_SALMON` | `(TinCLE_Color){255, 160, 122, 255}` | `TINCLE_COLOR_ORANGE_RED` | `(TinCLE_Color){255, 69, 0, 255}` |
| `TINCLE_COLOR_DARK_ORANGE` | `(TinCLE_Color){255, 140, 0, 255}` | `TINCLE_COLOR_ORANGE` | `(TinCLE_Color){255, 165, 0, 255}` |
| `TINCLE_COLOR_GOLD` | `(TinCLE_Color){255, 215, 0, 255}` | `TINCLE_COLOR_SADDLE_BROWN` | `(TinCLE_Color){139, 69, 19, 255}` |
| `TINCLE_COLOR_SIENNA` | `(TinCLE_Color){160, 82, 45, 255}` | `TINCLE_COLOR_CHOCOLATE` | `(TinCLE_Color){210, 105, 30, 255}` |
| `TINCLE_COLOR_PERU` | `(TinCLE_Color){205, 133, 63, 255}` | `TINCLE_COLOR_SANDY_BROWN` | `(TinCLE_Color){244, 164, 96, 255}` |
| `TINCLE_COLOR_BURLEY_WOOD` | `(TinCLE_Color){222, 184, 135, 255}` | `TINCLE_COLOR_TAN` | `(TinCLE_Color){210, 180, 140, 255}` |
| `TINCLE_COLOR_ROSY_BROWN` | `(TinCLE_Color){188, 143, 143, 255}` | `TINCLE_COLOR_MOCCASIN` | `(TinCLE_Color){255, 228, 181, 255}` |
| `TINCLE_COLOR_PEACH_PUFF` | `(TinCLE_Color){255, 218, 185, 255}` | `TINCLE_COLOR_NAVAJO_WHITE` | `(TinCLE_Color){255, 222, 173, 255}` |
| `TINCLE_COLOR_BISQUE` | `(TinCLE_Color){255, 228, 196, 255}` | `TINCLE_COLOR_BRICK_RED` | `(TinCLE_Color){153, 51, 51, 255}` |
| `TINCLE_COLOR_DEEP_ORANGE` | `(TinCLE_Color){255, 102, 0, 255}` | `TINCLE_COLOR_PUMPKIN` | `(TinCLE_Color){204, 102, 0, 255}` |
| `TINCLE_COLOR_RUST` | `(TinCLE_Color){153, 102, 51, 255}` | `TINCLE_COLOR_COPPER` | `(TinCLE_Color){204, 102, 51, 255}` |
| `TINCLE_COLOR_AMBER` | `(TinCLE_Color){255, 153, 0, 255}` | `TINCLE_COLOR_OCHRE` | `(TinCLE_Color){204, 153, 51, 255}` |
| `TINCLE_COLOR_MAHOGANY` | `(TinCLE_Color){102, 0, 0, 255}` |  |  |

#### 4. YELLOW / GREEN / EARTH SYSTEMS (45 Colors)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_DARK_KHAKI` | `(TinCLE_Color){189, 183, 107, 255}` | `TINCLE_COLOR_KHAKI` | `(TinCLE_Color){240, 230, 140, 255}` |
| `TINCLE_COLOR_PALE_GOLDENROD` | `(TinCLE_Color){238, 232, 170, 255}` | `TINCLE_COLOR_LIGHT_GOLDENROD_YELLOW` | `(TinCLE_Color){250, 250, 210, 255}` |
| `TINCLE_COLOR_LIGHT_YELLOW` | `(TinCLE_Color){255, 255, 224, 255}` | `TINCLE_COLOR_LEMON_CHIFFON` | `(TinCLE_Color){255, 250, 205, 255}` |
| `TINCLE_COLOR_PAPAYA_WHIP` | `(TinCLE_Color){255, 239, 213, 255}` | `TINCLE_COLOR_CORNSILK` | `(TinCLE_Color){255, 248, 220, 255}` |
| `TINCLE_COLOR_DARK_GREEN` | `(TinCLE_Color){0, 100, 0, 255}` | `TINCLE_COLOR_FOREST_GREEN` | `(TinCLE_Color){34, 139, 34, 255}` |
| `TINCLE_COLOR_SEA_GREEN` | `(TinCLE_Color){46, 139, 87, 255}` | `TINCLE_COLOR_MEDIUM_SEA_GREEN` | `(TinCLE_Color){60, 179, 113, 255}` |
| `TINCLE_COLOR_PALE_GREEN` | `(TinCLE_Color){152, 251, 152, 255}` | `TINCLE_COLOR_LIGHT_GREEN` | `(TinCLE_Color){144, 238, 144, 255}` |
| `TINCLE_COLOR_SPRING_GREEN` | `(TinCLE_Color){0, 255, 127, 255}` | `TINCLE_COLOR_MEDIUM_SPRING_GREEN` | `(TinCLE_Color){0, 250, 154, 255}` |
| `TINCLE_COLOR_LAWN_GREEN` | `(TinCLE_Color){124, 252, 0, 255}` | `TINCLE_COLOR_CHARTREUSE` | `(TinCLE_Color){127, 255, 0, 255}` |
| `TINCLE_COLOR_GREEN_YELLOW` | `(TinCLE_Color){173, 255, 47, 255}` | `TINCLE_COLOR_LIME_GREEN` | `(TinCLE_Color){50, 205, 50, 255}` |
| `TINCLE_COLOR_YELLOW_GREEN` | `(TinCLE_Color){154, 205, 50, 255}` | `TINCLE_COLOR_OLIVE_DRAB` | `(TinCLE_Color){107, 142, 35, 255}` |
| `TINCLE_COLOR_DARK_OLIVE_GREEN` | `(TinCLE_Color){85, 107, 47, 255}` | `TINCLE_COLOR_MINT_GREEN` | `(TinCLE_Color){102, 255, 153, 255}` |
| `TINCLE_COLOR_MOSS_GREEN` | `(TinCLE_Color){102, 153, 102, 255}` | `TINCLE_COLOR_SAGE` | `(TinCLE_Color){153, 204, 153, 255}` |
| `TINCLE_COLOR_EMERALD` | `(TinCLE_Color){0, 204, 102, 255}` | `TINCLE_COLOR_PINE_GREEN` | `(TinCLE_Color){0, 102, 51, 255}` |
| `TINCLE_COLOR_JADE` | `(TinCLE_Color){0, 153, 102, 255}` | `TINCLE_COLOR_BRIGHT_GREEN` | `(TinCLE_Color){102, 255, 0, 255}` |
| `TINCLE_COLOR_PASTEL_GREEN` | `(TinCLE_Color){204, 255, 204, 255}` | `TINCLE_COLOR_ARMY_GREEN` | `(TinCLE_Color){51, 102, 51, 255}` |
| `TINCLE_COLOR_SEA_FOAM` | `(TinCLE_Color){153, 255, 204, 255}` | `TINCLE_COLOR_PALE_YELLOW` | `(TinCLE_Color){255, 255, 153, 255}` |
| `TINCLE_COLOR_BANANA` | `(TinCLE_Color){255, 255, 102, 255}` | `TINCLE_COLOR_MUSTARD` | `(TinCLE_Color){204, 204, 51, 255}` |
| `TINCLE_COLOR_OLIVE_GREEN` | `(TinCLE_Color){102, 102, 0, 255}` | `TINCLE_COLOR_BRASS` | `(TinCLE_Color){153, 153, 51, 255}` |
| `TINCLE_COLOR_DESERT_SAND` | `(TinCLE_Color){204, 204, 153, 255}` | `TINCLE_COLOR_ECRU` | `(TinCLE_Color){204, 153, 102, 255}` |
| `TINCLE_COLOR_CAMEL` | `(TinCLE_Color){153, 102, 0, 255}` | `TINCLE_COLOR_SEPIA` | `(TinCLE_Color){102, 51, 0, 255}` |
| `TINCLE_COLOR_CHOCOLATE_DARK` | `(TinCLE_Color){51, 0, 0, 255}` | `TINCLE_COLOR_DEEP_FOREST` | `(TinCLE_Color){0, 51, 0, 255}` |
| `TINCLE_COLOR_NIGHT_GREEN` | `(TinCLE_Color){0, 51, 51, 255}` |  |  |

#### 5. CYAN / AQUA / BLUE SYSTEMS (50 Colors)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_DARK_CYAN` | `(TinCLE_Color){0, 139, 139, 255}` | `TINCLE_COLOR_LIGHT_SEA_GREEN` | `(TinCLE_Color){32, 178, 170, 255}` |
| `TINCLE_COLOR_CADET_BLUE` | `(TinCLE_Color){95, 158, 160, 255}` | `TINCLE_COLOR_DARK_TURQUOISE` | `(TinCLE_Color){0, 206, 209, 255}` |
| `TINCLE_COLOR_MEDIUM_TURQUOISE` | `(TinCLE_Color){72, 209, 204, 255}` | `TINCLE_COLOR_TURQUOISE` | `(TinCLE_Color){64, 224, 208, 255}` |
| `TINCLE_COLOR_PALE_TURQUOISE` | `(TinCLE_Color){175, 238, 238, 255}` | `TINCLE_COLOR_LIGHT_CYAN` | `(TinCLE_Color){224, 255, 255, 255}` |
| `TINCLE_COLOR_AZURE` | `(TinCLE_Color){240, 255, 255, 255}` | `TINCLE_COLOR_POWDER_BLUE` | `(TinCLE_Color){176, 224, 230, 255}` |
| `TINCLE_COLOR_LIGHT_BLUE` | `(TinCLE_Color){173, 216, 230, 255}` | `TINCLE_COLOR_SKY_BLUE` | `(TinCLE_Color){135, 206, 235, 255}` |
| `TINCLE_COLOR_LIGHT_SKY_BLUE` | `(TinCLE_Color){135, 206, 250, 255}` | `TINCLE_COLOR_DEEP_SKY_BLUE` | `(TinCLE_Color){0, 191, 255, 255}` |
| `TINCLE_COLOR_DODGER_BLUE` | `(TinCLE_Color){30, 144, 255, 255}` | `TINCLE_COLOR_CORNFLOWER_BLUE` | `(TinCLE_Color){100, 149, 237, 255}` |
| `TINCLE_COLOR_STEEL_BLUE` | `(TinCLE_Color){70, 130, 180, 255}` | `TINCLE_COLOR_ROYAL_BLUE` | `(TinCLE_Color){65, 105, 225, 255}` |
| `TINCLE_COLOR_MEDIUM_BLUE` | `(TinCLE_Color){0, 0, 205, 255}` | `TINCLE_COLOR_MIDNIGHT_BLUE` | `(TinCLE_Color){25, 25, 112, 255}` |
| `TINCLE_COLOR_ICE_BLUE` | `(TinCLE_Color){204, 255, 255, 255}` | `TINCLE_COLOR_BABY_BLUE` | `(TinCLE_Color){153, 204, 255, 255}` |
| `TINCLE_COLOR_ELECTRIC_BLUE` | `(TinCLE_Color){0, 204, 255, 255}` | `TINCLE_COLOR_DEEP_BLUE` | `(TinCLE_Color){0, 102, 255, 255}` |
| `TINCLE_COLOR_COBALT` | `(TinCLE_Color){0, 51, 204, 255}` | `TINCLE_COLOR_OCEAN_BLUE` | `(TinCLE_Color){0, 102, 153, 255}` |
| `TINCLE_COLOR_MARINE_BLUE` | `(TinCLE_Color){0, 51, 153, 255}` | `TINCLE_COLOR_PASTEL_BLUE` | `(TinCLE_Color){153, 153, 255, 255}` |
| `TINCLE_COLOR_DENIM` | `(TinCLE_Color){51, 102, 153, 255}` | `TINCLE_COLOR_SLATE_LIGHT` | `(TinCLE_Color){102, 153, 204, 255}` |
| `TINCLE_COLOR_AQUA_GREEN` | `(TinCLE_Color){51, 204, 153, 255}` | `TINCLE_COLOR_DARK_AQUA` | `(TinCLE_Color){0, 102, 102, 255}` |
| `TINCLE_COLOR_CYAN_DEEP` | `(TinCLE_Color){0, 153, 153, 255}` | `TINCLE_COLOR_TEAL_LIGHT` | `(TinCLE_Color){51, 153, 153, 255}` |
| `TINCLE_COLOR_NIGHT_BLUE` | `(TinCLE_Color){0, 0, 51, 255}` | `TINCLE_COLOR_SAPPHIRE` | `(TinCLE_Color){15, 82, 186, 255}` |
| `TINCLE_COLOR_ULTRAMARINE` | `(TinCLE_Color){18, 10, 143, 255}` | `TINCLE_COLOR_LAPIS` | `(TinCLE_Color){38, 97, 156, 255}` |
| `TINCLE_COLOR_CERULEAN` | `(TinCLE_Color){0, 123, 167, 255}` | `TINCLE_COLOR_INDIGO_DEEP` | `(TinCLE_Color){0, 46, 93, 255}` |
| `TINCLE_COLOR_CYAN_PALE` | `(TinCLE_Color){153, 204, 204, 255}` | `TINCLE_COLOR_BLUE_PALE` | `(TinCLE_Color){204, 204, 255, 255}` |
| `TINCLE_COLOR_AQUA_PALE` | `(TinCLE_Color){204, 255, 204, 255}` | `TINCLE_COLOR_SKY_PALE` | `(TinCLE_Color){153, 255, 255, 255}` |
| `TINCLE_COLOR_ROBINS_EGG` | `(TinCLE_Color){0, 204, 153, 255}` | `TINCLE_COLOR_MIDNIGHT_DEEP` | `(TinCLE_Color){10, 10, 40, 255}` |
| `TINCLE_COLOR_VOID_BLUE` | `(TinCLE_Color){5, 5, 25, 255}` | `TINCLE_COLOR_PACIFIC_BLUE` | `(TinCLE_Color){26, 153, 204, 255}` |
| `TINCLE_COLOR_STORM_BLUE` | `(TinCLE_Color){102, 102, 153, 255}` | `TINCLE_COLOR_SHADOW_BLUE` | `(TinCLE_Color){51, 51, 102, 255}` |

#### 6. PURPLE / PINK / LUXURY COSMETICS (50 Colors)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_INDIGO` | `(TinCLE_Color){75, 0, 130, 255}` | `TINCLE_COLOR_DARK_SLATE_BLUE` | `(TinCLE_Color){72, 61, 139, 255}` |
| `TINCLE_COLOR_SLATE_BLUE` | `(TinCLE_Color){106, 90, 205, 255}` | `TINCLE_COLOR_MEDIUM_SLATE_BLUE` | `(TinCLE_Color){123, 104, 238, 255}` |
| `TINCLE_COLOR_MEDIUM_PURPLE` | `(TinCLE_Color){147, 112, 219, 255}` | `TINCLE_COLOR_DARK_MAGENTA` | `(TinCLE_Color){139, 0, 139, 255}` |
| `TINCLE_COLOR_DARK_VIOLET` | `(TinCLE_Color){148, 0, 211, 255}` | `TINCLE_COLOR_DARK_ORCHID` | `(TinCLE_Color){153, 50, 204, 255}` |
| `TINCLE_COLOR_MEDIUM_ORCHID` | `(TinCLE_Color){186, 85, 211, 255}` | `TINCLE_COLOR_ORCHID` | `(TinCLE_Color){218, 112, 214, 255}` |
| `TINCLE_COLOR_VIOLET` | `(TinCLE_Color){238, 130, 238, 255}` | `TINCLE_COLOR_PLUM` | `(TinCLE_Color){221, 160, 221, 255}` |
| `TINCLE_COLOR_THISTLE` | `(TinCLE_Color){216, 191, 216, 255}` | `TINCLE_COLOR_LAVENDER` | `(TinCLE_Color){230, 230, 250, 255}` |
| `TINCLE_COLOR_DEEP_PINK` | `(TinCLE_Color){255, 20, 147, 255}` | `TINCLE_COLOR_HOT_PINK` | `(TinCLE_Color){255, 105, 180, 255}` |
| `TINCLE_COLOR_PALE_VIOLET_RED` | `(TinCLE_Color){219, 112, 147, 255}` | `TINCLE_COLOR_MEDIUM_VIOLET_RED` | `(TinCLE_Color){199, 21, 133, 255}` |
| `TINCLE_COLOR_LIGHT_PINK` | `(TinCLE_Color){255, 182, 193, 255}` | `TINCLE_COLOR_PINK` | `(TinCLE_Color){255, 192, 203, 255}` |
| `TINCLE_COLOR_MISTY_ROSE` | `(TinCLE_Color){255, 228, 225, 255}` | `TINCLE_COLOR_LAVENDER_PALE` | `(TinCLE_Color){204, 153, 255, 255}` |
| `TINCLE_COLOR_VIOLET_BRIGHT` | `(TinCLE_Color){204, 0, 255, 255}` | `TINCLE_COLOR_MAGENTA_DARK` | `(TinCLE_Color){153, 0, 153, 255}` |
| `TINCLE_COLOR_PURPLE_DARK` | `(TinCLE_Color){102, 0, 102, 255}` | `TINCLE_COLOR_AMETHYST` | `(TinCLE_Color){153, 102, 204, 255}` |
| `TINCLE_COLOR_BOYSENBERRY` | `(TinCLE_Color){102, 0, 51, 255}` | `TINCLE_COLOR_MAUVE` | `(TinCLE_Color){204, 153, 204, 255}` |
| `TINCLE_COLOR_PASTEL_PINK` | `(TinCLE_Color){255, 204, 204, 255}` | `TINCLE_COLOR_PASTEL_PURPLE` | `(TinCLE_Color){204, 204, 255, 255}` |
| `TINCLE_COLOR_WINE` | `(TinCLE_Color){102, 51, 51, 255}` | `TINCLE_COLOR_BURGUNDY` | `(TinCLE_Color){128, 0, 32, 255}` |
| `TINCLE_COLOR_LILAC` | `(TinCLE_Color){200, 162, 200, 255}` | `TINCLE_COLOR_REDRUM` | `(TinCLE_Color){51, 0, 0, 255}` |
| `TINCLE_COLOR_VOID_PURPLE` | `(TinCLE_Color){25, 5, 25, 255}` | `TINCLE_COLOR_FUSCHIA_PALE` | `(TinCLE_Color){255, 153, 255, 255}` |
| `TINCLE_COLOR_ROSE_DEEP` | `(TinCLE_Color){255, 51, 153, 255}` | `TINCLE_COLOR_ROSE_DARK` | `(TinCLE_Color){153, 51, 102, 255}` |
| `TINCLE_COLOR_ROSE_PALE` | `(TinCLE_Color){255, 204, 221, 255}` | `TINCLE_COLOR_BERRY` | `(TinCLE_Color){204, 0, 102, 255}` |
| `TINCLE_COLOR_MULBERRY` | `(TinCLE_Color){153, 51, 153, 255}` | `TINCLE_COLOR_RAISIN` | `(TinCLE_Color){51, 25, 51, 255}` |
| `TINCLE_COLOR_NIGHT_PURPLE` | `(TinCLE_Color){51, 0, 51, 255}` | `TINCLE_COLOR_BUBBLEGUM` | `(TinCLE_Color){255, 102, 204, 255}` |
| `TINCLE_COLOR_MAGENTA_PALE` | `(TinCLE_Color){255, 102, 255, 255}` | `TINCLE_COLOR_ORCHID_DARK` | `(TinCLE_Color){102, 51, 102, 255}` |
| `TINCLE_COLOR_PLUM_DARK` | `(TinCLE_Color){153, 102, 153, 255}` | `TINCLE_COLOR_SANGRIA` | `(TinCLE_Color){153, 0, 51, 255}` |
| `TINCLE_COLOR_VIOLET_PALE` | `(TinCLE_Color){238, 180, 238, 255}` | `TINCLE_COLOR_BLUSH` | `(TinCLE_Color){222, 93, 131, 255}` |

#### 7. SPECIAL ARCHITECTURE & GHOST DETAILS (41 Colors)

| Macro Name | Value | Macro Name | Value |
| --- | --- | --- | --- |
| `TINCLE_COLOR_SLATE_GRAY` | `(TinCLE_Color){112, 128, 144, 255}` | `TINCLE_COLOR_LIGHT_SLATE_GRAY` | `(TinCLE_Color){119, 136, 153, 255}` |
| `TINCLE_COLOR_DARK_SLATE_GRAY` | `(TinCLE_Color){47, 79, 79, 255}` | `TINCLE_COLOR_ALICE_BLUE` | `(TinCLE_Color){240, 248, 255, 255}` |
| `TINCLE_COLOR_GHOST_WHITE` | `(TinCLE_Color){248, 248, 255, 255}` | `TINCLE_COLOR_SEASHELL` | `(TinCLE_Color){255, 245, 238, 255}` |
| `TINCLE_COLOR_WHITE_SMOKE` | `(TinCLE_Color){245, 245, 245, 255}` | `TINCLE_COLOR_BEIGE` | `(TinCLE_Color){245, 245, 220, 255}` |
| `TINCLE_COLOR_OLD_LACE` | `(TinCLE_Color){253, 245, 230, 255}` | `TINCLE_COLOR_FLORAL_WHITE` | `(TinCLE_Color){255, 250, 240, 255}` |
| `TINCLE_COLOR_IVORY` | `(TinCLE_Color){255, 255, 240, 255}` | `TINCLE_COLOR_ANTIQUE_WHITE` | `(TinCLE_Color){250, 235, 215, 255}` |
| `TINCLE_COLOR_LINEN` | `(TinCLE_Color){250, 240, 230, 255}` | `TINCLE_COLOR_LAVENDER_BLUSH` | `(TinCLE_Color){255, 240, 245, 255}` |
| `TINCLE_COLOR_MINT_CREAM` | `(TinCLE_Color){245, 255, 250, 255}` | `TINCLE_COLOR_HONEYDEW` | `(TinCLE_Color){240, 255, 240, 255}` |
| `TINCLE_COLOR_SNOW` | `(TinCLE_Color){255, 250, 250, 255}` | `TINCLE_COLOR_SLATE_DARK` | `(TinCLE_Color){51, 51, 51, 255}` |
| `TINCLE_COLOR_SLATE_MEDIUM` | `(TinCLE_Color){102, 102, 102, 255}` | `TINCLE_COLOR_SLATE_PALE` | `(TinCLE_Color){153, 153, 153, 255}` |
| `TINCLE_COLOR_STEEL_DARK` | `(TinCLE_Color){51, 51, 102, 255}` | `TINCLE_COLOR_STEEL_PALE` | `(TinCLE_Color){153, 153, 204, 255}` |
| `TINCLE_COLOR_CHARCOAL` | `(TinCLE_Color){30, 30, 30, 255}` | `TINCLE_COLOR_GUNMETAL` | `(TinCLE_Color){42, 52, 57, 255}` |
| `TINCLE_COLOR_ASPHALT` | `(TinCLE_Color){16, 16, 26, 255}` | `TINCLE_COLOR_PEWTER` | `(TinCLE_Color){139, 141, 132, 255}` |
| `TINCLE_COLOR_PLATINUM` | `(TinCLE_Color){229, 228, 226, 255}` | `TINCLE_COLOR_SILVER` | `(TinCLE_Color){192, 192, 192, 255}` |
| `TINCLE_COLOR_METALLIC_GRAY` | `(TinCLE_Color){102, 102, 153, 255}` | `TINCLE_COLOR_COOL_GRAY` | `(TinCLE_Color){153, 153, 179, 255}` |
| `TINCLE_COLOR_WARM_GRAY` | `(TinCLE_Color){179, 179, 153, 255}` | `TINCLE_COLOR_BONE` | `(TinCLE_Color){227, 218, 201, 255}` |
| `TINCLE_COLOR_PARCHMENT` | `(TinCLE_Color){245, 245, 220, 255}` | `TINCLE_COLOR_PEARL` | `(TinCLE_Color){234, 230, 202, 255}` |
| `TINCLE_COLOR_ALABASTER` | `(TinCLE_Color){242, 240, 235, 255}` | `TINCLE_COLOR_PALE_ROSE` | `(TinCLE_Color){255, 221, 221, 255}` |
| `TINCLE_COLOR_PALE_ORANGE` | `(TinCLE_Color){255, 221, 153, 255}` | `TINCLE_COLOR_PALE_LIME` | `(TinCLE_Color){221, 255, 153, 255}` |
| `TINCLE_COLOR_PALE_AQUA` | `(TinCLE_Color){153, 255, 221, 255}` | `TINCLE_COLOR_PALE_SKY` | `(TinCLE_Color){153, 221, 255, 255}` |
| `TINCLE_COLOR_PALE_LAVENDER` | `(TinCLE_Color){221, 153, 255, 255}` |  |  |

#### 8. GLOBAL ALIAS DEFINITIONS (For High-Speed Prototyping)

| Alias Macro Name | Maps To | Alias Macro Name | Maps To |
| --- | --- | --- | --- |
| `TINCLE_COLOR_BLK` | `TINCLE_COLOR_BLACK` | `TINCLE_COLOR_WHT` | `TINCLE_COLOR_WHITE` |
| `TINCLE_COLOR_GRN` | `TINCLE_COLOR_GREEN` | `TINCLE_COLOR_BLU` | `TINCLE_COLOR_BLUE` |
| `TINCLE_COLOR_YEL` | `TINCLE_COLOR_YELLOW` | `TINCLE_COLOR_MAG` | `TINCLE_COLOR_MAGENTA` |
| `TINCLE_COLOR_AQUA` | `TINCLE_COLOR_CYAN` | `TINCLE_COLOR_FUCHSIA` | `TINCLE_COLOR_MAGENTA` |
