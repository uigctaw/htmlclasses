# htmlclasses

Python in, HTML out.

There are templating engines making it possible to write code
in HTML template files. However, I would very much prefer
to be able to write Python that gets converted to HTML 
rather than write Python-like mini language engulfed in HTML. 

## Version

0.3.2

## Goals

Generating valid HTML from pure Python code.

## Non-goals

Features geared toward JavaScript.

1. I find using 2 intertwined languages too cumbersome.
2. JavaScript is heavily overused and misused.
   I don't want to add to the problem.


## Installation

`pip install htmlclasses`

## Developing

This project is managed with poetry: https://github.com/python-poetry/poetry

1. `git clone git@github.com:uigctaw/htmlclasses.git`
2. `poetry install`

### Running tests

`./check_all.sh`

## Examples

To convert Python to HTML run:

```python
from htmlclasses import to_string

to_string(html, indent='    ')
```

### Hello World

```python
from htmlclasses import E


class html(E):

    class head:
        pass

    class body:

        class p:

            TEXT = 'Hello, world!'
```

```html
<!DOCTYPE html>
<html>
    <head/>
    <body>
        <p>
            Hello, world!
        </p>
    </body>
</html>
```

### Repeated Elements

```python
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
```

```html
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
```

## Work in progress

SVG utilities for creating plots.

## Alternatives

https://pypi.org/project/html
