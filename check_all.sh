#!/bin/bash
set -e

./run_tests.sh
./flake8.sh
./bandit.sh
./spelling.sh
