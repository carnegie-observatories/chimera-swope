#!/bin/zsh
# Launched by /Library/LaunchDaemons/com.henrietta.chimera.plist
# Waits for Henrietta.app GUI TCP port to be reachable, then execs chimera.
# Without this gate, chimera-swope's Henrietta driver fails on startup
# if the GUI is not up yet.

set -u
HENRIETTA_HOST="${HENRIETTA_HOST:-127.0.0.1}"
HENRIETTA_PORT="${HENRIETTA_PORT:-52801}"
CHIMERA_BIN="${CHIMERA_BIN:-/Users/henrietta/.chimera/venv/bin/chimera}"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

while ! /usr/bin/nc -zw1 "$HENRIETTA_HOST" "$HENRIETTA_PORT" 2>/dev/null; do
    echo "[chimera-launch] $(ts) waiting for Henrietta.app on $HENRIETTA_HOST:$HENRIETTA_PORT..."
    sleep 5
done
echo "[chimera-launch] $(ts) Henrietta.app reachable, starting chimera"

exec "$CHIMERA_BIN" -vvvv
