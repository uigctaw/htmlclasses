from typing import Optional

from .htmlclasses import E, ELEMENT_ATTRIBUTES, OWNED_ELEMENTS


def to_string(
        element: E,
        *,
        indent: Optional[str] = None,
        html_doctype: bool = True,
        _cumulative_indent: str = '',
        ) -> str:
    """Serialize an E instance.

    Parameters
    ----------
    element: n/c.
    indent: If it's given the code will be indented accordingly.
    html_doctype: Whether to prepend the DOCTYPE html declaration.
    _cumulative_indent: It's private. Don't use.

    Returns
    -------
    Valid HTML string.
    """

    doctype = '<!DOCTYPE html>' if html_doctype else ''
    doctype = doctype + '\n' if indent and doctype else doctype

    nl = '\n'
    children = f'{"" if indent is None else nl}'.join(
            to_string(
                e(),
                indent=indent,
                html_doctype=False,
                _cumulative_indent=_cumulative_indent + (indent or ''),
                )
            for e in getattr(element, OWNED_ELEMENTS)
            )

    tag = type(element).__name__

    attrs = ' '.join(
            f'{k}="{v}"'
            for k, v in getattr(element, ELEMENT_ATTRIBUTES).items()
            )

    attrs = ' ' + attrs if attrs else ''

    element_str = _calculate_element_str(
            indent=indent,
            cumulative_indent=_cumulative_indent,
            element_text=element.TEXT,
            children_str=children,
            attrs=attrs,
            tag=tag,
            )

    string = doctype + element_str

    return string.rstrip('\n')


def _calculate_element_str(
        *,
        indent: Optional[str],
        cumulative_indent: str,
        element_text: str,
        children_str: str,
        attrs: str,
        tag: str,
        ):

    if indent is None:
        if element_text or children_str:
            return f'<{tag}{attrs}>{element_text}{children_str}</{tag}>'
        else:
            return f'<{tag}{attrs}/>'
    else:
        nl = '\n'
        indent = indent or ''
        if element_text or children_str:

            if children_str:
                children_str = nl + children_str + nl
                suffix_indent = cumulative_indent
            else:
                suffix_indent = ''

            return (
                    f'{cumulative_indent}<{tag}{attrs}>{element_text}'
                    f'{children_str}'
                    f'{suffix_indent}</{tag}>{nl}'
                    )
        else:
            return f'{cumulative_indent}<{tag}{attrs}/>{nl}'
