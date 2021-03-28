#!/usr/bin/python3

from dataclasses import dataclass
from importlib import import_module
import argparse
import hashlib
import json
import pathlib
import re


EXAMPLE_FILE_PATTERN = re.compile(r'example_(\w+)\.py')
ALL_EXAMPLES = 'all'
THIS_MODULE_PATH = pathlib.Path(__file__).parent
CHECKSUM_FILE = 'checksums.txt'


@dataclass
class PathText:

    name: str
    text: str

    @property
    def pretty_name(self):
        stripped_name, = EXAMPLE_FILE_PATTERN.match(self.name).groups()
        return stripped_name.replace('_', ' ').title()


def iter_examples():
    examples = filter(
            lambda path: EXAMPLE_FILE_PATTERN.match(path.parts[-1]),
            THIS_MODULE_PATH.glob('*'),
            )
    for example in examples:
        with open(example, 'r') as fh:
            text = fh.read()
        example_file_name = pathlib.Path(example).parts[-1]
        yield PathText(name=example_file_name, text=text)


def iter_example_modules():
    for example in iter_examples():
        module = import_module(
                'tests.readme_examples.' + example.name.strip('.py'))
        yield module


def _calculate_checksums(examples):
    return {
        example.name: hashlib.md5(example.text.encode()).hexdigest()
        for example in iter_examples()
    }


def calculate_checksums():
    return _calculate_checksums(iter_examples())


def read_checksums():
    with open(file_here(CHECKSUM_FILE)) as fh:
        return json.load(fh)


def file_here(name):
    return THIS_MODULE_PATH.joinpath(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--do',
            action='store_true',
            help='Recalculate the checksums',
            )
    args = parser.parse_args()
    if args.do:
        checksums = calculate_checksums()
        with open(file_here(CHECKSUM_FILE), 'w') as fh:
            json.dump(checksums, fh)
    else:
        print('Doing nothing.')
