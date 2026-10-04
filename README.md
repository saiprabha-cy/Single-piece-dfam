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

| Stage | Folder | Status |
|---|---|---|
| 1. Propulsion calculations | `01_calculations/` | ✅ Complete |
| 2. Baseline multi-part CAD | `02_cad/baseline_multipart/` | ✅ Complete |
| 3. Single-piece DfAM redesign | `02_cad/dfam_redesign/` | ✅ Complete |
| 4. Structural/thermal validation | `03_simulation/` | ✅ Structural complete; thermal documented as a known limitation |
| 5. Sensor/telemetry board | `04_kicad_board/` | ✅ Complete (0 DRC errors) |
| 6. Print-readiness analysis | `05_print_readiness/` | 🔜 Scoped as future work (see below) |
| 7. Final report | `06_report/` | ✅ Complete |

## Design Case (Assumed, Representative Values)

This project uses **representative values** for a generic small LOX/Kerosene
test-case engine, not any specific company's proprietary specifications.

- Target thrust: 3,000 N
- Chamber pressure: 20 bar
- Propellants: LOX / Kerosene (RP-1)
- Assumed sea-level Isp: 290 s

## Key Results

| Metric | Baseline (multi-part) | Redesign (single-piece) |
|---|---|---|
| Part count | 3 | 1 |
| Fastener interfaces | 2 (1 bolted, 1 rigid-joint only) | 0 |
| Mounting holes | 8 | 0 |
| Cooling provisions | None | 6 integrated channels |
| Structural safety factor (20 bar) | — | 6.24 (Ti-6Al-4V, SimScale) |

## Tools Used

- **Python** (SciPy) — propulsion calculations
- **Autodesk Fusion 360** (Personal Use license) — CAD modeling + built-in simulation
- **SimScale** — structural/thermal validation
- **KiCad** — sensor/telemetry PCB design

### Future Extensions
- **PrusaSlicer / Cura** — print-readiness and support-structure analysis
  (scoped as future work; see `05_print_readiness/`)
- Coolant inlet/outlet port routing on the DfAM redesign
- Full channel count (6 → 24) for production-representative coverage
- Chamber L* correction (increase straight-section length for realistic
  combustion residence time)

## Known Limitations

- **Chamber L\*** (characteristic length) is 263mm against a typical
  800-1500mm range for LOX/Kerosene engines — the as-modeled chamber is
  shorter than standard practice would recommend. This is a known,
  documented simplification; it does not affect the validity of the
  single-piece consolidation comparison, which is geometry-independent of
  chamber length. See `01_calculations/results/design_targets.json`.
- **Thermal simulation** was attempted in SimScale but diverged (likely due
  to an incomplete fluid-flow boundary definition in the initial CHT setup).
  Due to free-tier compute limits, a corrected re-run was not completed.
  The Stage 1 hand-calculated estimate (19.2 MW/m², target wall temp 800K)
  is retained as the primary thermal reference. See
  `03_simulation/validation_comparison.md`.
- **Cooling channel count** was reduced from a production-representative
  24 channels to 6, to keep the modeling scope achievable within the
  project timeline.
- **Print-readiness analysis** (slicer-based orientation/support check) was
  not completed; see Future Extensions above.
