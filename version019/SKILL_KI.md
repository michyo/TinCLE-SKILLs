---
name: tincle-ki
description: Use when encoding binary files (such as TinyCC executables or archives) into plain-ASCII ISH text files, or decoding/restoring ISH archives (jis7, jis8, shift jis, non-kana, old_style, multi-volume, or damaged logs with up to 2 lost lines per block) using the TinCLE external utility knish. [TinCLE Tool Skill v0.19]
---

# TinCLE External Utility Skill: `knish` (v0.19)

`knish` (**Knitter & tiNker for ISH**) is a standalone, zero-dependency CLI utility in the TinCLE ecosystem for encoding binary files into error-correcting plain-ASCII ISH text and decoding/restoring MS-DOS ISH Ver 2.00–compatible archives.

---

## 1. Command Syntax & Mode Auto-Detection

```text
knish [options] <input> [more .ish files ...]
```

### Automatic Mode Selection (Default)

* **Decode mode**: Triggered automatically when the first input file has the `.ish` extension (case-insensitive).
* **Encode mode**: Triggered automatically for any other extension. By default, outputs `<input>.ish` in the same path.
* **Multi-volume merge**: Passing multiple `.ish` files decodes and merges all volumes in a single run (volume order does not matter).

---

## 2. CLI Options Reference

| Option | Argument | Description |
| --- | --- | --- |
| `-e`, `--encode` | — | Force **encode** mode (`jis7`, single volume). Accepts **exactly 1** input file. |
| `-d`, `--decode` | — | Force **decode** mode. Accepts 1 or more input files. |
| `-o <path>` | Path | **Encode**: output `.ish` file path.<br>**Decode**: output file path (when 1 file is restored) or output directory (must already exist, or end with `/` or `\`; **required** to be a directory if multiple files are restored from a concatenated log). |
| `-f`, `--force` | — | Overwrite existing output files during decode. Without `-f`, `knish` aborts with a non-zero exit code if the destination file already exists. |
| `-q`, `--quiet` | — | Suppress startup banner and progress logs (`stderr` errors are still printed). |
| `-h`, `--help` | — | Print banner and usage help, then exit with `0`. |
| `-v`, `--version` | — | Print `knish 0.19` (without banner), then exit with `0`. |

### Exit Codes

* **`0`**: Operation succeeded (all CRCs verified and output written).
* **Non-zero (`1`)**: Invalid arguments, no input specified, file I/O failure, existing destination without `-f`, no ISH data found, unrecoverable damage (3+ lost/corrupted lines in one block), CRC-16/CRC-32 mismatch, or missing volumes in a multi-volume archive.

---

## 3. Capabilities & Format Compatibility

### Encoding (`knish` → `.ish`)

* **Format**: `jis7` (pure 7-bit printable ASCII, 63 binary bytes / 78 chars per line, 62 lines per block, standard 2-line error correction).
* **Volume**: Single volume.
* **Metadata**:
  * Generates a safe MS-DOS 8.3 FCB filename in the binary header (no OS API dependency).
  * Embeds the full UTF-8 basename in the first comment line via `[knish:<utf8_basename>]`. For pure printable ASCII names without spaces or brackets (`<= 200` bytes), also places the long name at the start of the `<<< <name> ... >>>` comment line for `LhaForge` / legacy tool interoperability.
  * Stores File CRC-16, File CRC-32, and local modification timestamp (DOS format, 2-second resolution, year >= 1980).

### Decoding (`.ish` → original binary)

* **Supported encodings**: All 4 MS-DOS ISH Ver 2.00 formats:
  * `jis7` (13-bit, 63B/line, 62 lines/block)
  * `jis8` (7-bit, 69B/line, 68 lines/block)
  * `shift jis` (15-bit, 73B/line, 72 lines/block)
  * `shift jis (non-kana)` (14-bit, 69B/line, 68 lines/block)
  * Legacy `old_style` (70-byte / 80-char diagonal checksum line, sequence `68`) and `jis8` headers (69 bytes).
* **Error correction**: Automatically repairs **up to 2 missing or corrupted lines per block** using vertical and diagonal checksums.
* **Noise tolerance**: Ignores mail/log quote prefixes (e.g., `> `), blank lines, and arbitrary text between blocks.
* **Multi-volume & concatenated logs**:
  * Automatically groups and merges multi-volume archives (up to 250 volumes) across one or multiple input files, even when volumes appear out of order.
  * Automatically extracts multiple distinct files concatenated inside a single text log.
* **Integrity verification**: Verifies per-line CRC-16, stream-tail CRC-16, Volume CRC-16 (when flagged), File CRC-16, and File CRC-32 before writing output.
* **Unicode & filename restoration priority**:
  1. Explicit `-o <file_path>` (single-file output only)
  2. `[knish:<name>]` tag in the preceding comment line
  3. Long filename in `<<< <name> ... >>>` comment line (on Windows, non-UTF-8 Shift_JIS/CP932 names from `ISH32.DLL` are automatically converted to UTF-8)
  4. Header 11-byte 8.3 FCB filename
    * Path traversal components (`../`, drive letters, illegal characters) are always stripped to a safe basename.
    * Full UTF-8 / Unicode file paths and console output are supported on Windows without changing the console code page.
    * Original DOS modification timestamp is restored when present in the header.

---

## 4. Recommended Usage Patterns for AI Agents

```bash
# 1. Encode a binary into plain ASCII (.ish) with quiet output
knish -q my_game.exe
# -> Creates my_game.exe.ish

# 2. Encode to an explicit output path
knish -q -e build/game.exe -o dist/game_payload.ish

# 3. Decode into a specific directory, overwriting existing files safely
knish -q -f -o restored_dir/ dist/game_payload.ish

# 4. Decode a single .ish to an explicit output filename
knish -q -f -d payload.txt -o restored_game.exe

# 5. Merge and restore a multi-volume ISH archive (any order)
knish -q -f -o restored_dir/ part2.ish part3.ish part1.ish
```

---

## 5. Constraints & Agent Pitfalls (Important)

1. **Always use `-f` in automated pipelines**: Without `-f`, decoding fails with exit code `1` if the target file already exists.
2. **One input file per encode**: `knish -e` rejects multiple input files. To wrap multiple files (e.g., an executable plus assets), archive them first (e.g., ZIP) and encode the single archive.
3. **Concatenated logs require a directory with `-o`**: If an `.ish` log contains 2 or more embedded files and `-o` points to a non-directory path, `knish` aborts with an error. Create the output directory first or pass a path ending in `/`.
4. **No `stdin`/`stdout` streaming**: Always pass actual filesystem paths; `"-"` is not treated as `stdin`/`stdout`.
5. **Memory limit on decode**: Decoded payload size is capped at 512 MB (`0x20000000` bytes) and buffered in memory.
6. **Non-`.ish` extension when decoding**: If an ISH text file has another extension (e.g., `.txt` or `.i01`), you **must** pass `-d` (otherwise `knish` auto-detects encode mode and re-encodes the text file!).
