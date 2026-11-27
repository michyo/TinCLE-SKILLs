---
name: tincle-ft
description: Use when localizing dialogue or filling missing language columns in TSV game scripts using actor-based persona LLM translation in the TinCLE ecosystem. [TinCLE Tool Skill v0.19]
---

# SKILL_FT.md - TinCLE Tool Talent Chip: fartran

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami)
* **Author:** Anchichi
* **Tool Name:** `fartran` (Fluent Actor-based Rephrase & TRANslator)
* **Target Ecosystem:** TinCLE Game Engine AI-first Toolchain
* **Binary:** `fartran.exe` (Pure C99 compiled via TinyCC `tcc`)

---

## 1. Overview & Purpose

`fartran` is an AI-first, ultra-lightweight command-line dialogue localization and rephrasing tool designed specifically for the **TinCLE** game engine ecosystem.

In game development, localization cannot be a bland, word-for-word literal translation. An arrogant dragon king, a rebellious princess, an eccentric old wizard, and an aggressive drill instructor must each speak with distinct cadence, vocabulary, and emotional resonance in every supported language.

`fartran` automates this nuanced process:
1. It parses game dialogue from standard Tab-Separated Values (`.tsv`) tables.
2. It identifies vacant target language columns (e.g., `EN`, `CH`, `KO`, `FR`, `IT`, `RU`) on each dialogue row.
3. It extracts the row's `SPEAKER` identity and injects an actor persona instruction into the LLM's system prompt.
4. If configured, it automatically injects comprehensive external character profiles (`PROFILE_FILE`) into the system prompt to guide the LLM on character lore, personality, slang, and speech habits.
5. It calls an OpenAI-compatible completion endpoint (either local `llama-server` or cloud LLM) via native Windows HTTP (`winhttp`).
6. It safely parses and cleans the response using DaveGamble's `cJSON`, updates the in-memory TSV table, and atomically overwrites the original TSV file.

---

## 2. Command-Line Interface & Usage for AI Agents

All TinCLE CLI tools are designed for frictionless invocation by AI agents and automated build pipelines.

### Basic Syntax

```bash
fartran.exe [path/to/dialog.tsv]
```

* If no argument is provided, `fartran.exe` defaults to looking for `dialog.tsv` in the current working directory.

### Arguments

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `tsv_path` | File Path | No | `dialog.tsv` | Path to the target Tab-Separated Values dialogue script. |

### Configuration (`fartran.ini`)

`fartran.exe` reads configuration parameters from `fartran.ini` in the current working directory.

```ini
# fartran.ini - Configuration for fartran LLM backend
ENDPOINT=http://127.0.0.1:8080/v1/chat/completions
API_KEY=none
MODEL=qwen2.5-7b-instruct-q4_k_m.gguf
PROFILE_FILE=character_profiles.txt
```

#### Configuration Keys

| Key | Required | Description | Example (Local llama-server) |
|---|---|---|---|
| `ENDPOINT` | **Yes** | URL of the OpenAI-compatible `/v1/chat/completions` endpoint. | `http://127.0.0.1:8080/v1/chat/completions` |
| `API_KEY` | **Yes** | Bearer authorization token. Use `none` if unauthenticated. | `none` |
| `MODEL` | **Yes** | Name of the target model recognized by the endpoint. | `qwen2.5-7b-instruct-q4_k_m.gguf` |
| `PROFILE_FILE` | No | Path to optional external character profiles text/markdown file. | `character_profiles.txt` |

---

## 3. External Character Profiles (`PROFILE_FILE`)

To prevent shallow or stereotypical AI translations, you can supply rich character dossiers via `PROFILE_FILE`.

### Behavior & Fallback
* When specified in `fartran.ini`, `fartran` dynamically reads the entire file into memory (handling UTF-8 BOM automatically).
* If the file is not found, `fartran` prints a mild warning to `stderr` and proceeds with standard translation without crashing.
* When loaded, the contents are appended to the system prompt under `# Character Profiles`.

### Example `character_profiles.txt`

```markdown
# Character Profiles

## Hero
- Tone: Energetic, direct, rough-edged young adventurer.
- Slang: Uses casual street terms ("Yo", "Damn", "Let's roll").
- Speech Style: Short, punchy sentences. Never speaks formally.

## Princess
- Tone: Aristocratic, haughty, elegant yet determined.
- Speech Style: Sophisticated vocabulary, haughty imperiousness, polite grammatical forms.

## OldWizard
- Tone: Ancient, cynical, speaks with archaic wisdom and world-weary gravel.
- Speech Style: Uses archaic phrasing ("Hark", "By the heavens", "Alas").

## Hartman
- Tone: Aggressive military drill sergeant.
- Speech Style: Extremely loud, vulgar, commanding, intimidating bark.
```

---

## 4. TSV Format & Schema

`fartran` expects standard Tab-Separated Values files (`.tsv`). It automatically recognizes header names regardless of casing.

### Typical Header Layout

```tsv
ID	SPEAKER	JA	EN	CH	KO	FR	IT	RU
```

* **`ID` Column:** Unique identifier for each line (ignored during translation).
* **`SPEAKER` Column:** Character name matching the profile key (e.g., `Hero`, `Princess`, `OldWizard`, `Hartman`). If left blank, `fartran` prompts for a neutral translation.
* **Source Column:** Defaults to `JA` (or first non-empty text column if `JA` is not found).
* **Target Columns:** Any additional columns (e.g., `EN`, `CH`, `KO`, `FR`, `IT`, `RU`, `DE`, `ES`).

### Supported Language Column Codes

`fartran` includes built-in case-insensitive code-to-name mapping for the following 10 languages to maximize LLM translation accuracy:

| Target Language | Recognized Column Codes (Case-Insensitive) |
|---|---|
| **Japanese** | `JA`, `JP`, `JPN` |
| **English** | `EN`, `ENG` |
| **Chinese** | `CH`, `ZH`, `CN` |
| **Korean** | `KO`, `KOR` |
| **French** | `FR`, `FRA` |
| **German** | `DE`, `DEU`, `GER` |
| **Spanish** | `ES`, `SPA` |
| **Italian** | `IT`, `ITA` |
| **Portuguese** | `PT`, `POR` |
| **Russian** | `RU`, `RUS` |

* **Other Languages (Fallback):** Any column header not listed above is passed directly to the LLM as the target language name. For unlisted languages, use the full English language name as the column header (e.g., `Arabic`, `Vietnamese`, `Thai`, `Indonesian`) rather than an abbreviation to avoid ambiguity.

### Example Before Translation

```tsv
ID	SPEAKER	JA	EN	CH
1	Hero	おい、早くここから逃げるぞ！		
2	Princess	おい、早くここから逃げるぞ！		
3	Hartman	おい、早くここから逃げるぞ！		
```

### Example After Running `fartran`

```tsv
ID	SPEAKER	JA	EN	CH
1	Hero	おい、早くここから逃げるぞ！	Yo, hurry up and get the hell out of here!	喂，快点从这里逃出去！
2	Princess	おい、早くここから逃げるぞ！	We must make our escape at once!	我们必须立刻离开此地！
3	Hartman	おい、早くここから逃げるぞ！	Move your asses, double time! Out of here NOW!	全都给老子跑起来！快滚！
```

---

## 5. Persona Prompting Architecture

For each vacant cell, `fartran` builds an OpenAI-compatible payload:

1. **System Prompt Formulation:**
   * **Base Persona:**
     ```
     You are an expert translator and creative writer. Act completely as {SPEAKER}. Prioritize the character's unique tone, slang, and personality OVER literal translation accuracy. Output ONLY the translated text. Do not output anything else.
     ```
   * **Profile Append (if `PROFILE_FILE` loaded):**
     ```
     {Base Persona}

     # Character Profiles
     {Profile File Contents}
     ```
2. **User Prompt Formulation:**
   * Formats the request to translate the source text into the column's target language:
     ```
     Translate the following text into {TARGET_LANG}:\n{SOURCE_TEXT}
     ```
3. **Response Sanitization:**
   * Trims leading/trailing whitespace and surrounding quotation marks.
   * Flattens newlines and internal tabs into spaces to protect TSV table formatting.

---

## 6. Error Handling & Return Codes

In accordance with TinCLE strict error specifications:

* **Connection Failure:** If the HTTP endpoint cannot be reached, the server refuses connection, or returns gateway errors (502/503/504), `fartran` outputs:
  ```text
  [fartran] Failed to connect to the LLM service.
  ```
  and immediately terminates with exit code `1`.
* **Missing Config / Missing TSV:** Outputs a descriptive error message to `stderr` and terminates with exit code `1`.
* **Missing Profile File:** Emits a warning to `stderr` and gracefully continues translation.
* **Idempotency:** If all target cells are already populated, `fartran` reports:
  ```text
  [fartran] Completed successfully. Total cells translated: 0
  ```
  and exits with code `0`.

### [CRITICAL AI AGENT FALLBACK PROTOCOL]

When an autonomous/agentic AI executes `fartran.exe` and receives **either** of the following error messages:

* `[fartran] Failed to connect to the LLM service.`
* `[fartran] Error: Could not read 'fartran.ini' or required keys missing (ENDPOINT, API_KEY, MODEL).`

This means the user has **NOT** prepared a local LLM environment for you to offload the translation workload. **Do NOT get stuck in a retry loop or abort the entire game development task.** Instead, you **MUST** immediately take one of the following two actions:

1. **Translate Directly Yourself (Autonomous Fallback - Recommended):**
   Accept that no shortcut is configured and **perform the actor-based multilingual translation yourself** by directly editing and populating the vacant language columns in the `.tsv` file (strictly preserving each `SPEAKER`'s persona and any rules in `character_profiles.txt`).
2. **Request Local LLM Configuration from the User (Human-in-the-Loop):**
   If the dialogue volume is too large to translate manually or the user explicitly wants to use `fartran`, politely inform the user that `fartran` could not reach a local LLM backend, and instruct them to:
   * Configure `fartran.ini` with a valid local `ENDPOINT`, `API_KEY=none`, and `MODEL` (for a local LLM server such as `llama-server`, Ollama, or LM Studio), and
   * Ensure the local LLM server is actively running before re-running `fartran.exe`.

> **[SECURITY RULE FOR AI AGENTS]:** Never ask the user to paste paid cloud API keys (e.g., OpenAI, Gemini, Anthropic) into `fartran.ini` inside an agent-accessible workspace, and never read, echo, or commit sensitive credentials from `fartran.ini` into chat logs or release packages.

---

## 7. Developer Build Guide

### Prerequisites
* Windows 10/11 environment.
* TinyCC (`tcc`) accessible via `sptcc32` or `sptcc64`.
* Standard Windows system libraries (`winhttp.dll`).

### Building `fartran.exe`

```cmd
sptcc32
tcc fartran.c -lwinhttp -o fartran.exe
```

### Running with Local LLM (`llama-server`)

```cmd
:: 1. Launch local llama-server
stllama

:: 2. Execute translation on dialog script
fartran.exe dialog.tsv
```
