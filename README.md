# Single-Piece DfAM Redesign of a Liquid Rocket Injector/Nozzle Assembly

A capstone project applying **Design for Additive Manufacturing (DfAM)**
principles to a small liquid rocket engine injector/nozzle assembly —
exploring how a traditionally multi-part, bolted engine assembly can be
redesigned as a single consolidated 3D-printed part.

## Motivation

Several modern small-launch-vehicle companies have moved toward 3D-printing
entire rocket engines as a single piece, eliminating the joints, fasteners,
and assembly steps of traditionally machined multi-part engines. This
project applies that same design philosophy at a smaller, student-accessible
scale: take a conventionally-designed multi-part injector/nozzle assembly,
redesign it as one consolidated additively-manufactured part, and validate
the redesign with both hand calculations and simulation.

## Project Stages

| Stage | Folder | Description |
|---|---|---|
| 1 | `01_calculations/` | Python propulsion calculations → design targets (thrust, mass flow, injector orifice sizing, nozzle geometry, first-order thermal estimate) |
| 2 | `02_cad/baseline_multipart/` | Traditional multi-part CAD model (Fusion 360) |
| 3 | `02_cad/dfam_redesign/` | Single-piece, DfAM-optimized redesign (Fusion 360) |
| 4 | `03_simulation/` | Structural/thermal validation (SimScale) vs. hand calculations |
| 5 | `04_kicad_board/` | Sensor/telemetry board design (KiCad) for instrumenting the part in a test setup |
| 6 | `05_print_readiness/` | Slicer-based printability analysis (PrusaSlicer/Cura) |
| 7 | `06_report/` | Final case-study report and portfolio write-up |

## Design Case (Assumed, Representative Values)

This project uses **representative small-engine values** for a generic
LOX/Kerosene test-case engine, not any specific company's proprietary
specifications. This is explicitly noted here and in the final report.

- Target thrust: 3,000 N
- Chamber pressure: 20 bar
- Propellants: LOX / Kerosene (RP-1)
- Assumed sea-level Isp: 290 s

## Tools Used

- **Python** (SciPy) — propulsion calculations
- **Autodesk Fusion 360** (Personal Use license) — CAD modeling + built-in simulation
- **SimScale** — structural/thermal validation
- **KiCad** — sensor/telemetry PCB design
- **PrusaSlicer / Cura** — print-readiness analysis

## Status

🚧 In progress — Stages 1-4 complete (calculations, baseline CAD, single-piece
redesign, structural validation). Thermal simulation attempted; documented
as a known limitation due to solver divergence and free-tier compute limits
(see `03_simulation/validation_comparison.md`).
