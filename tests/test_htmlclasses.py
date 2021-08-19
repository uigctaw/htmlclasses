import pytest
import textwrap

from htmlclasses import E, to_string


def to_str(element):
    return to_string(element, indent=None, html_doctype=False)


class TestBasics:

    def test_html_with_no_data(self):

        class html(E):
            pass

        assert to_string(html) == '<!DOCTYPE html><html/>'

    def test_html_with_data(self):

        class html(E):
            TEXT = 'Hello world!'

        assert to_string(html) == (
                '<!DOCTYPE html><html>Hello world!</html>')

    def test_html_with_head_and_body(self):

        class html(E):

            class head(E):
                pass

            class body(E):
                pass

        assert to_string(html) == (
                '<!DOCTYPE html><html><head/><body/></html>')


def test_escaping():

    class foo(E):

        TEXT = '</foo>'

    assert to_str(foo) == '<foo>&lt;/foo&gt;</foo>'


def test_duplicate_tags_are_fine():

    class body(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

        class p(E):  # noqa: F811
            TEXT = 'baz'

    assert to_str(body) == '<body><p>foo</p><p>bar</p><p>baz</p></body>'


def test_inheritance_preserves_the_elements_but_not_the_name():

    class body_base(E):

        class p(E):
            TEXT = 'foo'

        class p(E):  # noqa: F811
            TEXT = 'bar'

    class body(body_base):

        class p(E):
            TEXT = 'baz'

    assert to_str(body) == '<body><p>foo</p><p>bar</p><p>baz</p></body>'


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

    assert to_str(body) == (
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

    assert to_str(body) == (
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

    assert to_str(body) == '<body><p>foo</p><p>barbaz</p><p>qux</p></body>'

    class body(get_body('baz2')):

        class p(E):
            TEXT = 'quux'

    assert to_str(body) == '<body><p>foo</p><p>barbaz2</p><p>quux</p></body>'


def test_adding_attributes_through_class_constants():

    class x(E):
        foo = 'bar'

        class p(E):
            TEXT = 'Hello'
            attr1 = 'Hmm'
            class_ = 'Hi'
            with_dash = 'H_i'

    assert to_str(x) == (
        '<x foo="bar"><p attr1="Hmm" class="Hi" with-dash="H_i">Hello</p></x>'
        )


def test_adding_attributes_with_subclass():

    class X(E):
        foo = 'bar'

    class Y(X):
        baz = 'qux'

    assert to_str(Y) == '<Y foo="bar" baz="qux"/>'


def test_no_need_to_subclass():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'qux'
                quux = 'quz'

    assert to_str(foo) == '<foo><bar><baz quux="quz">qux</baz></bar></foo>'


def test_indenting_of_elements_with_single_line_texts():

    class foo(E):

        class bar(E):

            class baz:

                TEXT = 'qux'
                quux = 'quz'

            class baz:  # noqa: F811

                TEXT = 'qux2'
                quux = 'quz2'

    actual = to_string(foo, indent='  ', html_doctype=False)

    assert actual == (
            '<foo>\n'
            '  <bar>\n'
            '    <baz quux="quz">\n'
            '      qux\n'
            '    </baz>\n'
            '    <baz quux="quz2">\n'
            '      qux2\n'
            '    </baz>\n'
            '  </bar>\n'
            '</foo>'
            )


def test_indenting_of_empty_elements():

    class foo(E):

        class bar:
            pass

        class bar:  # noqa: F811

            TEXT = ''

        class bar:  # noqa: F811

            TEXT = 'baz'

    actual = to_string(foo, indent='  ', html_doctype=False)

    assert actual == textwrap.dedent('''
            <foo>
              <bar/>
              <bar>
              </bar>
              <bar>
                baz
              </bar>
            </foo>
            ''').strip()


def test_indenting_of_multi_line_text():

    class foo(E):

        class bar:

            class baz:

                TEXT = 'foo\nbar\nbaz'

        class bar:  # noqa: F811

            TEXT = 'foo\nbar'

    actual = to_string(foo, indent='  ', html_doctype=False)

    assert actual == textwrap.dedent('''
            <foo>
              <bar>
                <baz>
                  foo
                  bar
                  baz
                </baz>
              </bar>
              <bar>
                foo
                bar
              </bar>
            </foo>
            ''').strip()


class TestPreTag:

    def test_new_lines_in_text_are_preserved_in_pre_element(self):

        class foo(E):

            class pre:

                TEXT = 'foo\nbar\nbaz'

            class PRE:

                TEXT = 'abc\nxyz'

            class bar:

                TEXT = 'foo\nbar'

        actual = to_string(foo, indent='  ', html_doctype=False)
        expected = textwrap.dedent('''
                <foo>
                  <pre>foo{nl}bar{nl}baz</pre>
                  <PRE>abc{nl}xyz</PRE>
                  <bar>
                    foo
                    bar
                  </bar>
                </foo>
                ''').strip().format(nl='\n')

        assert actual == expected

    def test_pre_with_no_text_is_fine(self):

        class foo(E):

            class PrE:
                pass

            class pRe:

                TEXT = ''

        actual = to_string(foo, indent='  ', html_doctype=False)
        expected = textwrap.dedent('''
                <foo>
                  <PrE/>
                  <pRe></pRe>
                </foo>
                ''').strip()

        assert actual == expected

    def test_pre_with_multiple_text_fields_is_illegal(self):

        class foo(E):

            class pre(E):

                TEXT = 'foo\nbar\nbaz'
                TEXT = 'foo\nbar'

        with pytest.raises(NotImplementedError):
            to_string(foo)

    def test_pre_with_subelements_is_illegal(self):

        class foo(E):

            class pre:

                class requisite:
                    pass

        with pytest.raises(NotImplementedError):
            to_string(foo)

    def test_content_in_pre_is_escaped(self):

        class foo(E):

            class pre:

                TEXT = ' Hi & hello '

        actual = to_string(foo, indent='  ', html_doctype=False)
        expected = textwrap.dedent('''
                <foo>
                  <pre> Hi &amp; hello </pre>
                </foo>
                ''').strip()

        assert actual == expected


def test_text_can_appear_before_child_element():

    class foo(E):

        TEXT = 'baz'

        class bar(E):

            TEXT = 'bar'

    actual = to_str(foo)

    assert actual == (
            '<foo>baz<bar>bar</bar></foo>'
            )


def test_text_can_appear_after_child_element():

    class foo(E):

        class bar(E):

            TEXT = 'bar'

        TEXT = 'baz'

    actual = to_str(foo)

    assert actual == (
            '<foo><bar>bar</bar>baz</foo>'
            )


def test_text_can_appear_multiple_times_in_various_places():

    class foo(E):

        TEXT = 'foo1'

        class bar(E):

            TEXT = 'bar'

        TEXT = 'foo2'
        TEXT = 'foo3'

        class bar(E):  # noqa: F811

            TEXT = 'bar'

        TEXT = 'foo4'

    actual = to_string(foo, indent='  ', html_doctype=False)

    assert actual == textwrap.dedent('''
            <foo>
              foo1
              <bar>
                bar
              </bar>
              foo2
              foo3
              <bar>
                bar
              </bar>
              foo4
            </foo>
            ''').strip()


def test_simplified_syntax_for_mix_of_text_and_elements():

    class p(E):

        TEXT = E(
            'Do',
            E.em('<em>', attr='ok'),
            'and',
            E.i('<i>'),
            'look similar?',
        )
        TEXT = 'What browser are you using?'

    actual = to_string(p, indent='  ', html_doctype=False)

    assert actual == textwrap.dedent('''
            <p>
              Do
              <em attr="ok">
                &lt;em&gt;
              </em>
              and
              <i>
                &lt;i&gt;
              </i>
              look similar?
              What browser are you using?
            </p>
            ''').strip()


def test_meta_attribute_has_special_treatment():

    class p(E):

        TEXT = 'hello'
        META = 'this is meta'

        class _p:

            TEXT = 'world'
            META = 'so is this'

            class _div:

                TEXT = 'hmmm'
                META = dict(a=1, b=2)

            div = _div

        p = _p

    assert p.META == 'this is meta'
    assert p._p.META == 'so is this'
    assert p._p._div.META == dict(a=1, b=2)
