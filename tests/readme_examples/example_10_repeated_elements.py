from htmlclasses import E


class html(E):

    class head(E):  # Must sublcass if repeating tags

        class meta:
            name = 'description'
            content = 'Framework usage examples'

        class meta:  # type: ignore[no-redef]  # noqa: F811
            name = 'keywords'
            content = 'Python, HTML'

    class body:

        class p:

            TEXT = 'Hello, world!'


EXPECTED_HTML = '''
<!DOCTYPE html>
<html>
    <head>
        <meta name="description" content="Framework usage examples"/>
        <meta name="keywords" content="Python, HTML"/>
    </head>
    <body>
        <p>
            Hello, world!
        </p>
    </body>
</html>
'''
