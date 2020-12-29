from htmlclasses.htmlclasses import E, to_string


def to_str(element):
    return to_string(element, indent=None, html_doctype=False)


def test_html_with_no_data():

    class html(E):
        pass

    assert to_string(html()) == '<!DOCTYPE html><html/>'


def test_html_with_data():

    class html(E):
        TEXT = 'Hello world!'

    assert to_string(html()) == (
            '<!DOCTYPE html><html>Hello world!</html>')


def test_html_with_head_and_body():

    class html(E):

        class head(E):
            pass

        class body(E):
            pass

    assert to_string(html()) == (
            '<!DOCTYPE html><html><head/><body/></html>')


def test_duplicate_tags_are_fine():

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


def test_no_need_to_subclass():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'qux'
                quux = 'quz'

    assert to_str(foo()) == '<foo><bar><baz quux="quz">qux</baz></bar></foo>'


def test_indenting_of_elements_with_single_line_texts():

    class foo(E):

        class bar(E):

            class baz:

                TEXT = 'qux'
                quux = 'quz'

            class baz:  # noqa: F811

                TEXT = 'qux2'
                quux = 'quz2'

    actual = to_string(foo(), indent='  ', html_doctype=False)

    assert actual == (
            '<foo>\n'
            '  <bar>\n'
            '    <baz quux="quz">qux</baz>\n'
            '    <baz quux="quz2">qux2</baz>\n'
            '  </bar>\n'
            '</foo>'
            )


def test_indenting_of_multi_line_text():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'foo\nbar\nbaz'

        class bar:  # noqa: F811

            TEXT = 'foo\nbar'

    actual = to_string(foo(), indent='  ', html_doctype=False)

    assert actual == (
            '<foo>\n'
            '  <bar>\n'
            '    <baz>foo\n'
            'bar\n'
            'baz</baz>\n'
            '  </bar>\n'
            '  <bar>foo\n'
            'bar</bar>\n'
            '</foo>'
            )


def test_new_lines_in_text_are_preserved():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'foo\nbar\nbaz'

        class bar:  # noqa: F811

            TEXT = 'foo\nbar'

    actual = to_string(foo(), indent=None, html_doctype=False)

    assert actual == (
            '<foo><bar><baz>foo\nbar\nbaz</baz></bar><bar>foo\nbar</bar></foo>'
            )
