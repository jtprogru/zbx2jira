#!/usr/bin/env bash

set -e

# shellcheck disable=SC2164
cd /opt/zbxjira

source ./venv/bin/activate

python3 main.py "$1"

exit 0