import inspect
import types

OWNED_ELEMENTS = '_OWNED_ELEMENTS'
ELEMENT_ATTRIBUTES = '_ELEMENT_ATTRIBUTES'

OWNED_ELEMENT_INSTANCES = '_OWNED_ELEMENT_INSTANCES'
_TEXT_ATTRIBUTE_NAME = 'TEXT'


class _Element:
    pass


def _is_elem_attribute(name):
    return not name.startswith('_') and name != _TEXT_ATTRIBUTE_NAME


def _to_elem_attr_name(name):
    return name.rstrip('_').replace('_', '-')


def _is_elem_class(value):
    return inspect.isclass(value) and issubclass(value, _Element)


def _can_be_converted_to_element_class(name, value):
    # Save a few key strokes by not having to type `class foo(E):`
    # and instead just write `class foo:`.
    #
    # Attributes that meet the requirements will be
    # converted to subclasses of _Element.
    return (
            inspect.isclass(value)
            and not issubclass(value, _Element)
            and not name.startswith('_')
            )


def _create_element_class(name, value):
    """Covert plain `class foo:` to sublcass of `_Element`"""

    def populate_namespace(ns):
        ns[_TEXT_ATTRIBUTE_NAME] = ns.get(_TEXT_ATTRIBUTE_NAME, '')
        for k, v in value.__dict__.items():
            ns[k] = v

    new = types.new_class(
            name,
            (_Element,),
            kwds=dict(metaclass=_Meta),
            exec_body=populate_namespace,
            )

    return new


class _DictForCollectingElements(dict):

    def __init__(self):
        """Collect some items on the fly.

        Python class cannot have 2 different attributes
        under the same name.
        But given that we want to use Python classes to construct
        HTML elements, we have to circumvent this constraint.
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


class _Meta(type):

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        d = _DictForCollectingElements()
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


class E(_Element, metaclass=_Meta):
    """Subclass this element to create an HTML tree.

    Example:

        class html(E):
            class head(E):
                class title(E):
                    TEXT = 'This is a title'

                class meta(E):
                    charset = 'UTF-8'

                class meta(E):
                    # note the duplicated class names - that's fine
                    name = 'description'
                    content = 'usage example'

            class body(E):
                ...
    """

    TEXT = ''
