# chimera-swope launchd daemon (hen-obs)

chimera-swope is run on hen-obs as a system LaunchDaemon (`com.henrietta.chimera`)
instead of from a Terminal.app session. Two reasons:

1. **macOS Local Network Privacy.** Long-running shells eventually wedge with
   `EHOSTUNREACH` on local-subnet TCP because the LNP responsible-process
   chain breaks when an ancestor (Terminal.app) restarts. System daemons
   bypass per-app LNP gating because there is no responsibility chain.
2. **Survives reboots and SSH disconnects.** No GUI session required.

## Files

- [`com.henrietta.chimera.plist`](com.henrietta.chimera.plist) — the LaunchDaemon
  definition. Installed at `/Library/LaunchDaemons/com.henrietta.chimera.plist`.
- [`chimera-launch.sh`](chimera-launch.sh) — wrapper that waits for the
  Henrietta.app GUI TCP port (`127.0.0.1:52801`) before launching chimera, so
  the daemon doesn't fail at boot if the GUI isn't up yet. Installed at
  `/Users/Shared/henrietta/bin/chimera-launch.sh`.

Logs go to `/Users/Shared/henrietta/logs/chimera.{out,err}.log`.

## Install (one-time)

Run from the repo root on your dev machine. Assumes ssh access to `hen-obs`
and passwordless sudo for `henrietta`.

```bash
# Copy the artifacts to hen-obs
scp deploy/launchd/chimera-launch.sh hen-obs:/Users/Shared/henrietta/bin/
scp deploy/launchd/com.henrietta.chimera.plist hen-obs:/tmp/

# Install on hen-obs
ssh hen-obs '
chmod +x /Users/Shared/henrietta/bin/chimera-launch.sh
sudo install -m 644 -o root -g wheel /tmp/com.henrietta.chimera.plist \
    /Library/LaunchDaemons/com.henrietta.chimera.plist
plutil -lint /Library/LaunchDaemons/com.henrietta.chimera.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/com.henrietta.chimera.plist
sudo launchctl print system/com.henrietta.chimera | head -30
'
```

After install, the daemon is also loaded on every boot.

## Operations

```bash
# Status (look for "state = running" and recent "last exit code = 0")
ssh hen-obs 'sudo launchctl print system/com.henrietta.chimera | head -30'

# Restart on demand (graceful: SIGTERM then re-spawn)
ssh hen-obs 'sudo launchctl kickstart -k system/com.henrietta.chimera'

# Stop (until next reboot or bootstrap)
ssh hen-obs 'sudo launchctl kill SIGTERM system/com.henrietta.chimera'

# Watch logs
ssh hen-obs 'tail -f /Users/Shared/henrietta/logs/chimera.err.log'

# Reload after editing plist (full unload + reload)
ssh hen-obs '
sudo launchctl bootout system/com.henrietta.chimera
sudo launchctl bootstrap system /Library/LaunchDaemons/com.henrietta.chimera.plist
'
```

## Updating the launch command or environment

Edit `com.henrietta.chimera.plist` in this repo, then:

```bash
scp deploy/launchd/com.henrietta.chimera.plist hen-obs:/tmp/
ssh hen-obs '
sudo install -m 644 -o root -g wheel /tmp/com.henrietta.chimera.plist \
    /Library/LaunchDaemons/com.henrietta.chimera.plist
sudo launchctl bootout system/com.henrietta.chimera 2>/dev/null
sudo launchctl bootstrap system /Library/LaunchDaemons/com.henrietta.chimera.plist
'
```

## Troubleshooting

- **Daemon stuck waiting on Henrietta port.** Tail the err log; you'll see
  `[chimera-launch] ... waiting for Henrietta.app on 127.0.0.1:52801`. Open
  the Henrietta GUI; the daemon will detect the port and start chimera within
  5 seconds.
- **`uv` not found.** `EnvironmentVariables.PATH` in the plist must include
  the directory containing uv. Verify with
  `ssh hen-obs '/Users/henrietta/.local/bin/uv --version'` and adjust the
  plist if uv has moved.
- **`EHOSTUNREACH` errors persist after switching to the daemon.** The daemon
  context should not be subject to per-app LNP, but if it ever is, change
  `UserName` from `henrietta` to `root` in the plist and reload. Root
  daemons reliably bypass LNP.
- **Daemon won't restart after a clean exit.** That's by design — `KeepAlive`
  is set to restart only on crash (`SuccessfulExit = false`). Run
  `launchctl kickstart` to restart manually, or change `SuccessfulExit` to
  `true` if you want unconditional restart.
