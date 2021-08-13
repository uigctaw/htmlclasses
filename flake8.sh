#!/bin/bash
poetry run python -m flake8 htmlclasses --ignore=F811,E123,E126,W503
poetry run python -m flake8 tests --ignore=F811,E123,E126,W503
