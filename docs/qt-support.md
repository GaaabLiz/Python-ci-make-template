# Qt Support

Qt support is optional. Use it only if your app uses PySide or PyQt and you need to turn a Qt `.qrc` resource file into Python code.

## Enable the Qt command

1. Keep `qt.mk` next to `Makefile`.
2. In `project.mk`, remove the `#` from `include qt.mk`.
3. Set the Qt paths if your files are not in the example locations.
4. Add the needed Qt tools to the appropriate dependency group in `pyproject.toml`.

The settings are:

- `QT_COMMAND_GEN_RES`: the resource compiler command, usually `pyside6-rcc` or `pyrcc6`
- `QT_QRC_FILE`: your `.qrc` input file
- `QT_RESOURCE_PY`: where to write the generated Python file

Run the generator with:

```sh
make gen-qt-res-py
```

You can pass different file paths for one run:

```sh
make gen-qt-res-py QT_QRC_FILE=res/icons.qrc QT_RESOURCE_PY=myapp/icons_rc.py
```
