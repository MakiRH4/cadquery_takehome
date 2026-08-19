# CadQuery Take-Home

CadQuery/Solidgold take-home assignment.

## Environment setup

### CQ-editor environment (includes CADquery)

```bash
python3.10 -m venv .venv_cqeditor
source .venv_cqeditor/bin/activate
python -m pip install -r requirements-cqeditor.txt
deactivate
```

### Start CQ-editor

```bash
source .venv_cqeditor/bin/activate
cq-editor
```

### WSL specific

If CQ-editor fails to start due to missing Qt/XCB libraries, install the required system dependencies:

```bash
sudo apt update
sudo apt install \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0
```

If CQ-editor displays a black rendering window due to OpenGL/WSLg graphics acceleration. In that case, start it using software rendering and the XCB backend:

```bash
source .venv_cqeditor/bin/activate
LIBGL_ALWAYS_SOFTWARE=1 cq-editor --platform xcb