# Steel Beam Optimization Task

You are a structural engineer responsible for selecting an optimal steel beam design for a building application.

Your goal is to select a beam configuration that satisfies all structural performance requirements while minimizing structural weight.

## Design Objective

Choose a steel beam section that performs safely under the required loading conditions.

The design should:

- minimize beam weight
- satisfy bending strength requirements
- satisfy shear strength requirements
- maintain acceptable serviceability performance
- remain within the available design options

## Available Information

Public design information is available in the `/data` directory.

Review all files in `/data` before creating your design.

## Required Output

You must create exactly one file:

/tmp/output/design.json

The file must contain a JSON object with the following fields:

```json
{
  "beam_section": "selected beam designation",
  "material": "selected material",
  "span_ft": 0,
  "design_notes": "brief explanation of why this beam was selected"
}
```
