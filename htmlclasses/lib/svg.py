from typing import Optional, Union

from htmlclasses import E


def line(
        *,
        point_from: tuple[float, float],
        point_to: tuple[float, float],
        color: str,
        width: str,
        marker_start_id: Optional[str] = None,
        marker_end_id: Optional[str] = None,
        ):

    class line(E):
        x1, y1 = point_from
        x2, y2 = point_to
        stroke = color
        stroke_width = width
        if marker_start_id:
            marker_start = f'url(#{marker_start_id})'
        if marker_end_id:
            marker_end = f'url(#{marker_end_id})'

    return line


def axes(
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        x_axis_length: float,
        y_axis_length: float,
        ):
    # assuming axes are intersecting
    # TODO: when it's not the case

    # TODO support for units of length

    x_start, x_end = x_range
    y_start, y_end = y_range

    for a, b in [(x_start, x_end), (y_start, y_end)]:
        assert b > a
        assert b >= 0

    x_fraction_on_left_side = -x_start / (x_end - x_start)
    y_fraction_on_top_side = -y_start / (y_end - y_start)

    point_0 = (
            x_axis_length * x_fraction_on_left_side,
            y_axis_length * y_fraction_on_top_side,
            )
    x0, y0 = point_0

    l = line

    _marker_size = 10

    class g(E):

        class defs:

            class marker:
                id = 'arrow'
                viewBox = '0 0 10 10'
                refX = 0
                refY = _marker_size / 2
                markerWidth = _marker_size / 2
                markerHeight = _marker_size / 2
                orient = 'auto-start-reverse'

                class path:
                    d = 'M 0 2 L 10 5 L 0 8 z'

        # x axis
        line = l(
                point_from=(0, y0 + _marker_size),
                point_to=(x_axis_length, y0 + _marker_size),
                color='black',
                width='2',
                marker_end_id='arrow',
                )
        # x axis left extension  
        if _x_range_greater_than_0:
            ...
        # x axis right extension
        if _x_range_less_than_0:
            ...

        # y axis
        line = l(
                point_from=(x0, y_axis_length + _marker_size),
                point_to=(x0, _marker_size),
                color='black',
                width='2',
                marker_end_id='arrow',
                )
        # y axis top extension
        if _y_range_greater_than_0:
        # y axis bottom extension
   
    return g
