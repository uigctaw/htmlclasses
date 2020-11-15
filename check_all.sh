#!/bin/bash
./run_tests.sh
./flake8.sh
./mypy.sh
./bandit.sh
