#!/bin/bash
poetry run mypy --show-error-codes htmlclasses --disable-error-code no-redef
poetry run mypy --show-error-codes tests --disable-error-code no-redef
