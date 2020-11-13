from htmlclasses.htmlclasses import E, to_string


def to_str(element):
    return to_string(
            element, indent=False, encoding=None, prepend_doctype=None)


def test_html_with_no_data():

    class html(E):
        pass

    assert to_string(html(), encoding=None) == '<!DOCTYPE html>\n<html/>'


def test_html_with_data():

    class html(E):
        TEXT = 'Hello world!'

    assert to_string(html(), encoding=None) == (
            '<!DOCTYPE html>\n<html>Hello world!</html>')


def test_html_with_head_and_body():

    class html(E):

        class head(E):
            pass

        class body(E):
            pass

    assert to_string(html(), indent=False, encoding=None) == (
            '<!DOCTYPE html>\n<html><head/><body/></html>')


def test_dupe_tags_are_fine():

    class body(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

        class p(E):  # noqa: F811
            TEXT = 'baz'

    assert to_str(body()) == '<body><p>foo</p><p>bar</p><p>baz</p></body>'


def test_inheritance_preserves_the_elements_but_not_the_name():

    class body_base(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

    class body(body_base):

        class p(E):
            TEXT = 'baz'

    assert to_str(body()) == '<body><p>foo</p><p>bar</p><p>baz</p></body>'


def test_multiple_inheritence_preserves_all_elements():

    class body_base_1(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

    class body_base_2(E):

        class p(E):
            TEXT = 'baz'

    class body(body_base_1, body_base_2):

        class p(E):
            TEXT = 'qux'

    assert to_str(body()) == (
            '<body><p>foo</p><p>bar</p><p>baz</p><p>qux</p></body>')


def test_deep_inheritence_preserves_all_elements():

    class body_base_1(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

    class body_base_2(body_base_1):

        class p(E):
            TEXT = 'baz'

    class body(body_base_2):

        class p(E):
            TEXT = 'qux'

    assert to_str(body()) == (
            '<body><p>foo</p><p>bar</p><p>baz</p><p>qux</p></body>')


def test_reuse():

    def get_body(second_p_suffix):

        class body(E):

            class p(E):
                TEXT = 'foo'

            class p():  # noqa: F811E
                TEXT = 'bar' + second_p_suffix

        return body

    class body(get_body('baz')):

        class p(E):
            TEXT = 'qux'

    assert to_str(body()) == '<body><p>foo</p><p>barbaz</p><p>qux</p></body>'

    class body(get_body('baz2')):

        class p(E):
            TEXT = 'quux'

    assert to_str(body()) == '<body><p>foo</p><p>barbaz2</p><p>quux</p></body>'


def test_adding_attributes_through_class_constants():

    class x(E):
        foo = 'bar'

        class p(E):
            TEXT = 'Hello'
            attr1 = 'Hmm'
            class_ = 'Hi'
            with_dash = 'H_i'

    assert to_str(x()) == (
        '<x foo="bar"><p attr1="Hmm" class="Hi" with-dash="H_i">Hello</p></x>'
        )


def test_adding_attributes_with_subclass():

    class X(E):
        foo = 'bar'

    class Y(X):
        baz = 'qux'

    assert to_str(Y()) == '<Y foo="bar" baz="qux"/>'


def test_bytes():

    class foo(E):
        pass

    assert b'<foo/>' == to_string(foo(), prepend_doctype=None)


def test_no_need_to_subclass():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'qux'
                quux = 'quz'

    assert to_str(foo()) == '<foo><bar><baz quux="quz">qux</baz></bar></foo>'


def test_indent_print():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'qux'
                quux = 'quz'

    actual = to_string(foo(), indent='  ', prepend_doctype=None, encoding=None)
    assert actual == (
            '<foo>\n'
            '  <bar>\n'
            '    <baz quux="quz">qux</baz>\n'
            '  </bar>\n'
            '</foo>'
            )
