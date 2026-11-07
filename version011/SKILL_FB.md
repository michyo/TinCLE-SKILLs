# SKILL_FB.md - fartbox Integration & Synthesis Talent Chip Version 0.11

## 1. Overview & Philosophy

### Tool Identity

`fartbox` (Fast Audio Rendering Tool) is a 1-shot procedural sound effect generator designed for the TinCLE ecosystem. It takes text-based synth parameters (`.fart` files) or CLI arguments and renders uncompressed, high-fidelity 16-bit 44.1kHz WAV files in milliseconds.

---

## 2. CLI Command Specification

`fartbox` provides three core operational workflows via command-line flags:

### Pattern A: Preset Generation & Parameter Export

Generates a sound based on a named preset algorithm, outputs the WAV file, and optionally saves the generated parameters to a `.fart` text file for future editing.

```bash
fartbox -t <preset_name> -o <output.wav> [-save <output.fart>] [-s <seed_number>]
```

* `-t <preset_name>`: Specifies the sound preset generator.
* `-o <output.wav>`: Output target WAV file path.
* `-save <output.fart>`: (Optional) Saves the randomized parameters of the generated preset to a text file.
* `-s <seed_number>`: (Optional) Integer seed for reproducible pseudo-random generation.

### Pattern B: Direct Synthesis from Parameter File (`.fart`)

Reads an existing `.fart` parameter text file and renders it directly into a WAV file. This is the primary method for AI agents to write custom audio parameters.

```bash
fartbox -c <input.fart> -o <output.wav>
```

* `-c <input.fart>`: Source `.fart` parameter configuration file.
* `-o <output.wav>`: Output target WAV file path.

### Pattern C: Mutation Workflow

Loads a `.fart` parameter file, applies slight random variations (mutations) to the active parameters, renders the mutated WAV, and optionally saves the new parameters.

```bash
fartbox -c <input.fart> -m -o <output.wav> [-save <mutated.fart>] [-s <seed_number>]
```

* `-c <input.fart>`: Base parameter file to mutate.
* `-m`: Enables mutation mode.
* `-o <output.wav>`: Output target WAV file path for mutated sound.
* `-save <mutated.fart>`: (Optional) Saves the newly mutated parameters.
* `-s <seed_number>`: (Optional) Seed controlling the mutation variance.

---

## 3. Preset Types Reference

The following preset identifiers can be passed to the `-t` option:

* `coin` / `pickup`: Short, high-pitched arpeggiated tones suited for item collection or scoring.
* `laser` / `shoot`: Frequency-sweeping downward tones for projectiles and energy weapons.
* `explosion`: Noise-based low-frequency rumble with pitch drop and distortion.
* `powerup`: Rising pitch sweeps with vibrato or arpeggiation for enhancements.
* `hit` / `hurt`: Short, impactful noise or square waves for damage feedback.
* `jump`: Upward frequency slides for character locomotion.
* `blip` / `select`: Extremely short, high-frequency tones for UI interaction.
* `random`: Unconstrained parameter randomization for abstract or unusual sound effects.

## 4. `.fart` Parameter Reference

The `.fart` parameter file is a plain-text key-value configuration file containing all synthesis parameters required by the `fartbox` synth core. Each line consists of `parameter_name = float_value`. Comments starting with `#` are ignored.

All parameters accept floating-point numbers. The valid parameter keys and their ranges/effects are detailed below:

### Waveform Selection

* `wave_type` (Integer: 0, 1, 2, 3)
  * `0`: Square / Pulse wave (classic retro 8-bit chip synth).
  * `1`: Sawtooth wave (harsh, rich harmonic spectrum).
  * `2`: Sine wave (pure fundamental tone, smooth).
  * `3`: White Noise wave (percussive sounds, explosions, impacts).

### Pitch & Frequency

* `p_base_freq` (Float: 0.0 to 1.0)
  * Primary synthesis frequency (pitch). Higher values yield higher tones.
* `p_freq_limit` (Float: 0.0 to 1.0)
  * Lower cutoff limit for frequency sweeps. If a downward frequency sweep hits this limit, generation terminates.
* `p_freq_ramp` (Float: -1.0 to 1.0)
  * Frequency slide rate. Negative values slide pitch down (lasers, hits); positive values slide pitch up (jumps, powerups).
* `p_freq_dramp` (Float: -1.0 to 1.0)
  * Acceleration of the frequency slide. Controls non-linear pitch curving.

### Pulse Width / Duty Cycle (Square Wave Only)

* `p_duty` (Float: 0.0 to 1.0)
  * Pulse width modulation for square waves (`wave_type = 0`). Controls timbre thickness.
* `p_duty_ramp` (Float: -1.0 to 1.0)
  * Sweeps the pulse width over time, introducing dynamic harmonic motion.

### Pitch Vibrato

* `p_vib_strength` (Float: 0.0 to 1.0)
  * Pitch modulation depth (vibrato intensity).
* `p_vib_speed` (Float: 0.0 to 1.0)
  * Modulation frequency / speed of vibrato.
* `p_vib_delay` (Float: 0.0 to 1.0)
  * Delay before vibrato modulation engages.

### ADSR Envelope

* `p_env_attack` (Float: 0.0 to 1.0)
  * Attack time. 0.0 provides instant impact; higher values create a fade-in.
* `p_env_sustain` (Float: 0.0 to 1.0)
  * Hold time at peak amplitude.
* `p_env_decay` (Float: 0.0 to 1.0)
  * Release / decay duration. Controls overall sound length.
* `p_env_punch` (Float: 0.0 to 1.0)
  * Initial volume boost during attack phase, adding punch to impacts.

### Low-Pass Filter (LPF)

* `p_lpf_freq` (Float: 0.0 to 1.0)
  * LPF cutoff frequency. 1.0 disables filter; lower values muffle the sound.
* `p_lpf_ramp` (Float: -1.0 to 1.0)
  * Cutoff frequency sweep over time.
* `p_lpf_resonance` (Float: 0.0 to 1.0)
  * Resonance multiplier near the cutoff frequency, adding squelch or metallic ringing.

### High-Pass Filter (HPF)

* `p_hpf_freq` (Float: 0.0 to 1.0)
  * HPF cutoff frequency. Removes bass frequencies. Higher values result in thinner sounds.
* `p_hpf_ramp` (Float: -1.0 to 1.0)
  * HPF Cutoff sweep over time.

### Phaser Effect

* `p_pha_offset` (Float: -1.0 to 1.0)
  * Phase cancellation offset, creating jet-engine or swooshing effects.
* `p_pha_ramp` (Float: -1.0 to 1.0)
  * Phase shift speed and direction.

### Arpeggio & Repeat

* `p_repeat_speed` (Float: 0.0 to 1.0)
  * Triggers automatic re-attatck of the sound at specified intervals (stutter effect).
* `p_arp_speed` (Float: 0.0 to 1.0)
  * Speed of two-note pitch interval jumping.
* `p_arp_mod` (Float: -1.0 to 1.0)
  * Pitch interval for arpeggiation. Positive jumps pitch up (e.g. coin effect); negative drops pitch.

---

## 5. AI Workflow Guidelines

When an AI agent needs to generate sound assets for a TinCLE project, it must adhere to the following decision tree:

### Step 1: Initial Prototype Phase

Always start by generating a baseline audio asset using a standard preset. Save the text configuration (`.fart`) alongside the WAV file so parameters can be inspected or modified later.

```bash
fartbox -t laser -o assets/sfx/laser.wav -save assets/sfx/laser.fart
```

### Step 2: Variation Generation (Mutation)

If multiple distinct sound variations are required (e.g., subtle variations of footstep or explosion sounds), load the base `.fart` file and execute mutation mode.

```bash
fartbox -c assets/sfx/explosion_base.fart -m -o assets/sfx/explosion_var01.wav -save assets/sfx/explosion_var01.fart -s 101
fartbox -c assets/sfx/explosion_base.fart -m -o assets/sfx/explosion_var02.wav -save assets/sfx/explosion_var02.fart -s 102
```

### Step 3: Precision Manual Tuning

When specific sound design constraints are requested (e.g., "Make the laser decay longer" or "Make the explosion lower pitched"):

1. Do NOT re-run randomized presets.
2. Open and inspect the existing `.fart` parameter file.
3. Modify specific parameters directly:
  * To lengthen decay: Increase `p_env_decay`.
  * To lower pitch: Decrease `p_base_freq`.
  * To add crunch/punch: Increase `p_env_punch` or adjust `p_lpf_resonance`.
4. Re-render the audio directly from the edited `.fart` file:
  ```bash
  fartbox -c assets/sfx/laser.fart -o assets/sfx/laser.wav
  ```

### Rule A: Primary Output Contract (Chat AI Mode)
* **If you are acting as a Chat AI (Interactive Assistant without direct CLI access):**
  * **ALWAYS output ONLY the raw `.fart` text parameter block.**
  * **DO NOT attempt to render, compile, generate, or attach audio files (`.wav`).**
  * The frontend client environment (e.g., mobile chat apps) may fail to display or send rendered binary audio attachments, causing complete response silences.
  * The user will take your generated `.fart` text configuration and feed it directly into `fartbox` on their local machine. Outputting clean, copyable text parameters is your 100% complete and final deliverable.

### Rule B: Autonomous Pipeline Executions (Agentic AI Mode)
* **If you are acting as an Autonomous Agent (with direct CLI execution access):**
  * Generate or edit the `.fart` parameter text file first.
  * Execute `fartbox -c <input.fart> -o <output.wav>` directly via CLI to render the audio asset into the project's sound directory.

## 6. `.fart` Boilerplate Templates

Below are standard boilerplate configurations for common sound categories. AI agents should use these templates as starting baselines for direct editing or generation.

### Template 1: Standard Laser / Projectile (`laser_base.fart`)

```ini
# fartbox Sound Parameter - Laser Base
wave_type = 0
p_base_freq = 0.600000
p_freq_limit = 0.200000
p_freq_ramp = -0.250000
p_freq_dramp = 0.000000
p_duty = 0.400000
p_duty_ramp = -0.100000
p_vib_strength = 0.000000
p_vib_speed = 0.000000
p_vib_delay = 0.000000
p_env_attack = 0.000000
p_env_sustain = 0.100000
p_env_decay = 0.200000
p_env_punch = 0.100000
p_lpf_resonance = 0.000000
p_lpf_freq = 1.000000
p_lpf_ramp = 0.000000
p_hpf_freq = 0.100000
p_hpf_ramp = 0.000000
p_pha_offset = 0.000000
p_pha_ramp = 0.000000
p_repeat_speed = 0.000000
p_arp_speed = 0.000000
p_arp_mod = 0.000000
```

### Template 2: Heavy Explosion / Impact (`explosion_base.fart`)

```ini
# fartbox Sound Parameter - Explosion Base
wave_type = 3
p_base_freq = 0.250000
p_freq_limit = 0.000000
p_freq_ramp = -0.150000
p_freq_dramp = 0.000000
p_duty = 0.000000
p_duty_ramp = 0.000000
p_vib_strength = 0.200000
p_vib_speed = 0.300000
p_vib_delay = 0.000000
p_env_attack = 0.000000
p_env_sustain = 0.200000
p_env_decay = 0.500000
p_env_punch = 0.400000
p_lpf_resonance = 0.300000
p_lpf_freq = 0.800000
p_lpf_ramp = -0.100000
p_hpf_freq = 0.000000
p_hpf_ramp = 0.000000
p_pha_offset = -0.100000
p_pha_ramp = -0.100000
p_repeat_speed = 0.000000
p_arp_speed = 0.000000
p_arp_mod = 0.000000
```

### Template 3: 8-Bit Coin / Item Pickup (`coin_base.fart`)

```ini
# fartbox Sound Parameter - Coin Base
wave_type = 0
p_base_freq = 0.450000
p_freq_limit = 0.000000
p_freq_ramp = 0.000000
p_freq_dramp = 0.000000
p_duty = 0.500000
p_duty_ramp = 0.000000
p_vib_strength = 0.000000
p_vib_speed = 0.000000
p_vib_delay = 0.000000
p_env_attack = 0.000000
p_env_sustain = 0.080000
p_env_decay = 0.250000
p_env_punch = 0.300000
p_lpf_resonance = 0.000000
p_lpf_freq = 1.000000
p_lpf_ramp = 0.000000
p_hpf_freq = 0.000000
p_hpf_ramp = 0.000000
p_pha_offset = 0.000000
p_pha_ramp = 0.000000
p_repeat_speed = 0.000000
p_arp_speed = 0.600000
p_arp_mod = 0.500000
```

### Template 4: UI Cursor / Select Blip (`blip_base.fart`)

```ini
# fartbox Sound Parameter - UI Blip Base
wave_type = 0
p_base_freq = 0.350000
p_freq_limit = 0.000000
p_freq_ramp = 0.000000
p_freq_dramp = 0.000000
p_duty = 0.500000
p_duty_ramp = 0.000000
p_vib_strength = 0.000000
p_vib_speed = 0.000000
p_vib_delay = 0.000000
p_env_attack = 0.000000
p_env_sustain = 0.050000
p_env_decay = 0.100000
p_env_punch = 0.000000
p_lpf_resonance = 0.000000
p_lpf_freq = 1.000000
p_lpf_ramp = 0.000000
p_hpf_freq = 0.150000
p_hpf_ramp = 0.000000
p_pha_offset = 0.000000
p_pha_ramp = 0.000000
p_repeat_speed = 0.000000
p_arp_speed = 0.000000
p_arp_mod = 0.000000
```
