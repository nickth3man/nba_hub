#!/bin/bash
set -e

echo "Running Cargo Check..."
cargo check --workspace

echo "Running Cargo Test..."
cargo test --workspace

echo "All Rust checks passed!"
