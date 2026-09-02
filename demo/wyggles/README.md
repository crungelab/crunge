# Wyggles :bug:

## Install

This package requires Cairo.  Either enter this on Ubuntu or visit https://www.cairographics.org/download/

```bash
sudo apt install libcairo2-dev
```

## Development

```bash
hatch shell
pip install -e ../.. # installs crunge.abt into the wyggles virtual environment
```

## Run

```bash
cd examples/wyggles
hatch shell
python -m wyggles
```