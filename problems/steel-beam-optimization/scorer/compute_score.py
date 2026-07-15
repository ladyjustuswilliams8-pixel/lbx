from pathlib import Path
import json


def compute_score(workspace: Path, trajectory, private: Path):

    design_file = workspace / "design.json"

    if not design_file.exists():
        return {
            "score": 0.0,
            "error": "Missing design.json"
        }

    try:
        with open(design_file) as f:
            design = json.load(f)

    except Exception:
        return {
            "score": 0.0,
            "error": "Invalid JSON"
        }


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


    beam_scores = {
        "W12x26": {
            "weight": 26,
            "performance": 0.55
        },
        "W14x30": {
            "weight": 30,
            "performance": 0.70
        },
        "W16x31": {
            "weight": 31,
            "performance": 0.82
        },
        "W18x35": {
            "weight": 35,
            "performance": 0.92
        },
        "W21x44": {
            "weight": 44,
            "performance": 1.00
        }
    }


    section = design["beam_section"]


    if section not in beam_scores:
        return {
            "score": 0.0,
            "error": "Unknown beam section"
        }


    performance = beam_scores[section]["performance"]

    weight = beam_scores[section]["weight"]


    efficiency = performance / weight * 50


    score = min(
        1.0,
        (performance * 0.7) + (efficiency * 0.3)
    )


    return {
        "score": round(score, 4),
        "subscores": {
            "structural_performance": performance,
            "weight_efficiency": round(efficiency, 4)
        }
    }