# htmlclasses

Python in, HTML out.

There are templating engines making it possible to write code
in HTML template files. However, I would very much prefer
to be able to write Python that gets converted to HTML 
rather than write Python-like minilanguage engulffed in HTML. 


## Goals

Being able to write unconstrained Python code that is converted to HTML.

## Non-goals

Features geared toward JavaScript.

1. I find using 2 intertwined languages too cumbersome.
2. JavaScript is heavily overused and misued and I would not like to
   encourage it.


## Installation

TBD

## Developing

This project uses poetry: https://github.com/python-poetry/poetry

1. `git clone git@github.com:uigctaw/htmlclasses.git`
2. `poetry install`

### Running tests

1. *./check_all.sh*, which executes:
    1. *./run_tests.sh* - unit tests
    2. *./flake8.sh* - lint
    3. *./mypy.sh* - static type checker
    4. *./bandit.sh* - common securtiy issues checker

## Examples

Every example uses:

```python
from htmlclasses import E
```

### 1. Hello world




## Alternatives

https://pypi.org/project/html
