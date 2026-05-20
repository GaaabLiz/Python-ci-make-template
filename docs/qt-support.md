# Qt Support

Qt support is optional and lives in `qt.mk`.

## Enable it

1. Keep `qt.mk` next to `Makefile`
2. Uncomment `include qt.mk` in `project.mk`
3. Override the Qt variables before the include if needed

## Main variables

- `QT_COMMAND_GEN_RES`: resource compiler command, usually `pyside6-rcc` or `pyrcc6`
- `QT_QRC_FILE`: source `.qrc` file
- `QT_RESOURCE_PY`: generated Python resource module output path

## Target

Compile the Qt resource file into a Python module:

```bash
make gen-qt-res-py
```

Example with overrides:

```bash
make gen-qt-res-py QT_QRC_FILE=res/icons.qrc QT_RESOURCE_PY=myapp/icons_rc.py
```

## Requirement

The required Qt tooling must be installed in the `uv` environment. For PySide6 projects, that usually means adding `pyside6` to the appropriate dependency group.