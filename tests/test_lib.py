import numpy as np
import pytest

from htmlclasses import E, to_string
from htmlclasses.lib import svg


def show(svg_stuff):
    """For manual debugging."""
    import tempfile
    import webbrowser

    class html(E):

        class body(E):

            class svg(E):
                width = 1000
                height = 1000

                g = svg_stuff

    with tempfile.TemporaryDirectory() as td:
        with open(path := td + '/myhtml.html', 'w') as fh:
            fh.write(to_string(html, indent=' '))
        webbrowser.open(path)
        breakpoint()


def test_plot_line():
    line = svg.build_line(
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
    g = svg.axes(
            x_range=(-120, -70),
            y_range=(-250, -151),
            x_axis_length=200,
            y_axis_length=100,
            )
    show(g)


@pytest.mark.skip('wip, feature not ready')
def test_2_plots():
    xs1 = np.linspace(-5, 10)
    ys1 = np.sin(xs1) * 2
    g = svg.build_plot(
        points=zip(xs1, ys1),
        x_axis_length=400,
        y_axis_length=300,
        y_axis_name='Just sine',
        x_axis_name='X',
    )
    show(g)


# TODO: add test for META
