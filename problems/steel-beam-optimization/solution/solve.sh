#!/bin/bash

mkdir -p /tmp/output

cat <<EOF > /tmp/output/design.json
{
  "beam_section": "W21x44",
  "material": "A992 steel",
  "span_ft": 25,
  "design_notes": "Selected the W21x44 section because it provides the highest structural performance margin for the required loading conditions."
}
EOF