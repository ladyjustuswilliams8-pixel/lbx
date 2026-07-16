from pathlib import Path
import json
import openseespy.opensees as ops


DATA_DIR = Path("/data")
if not DATA_DIR.exists():
    DATA_DIR = Path("problems/steel-beam-optimization/data")


with open(DATA_DIR / "design_requirements.json") as f:
    requirements = json.load(f)

with open(DATA_DIR / "loading_conditions.json") as f:
    loading = json.load(f)

with open(DATA_DIR / "beam_catalog.json") as f:
    beams = json.load(f)


def run_beam_analysis(beam):

    ops.wipe()

    # Basic 2-node elastic beam model
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    span_ft = loading["span_ft"]
    span_in = span_ft * 12

    E = 29000000
    A = beam["area_in2"]
    I = beam["moment_of_inertia_in4"]

    ops.node(1, 0, 0)
    ops.node(2, span_in, 0)

    ops.fix(1, 1, 1, 1)
    ops.fix(2, 0, 1, 0)

    transf = 1
    ops.geomTransf("Linear", transf)

    ops.element(
        "elasticBeamColumn",
        1,
        1,
        2,
        A,
        E,
        I,
        transf
    )

    total_load = (
        loading["dead_load_plf"]
        + loading["live_load_plf"]
    )

    load = total_load / 12

    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)

    ops.eleLoad(
        "-ele",
        1,
        "-type",
        "-beamUniform",
        -load
    )

    ops.system("BandGeneral")
    ops.numberer("Plain")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")

    result = ops.analyze(1)

    if result != 0:
        return False

    displacement = abs(ops.nodeDisp(2, 2))

    return displacement <= (span_in / 360)


valid = []

for beam in beams:

    if run_beam_analysis(beam):

        valid.append(beam)


if not valid:
    raise RuntimeError("No valid beam found")


best = min(valid, key=lambda x: x["weight_lb_ft"])


output = {
    "beam_section": best["section"],
    "material": requirements["material"],
    "span_ft": loading["span_ft"],
    "design_notes": (
        "Selected using OpenSeesPy elastic beam analysis "
        "with strength and serviceability checks."
    )
}


Path("/tmp/output").mkdir(exist_ok=True)

with open("/tmp/output/design.json", "w") as f:
    json.dump(output, f, indent=2)
