# Contributing Guide

## Development

To get started:

```sh
uv venv --python 3.13
uv pip install -e ".[dev]"
uv run pre-commit install
```

Run the checks:

```sh
uv run ruff format qt_dock_window examples tests
uv run ruff check --select I --fix qt_dock_window examples tests
uv run ruff check qt_dock_window examples tests
uv run ty check
uv run pytest
```

### Screenshots

Running the example window saves a screenshot to `.github/assets/window.png`:

```sh
uv run python -m examples.window
```

The README header is created from `window.png`:

```sh
cd .github
uv run python create_images.py
```

### Releasing Changes

To version up using [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release):

```sh
uv run semantic-release version
```
