#!/bin/bash
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place . --exclude=__init__.py
black . --exclude="\.venv"
isort .
