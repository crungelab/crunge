# Hatch

## Setting the project

```bash
hatch config set projects.crunge /home/kurt/Dev/crunge
```

## Setting the project for the package directory

The following needs to go in crunge/pkg/.envrc

```bash
# Every subdirectory will inherit the HATCH_PROJECT environment variable
export HATCH_PROJECT=crunge
```

```bash
hatch shell -v
```