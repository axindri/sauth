#!/bin/sh
set -e
cd /opt/sauth
# uv creates .venv at runtime (no .venv copied into image)
uv sync --frozen --no-dev
export PATH="/opt/sauth/.venv/bin:$PATH"
exec sh /start.sh
