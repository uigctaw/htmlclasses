from collections.abc import Sequence

from .drawing import core as drawing
from .drawing import plot2d


class NoDataError(Exception):
    pass


class _Points(list):

    def __init__(self, xys):
        super().__init__(xys)
        self.xs, self.ys = zip(*self)
        self.max_x = max(self.xs)
        self.min_x = min(self.xs)
        self.span_x = self.max_x - self.min_x
        self.max_y = max(self.ys)
        self.min_y = min(self.ys)
        self.span_y = self.max_y - self.min_y


def build_2d_plot(
        *,
        points: Sequence[tuple[float, float]],
        plot_height,
        plot_width,
        y_axis_name,
        x_axis_name,
        ):
    """Build an SVG `g` element representing a ... 2D plot.

    Raises
    ------
    NoDataError:
        When no data is supplied or it represents a single point.
    """
    if not points:
        raise NoDataError('No points supplied.')

    points = _Points(points)
    plot = plot2d.Plot2D(
            data_points=points,
            width=plot_width,
            height=plot_height,
            title=f'{y_axis_name}({x_axis_name})',
            )
    svg_g = drawing.transform_to_svg(plot)
    return svg_g
