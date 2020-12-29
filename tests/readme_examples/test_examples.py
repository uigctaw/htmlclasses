from .generate_checksums import iter_example_modules
from htmlclasses.htmlclasses import to_string


def test_example_scripts_generate_expected_code():
    failed = []
    for module in iter_example_modules():
        expected = module.EXPECTED_HTML.strip()
        actual = to_string(module.html(), indent='    ')
        if actual != expected:
            failed.append(module.name)
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
