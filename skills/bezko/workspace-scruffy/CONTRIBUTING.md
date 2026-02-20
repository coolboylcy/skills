# Contributing to KlausNomi

We welcome contributions! Follow these steps to get started:

## Development setup

```bash
# Clone the repository
git clone https://github.com/openclaw/klausnomi.git
cd klausnomi

# Create a virtual environment (using uv or venv)
uv venv venv   # or: python -m venv venv
source venv/bin/activate

# Install the package in editable mode with dev dependencies
pip install -e "[dev]"
```

## Running the test suite

```bash
pytest
```

## Linting & type checking

```bash
ruff check src/   # linting
mypy src/klausnomi  # static type checking
```

## Making changes

1. Create a new branch for your feature or bug fix.
2. Keep the code style consistent (PEP 8, type hints, docstrings).
3. Add or update tests as needed.
4. Run the full test suite and linters before committing.
5. Submit a pull request with a clear description of your changes.

## Documentation

- Keep the `README.md` up‑to‑date with any new commands or usage examples.
- Update `CONTRIBUTING.md` if you add new contribution steps.

Thank you for helping improve KlausNomi!