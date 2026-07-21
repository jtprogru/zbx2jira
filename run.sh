#!/usr/bin/env bash

set -e

# shellcheck disable=SC2164
cd /opt/zbxjira

uv run python main.py "$1"

exit 0