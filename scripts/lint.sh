

set -e
set -x

mypy .
flake8 .
black . --check --exclude="\.venv"
isort . --check-only
