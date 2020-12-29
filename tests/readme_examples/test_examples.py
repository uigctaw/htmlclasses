from .generate_checksums import iter_examples
from importlib import import_module
from htmlclasses.htmlclasses import to_string


def test_example_scripts_generate_expected_code():
    failed = []
    for example in iter_examples():
        module = import_module(
                'tests.readme_examples.' + example.name.strip('.py'))
        expected = module.EXPECTED_HTML.strip()
        actual = to_string(module.html(), indent='    ')
        if actual != expected:
            failed.append(example.name)
            print(
                    'Expected:',
                    '----',
                    expected,
                    '----',
                    sep='\n',
                    )
            print()
            print(
                    'Aactual:',
                    '----',
                    actual,
                    '----',
                    sep='\n',
                    )
    assert not failed, failed
