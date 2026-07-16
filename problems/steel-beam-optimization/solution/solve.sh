#!/bin/bash

set -e

mkdir -p /tmp/output

python3 "$(dirname "$0")/beam_model.py"

cp /tmp/output/design.json ./design.json
