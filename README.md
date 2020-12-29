# htmlclasses

Python in, HTML out.

There are templating engines making it possible to write code
in HTML template files. However, I would very much prefer
to be able to write Python that gets converted to HTML 
rather than write Python-like mini language engulfed in HTML. 


## Goals

Being able to write unconstrained Python code that ends up being
converted into HTML.

## Non-goals

Features geared toward JavaScript.

1. I find using 2 intertwined languages too cumbersome.
2. JavaScript is heavily overused and misused.
   I don't want to add to the problem.


## Installation

TBD

## Developing

This project is managed with poetry: https://github.com/python-poetry/poetry

1. `git clone git@github.com:uigctaw/htmlclasses.git`
2. `poetry install`

### Running tests

`./check_all.sh`

## Examples

### Hello World

This Python code:

```python
from htmlclasses.htmlclasses import E


class html(E):

    class head:
        pass

    class body:

        class p:

            TEXT = 'Hello, world!'
```

Produces this HTML code:

```html
<html>
    <head/>
    <body>
        <p>Hello, world!</p>
    </body>
</html>
```

Which renders as:

<html>
    <head/>
    <body>
        <p>Hello, world!</p>
    </body>
</html>

## Alternatives

https://pypi.org/project/html
