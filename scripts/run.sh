#!/bin/bash
# usage: scripts/run.sh posts/<folder>   (folder must contain spec.json)
set -e
D=$(dirname "$0")
python3 "$D/make_post.py" "$1/spec.json" "$1"
python3 "$D/gen_post.py" "$1/spec.json" "$1"
