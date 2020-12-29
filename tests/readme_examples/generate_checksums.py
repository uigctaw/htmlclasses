from collections import namedtuple
import argparse
import hashlib
import json
import pathlib
import re
import yaml


EXAMPLE_FILE_PATTERN = re.compile(r'example_\w+\.py')
ALL_EXAMPLES = 'all'
THIS_MODULE_PATH = pathlib.Path(__file__).parent
CHECKSUM_FILE = 'checksums.txt'

_path_text = namedtuple('PathText', 'name text') 


def iter_examples():
    examples = filter(
            lambda path: EXAMPLE_FILE_PATTERN.match(path.parts[-1]),
            THIS_MODULE_PATH.glob('*'),
            )
    for example in examples:
        with open(example, 'r') as fh:
            text = fh.read()
        example_file_name = pathlib.Path(example).parts[-1]
        yield _path_text(name=example_file_name, text=text)


def _calculate_checksums(examples):
    return {
        example.name: hashlib.md5(example.text.encode()).hexdigest()
        for example in iter_examples()
    }


def calculate_checksums():
    return _calculate_checksums(iter_examples())


def read_checksums():
    with open(file_here(CHECKSUM_FILE)) as fh:
        return yaml.safe_load(fh.read())


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

