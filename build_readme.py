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
README_TEMPLATE = 'readme_template.txt'
README_FILE = 'README.md'


def file_here(name):
    return THIS_MODULE_PATH.joinpath(name)


def get_formatted_examples():
    formatted = []
    python_code_end = 'EXPECTED_HTML'
    for example, module in zip(iter_examples(), iter_example_modules()):
        formatted.append('### ' + example.pretty_name)
        python_code, = re.match(
                r'(.*)' + python_code_end,
                example.text,
                re.DOTALL,
                ).groups()
        html_code = to_string(
                module.html(), 
                indent='    ', 
                html_doctype=False,
                )
        formatted.append('This Python code:')
        formatted.append('```python\n' + python_code.strip()  + '\n```')
        formatted.append('Produces this HTML code:')
        formatted.append('```html\n' + html_code.strip()  + '\n```')
        formatted.append('Which renders as:')
        formatted.append(html_code.strip())
    return '\n\n'.join(formatted)


def get_formatted_readme():
    formatted_examples = get_formatted_examples()
    with open(file_here(README_TEMPLATE)) as fh:
        readme_template = fh.read()
    readme_text = readme_template.format(examples=formatted_examples)
    return readme_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--do',
            action='store_true',
            help='Generate README.md',
            )
    parser.add_argument(
            '--test',
            action='store_true',
            help='Test the readme is up to date',
            )
    args = parser.parse_args()

    if args.do and args.test:
        raise RuntimeError('I am confused')
    elif args.do:
        readme_text = get_formatted_readme()
        with open(file_here(README_FILE), 'w') as fh:
            fh.write(readme_text)
    elif args.test:
        expected_readme_text = get_formatted_readme()
        with open(file_here(README_FILE)) as fh:
            current_readme_text = fh.read()
        assert expected_readme_text == current_readme_text
    else:
        print('Doing nothing.')

