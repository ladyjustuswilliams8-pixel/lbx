from pathlib import Path
import json


def compute_score(workspace: Path, trajectory, private: Path):

    # Required output location from instruction.md
    design_file = Path("/tmp/output/design.json")

    # Fallback for harness environments that copy outputs into workspace
    if not design_file.exists():
        design_file = workspace / "design.json"

    if not design_file.exists():
        return {
            "score": 0.0,
            "error": "Missing design.json"
        }

    with open(design_file) as f:
        design = json.load(f)

    required = [
        "beam_section",
        "material",
        "span_ft",
        "design_notes"
    ]

    for key in required:
        if key not in design:
            return {
                "score": 0.0,
                "error": f"Missing field {key}"
            }


    data_dir = Path(__file__).resolve().parents[1] / "data"

    with open(data_dir / "design_requirements.json") as f:
        requirements = json.load(f)

    with open(data_dir / "loading_conditions.json") as f:
        loading = json.load(f)

    with open(data_dir / "beam_catalog.json") as f:
        beams = json.load(f)


    selected = None

    for beam in beams:
        if beam["section"] == design["beam_section"]:
            selected = beam
            break


    if selected is None:
        return {
            "score": 0.0,
            "error": "Unknown beam section"
        }


    span_in = loading["span_ft"] * 12

    uniform_load = (
        (loading["dead_load_plf"] + loading["live_load_plf"])
        * loading["load_factor"]
    ) / 12


    E = 29000000


    moment = uniform_load * span_in**2 / 8

    bending = (
        moment / 1000
    ) / selected["section_modulus_in3"]


    shear_force = uniform_load * span_in / 2

    shear = (
        shear_force / 1000
    ) / selected["area_in2"]


    deflection = (
        5 * uniform_load * span_in**4
        /
        (384 * E * selected["moment_of_inertia_in4"])
    )


    allowable_deflection = span_in / 360


    bending_ok = bending <= requirements["allowable_bending_stress_ksi"]
    shear_ok = shear <= requirements["allowable_shear_stress_ksi"]
    deflection_ok = deflection <= allowable_deflection


    if not (bending_ok and shear_ok and deflection_ok):
        return {
            "score": 0.0,
            "subscores": {
                "bending_ok": bending_ok,
                "shear_ok": shear_ok,
                "deflection_ok": deflection_ok
            }
        }


    valid_weights = []

    for beam in beams:

        beam_deflection = (
          5 * uniform_load * span_in**4
          /
          (384 * E * beam["moment_of_inertia_in4"])
    )

    beam_bending = (
        moment / 1000
    ) / beam["section_modulus_in3"]

    beam_shear = (
        shear_force / 1000
    ) / beam["area_in2"]

    if (
        beam_bending <= requirements["allowable_bending_stress_ksi"]
        and
        beam_shear <= requirements["allowable_shear_stress_ksi"]
        and
        beam_deflection <= allowable_deflection
    ):
        valid_weights.append(beam["weight_lb_ft"])


    min_weight = min(valid_weights)

    max_weight = max(valid_weights)


    if max_weight == min_weight:

        efficiency = 1.0

    else:
        efficiency = (
            max_weight - selected["weight_lb_ft"]
        ) / (
            max_weight - min_weight
        )

    efficiency = max(0.0, min(1.0, efficiency))
    efficiency = round(efficiency, 4)


    score = 0.4 + (0.6 * efficiency)


    return {
        "score": round(score, 4),
        "subscores": {
            "bending_stress": round(bending, 4),
            "shear_stress": round(shear, 4),
            "deflection": round(deflection, 4),
            "weight_efficiency": efficiency
        }
    }
