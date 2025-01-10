# Development environment

```bash
pip install --editable .
```

```bash
branch="main"
sudo pip install --force "git+https://github.com/IoT-balance-project/balance-mqtt-subscriber@$branch"
```

# Testing

```bash
black src
flake8 8
pytest
```

# Release process

1. Increase the veresion number in `pyproject.toml`
2. [Draft a new release](https://github.com/IoT-balance-project/balance-mqtt-subscriber/releases/new) using the [GitHub Release feature](https://docs.github.com/en/repositories/releasing-projects-on-github) on this repository.
3. The `publish.yaml` GitHub Actions workflow will build and upload the package to the [Python Package Index](https://pypi.org/) (PyPI).
