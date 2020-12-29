#!/bin/bash
poetry run python -m pytest
poetry run python -m build_readme --test
