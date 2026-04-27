## hen-obs (production observatory)

chimera-swope on hen-obs runs as a system LaunchDaemon. See
[`deploy/launchd/README.md`](deploy/launchd/README.md) for install steps and
day-to-day operations (start/stop/status/logs).

## Source rsync

rsync repositories to the server:

```bash
rsync -avz --delete --exclude=.venv/ --exclude=__pycache__/ --exclude=.history/ ~/workspace/chimera/chimera-swope/ puma:william/chimera/chimera-swope/
rsync -avz --delete --exclude=.venv/ --exclude=.history/ ~/workspace/henrietta-python/ puma:william/henrietta-python/
rsync -avz --delete --exclude=.venv/ --exclude=.history/ ~/workspace/swope-python/ puma:william/swope-python/
rsync -avz --delete --exclude=.venv/ --exclude=.history/ ~/workspace/chimera/chimera/ puma:william/chimera/chimera/
```

{"Command": "SLEW"}
{"Command": "STATUS"}
{"Command": "VER"}