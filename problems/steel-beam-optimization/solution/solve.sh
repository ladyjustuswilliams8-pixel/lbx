#!/bin/bash

set -e

mkdir -p /tmp/output

python3 <<'PY'
from pathlib import Path
import json

# Locate public task data
DATA_DIR = Path("/data")
if not DATA_DIR.exists():
    DATA_DIR = Path("problems/steel-beam-optimization/data")

with open(DATA_DIR / "design_requirements.json") as f:
    requirements = json.load(f)

with open(DATA_DIR / "loading_conditions.json") as f:
    loading = json.load(f)

with open(DATA_DIR / "beam_catalog.json") as f:
    beams = json.load(f)

span_ft = loading["span_ft"]
span_in = span_ft * 12

# Uniform load (lb/in)
uniform_load = (
    (loading["dead_load_plf"] + loading["live_load_plf"])
    * loading["load_factor"]
) / 12

# Steel modulus (psi)
E = 29000000

valid_designs = []

for beam in beams:

    section = beam["section"]
    area = beam["area_in2"]
    I = beam["moment_of_inertia_in4"]
    S = beam["section_modulus_in3"]

    # Maximum moment (lb-in)
    M = uniform_load * span_in**2 / 8

    # Bending stress (ksi)
    bending = (M / 1000) / S

    # Maximum shear (lb)
    V = uniform_load * span_in / 2

    # Approximate shear stress (ksi)
    shear = (V / 1000) / area

    # Midspan deflection (in)
    delta = (
        5 * uniform_load * span_in**4
        /
        (384 * E * I)
    )

    allowable_delta = span_in / 360

    if (
        bending <= requirements["allowable_bending_stress_ksi"]
        and shear <= requirements["allowable_shear_stress_ksi"]
        and delta <= allowable_delta
    ):
        valid_designs.append({
            "beam": beam,
            "weight": beam["weight_lb_ft"]
        })

if not valid_designs:
    raise RuntimeError("No beam satisfies the design requirements.")

best = min(valid_designs, key=lambda x: x["weight"])

output = {
    "beam_section": best["beam"]["section"],
    "material": requirements["material"],
    "span_ft": span_ft,
    "design_notes": "Selected using bending, shear, deflection, and minimum weight calculations."
}

with open("/tmp/output/design.json", "w") as f:
    json.dump(output, f, indent=2)

PY
