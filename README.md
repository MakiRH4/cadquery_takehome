# CadQuery Take-Home

CadQuery/Solidgold take-home assignment.

## Environment setup

Two separate virtual environments are used:

- `.venv_cadquery` — CadQuery development
- `.venv_cqeditor` — CQ-editor and its GUI dependencies

### CadQuery environment

```bash
python3.10 -m venv .venv_cadquery
source .venv_cadquery/bin/activate
python -m pip install -r requirements-cadquery.txt
deactivate
```

### CQ-editor environment

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