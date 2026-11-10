---
name: tincle-pt
description: Use when composing, generating, or editing MML (Music Macro Language) music files for pisstrak synthesizer. Enforces strict bar-length duration calculations, octave persistence rules, multi-channel track synchronization, and raw MML text output contract. [TinCLE Tool Skill v0.18]
---

# SKILL_PT.md - TinCLE Tool Talent Chip [Composition & MML Generation]

* **Copyright & License:** Copyright (C) 2026 michyo (Michiyo Tagami). All rights reserved.

This document defines the instructions, rules, and syntax for generating MML (Music Macro Language) files compatible with the `pisstrak` sound synthesizer engine.

---

## 1. Mandatory Note Value & Duration Lookup Table (CRITICAL)

Before writing ANY note, resolve its duration from this table.
NEVER derive durations from memory. ALWAYS use this table.

| Suffix | Name            | Quarter Beats | 8th units | 16th ticks |
|--------|-----------------|---------------|-----------|------------|
| `1`    | Whole           | 4.0           | 8         | 16         |
| `2`    | Half            | 2.0           | 4         | 8          |
| `4`    | Quarter         | 1.0           | 2         | 4          |
| `8`    | Eighth          | 0.5           | 1         | 2          |
| `16`   | Sixteenth       | 0.25          | 0.5       | 1          |
| `2.`   | Dotted Half     | 3.0           | 6         | 12         |
| `4.`   | Dotted Quarter  | 1.5           | 3         | 6          |
| `8.`   | Dotted Eighth   | 0.75          | 1.5       | 3          |
| `R4`   | Quarter Rest    | 1.0           | 2         | 4          |
| `R2`   | Half Rest       | 2.0           | 4         | 8          |
| `R8`   | Eighth Rest     | 0.5           | 1         | 2          |

**The default Ln applies ONLY to bare notes (C, D, E, ...).**  
**A note WITH an explicit suffix (C2, D4, E8) IGNORES the default Ln completely.**

---

## 2. Syntax & Command Reference

pisstrak parses ASCII text MML files. Commands are case-insensitive.

* **Channel Selection**: `CH1:` to `CH8:` (Declares which channel the following stream belongs to).
* **Tempo**: `Tn` (e.g., `T120` = 120 BPM).
* **Octave**: `On` (n = 1 to 8, default `O4`).
* **Volume**: `Vn` (n = 0 to 15, default `V12`).
* **Instrument / Patch**: `@n` (n = 0 to 127. Standard General MIDI Program Numbers).
* **Default Length**: `Ln` (n = 1, 2, 4, 8, 16, 32, 64. Default `L4`).
* **Notes**: `C`, `D`, `E`, `F`, `G`, `A`, `B`.
  * Sharp: `+` or `#` (e.g., `C+`, `F#`)
  * Flat: `-` (e.g., `B-`)
  * Explicit Length: Append number after note (e.g., `C8`, `G2.`)
  * Dotted Note: Append `.` (increases length by 1.5x, e.g., `C4.`)
* **Rest**: `R` (e.g., `R4` = Quarter rest). Safely stops previous note and advances time.
* **Octave Shift**:
  * Permanent Octave Shift: `<` (Down 1 base octave), `>` (Up 1 base octave).
  * `^` (One-shot octave UP: Applies ONLY to the single immediately following note without changing the base octave, e.g., `^C`).
  * `_` (One-shot octave DOWN: Applies ONLY to the single immediately following note without changing the base octave, e.g., `_C`).
* **Tie**: `&` (Connects current note duration to the next matching note).
* **Loop Macro**: `[ MML_SEQUENCE ]N` (Repeats the sequence inside brackets `N` times. Default `N=2`).
* **Comments & Bar Lines**: You MAY use `;` for line comments and `|` as visual bar separators to improve readability. The parser safely ignores them.

### 2.1 Strict Octave & Pitch State Rules (CRITICAL)

**MANDATORY** Temporary high-pitched notes are permitted to add dynamic variation to the music. However, at least 90% of the notes in the entire piece must fall within the O6 range or lower, so as not to be jarring to the ear.

To prevent catastrophic octave drift (e.g., pitch creeping up to unusable O8+ registers), you MUST strictly adhere to the following state management rules:

#### Rule 1: Principle of Absolute State Persistence

* **Octave states are strictly persistent per channel.**
* Moving to a new line (e.g., `CH1:`), passing bar lines `|`, or changing measures DOES NOT reset the octave.
* **CRITICAL MISCONCEPTIONS TO AVOID**: The base octave NEVER automatically resets to `O5` or default when a new line begins.

#### Rule 2: Mandatory Explicit Base Octave (`On`) at Line Start

To eliminate pitch tracking errors, **EVERY SINGLE line starting with `CHn:` MUST explicitly state its base octave (e.g., `O5`) at the very beginning of the line.**

  * **Good**: `CH1: O5 T96 V13 @73 L8`
  * **Good**: `CH1: O5 D4 R4 F4 R4 | A4 R8 G8 F4 E4`

#### Rule 3: Single-Note Leaps vs. Base Octave Shifts

1. **One-Shot Modifiers (`^` / `_`) [DEFAULT FOR MELODIC LEAPS]**:
   * Use `^` (up) or `_` (down) for momentary jumps, accents, or decorative notes.
   * `^C`: Plays ONLY this single C note one octave higher. The base octave for all subsequent notes remains untouched.
   * `_C`: Plays ONLY this single C note one octave lower. The base octave for all subsequent notes remains untouched.
2. **Relative Modifiers (`>` / `<`) [WIDE RANGE SHIFTS ONLY]**:
   * Use `>` or `<` ONLY when shifting the baseline register of an entire phrase permanently.
   * **STRICTLY PROHIBITED**: Never use `>` or `<` for single-note accents! Repeated use of `>` will cause pitch to stack endlessly into broken ultra-high frequencies.

#### Rule 4: Anti-Pattern Examples (Bad vs. Good)

**Bad (Broken & Uncontrolled Creep):**
  ```mml
  ; Base octave starts at O5
  CH1: O5 C4 D4 >E4 F4       ; '>' shifts base octave to O6!
  CH1: D4 F8 A8 >D4 C8 <A8   ; '>' shifts base octave to O7! Creeps endlessly higher!
  ```

**Good 1 (Bulletproof & Recommended: One-Shot Modifiers):**
  ```mml
  ; Use '^' or '_' for momentary leaps. Base octave stays safely at O5!
  CH1: O5 C4 D4 ^E4 F4       ; '^E4' plays E in O6, but base octave REMAINS O5!
  CH1: O5 D4 F8 A8 ^D4 C8 A8 ; Head of line explicitly has 'O5', base octave is rock solid!
  ```

**Good 2 (Explicit Shift & Reset):**
  ```mml
  ; If you MUST use '>' for a passage, ALWAYS reset it with '<'!
  CH1: O5 C4 D4 >E4 F4        ; Shift base octave to O6
  CH1: O6 D4 F8 A8 D4 C8 <A8  ; Shift base octave back to O5!
  ```

#### Pre-Output Checklist (Octave & Pitch Check)

1. [ ] Is every line starting with `CHn:` explicitly writing its base octave (`On`) at the start?
2. [ ] Are consecutive `>` shifts without intervening `<` resets avoided?
3. [ ] Are temporary note leaps written with `^` / `_` instead of `>` / `<`?
4. [ ] Are all resulting pitches within a comfortable human listening range (O2 to O6)?

---

## 3. Arrangement & Multi-Channel Rules

Always create a rich, multi-track arrangement using at least 3 to 4 channels unless specifically instructed otherwise.

* Pattern 1: Luxurious - In many cases, this style is preferred in video game music.

  * **CH1 (Lead/Melody)**: Main melody instrument (e.g., `@0` Piano, `@80` Square/Lead, `@73` Flute).
  * **CH2 (Sub/Melody)**: Sub melody instrument (e.g., `@24` Guitar, `@16` Organ, `@56` Trumpet).
  * **CH3 (Harmony/Counter)**: Accompaniment, arpeggios, or chords (e.g., `@24` Guitar, `@4` Electric Piano).
  * **CH4 (Harmony/Counter)**: Accompaniment, arpeggios, or chords (e.g., `@24` Guitar, `@4` Electric Piano).
  * **CH5 (Harmony/Counter)**: Accompaniment, arpeggios, or chords (e.g., `@24` Guitar, `@4` Electric Piano).
  * **CH6 (Strings)**: Low end anchor notes (e.g., `@40` Violin, `@98` Crystal).
  * **CH7 (Bassline)**: Low end anchor notes (e.g., `@33` Fingered Bass, `@38` Synth Bass).
  * **CH8 (Percussion/Drums)**: Rhythm track (e.g., `@128` Standard Drum Kit, or short tuned percussion).

* Pattern 2: Simple - This may be more suitable for games that emphasize quiet scenes or simplicity.

  * **CH1 (Lead/Melody)**: Main melody instrument (e.g., `@0` Piano, `@80` Square/Lead, `@73` Flute).
  * **CH2 (Harmony/Counter)**: Accompaniment, arpeggios, or chords (e.g., `@24` Guitar, `@4` Electric Piano).
  * **CH3 (Bassline)**: Low end anchor notes (e.g., `@33` Fingered Bass, `@38` Synth Bass).
  * **CH4 (Percussion/Drums)**: Rhythm track (e.g., `@128` Standard Drum Kit, or short tuned percussion).

---

## 4. Strict Timing & Synchronization Constraints (CRITICAL)

To prevent tracks from ending prematurely, desynchronizing, or playing at incorrect speeds, you MUST follow these timing rules with 100% mathematical precision:

### Rule A: Absolute Bar Length & Note Calculation

In standard 4/4 time, the total duration of notes/rests within 1 bar (delimited by `|`) MUST equal **16 sixteenth-note ticks (or 4 full quarter-note beats / 8 eighth-note ticks)**.
  * **Mathematical Accuracy First**: Prioritize exact duration totals over visual symmetry or pattern appearance.
  * **Default Length Awareness (`Ln`)**:
    * If `L16` is set, a 4/4 bar MUST contain exactly 16 sixteenth units.
    * If `L8` is set, a 4/4 bar MUST contain exactly 8 eighth units.
  * **Explicit Length Overrides**: When mixing default lengths with explicit numbers (e.g., `C4`, `F8.`), calculate the sum explicitly.

### Rule B: Inline Calculation Comments for Verification

When generating complex rhythms or mixing note lengths, you MUST include inline duration calculation comments at the end of measures or lines to prove bar length validity.
  * **Target Units**: 16 sixteenth ticks per bar (in 4/4 time).
  * **Example**:
    ```mml
    CH1: C4 D8 E8 G2 | ; 4+2+2+8 = 16 (16th-note ticks: OK!)
    CH1: C4. D8 E4   | ; 6+2+4 = 12 (ERROR: Less than 16 sixteenth ticks! Must fix!)
    ```

### Rule C: Loop Macro `[ ]N` Pre-Verification

Before wrapping a phrase in loop brackets `[ ... ]N`, extract a single measure from the interior and verify that its total note duration equals exactly 1 bar (16 sixteenth ticks). Never loop an incomplete or overflowing bar.

### Rule D: All Channels Bar Count & Duration Sync

* **Bar Count Parity**: All active channels (`CH1` through `CH8`) MUST contain the exact same total number of bars.
* **Ending Sync**: Calculate total playback duration in seconds for each channel. All channels MUST finish at the exact same millisecond. Never allow secondary channels to run out of notes early.

### Rule E: Self-Correction Loop

If any bar fails to sum to the target bar length (e.g., 16 sixteenth ticks in 4/4 time), you MUST automatically recalculate and adjust the note lengths before producing the final output.

### Rule F: Token Efficiency & Loop Macro Enforcement (CRITICAL)

To prevent text output limits from being exceeded during generation:
1. **Mandatory Use of Loop Bracket `[ MML_SEQUENCE ]N`**:
  * Repeated phrases, chord progressions, backing arpeggios, and drum patterns MUST be wrapped using loop brackets `[ ... ]N`.
  * NEVER expand loops manually line-by-line.
2. **Target Line Budget**:
  * A full 2-to-3 minute song MUST fit within **150 to 300 total lines** across all active channels.
  * At Tempo 96 (4/4 time), a 2.5-minute song only requires exactly **60 bars** of music.

### Rule G: Dynamic Song Length Calculation & Absolute Termination (MANDATORY)

To guarantee the generated MML matches the user's requested duration precisely and NEVER loops infinitely:

1. **Calculate Target Bar Count First**:
  Before generating MML code, calculate the total number of bars required using this exact formula:
  $$\text{Total Seconds} = \frac{60}{\text{Tempo (BPM)}} \times \text{Beats per Bar} \times \text{Total Bars}$$

  * *Example (Tempo 96, 4/4 Time, Target: 2.5 minutes / 150 seconds)*:
    * Seconds per Bar = $(60 / 96) \times 4 = 2.5$ seconds
    * Total Bars Needed = $150 / 2.5 = \mathbf{60\text{ bars}}$

2. **Length Control (Mandatory):**
  * Hard limit: Do not exceed target_bars + 4.
  * For pieces longer than 60 seconds, you MUST use loop constructs (`[ : ... : ]n`) for repeating sections. Unrolling the same 4-8 bar phrase more than twice is prohibited.
  * Aim for total MML source under 120 lines when possible. Compactness is a quality criterion.

3. **Distribute Structure to Fit Calculated Bar Count**:
  Divide the calculated total bars into logical song sections (Intro, A, B, Chorus, Outro).
  * *Example for 60 Bars*: Intro (4) $\rightarrow$ A (16) $\rightarrow$ B (16) $\rightarrow$ Chorus (16) $\rightarrow$ Outro (8) = 60 Bars.

4. **Strict Termination Flag**:
  * Once the exact calculated number of bars is output for each channel, the AI MUST terminate the MML output immediately.
  * NEVER generate continuous bar repetitions beyond the calculated limit.
  * Before outputting, verify total bars <= target. If the generation exceeds the limit, stop and redesign with more loops / fewer variations.
  * Never pad length with empty bars, near-silence, or mechanical repetition of the same phrase.

### Pre-Output Timing Checklist

1. [ ] Does every bar in 4/4 time equal exactly 16 sixteenth ticks (or 4 quarter beats)?
2. [ ] Did you count actual accumulated durations rather than visual note counts?
3. [ ] Are loop macro interiors verified for exact bar length?
4. [ ] Do all channels have identical total bar counts and finish at the same time?

---

## 5. Music Theory & Composition Guidelines

### A. Harmonic Alignment (60% Rule for Melody)

* For any given bar or chord duration, **at least 60% of the melody notes (CH1) duration MUST consist of chord tones** (1st, 3rd, 5th, or 7th intervals of the current chord).
* Use non-chord tones (passing tones, neighbor tones) for the remaining 40% duration to add expression without creating harsh dissonance.

### B. Suggested Chord Progressions (Degrees)

Use these Roman Numeral progressions as reference templates (Adapt as needed, do not strictly enforce if creative direction differs):

| Atmosphere | Progression (Degree) | Atmosphere | Progression (Degree) | Atmosphere | Progression (Degree) |
| --- | --- | --- | --- | --- | --- |
| `AbsoluteBanger` | `I - V/VII - VIm - IIIm/V - IV V - I` | `Flat7Sub_m5` | `IIm7 - IVm(b5)/V - I` | `Flat7Sub_Minor` | `IIm7 - IVm/V - I` |
| `SunnyAF` | `I/IV - Vsus4 - IIIm7 - V/VI` | `TwoStageChorus` | `IV - I - V - VIm - I V/VII - VIm V` | `Room335` | `IVmaj7 - IIIm7(#5) - IIm7 - IIIm7` |
| `Vibe70s` | `Imaj7 - bVImaj7 - IVm7 - bVII7` | `ClassicWest70s` | `IVmaj7 - IIIm7 - IIm7 - Imaj7` | `ClassicWest70s_v2` | `IVmaj7 - IIIm7 - IIm7 - IIIm7` |
| `BridgeToChorus` | `IV - I/III - IIm7 - Vsus4 V` | `B_MelodyVibe` | `IIm7 - VIm - IVM7 - Vsus4 V` | `B_MelodyVibe_v2` | `IIm7 - VIm - IVM7 - IIIsus4 III7` |
| `TwoFive_To_4` | `Vm7 - I7 - IV` | `JPopGold` | `IV - V - IIIm - VIm` | `JPopGold_Remix` | `IV - V/IV - III7 - VIm` |
| `JustTwoOfUs` | `IVmaj7-III7-VIm7-I7` | `KawaiiStructure` | `VIm7 - bVIm7 - Vm7 - I7` | `MyRevolution` | `I - VIm - IV - V` |
| `Smooth_RnB` | `IIm9 - V7 - IM7 - IVM7 - VIIm7-5 - III7 - VIm - VI7` | `TwoFive_To_6m` | `VIIm7 - III7 - VIm` | `YOASOBI_Vibe` | `IV - V - IIIm7 - VIm7 - IIm7 - III7 - VIm - Vm7 - I7` |
| `SuperLit` | `VIm - bIIIm(b5) - #IVm(b5) - III` | `AnisonCanon` | `I - VIIm7(b5) - III7 - VIm7 - Vm7 - I7 - IVmaj7 - IIIm7 - IIm7 - IV/V - V` | `AnisonGold` | `I - VIIm7(b5) - III7 - VIm7 - Vm7 - I7 - IVmaj7` |
| `AnisonHit` | `IV - V - bVI - bVII- I` | `EnnuiBabe` | `I - VI/I# - IIm - IVm - I/V - II/#IV - IV - V` | `YesterdayVibe` | `I - III - VIm - V` |
| `Classic1625` | `I - VIm - IIm - V` | `BestiesVibe` | `I - VIm - IV - V` | `Interstellar` | `IV - V - VIm - V` |
| `EpicPedal` | `I - bII/I - II/I - bIII/I` | `PureEmotional` | `IV - V - I - III` | `AllRounder` | `VIm - V - IV - V` |
| `ChicBabe` | `IVmaj7 - IIIm7 - VIm7 - I` | `MarusaChic` | `IVmaj7 - III7 - VIm7 - II7` | `ChillGoodnight` | `IVmaj7 - Imaj7 - III/#IV - IIIm/VI` |
| `TangoVibe` | `VIm - IIm - III - VIm` | `CanonClassic` | `I - V - VIm - IIIm - IV - I - IIm - V` | `CafeLofi` | `VIm9 - IIm7 - IIIm7` |
| `CrowdPleaser` | `I - IV - VIm - V` | `CatchyInterlude` | `I - V - I - V` | `CleanAesthetic` | `I/III - IV - V - VIm` |
| `ClassicalGrand` | `IVmaj7 #IVm(b5) - V6 bVIdim - VIm bVIIdim - VII - III` | `ClassicalSeeker` | `IIm7(b5) - bII/IV - IVm(b5)/VII - I` | `GameMelodyScent` | `IVmaj7 - IIIm7 - bIIImaj7 - IIm7` |
| `ClutchMoment` | `IV - V - I` | `FloatyChic` | `IIm7 - Imaj7 - bVIImaj7 - VIIm7(b5) - III7` | `PureSimple` | `VIm - V - IV - V` |
| `TheBlues` | `I7 - IV7 - I7 - IV7 - V7 - IV7 - I7 - V7` | `SouthernVibe` | `IIm9 - V7 - IIIm7 - VIm` | `SuspenseRise` | `VIm - IV/VI - #IVm(b5)/VI - VIm7` |
| `ChorusRush` | `VIm - V/VII - I - IIm - IIIsus4 - III` | `ChorusHit` | `I - III - IV - V - VIm (or I)で帰結` | `ChorusPower` | `I - V - IV - V` |
| `PreChorusRegular` | `IV - #IVm(b5) - V - bVIm(b5)` | `UnstoppablePassions` | `I - Iaug/#IV - IVmaj7 - V` | `CityPopVibe` | `VIm - I - IV - III` |
| `CinematicMood` | `IIm - VIm - I - V` | `JazzStandard_1` | `IIm7 - V7 - Imaj - Imaj` | `JazzStandard_2` | `IIm7 - V7 - Imaj - VI7` |
| `JazzStandard_3` | `Imaj - VIm7 - IIm7 - V7` | `JazzStandard_4` | `Imaj - I#o7 - IIm7 - V7` | `JazzStandard_5` | `Imaj - I7 - IVΔ - IVm7` |
| `JazzStandard_6` | `VIm7(b5) - IIm7 - V7 - Imaj` | `JazzStandard_7` | `IIm7(b5) - V7 - Im7 - Im7` | `JazzStandard_8` | `Im7 - V7 - Im7 - V7` |
| `JazzBasic` | `IIm7 - V7 - Imaj7 - VI7` | `SimpleIsBest` | `I - IV - V` | `SweetPrincess` | `I - VI/I# - IIm - IVm - I/V - II/#IV - IV - V` |
| `StylishMood` | `VIm9 - IIm7 - IIIm7` | `SpyAgent` | `VIm - IV/VI - #IVm(b5)/VI - VIm7` | `SpanishTrip` | `III - IV - V - IV` |
| `StandardTwoFive` | `IIm7 - V7 - I` | `DystopianWorld` | `VIm - VII - IIm - III` | `DramaPulse` | `IIm7 - I - VII - IIIsus4 III7` |
| `DramaPulse_v2` | `IIm7 - VIIm7-5 - IIIsus4 - III7` | `DorianMode` | `IIm - IIIm/II - IV/II - IIIm/II` | `DorianProof` | `IIIm/II - IIm` |
| `DressCodeFormal` | `IVmaj7 - Iaug/bVII - IIIm7/VI - II/#IV` | `NaturalDaily` | `I - IIm7 - I/III - IV` | `SmoothCanon` | `I - V/VII - VIm - IIIm/V - IV - I/III - IIm - V` |
| `AiryVibe` | `I - IIIm/VII - VIm - IV` | `PartyTune` | `I - IV - V - IV` | `PirateQuest` | `VIm - IIm - III - VIm` |
| `HouseGroove` | `IIm7/V - IIIm7/VI` | `BackdoorTwoFive` | `IVm7 - bVII7 - I` | `HappyVibes` | `VIm7 - II7 - IV/V - I` |
| `ParallelWorld` | `VI - IV - IIm - III` | `BaroqueSequence` | `VIm - IIm - V - I - IV - VIIm(b5) - III` | `BaroqueClassic` | `VIm - IIm - V - I - IV - VIIm(b5) - III` |
| `HitChartBanger` | `I - IV - V - I` | `BillboardTop` | `VIm - I - V - IV` | `FantasyWorld` | `VIm - II - IV - V` |
| `FusionSub` | `IIm7 - IV/V - I` | `BlackadderSub` | `IIm7 - IVaug/V - I` | `BluesyFeel` | `I7 - IV7 - I7 - IV7 - V7 - IV7 - I7 - V7` |
| `Blues12Bar` | `I7 - I7 - I7 - I7 - IV7 - IV7 - I7 - I7 - V7 - IV7 - I7 - I7` | `DeepBassLine` | `I - Iaug - VIm/I - I7` | `PedalRise_1` | `I - bII/I - II/I - bIII/I - III/I` |
| `PedalRise_2` | `I - IIm/I - IIIm/I - IV/I - Vsus4/I - V` | `PedalRise_3` | `I - V/I - IV/I - bVI/I - bVII/I` | `HolyTexture` | `VIm - V/VII - V - I - IV - VIIm7(b5) - III7 - III7/#VI` |
| `Pops_1` | `I - V - VIm - IV` | `Pops_2` | `I - IV - V - I` | `Pops_3` | `I - IV - Vsus4 - V` |
| `Pops_4` | `I - VIm - IIm - V` | `Pops_5` | `I - IIm - IV - V` | `Pops_6` | `I - V/VII - VIm - V` |
| `Pops_7` | `VIm - IIm - III - VIm` | `Pops_8` | `VIm - I - IIm - IIIm` | `PopPunkBanger` | `I - V - VIm - IV` |
| `MixolydianFlow` | `V - IV - I` | `MixolydianSpace` | `V - IIm - VIm - V` | `MysteryDrama` | `VIm - VIm - IV7 - III7` |
| `MysteryNovel` | `VIm - IV7 - III7` | `MellowOudou` | `IVmaj7 - V7/IV - IIIm7 - VIm7` | `ModernMetal` | `VI5add9 - IV5add9 - bIII5add9 - I5add9` |
| `MonochromeCanon` | `I - VIIm7(b5) - III7 - VIm - V` | `EurobeatEnergy` | `IV - V - VIm` | `ClimaxRush` | `VIm - III7/#VI - IIIm/V - II/#IV - IV - I/III - IIm7 - Vsus4 V - I` |
| `FantasyGhibli` | `VIm - V - IV - IIIm - IIm - VIm/I - VII7 - III7 - VIm` | `LoveStory` | `I - IV - IIIm - VIm` | `RhythmAndBlues` | `Imaj7 - bVImaj7 - IVm7 - bVII7` |
| `LydianBright` | `IV - V/IV` | `RelaxChillin` | `I - IIm7 - I/III - IV` | `LoopDrive` | `IIm7 - IIIm7 - IIm7 - IIIm7` |
| `LoopDrive_v2` | `IIm7 - VIm7 - IIm7 - VIm7` | `RareCharacter` | `IVmaj7 - IIIm7 - bIIIdim7 - IIm7` | `RockDrive_1` | `I - VIm - IV - V` |
| `RockDrive_2` | `I - IV - I - V` | `RockDrive_3` | `I - I - bIII - IV` | `RockDrive_4` | `I - III - IV - IVm` |
| `RockDrive_5` | `IIm - I - V - bVII` | `RockDrive_6` | `V - V - IV - I` | `RockDrive_7` | `VIm - IV - I - V` |
| `RockDrive_8` | `VIm - III7 - II - V7` | `RockVocalist` | `IVmaj7 - V7/IV - IIIm7/V - VIm7` | `RomanceMelody` | `IV - V - III7 - VIm` |
| `RomanticNight` | `I - IMaj7/VII - I7/bVII - VI7 - IIm - I#aug - IIm7/I - V` | `NostalgicEuro` | `IIm7 - V7 - IIIm7 - VIm` | `LiveForLove` | `I - VIIm7(b5) /II - III7 - VIm7 - V` |
| `SurpriseTwist` | `I - V - bVII - IV - bVI - I - II - V` | `IsekaiFantasy` | `VIm - II - IV - V` | `FirstStarReborn` | `IVmaj7 - IIIm7 - VIm7 - I` |
| `SciFiSpace` | `VIm - Im - VIm - IVm` | `HeroicEpic` | `VIm - III/#VI - VI7/V - IIm - IV - IIIsus4 III` | `FlameBreath` | `VIm - V - IV - I` |
| `GlobalHit` | `I - IV - VIm - V` | `OudouClassic` | `IV - V - IIIm - VIm` | `MyFavoriteBanger` | `VIm - #IVm7(b5) - IVmaj7 - IIm7 - IIIm7` |
| `WarmHalfStepRise` | `I - Iaug - VIm/I - I7` | `KachouFugetsu` | `IV6 - V6 - VI7sus4 - IIIsus4` | `GorgeousMelody` | `I - III/VII - VIm - V - IV - IIIm - IIm` |
| `SalvationRise` | `IV - V - VI` | `OuterSpaceJourney` | `VIm - bIIIm - VIm - IVm - VIm - bIIIm - bVIIm - IIm - #IVm` | `RevolutionPulse` | `VIm - IV/VI - VIm - VII7/VI - III/#VI - IIIm(b5)/V - II/#IV - IIm/IV - VI/III` |
| `InterludeSpecial` | `VIm - IIm7 - IV - V` | `MarusaLoop` | `IVmaj7 - III7 - VIm7 - I7` | `MarusaLoop_v2` | `IVmaj7 - III7 - VIm7 - Vm7 I7` |
| `MarusaLoop_v3` | `IVmaj7 - III7 - VIm7 - II7` | `RareSpecies` | `IIIm - IV - VIm - I` | `HypeBuildUp` | `VIm - IIIm/V - IV V - I` |
| `YourTrueForm` | `VIm - IIm7 - IV - V` | `CyberFuture` | `VIm - V/VI - IV/VI - IIIm/VI` | `MoonlightShine` | `VIm - III/#VI - VI7/V - IIm/IV - IV7 - III/#VI` |
| `UnreachableSky` | `IV - II/#IV - Vsus4 V - VIsus4 VI - IIsus4 II` | `MiragePhantom` | `IVmaj7 - VIIm7(b5)/IV - IIIm7 - IIIdim7 - IIm7 - V7/II - Imaj7 - I6` | `Phantasmagoric` | `I - bVII - bVI - bVII` |
| `AutumnLeaves` | `IIm7 - V7 - Imaj7 - IVmaj7 - VIIm7(b5) - III7 - VIm7` | `2AM_Crossing` | `Iadd9 - VIm7 - V - IV` | `DeepRegret` | `IIm - VIm/I - VIIm7(b5) - III7` |
| `HeartPounding` | `IV - #IVdim - V - bVIdim - VIm` | `HighClassElegance` | `Imaj7 - I#dim7 - IIm7 - V7/II` | `ToughProgress` | `VIm - V/VII - I - IIm - IIIsus4 - III` |
| `SweetSugar` | `IV - VIm - IIm - I` | `UltimateBanger` | `IV - V - VIm - VIm - V - IV` | `FinalHit` | `VIm - V - IV - I` |
| `RadiantShine` | `I - V - bVII - IV - bVI - I - II - V` | `CircularLoop` | `I-VIm-IIm-V7` | `StepwiseDescending` | `VIm - V - IV - IIIm - IIm - I` |
| `RunUpStart` | `IIm7 - IIIm7 - IVmaj7 - V` | `KomuroDynamite` | `VIm - IIm - V - I` | `KomuroClassic` | `VIm - IV - V - I` |
| `KomuroClassic_v2` | `VIm - IV - V - I V/VII - VIm` | `KomuroClassic_v3` | `VIm - IIm - V - I` | `TimelessBanger` | `I - V - IV - V` |
| `FieryPassion` | `VIm - VII/VI - VIIm(b5)/VI - VIm - I/V - #IVm(b5) - IV7(b5) - III7` | `ForwardDrive` | `I - bVII - bVI - bVII` | `FinallyFree` | `VIm - III7/#VI - IVmaj7 - IIm9 - Vsus4` |
| `OneWorld` | `Isus4 - Isus4/bII - Isus4/bIII - Isus4/IV - Isus4/V` | `HypeRise` | `IIm7 - IIIm7 - IVM7 - V` | `HypeRise_v2` | `IIm7 - IIIm7 - IVM7 - II/#IV - Vsus4 V` |
| `YouthfulDays` | `I - III - VIm - V` | `NostalgiaTrigger` | `VIm - IIIm - IV - V - I` | `MajesticGrand` | `Isus4 - Isus4/bII - Isus4/bIII - Isus4/IV - Isus4/V` |
| `BeyondAtmosphere` | `IIm7 - IIIm7 - IVm7 - Vm7` | `GrandFinale` | `I - I/III - Isus4/IV - Isus4/V` | `ChaserOudou` | `IVmaj7 - bVII7 - IIIm7 - IIIdim7/VI` |
| `ClassicBassChromatic` | `VIm - bVIaug - I/V - #IVm7(b5)` | `CyberGirl` | `VIm7 - bVIm7 - Vm7 - I7` | `GrandOpening` | `VIm - V/VI - IV/VI - IIIm/VI` |
| `UrbanAesthetic` | `VIm7 - II7 - IV/V - I` | `OrientalMystery` | `IV6 - V6 - VIsus4 - IIIsus4` | `SpecialMarusa` | `VIm - I - IV - III` |
| `EnemyWithin` | `IV - VIm - Im - V/II - bVIIm/bII - IV/I - VIIdim7 - III7/#VI` | `PathosGrief` | `VIm - VII - IIm - III` | `FlyingGirl` | `IV - V - VI` |
| `BeautifulCanon` | `I - V/VII - VIm - IIIm/V - IV - I/III - IIm - V` | `NightParade` | `IIIsus4addb9 - IIIsus4addb9/IV - IIIsus4addb9/II - IIIsus4addb9` | `SuddenBittersweet` | `IV - V - I - III` |
| `AntiOrdinary` | `#IVm7(b5) - IVmaj7 - IIIm7 - VIm7` | `FloatingVibe` | `I - I/III - Isus4/IV - Isus4/V` | `MasqueradeBall` | `VIm - VII/VI - VIIm(b5)/VI - VIm - I/V - #IVm(b5) - IV7(b5) - III7` |
| `TwoFive_To_RelativeMinor` | `VIIm7(b5) - III7 - VIm` | `HeiseiBalladWeapon` | `IIIm7 - VIm7/III - IIm7 - V7/II` | `KomeKomeLoop` | `IIm7 - V7 - IM7 - VIm7 - bVI7 - IIm7/V - V7 - I` |
| `J_PopPunk` | `IV - I - V - VIm` | `OurFuture` | `I - IIIm/VII - Vm7/bVII - VI7 - IIm - I#aug - IV/I - V7/VII` | `AllPurposeSeasoning` | `IV - V - VIm - I` |
| `BittersweetLove` | `I - V - VIm - IV` | `SunlightFiltered` | `IVmaj7 - IVmmaj7 - IIIm7 - Vm7/VI` | `ElegantPassingDim` | `Imaj7 - I#dim7 - IIm7 - V7` |
| `PlayfulVibe` | `I - V/I - IV/I - bVI/I - bVII/I` | `WesternChartHit` | `IV - I - V - I` | `WesternStyle` | `VIm - I - V - IV` |
| `WesternPopPunk` | `VIm - IV - I - V` | `WesternStandard` | `VIm - IV - I - V` | `TritoneSub` | `IIm7 - bII7 - I` |
| `TearsFalling` | `IV - V - bVIdim - VIm` | `TearjerkerWeapon` | `IV - V - bVIm(b5) - VIm` | `PowerOfLove` | `I - IIIm/VII - VIm - IV` |
| `SparklingShine` | `I - IVm6/I` | `PureBeauty` | `IVmaj7 - VIIm7(b5)/IV - IIIm7 - IIIdim7 - IIm7 - V7/II - Imaj7 - I6` | `VioletTwoFiveCombo` | `I - IIIm7(b5) - VI7 - IIm7 - VIIm7 - III7` |
| `Soca_TropicalParty` | `I - IV - V - IV` | `Soca_TwoCordDrive` | `I - V` | `Soca_BahiaAnthem` | `I - bVII - IV - I` |
| `Soca_AmazonToada` | `VIm - IV - V - VIm` | `Soca_PagodeDrive` | `I - VIm - IIm - V` | `Soca_CarnivalRise` | `IV - V - I - VIm` |

---

## 6. Scale Reference

By using only the notes belonging to each scale below, you can create music with various unique atmospheres. Please use this as a reference.

### 6.1 Basic Scales & Church Modes

| English Name | Scale Degrees | English Name | Scale Degrees | English Name | Scale Degrees |
| --- | --- | --- | --- | --- | --- |
| `Major Scale / Ionian Mode` | `1, 2, 3, 4, 5, 6, 7` | `Natural Minor Scale / Aeolian Mode` | `1, 2, b3, 4, 5, b6, b7` | `Harmonic Minor Scale` | `1, 2, b3, 4, 5, b6, 7` |
| `Melodic Minor Scale` | `1, 2, b3, 4, 5, 6, 7` | `Dorian Mode` | `1, 2, b3, 4, 5, 6, b7` | `Phrygian Mode` | `1, b2, b3, 4, 5, b6, b7` |
| `Lydian Mode` | `1, 2, 3, #4, 5, 6, 7` | `Mixolydian Mode` | `1, 2, 3, 4, 5, 6, b7` | `Locrian Mode` | `1, b2, b3, 4, b5, b6, b7` |

### 6.2 Harmonic & Melodic Minor Derived Scales

| English Name | Scale Degrees | English Name | Scale Degrees | English Name | Scale Degrees |
| --- | --- | --- | --- | --- | --- |
| `Locrian natural 6 Scale` | `1, b2, b3, 4, b5, 6, b7` | `Ionian #5 Scale` | `1, 2, 3, 4, #5, 6, 7` | `Dorian #4 Scale` | `1, 2, b3, #4, 5, 6, b7` |
| `Phrygian Dominant (H.M. P5 Below)` | `1, b2, 3, 4, 5, b6, b7` | `Lydian #2 Scale` | `1, #2, 3, #4, 5, 6, 7` | `Super Locrian b7 Scale` | `1, b2, b3, b4, b5, b6, bb7` |
| `Dorian b2 Scale` | `1, b2, b3, 4, 5, 6, b7` | `Lydian #5 Scale / Lydian Augmented` | `1, 2, 3, #4, #5, 6, 7` | `Lydian b7 Scale / Acoustic Scale` | `1, 2, 3, #4, 5, 6, b7` |
| `Mixolydian b6 Scale` | `1, 2, 3, 4, 5, b6, b7` | `Locrian natural 2 Scale / Half-Diminished` | `1, 2, b3, 4, b5, b6, b7` | `Super Locrian Scale / Altered Scale` | `1, b2, b3, b4, b5, b6, b7` |

### 6.3 Symmetrical, Pentatonic & Special Scales

| English Name | Scale Degrees | English Name | Scale Degrees | English Name | Scale Degrees |
| --- | --- | --- | --- | --- | --- |
| `Whole Tone Scale` | `1, 2, 3, #4, #5, #6` | `Diminished Scale (Half-Whole)` | `1, b2, b3, 3, #4, 5, 6, b7` | `Diminished Scale (Whole-Half)` | `1, 2, b3, 4, b5, b6, 6, 7` |
| `Chromatic Scale` | `1, #1, 2, #2, 3, 4, #4, 5, #5, 6, #6, 7` | `Symmetrical Augmented Scale` | `1, b3, 3, 5, #5, 7` | `Major Pentatonic Scale` | `1, 2, 3, 5, 6` |
| `Minor Pentatonic Scale` | `1, b3, 4, 5, b7` | `Blues Scale` | `1, b3, 4, b5, 5, b7` | `Bebop Dominant Scale` | `1, 2, 3, 4, 5, 6, b7, 7` |
| `Prometheus Scale` | `1, 2, 3, #4, 6, b7` | `Enigmatic Scale` | `1, b2, 3, #4, #5, #6, 7` | `Tritone Scale` | `1, b2, 3, b5, 5, b7` |
| `Harmonic Major Scale` | `1, 2, 3, 4, 5, b6, 7` | `Major Locrian Scale` | `1, 2, 3, 4, b5, b6, b7` | `Neapolitan Major Scale` | `1, b2, b3, 4, 5, 6, 7` |
| `Neapolitan Minor Scale` | `1, b2, b3, 4, 5, b6, 7` |  |  |  |  |

### 6.4 Japanese Traditional & Modern Scales

| English Name | Scale Degrees | English Name | Scale Degrees | English Name | Scale Degrees |
| --- | --- | --- | --- | --- | --- |
| `Ryosenpou` | `1, 2, 3, 5, 6` | `Ritsusenpou` | `1, 2, 4, 5, 6` | `Yousenpou / Inakabushi` | `1, 2, 4, 5, b7` |
| `Insenpou / Miyakobushi / Insen` | `1, b2, 4, 5, b7` | `Ryukyu Scale` | `1, 3, 4, 5, 7` | `Yona Nuki Major Scale` | `1, 2, 3, 5, 6` |
| `Yona Nuki Minor Scale` | `1, 2, b3, 5, b6` | `Niro Nuki Major Scale` | `1, b3, 4, 5, b7` | `Niro Nuki Minor Scale` | `1, 3, 4, 5, 7` |
| `Kumoi Scale` | `1, 2, b3, 5, 6` | `Iwato Scale` | `1, b2, 4, b5, b7` | `Hirajoshi Scale` | `1, 2, b3, 5, b6` |

### 6.5 World Ethnic Scales

| English Name | Scale Degrees | English Name | Scale Degrees | English Name | Scale Degrees |
| --- | --- | --- | --- | --- | --- |
| `Gong Mode (Chinese Scale)` | `1, 2, 3, 5, 6` | `Shang Mode (Chinese Scale)` | `1, 2, 4, 5, b7` | `Jiao Mode (Chinese Scale)` | `1, b3, 4, b6, b7` |
| `Zhi Mode (Chinese Scale)` | `1, 2, 4, 5, 6` | `Yu Mode (Chinese Scale)` | `1, b3, 4, 5, b7` | `Gypsy Scale / Hungarian Gypsy` | `1, b2, 3, 4, 5, b6, 7` |
| `Spanish Scale / Flamenco Scale` | `1, b2, 3, 4, 5, b6, b7` | `Hungarian Scale / Hungarian Minor` | `1, 2, b3, #4, 5, b6, 7` | `Scottish Scale` | `1, 2, 3, 5, 6` |
| `Pelog Scale` | `1, b2, b3, 5, b6` | `Bilaval Thaat` | `1, 2, 3, 4, 5, 6, 7` | `Khamaj Thaat` | `1, 2, 3, 4, 5, 6, b7` |
| `Kafi Thaat` | `1, 2, b3, 4, 5, 6, b7` | `Asavari Thaat` | `1, 2, b3, 4, 5, b6, b7` | `Bhairav Thaat` | `1, b2, 3, 4, 5, b6, 7` |
| `Bhairavi Thaat` | `1, 2, b3, 4, 5, b6, b7` | `Kalyan Thaat` | `1, 2, 3, #4, 5, 6, 7` | `Marwa Thaat` | `1, b2, 3, #4, 5, 6, 7` |
| `Poorvi Thaat` | `1, b2, 3, #4, 5, b6, 7` | `Todi Thaat` | `1, b2, b3, #4, 5, b6, 7` | `Maqam Rast` | `1, 2, b3 (Quarter Tone), 4, 5, 6, b7 (Quarter Tone)` |
| `Maqam Nahawand` | `1, 2, b3, 4, 5, b6, 7` | `Maqam Nawa Athar` | `1, 2, b3, #4, 5, b6, 7` | `Algerian Scale` | `1, 2, b3, #4, 5, b6, 7` |
| `Double Harmonic / Byzantine / Arabic` | `1, b2, 3, 4, 5, b6, 7` |  |  |  |  |

---

## 7. Song Cadence Patterns

Refer to the following techniques when creating the ending section of a song.

* To create the feeling that the song is coming to an end, it is essential to establish a sense of finality. Consider using the following methods:
  * **Authentic Cadence**
    * Progression: Dominant ($V$ or $V_7$) to Tonic ($I$)
    * Characteristics: Provides the strongest sense of stability. It functions like a period (.) at the end of a sentence, clearly signaling to the listener that the song has concluded.
  * **Half Cadence**
    * Progression: Tonic (or other chords) pausing on the Dominant ($V$)
    * Characteristics: While it creates a temporary pause, it leaves a floating, unresolved feeling. It acts like a comma (,) in a sentence, building anticipation for what comes next.
  * **Plagal Cadence**
    * Progression: Subdominant ($IV$) to Tonic ($I$)
    * Characteristics: Commonly known as the "Amen Cadence" used in church music, it delivers a gentle, soft, and soothing resolution.
  * **Deceptive Cadence**
    * Progression: Dominant ($V$) to a chord other than the Tonic (typically $VI$)
    * Characteristics: Just when the listener expects a resolution, it subverts expectations by moving to a different chord, creating a dramatic effect that suggests the music is still continuing.

Additionally, sustaining the final note for a longer duration strongly reinforces the feeling that the song has ended.
Conversely, when creating loopable tracks, maintaining shorter notes until the end without following these cadence patterns ensures a smooth and natural transition when the song seamlessly loops back to the beginning.

---

## 8. Various Techniques for Song Composition

* To avoid creating a monotonous song, it is not recommended to have consecutive, adjacent notes of the same duration for more than four measures.
* In music for scenes such as battles, you can convey a sense of tension by making the melody’s pitch fluctuations more dramatic and increasing the tempo. Consider making extensive use of sixteenth notes and thirty-second notes and a tempo of 130 BPM or higher.
* In music for horror scenes or dungeons, you can express tension and anxiety by deliberately incorporating a greater number of dissonant chords.
* It is not recommended to structure a piece entirely as multiple repetitions of the same pattern from start to finish, as this leads to monotony. Try to avoid monotony by, for example, repeating the same phrase twice, inserting a different phrase once, and then returning to the original phrase.
* For tracks set in towns or open fields, music with a sense of expansiveness is preferred. It's best to create a refreshing atmosphere by letting each note ring out a bit longer. In the case of field music, there tends to be a preference for pieces that sound like marches in 2/4 time.
* **MANDATORY** It is not acceptable for an entire track to consist solely of a single looped phrase across all channels. For example, a 1.5-minute song in which all channels repeat the same phrase three times is, in effect, only a 30-second song. Be sure to introduce variations in some part of the track-such as the melody or accompaniment-to avoid having the entire song consist of nothing but repetitions of the exact same phrase.
* When composing music that evokes a sense of vastness-such as the sky or the ocean-it is particularly important to vary the duration of the notes. Avoid pieces that consist solely of a continuous sequence of quarter notes. You can also create a sense of grandeur with a slow tempo, such as one at 100 BPM or below.
* When creating a mysterious track, using sustained sounds like `@52` Choir Aahs, `@53` Voice Oohs, `@50` Synth Strings, and `@98` Crystal with longer note durations can really set the mood.

---

## 9. Duration Calculation & Target Lengths

* **Calculation Formula**:
  * $\text{Duration of 1 Beat (Quarter Note)} = \frac{60}{\text{BPM}} \text{ seconds}$
  * At `T120`, a 4/4 bar (4 quarter notes) = **2.0 seconds**.
  * A 2-minute (120 seconds) song at `T120` requires **60 bars** of music.
* Use the loop macro `[ ... ]N` efficiently to build verse/chorus repetitions and achieve requested target durations accurately.

---

## 10. Output Format & Execution Role Rules (CRITICAL)

### Single Code Block Constraint
ALWAYS output the ENTIRE MML content inside a **SINGLE code block**. Do NOT split channels into separate blocks or files. Write CH1, CH2, CH3, and CH4 consecutively in one unified text.

* Start the MML with a comment stating the calculated length:
  `; Target: XX bars @ Tnn ~= M:SS`

### Boilerplate Example (Short BGM Template)

```mml
; ============================================
; pisstrak Sample BGM - "Upbeat Town" (T128)
; ============================================

; --- CH1: Lead Melody ---
CH1: T128 O5 V14 @0 L8
CH1: C D E F G4 E4 | A4 F4 G2 | F E D C < B4 > D4 | C2. R4
CH1: C E D F G4 E4 | F4 A4 G2 | D E F C < B4 > D4 | C2. R4

; --- CH2: Accompaniment Arpeggio ---
CH2: T128 O4 V10 @24 L8
CH2: [ C E G E C E G E | F A > C < A F A > C < A | G B > D < B G B > D < B | C E G E C4 R4 ]2

; --- CH3: Bassline ---
CH3: T128 O3 V12 @33 L4
CH3: [ C R C R | F R F R | G R G R | C R C2 ]2
```

### Rule A: Primary Output Contract (Chat AI Mode)
* **If you are acting as a Chat AI (Interactive Assistant):**
  * **ALWAYS output ONLY the raw MML text block.**
  * **DO NOT attempt to render, compile, generate, or attach audio files (`.wav` / `.ogg`).**
  * The user will take your generated MML text and feed it into `pisstrak` on their local machine. Outputting raw text is your 100% complete and final deliverable.

### Rule B: Autonomous Pipeline Executions (Agentic AI Mode)
* **If you are acting as an Autonomous Agent (with direct CLI tool execution access):**
  * Generate the MML text content first.
  * Execute `pisstrak <input.mml> <output.ogg>` directly via CLI to render the audio file into the project asset directory.

---

## 11. Quick Start & Render Command Reference (For Assistant AI)

If the user asks how to render, play, or convert the generated MML file (e.g., "How do I render this?", "How to convert to WAV?"), provide the following `pisstrak` command-line instructions directly to the user.

```bash
pisstrak <input.mml> [output.wav|output.ogg] [tail_seconds] [soundfont.sf2]
```

* *Example:* `pisstrak mymusic.mml mymusic.ogg 2.5 mysoundfont.sf2`
* *Parameters:*
  * `<input.mml>`: Input MML score file.
  * `[output.wav|output.ogg]`: Output audio file path (Supports both `.wav` and `.ogg`).
  * `[tail_seconds]`: Extra fadeout/decay duration in seconds appended to the end of the rendered track (e.g., `2.5` adds 2.5s tail padding). If omitted (default `0`), the audio cuts off precisely at the final beat, which is ideal for seamless looping BGM tracks.
  * `[soundfont.sf2]`: SoundFont file for rendering (Defaults to `soundfont.sf2` if omitted).
