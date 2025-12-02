# Chimera Swope

Swope Telescope and Instruments chimera plugin

This is a plugin for the [Chimera observatory control system](https://github.com/astroufsc/chimera).

## Overview

The chimera-swope plugin provides comprehensive control interfaces for the Henrietta Swope 1.0-meter telescope 
at Las Campanas Observatory, including both Swope and Henrietta instrument systems.

## Installation

```bash
pip install -U chimera_swope
```

Or install from source:

```bash
git clone https://github.com/carnegie-observatories/chimera-swope.git
cd chimera-swope
uv sync
```

## Configuration Example

Add the following to your `chimera.config` file:

```yaml
telescope:
        name: swope
        type: SwopeTelescope
        tcs_host: 10.8.80.53
        aperture: 1000.0  # mm
        focal_length: 7000.0  # mm

    camera:
        name: swopecam
        type: SwopeCamera
        swope_ccd_host: 127.0.0.1
        swope_ccd_port: 51911

    dome:
        name: dome
        type: SwopeDome

    focuser:
        name: focuser
        type: SwopeFocuser

    weatherstation:
        name: weather
        type: SwopeWeatherStation
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/carnegie-observatories/chimera-swope.git
cd chimera-swope

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks
```

### Code Quality

This project uses:
- [Ruff](https://docs.astral.sh/ruff/) for linting and formatting
- [pre-commit](https://pre-commit.com/) for automated checks

```bash
# Run linter
uv run ruff check

# Run formatter
uv run ruff format

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

## License

GPL-2.0-or-later

## Contact

For more information, contact us on chimera's discussion list:
https://groups.google.com/forum/#!forum/chimera-discuss

Bug reports and patches are welcome and can be sent over our GitHub page:
https://github.com/carnegie-observatories/chimera-swope
