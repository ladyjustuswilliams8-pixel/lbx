# Steel Beam Optimization Task

You are a structural engineer responsible for selecting an optimal steel beam design for a building application.

Your goal is to select the lightest valid steel beam design while satisfying all structural performance requirements.

## Design Objective

Choose a steel beam section that performs safely under the required loading conditions.

The selected design should:

* minimize beam weight
* satisfy bending strength requirements
* satisfy shear strength requirements
* satisfy serviceability deflection limits
* remain within the available design options

## Available Information

Public design information is available in the `/data` directory.

Review all files in `/data` before creating your design.

The available files contain:

* structural design requirements
* loading conditions
* available steel beam sections
* beam section properties

Evaluate the available beam candidates and select the minimum-weight valid design.

## Required Output

You must create exactly one file:

```
/tmp/output/design.json
```

The file must contain a JSON object with exactly the following fields:

```json
{
  "beam_section": "selected beam designation",
  "material": "selected material",
  "span_ft": 0,
  "design_notes": "brief explanation of why this beam was selected"
}
```

The `design_notes` field should briefly explain that available beam candidates were evaluated for structural performance and that the minimum-weight valid design was selected.

