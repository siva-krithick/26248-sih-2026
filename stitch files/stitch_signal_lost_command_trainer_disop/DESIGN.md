---
name: Aegis Command
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#3d4947'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#00687a'
  on-secondary: '#ffffff'
  secondary-container: '#57dffe'
  on-secondary-container: '#006172'
  tertiary: '#8d4b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#b15f00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#ffdcc3'
  tertiary-fixed-dim: '#ffb77d'
  on-tertiary-fixed: '#2f1500'
  on-tertiary-fixed-variant: '#6e3900'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.005em
  title-sm:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.04em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.06em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-sm: 0.5rem
  gutter-lg: 1.5rem
  margin: 1.5rem
  margin-mobile: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system establishes a high-tier defense intelligence and mission command interface. It departs from cliché dark-mode "sci-fi combat" tropes in favor of an authoritative, high-clarity light aesthetic inspired by modern aerospace telemetry, joint operations centers, and state-of-the-art situational awareness consoles.

### Brand Personality
- **Sovereign Precision:** Uncompromising clarity, metric accuracy, and immediate scanability.
- **Strategic Restraint:** Devoid of decorative gamer ornamentation; every line, badge, and divider serves an operational orientation purpose.
- **Technical Rigor:** Dense, structured data delivery balanced with crisp editorial typography and deliberate modular layouts.

### Visual Style
A convergence of **High-Contrast Precision Minimalism** and **Tactical Instrumentation**. The visual architecture relies on engineered micro-borders, razor-sharp geometric alignment, subtle telemetry crosshairs, and dynamic grid overlays. Interactive command states project a live, responsive mission cadence through razor-thin borders, tactile micro-toggles, and targeted chromatic signals.

## Colors

The palette delivers maximum contrast under ambient tactical lighting, utilizing clean cool-slate surfaces paired with deep aerospace slate-navy inks and selective spectrum accents.

### Palette Architecture
- **Canvas & Containers:** Base surface is `#F8FAFC` (Slate 50) paired with `#FFFFFF` (Surface Elevated) and `#F1F5F9` (Surface Recessed / Trackers). Structural line separators utilize `#E2E8F0` and `#CBD5E1`.
- **Primary Ink Hierarchy:** `#0F172A` (Slate 900) for primary headlines, data values, and operational readouts; `#1E293B` (Slate 800) for body and labels; `#475569` (Slate 600) for secondary metadata and timestamps; `#94A3B8` (Slate 400) for grid reticles and passive markings.
- **Primary Accent (`#0D9488` / `#0F766E` Deep Teal):** Active operation vector, positive telemetry, locked targets, and verified status.
- **Secondary Accent (`#06B6D4` Tactical Cyan):** Sensor sweeps, telemetry vectors, simulation state projections, and secondary telemetry locks.
- **Alert & Critical Accent (`#D97706` Amber / `#DC2626` Hazard Red):** High-priority exceptions, interception alerts, threshold breaches, and cautionary override modes.

Use primary color sparingly to denote mission-critical focus. Neutral slate surfaces must constitute over 85% of total screen real estate.

## Typography

The typographic hierarchy implements a high-utility tri-font protocol engineered for command simulations:

1. **Display & Operational Headlines (Space Grotesk):** Provides mechanical, technical authority with balanced geometric curves. Used strictly for mission sector titles, unit headers, and high-level analytical markers.
2. **Operational Text & Reports (Geist):** Clean, neutral, high-legibility sans-serif optimized for continuous multi-pane reading, situational reports, and administrative logs.
3. **Telemetry & Metadata (JetBrains Mono):** Reserved for coordinates, timecodes (UTC/ZULU), vector coordinates, unit serials, system health metrics, and table figures. All numerical data columns must align via monospaced tabular figures.

## Layout & Spacing

The command interface employs a strict 12-column modular grid built on a 4px/8px incremental base unit. Layout density is adjustable depending on operational context: condensed for real-time telemetry panels, and open for tactical map visualization and incident review.

### Breakpoints & Reflow Protocol
- **Desktop / Ops Wall (≥ 1440px):** 12-column fluid layout with three persistent modular lanes: Telemetry Index (left, 280px fixed), Primary Theater Viewport (center, flexible auto-expand), and Tactical Feed / Simulation Controls (right, 360px fixed). Gutter: `1.5rem`.
- **Workstation / Tablet (768px – 1439px):** 8-column layout. Telemetry panes collapse into an expandable accordion side drawer; simulation workspace maintains operational dominance. Gutter: `1rem`.
- **Tactical Field / Mobile (< 768px):** 4-column linear stack. Viewports transition to tabbed navigation overlays (Sector, Sim, Log). Margin: `1rem`, Gutter: `0.5rem`.

## Elevation & Depth

This system avoids heavy, atmospheric drop shadows. Spatial separation is achieved through **precision structural lines, tonal layering, and fine technical borders**.

### Structural Elevation Levels
- **Level 0 (Base Substrate):** `#F8FAFC`. Background for entire viewport surfaces, map substrates, and simulation canvas backgrounds.
- **Level 1 (Docked Consoles & Field Modules):** `#FFFFFF` with a hairline border (`1px solid #E2E8F0`). Provides the core interactive containment with absolute edge fidelity.
- **Level 2 (Active Focus & Flyout Drawers):** `#FFFFFF` bordered by `#CBD5E1`, supported by a clean technical drop edge: `0 4px 12px -2px rgba(15, 23, 42, 0.06), 0 1px 3px 0 rgba(15, 23, 42, 0.04)`.
- **Level 3 (Tactical Overlays & Critical Alerts):** `#FFFFFF` with a `1px` high-contrast outline (`#0F172A` or `#D97706`) and directional ambient shadow: `0 12px 24px -4px rgba(15, 23, 42, 0.10)`.

### Technical Reticle Overlays
Precision surfaces may implement subtle SVG coordinate markings at container corners (2px crosshairs in `#94A3B8`) to reinforce modular positioning without compromising functional hierarchy.

## Shapes

The interface embraces a low-radius, architectural geometry. Surfaces feature controlled `0.25rem` (4px) corner rounding to soften harsh brutalist edges while maintaining the discipline of industrial flight hardware and hardened instrumentation.

### Corner Rules
- **Interactive Controls (Buttons, Inputs, Selectors):** Standardized to soft rounding (`0.25rem`).
- **Data Panels & Display Cards:** Standard `0.25rem` radius or strict `0px` when flush inside sidebars.
- **Pill Badges (Status Pills):** Limited specifically to operational indicators and alert counts with a restrained `0.25rem` box badge or fully rounded `9999px` capsule.

## Components

### Buttons & Interactive Triggers
- **Primary Command:** Solid `#0D9488` background, `#FFFFFF` text, `0.25rem` radius, uppercase `label-md` mono text, tracking `0.06em`. Hover transitions to `#0F766E`. Active state applies a crisp inset ring.
- **Secondary Tactical:** Crisp `1px solid #CBD5E1` border, `#FFFFFF` background, `#0F172A` text. Hover shifts background to `#F1F5F9` and border to `#94A3B8`.
- **Alert / Override:** `#D97706` background with white text for caution operations; `#DC2626` for abort or hostile actions.
- **Simulation Control Strips:** Linked segmented groups styled as flat precision toggles with mono labels and distinct green/teal active LEDs.

### Data Chips & Status Badges
- Constructed with `label-sm` monospaced font, 4px vertical / 8px horizontal padding.
- **Nominal/Active:** Background `#F0FDFA`, border `1px solid #99F6E4`, text `#0F766E`. Features a 6px static teal status dot.
- **Simulating/Processing:** Background `#ECFEFF`, border `1px solid #A5F3FC`, text `#0891B2`.
- **Warning/Threat:** Background `#FFFBEB`, border `1px solid #FDE68A`, text `#B45309`.

### Input Fields & Parameter Steppers
- Clean flat fields styled with `#FFFFFF` background and sharp `1px solid #CBD5E1` border.
- Text rendered in `Geist` body-md, with parameter units (e.g., `MGRS`, `KM/H`, `MSL`) locked on the right in `JetBrains Mono` at `#64748B`.
- Focus state activates a distinct `1px solid #0D9488` border with a subtle zero-blur `0 0 0 2px rgba(13, 148, 136, 0.15)` focus ring.

### Checkboxes, Switches & Radio Controls
- Square checkboxes (`16px × 16px`) with 2px radius and crisp slate borders. Selected state renders solid `#0D9488` with a geometric tick mark.
- Tactical Switches feature a recessed slate-200 track with an instantaneous slide action, marked by an integrated mono `I/O` status label.

### Command Cards & Instrumentation Panels
- Crisp white surfaces encased in a `1px solid #E2E8F0` border.
- Header bars feature a distinct `#F8FAFC` top strip with an integrated sector tag (e.g., `SEC-04 // TELEMETRY`) set in `label-sm` mono, followed by an operational control menu.
- Content divides utilize horizontal and vertical `1px` razor dividers without padding collapse.

### Specialized Simulation Modules
- **Radar & Spatial Reticles:** Pure `#F8FAFC` or `#F1F5F9` field inscribed with concentric vector rings (`1px solid #E2E8F0`), high-contrast sweep lines in `#06B6D4` with 20% opacity fades, and high-visibility tracking icons.
- **Time Scrubbers:** Monospaced military timecode scale (ZULU time) with dual-point timeline range handles in teal and numerical scrub-heads for real-time playout/rewind analysis.