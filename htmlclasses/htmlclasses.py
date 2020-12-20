from typing import Optional
import inspect
import types

OWNED_ELEMENTS = '__OWNED_ELEMENTS'
OWNED_ELEMENT_INSTANCES = '__OWNED_ELEMENT_INSTANCES'
ELEMENT_ATTRIBUTES = '__ELEMENT_ATTRIBUTES'
TEXT = 'TEXT'


class _Element:
    pass


def _is_elem_attribute(name):
    return not name.startswith('_') and name != TEXT


def _to_elem_attr_name(name):
    return name.rstrip('_').replace('_', '-')


def _is_elem_class(value):
    return inspect.isclass(value) and issubclass(value, _Element)


def _can_be_converted_to_element_class(name, value):
    # Save few key strokes by not having to type `class foo(E):`
    # and instead just write `class foo:`.
    #
    # Attributes that meet the requirements bekiw will be
    # converted to subclasses of _Element.
    return (
            inspect.isclass(value)
            and not issubclass(value, _Element)
            and not name.startswith('_')
            )


def _create_element_class(name, value):
    """Covert plain `class foo:` to sublcass of `_Element`"""

    def populate_namespace(ns):
        ns[TEXT] = ns.get(TEXT, '')
        for k, v in value.__dict__.items():
            ns[k] = v

    new = types.new_class(
            name,
            (_Element,),
            kwds=dict(metaclass=Meta),
            exec_body=populate_namespace,
            )

    return new


class DictForCollectingElements(dict):

    def __init__(self):
        """Collect some (class) attributes on the fly.

        Python class cannot have 2 different attributes
        under the same name.
        But given that we want to use Python classes to construct
        html elements we have to circumvent this constraint.
        """
        super().__init__()
        self[OWNED_ELEMENTS] = []
        self[ELEMENT_ATTRIBUTES] = {}

    def __setitem__(self, name, value):
        if _is_elem_class(value):
            self[OWNED_ELEMENTS].append(value)
        elif _can_be_converted_to_element_class(name, value):
            self[name] = _create_element_class(name, value)
        elif _is_elem_attribute(name):
            self[ELEMENT_ATTRIBUTES][_to_elem_attr_name(name)] = value
        else:
            super().__setitem__(name, value)


class Meta(type):

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        d = DictForCollectingElements()
        elements_owned_by_bases = sum(
                [getattr(base, OWNED_ELEMENTS, []) for base in bases],
                [],
                )
        d[OWNED_ELEMENTS].extend(elements_owned_by_bases)

        base_element_attributes = {
                k: v
                for base in bases
                for k, v in getattr(base, ELEMENT_ATTRIBUTES, {}).items()
        }
        d[ELEMENT_ATTRIBUTES] = base_element_attributes

        return d


class E(_Element, metaclass=Meta):

    TEXT = ''


def to_string(
        element: E,
        *,
        indent: Optional[str] = None,
        prepend_doctype: bool = True,
        _parent_indent: str = '',
        ) -> str:
    """Serialize an E instance.

    Parameters
    ----------
    element: n/c.
    indent: If it's given the code will be indented accordingly.
        Multi line TEXT can produce ugly results, because it's not given
        any special treatment.
    prepend_doctype: Whether to prepend the DOCTYPE html declaration.
    _parent_indent: It's private. Don't use.

    Returns
    -------
    Valid (hopefully) HTML string.
    """

    doctype = '<!DOCTYPE html>\n' if prepend_doctype else ''
    indent = indent or ''

    children = ''.join(
            to_string(
                e(),
                indent=indent,
                prepend_doctype=False,
                _parent_indent=_parent_indent + indent,
                )
            for e in getattr(element, OWNED_ELEMENTS)
            )

    tag = type(element).__name__

    attrs = ' '.join(
            f'{k}="{v}"'
            for k, v in getattr(element, ELEMENT_ATTRIBUTES).items()
            )

    attrs = ' ' + attrs if attrs else ''
    line_break = '\n' if indent and children else ''

    if element.TEXT == '' and not children:
        tag = f'{_parent_indent}<{tag}{attrs}/>{line_break}'
    else:
        tag = (
                f'{_parent_indent}<{tag}{attrs}>{element.TEXT}{line_break}'
                f'{children}{line_break}'
                f'{line_break and _parent_indent}</{tag}>'
                )

    string = doctype + tag

    return string
