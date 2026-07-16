#!/bin/bash

set -e

OUTPUT_DIR="/tmp/output"

mkdir -p "$OUTPUT_DIR"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "$SCRIPT_DIR/beam_model.py"

test -f "$OUTPUT_DIR/design.json"

cp "$OUTPUT_DIR/design.json" "$SCRIPT_DIR/design.json"
