import pytest
from htmlclasses import to_string
from htmlclasses.lib import svg


def show(svg):
    """For manual debugging."""
    import tempfile
    import webbrowser
    with tempfile.TemporaryDirectory() as td:
        with open(path := td + '/myhtml.html', 'w') as fh:
            fh.write(
                f'<!DOCTYPE html><html><body>'
                f'<svg width="1000" height="1000">{svg}</svg></body></html>')
        webbrowser.open(path)
        breakpoint()


def test_plot_line():
    line = svg.line(
            point_from=(4, 5.5),
            point_to=(53.5, 126),
            color='blue',
            width=2,
            )

    string = to_string(line, html_doctype=False)
    assert string == (
                    '<line x1="4" y1="5.5" x2="53.5" y2="126"'
                    + ' stroke="blue" stroke-width="2"/>'
                    )


@pytest.mark.skip('wip, feature not ready')
def test_plot_axes_x_range_is_all_greater_than_0():
    axes = svg.axes(
            x_range=(-120, -70),
            y_range=(-250, -151),
            x_axis_length=200,
            y_axis_length=100,
            )
    string = to_string(axes, html_doctype=False)
    show(string)
    assert string == (
        '<g>'
        '<defs>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="0" refY="5.0"'
        ' markerWidth="5.0" markerHeight="5.0" orient="auto-start-reverse">'
        '<path d="M 0 2 L 10 5 L 0 8 z"/>'
        '</marker>'
        '</defs>'
        '<line x1="0" y1="110.0" x2="200" y2="110.0" stroke="black"'
        ' stroke-width="2" marker-end="url(#arrow)"/>'
        '<line x1="100.0" y1="210" x2="100.0" y2="10" stroke="black"'
        ' stroke-width="2" marker-end="url(#arrow)"/>'
        '</g>'
        )
