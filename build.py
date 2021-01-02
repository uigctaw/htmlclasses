#!/usr/bin/python3

from tests.readme_examples.generate_checksums import (
        iter_example_modules,
        iter_examples,
)
from htmlclasses import to_string
import argparse
import pathlib
import re


THIS_MODULE_PATH = pathlib.Path(__file__).parent


def file_from_here(*names):
    return THIS_MODULE_PATH.joinpath(*names)


README_TEMPLATE = file_from_here('readme_template.txt')
README_FILE = file_from_here('README.md')
PKG_INIT = file_from_here('htmlclasses', '__init__.py')
PYPROJECT_TOML = file_from_here('pyproject.toml')


def get_formatted_examples():
    formatted = []
    python_code_end = 'EXPECTED_HTML'
    for example, module in zip(iter_examples(), iter_example_modules()):
        html = module.html
        to_html_code = "to_string(html(), indent='    ')"
        formatted.append('To convert Python to HTML run:')
        formatted.append('```python\nfrom htmlclasses import to_string')
        formatted.append(f'{to_html_code}\n```')
        formatted.append('### ' + example.pretty_name)
        python_code, = re.match(
                r'(.*)' + python_code_end,
                example.text,
                re.DOTALL,
                ).groups()
        html_code = eval(to_html_code)
        formatted.append('Python:')
        formatted.append('```python\n' + python_code.strip()  + '\n```')
        formatted.append('HTML:')
        formatted.append('```html\n' + html_code.strip()  + '\n```')
    return '\n\n'.join(formatted)


def get_formatted_readme():
    formatted_examples = get_formatted_examples()
    with open(README_TEMPLATE) as fh:
        readme_template = fh.read()
    readme_text = readme_template.format(
            examples=formatted_examples,
            version=get_version_from_pyproject_toml(),
            )
    return readme_text


def read_package_init():
    with open() as fh:
        readme_template = fh.read()


def get_version_from_init():
    version, _ = _get_version_and_all_but_last_line_from_init()
    return version


def get_formatted_init():
    _, all_but_last_line = _get_version_and_all_but_last_line_from_init()
    version = get_version_from_pyproject_toml()
    all_but_last_line.append(f"__version__ = '{version}'\n")
    return ''.join(all_but_last_line)


def _get_version_and_all_but_last_line_from_init():
    with open(PKG_INIT) as fh:
        module_lines = fh.readlines()
    last_line = module_lines.pop()
    if match := re.match(r"__version__ = '(\d+\.\d+\.\d+)'", last_line):
        version, = match.groups()
        return version, module_lines
    else:
        raise RuntimeError('No version found')
        
        
def get_version_from_pyproject_toml():
    with open(PYPROJECT_TOML) as fh:
        file_lines = fh.readlines()

    for line in file_lines:
        if match := re.match(r'version = "(\d+\.\d+\.\d+)"', line):
            version, = match.groups()
            return version
    else:
        raise RuntimeError('No version found')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--do',
            action='store_true',
            help='Generate README.md, package __init__.py',
            )
    parser.add_argument(
            '--test',
            action='store_true',
            help='Test the readme and version are up to date',
            )
    args = parser.parse_args()

    if args.do or args.test:
        if args.do:
            readme_text = get_formatted_readme()
            with open(README_FILE, 'w') as fh:
                fh.write(readme_text)

            init_text = get_formatted_init()
            with open(PKG_INIT, 'w') as fh:
                fh.write(init_text)

        if args.test:
            expected_readme_text = get_formatted_readme()
            with open(README_FILE) as fh:
                current_readme_text = fh.read()
            assert expected_readme_text == current_readme_text

            version_from_init = get_version_from_init()
            version_from_pyproject_toml = get_version_from_pyproject_toml()
            assert version_from_init == version_from_pyproject_toml
    else:
        print('Doing nothing.')

