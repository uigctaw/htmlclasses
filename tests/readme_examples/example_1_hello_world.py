from htmlclasses import E


class html(E):

    class head:
        pass

    class body:

        class p:

            TEXT = 'Hello, world!'


EXPECTED_HTML = '''
<!DOCTYPE html>
<html>
    <head/>
    <body>
        <p>
            Hello, world!
        </p>
    </body>
</html>
'''
