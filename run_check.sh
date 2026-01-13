#!/bin/bash
set -e

echo "Running Ruff Linting..."
uv run ruff check .

echo "Running Ruff Formatting..."
uv run ruff format --check .

echo "Running MyPy Type Checking..."
uv run mypy src

echo "All checks passed!"
