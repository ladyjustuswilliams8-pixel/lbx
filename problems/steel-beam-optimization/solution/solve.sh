#!/bin/bash

set -e

mkdir -p /tmp/output

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 "$SCRIPT_DIR/beam_model.py"

cp /tmp/output/design.json "$SCRIPT_DIR/design.json"
cp /tmp/output/design.json ./design.json
