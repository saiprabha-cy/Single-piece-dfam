"""
propulsion_calcs.py
--------------------
Design-target calculator for a small LOX/Kerosene liquid rocket engine
(injector + nozzle), built as the hand-calculation baseline for a
DfAM (Design for Additive Manufacturing) single-piece redesign project
inspired by Agnikul Cosmos' single-piece 3D-printed engine approach.

All results are exported to results/design_targets.json so they can be
directly referenced while modeling in Fusion 360.

Assumptions are representative student-project values, NOT Agnikul's
actual proprietary engine data. This is clearly stated in the report.
"""

import json
import math
from pathlib import Path
from scipy.optimize import brentq

# ----------------------------------------------------------------------
# 1. DESIGN INPUTS (assumed, representative small-engine test case)
# ----------------------------------------------------------------------
F_target = 3000.0          # Target thrust, N
Pc = 20e5                  # Chamber pressure, Pa (20 bar)
Pa = 101325.0               # Ambient pressure, Pa (sea level)
Isp = 290.0                 # Assumed sea-level specific impulse, s
g0 = 9.80665                 # Standard gravity, m/s^2
gamma = 1.2                  # Specific heat ratio of combustion gases
c_star = 1750.0              # Characteristic velocity, m/s (typical LOX/RP-1)

# Propellant properties (LOX / Kerosene, typical values)
OF_ratio = 2.5                # Oxidizer-to-fuel mass ratio (typical for LOX/RP-1)
rho_ox = 1141.0                # LOX density, kg/m^3
rho_fuel = 810.0               # Kerosene (RP-1) density, kg/m^3

# Injector design parameters
Cd = 0.7                     # Discharge coefficient, sharp-edged orifice
dP_injector_fraction = 0.175  # Injector pressure drop as fraction of Pc
orifice_diameter = 0.001      # Assumed single-orifice diameter, m (1 mm)

# Thermal parameters (first-order estimate only)
T_aw = 3200.0                 # Adiabatic wall temperature, K (typical for LOX/kerosene)
T_wall_target = 800.0         # Target max wall temperature, K (material limit assumption)
h_g_estimate = 8000.0         # Approx. gas-side heat transfer coeff., W/m^2-K
                               # (order-of-magnitude estimate; refine later with full Bartz eqn)


def compute_mass_flows():
    """Total and per-propellant mass flow rates from thrust and Isp."""
    Ve = Isp * g0
    mdot_total = F_target / Ve
    mdot_ox = mdot_total * (OF_ratio / (1 + OF_ratio))
    mdot_fuel = mdot_total / (1 + OF_ratio)
    return mdot_total, mdot_ox, mdot_fuel, Ve


def compute_injector_geometry(mdot_ox, mdot_fuel):
    """Orifice sizing for oxidizer and fuel using the incompressible
    orifice flow equation: mdot = Cd * A * sqrt(2 * rho * dP)."""
    dP = dP_injector_fraction * Pc

    A_ox_total = mdot_ox / (Cd * math.sqrt(2 * rho_ox * dP))
    A_fuel_total = mdot_fuel / (Cd * math.sqrt(2 * rho_fuel * dP))

    orifice_area = math.pi * (orifice_diameter / 2) ** 2
    n_ox_holes = math.ceil(A_ox_total / orifice_area)
    n_fuel_holes = math.ceil(A_fuel_total / orifice_area)

    return {
        "injector_dP_Pa": dP,
        "ox_total_orifice_area_m2": A_ox_total,
        "fuel_total_orifice_area_m2": A_fuel_total,
        "orifice_diameter_m": orifice_diameter,
        "n_ox_holes": n_ox_holes,
        "n_fuel_holes": n_fuel_holes,
    }


def compute_nozzle_geometry(mdot_total):
    """Throat area from c*, then exit Mach + area ratio for optimal
    (Pe = Pa) expansion using isentropic flow relations."""
    A_throat = mdot_total * c_star / Pc
    r_throat = math.sqrt(A_throat / math.pi)

    def pressure_ratio_residual(Me):
        Pe_over_Pc = (1 + (gamma - 1) / 2 * Me ** 2) ** (-gamma / (gamma - 1))
        return Pe_over_Pc - (Pa / Pc)

    Me = brentq(pressure_ratio_residual, 1.001, 10.0)

    area_ratio = (1 / Me) * (
        (2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * Me ** 2)
    ) ** ((gamma + 1) / (2 * (gamma - 1)))

    A_exit = A_throat * area_ratio
    r_exit = math.sqrt(A_exit / math.pi)

    return {
        "throat_area_m2": A_throat,
        "throat_radius_m": r_throat,
        "throat_diameter_mm": 2 * r_throat * 1000,
        "exit_mach": Me,
        "area_ratio_exit_to_throat": area_ratio,
        "exit_area_m2": A_exit,
        "exit_radius_m": r_exit,
        "exit_diameter_mm": 2 * r_exit * 1000,
    }


def compute_chamber_geometry_check(A_throat):
    """Validates the AS-MODELED chamber geometry (from the baseline CAD)
    against standard L* (characteristic length) and contraction-ratio
    guidelines for LOX/Kerosene engines. This checks the actual dimensions
    you modeled in Fusion 360, not just the theoretical injector/nozzle
    sizing above."""

    # --- As-modeled dimensions (from Baseline_Injector_Plate CAD) ---
    D_chamber = 0.055          # Chamber internal diameter, m (Ø55mm)
    L_straight = 0.090         # Straight chamber length, m (90mm)
    converging_half_angle_deg = 30.0   # Typical converging section angle

    r_chamber = D_chamber / 2
    r_throat = math.sqrt(A_throat / math.pi)

    # Convergent cone length (chamber radius down to throat radius)
    Lc = (r_chamber - r_throat) / math.tan(math.radians(converging_half_angle_deg))

    # Volume of straight cylindrical section
    V_cyl = math.pi * r_chamber ** 2 * L_straight

    # Volume of convergent frustum (cone connecting chamber to throat)
    V_frustum = (math.pi * Lc / 3) * (
        r_chamber ** 2 + r_chamber * r_throat + r_throat ** 2
    )

    V_chamber_total = V_cyl + V_frustum
    L_star = V_chamber_total / A_throat
    contraction_ratio = (r_chamber / r_throat) ** 2

    # Typical LOX/Kerosene guideline range for L* (meters)
    L_star_min_typical = 0.8
    L_star_max_typical = 1.5
    within_range = L_star_min_typical <= L_star <= L_star_max_typical

    return {
        "chamber_diameter_m": D_chamber,
        "straight_length_m": L_straight,
        "convergent_length_m": Lc,
        "chamber_volume_m3": V_chamber_total,
        "L_star_m": L_star,
        "L_star_typical_range_m": [L_star_min_typical, L_star_max_typical],
        "L_star_within_typical_range": within_range,
        "contraction_ratio_Ac_At": contraction_ratio,
        "note": (
            "L* below typical range indicates the as-modeled chamber is "
            "SHORTER than standard LOX/Kerosene practice would suggest — "
            "insufficient residence time for complete combustion in a real "
            "engine. Documented as a known limitation of this educational "
            "baseline; does not affect the validity of the DfAM part-count "
            "and single-piece consolidation comparison, which is geometry-"
            "independent of chamber length."
            if not within_range else
            "L* falls within typical LOX/Kerosene design practice."
        ),
    }


def compute_thermal_estimate():
    """First-order convective heat flux estimate (simplified Bartz-style).
    NOT a substitute for full Bartz correlation - flagged as an
    approximation to be refined/cross-checked in SimScale simulation."""
    q = h_g_estimate * (T_aw - T_wall_target)
    return {
        "adiabatic_wall_temp_K": T_aw,
        "target_wall_temp_K": T_wall_target,
        "estimated_heat_flux_W_per_m2": q,
        "note": "First-order estimate only; validate against SimScale thermal sim.",
    }


def main():
    mdot_total, mdot_ox, mdot_fuel, Ve = compute_mass_flows()
    injector = compute_injector_geometry(mdot_ox, mdot_fuel)
    nozzle = compute_nozzle_geometry(mdot_total)
    chamber_check = compute_chamber_geometry_check(nozzle["throat_area_m2"])
    thermal = compute_thermal_estimate()

    results = {
        "inputs": {
            "target_thrust_N": F_target,
            "chamber_pressure_Pa": Pc,
            "ambient_pressure_Pa": Pa,
            "assumed_Isp_s": Isp,
            "gamma": gamma,
            "c_star_m_s": c_star,
            "OF_ratio": OF_ratio,
        },
        "mass_flows": {
            "mdot_total_kg_s": mdot_total,
            "mdot_oxidizer_kg_s": mdot_ox,
            "mdot_fuel_kg_s": mdot_fuel,
            "exhaust_velocity_m_s": Ve,
        },
        "injector_design": injector,
        "nozzle_design": nozzle,
        "chamber_geometry_check": chamber_check,
        "thermal_estimate": thermal,
    }

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "design_targets.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    # Print human-readable summary
    print("=" * 60)
    print("DESIGN TARGET SUMMARY")
    print("=" * 60)
    print(f"Total mass flow:      {mdot_total:.4f} kg/s")
    print(f"  Oxidizer:           {mdot_ox:.4f} kg/s")
    print(f"  Fuel:                {mdot_fuel:.4f} kg/s")
    print(f"Injector dP:          {injector['injector_dP_Pa']/1e5:.2f} bar")
    print(f"  Ox orifices needed:  {injector['n_ox_holes']} x {orifice_diameter*1000:.1f}mm")
    print(f"  Fuel orifices needed:{injector['n_fuel_holes']} x {orifice_diameter*1000:.1f}mm")
    print(f"Throat diameter:      {nozzle['throat_diameter_mm']:.2f} mm")
    print(f"Exit diameter:        {nozzle['exit_diameter_mm']:.2f} mm")
    print(f"Exit Mach number:     {nozzle['exit_mach']:.3f}")
    print(f"Area ratio (Ae/At):   {nozzle['area_ratio_exit_to_throat']:.3f}")
    print(f"Est. heat flux:       {thermal['estimated_heat_flux_W_per_m2']/1e6:.2f} MW/m^2")
    print("-" * 60)
    print("CHAMBER GEOMETRY CHECK (as-modeled)")
    print(f"L* (characteristic length): {chamber_check['L_star_m']*1000:.1f} mm "
          f"(typical range: {chamber_check['L_star_typical_range_m'][0]*1000:.0f}-"
          f"{chamber_check['L_star_typical_range_m'][1]*1000:.0f} mm)")
    print(f"  Within typical range?     {chamber_check['L_star_within_typical_range']}")
    print(f"Contraction ratio (Ac/At): {chamber_check['contraction_ratio_Ac_At']:.2f}")
    print("=" * 60)
    print(f"Full results saved to: {out_path}")


if __name__ == "__main__":
    main()
