#!/bin/bash

source .venv/bin/activate
LIBGL_ALWAYS_SOFTWARE=1 cq-editor --platform xcb
