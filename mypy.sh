#!/bin/bash
poetry run python -m mypy --show-error-codes htmlclasses
poetry run python -m mypy --show-error-codes tests
