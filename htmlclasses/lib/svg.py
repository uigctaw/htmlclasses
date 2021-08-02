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
        dotted=False,
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
        if dotted:
            stroke_dasharray = width

    return line


def axes(
        x_range: tuple[float, float],
        y_range: tuple[float, float],
        x_axis_length: float,
        y_axis_length: float,
        ):
    # TODO support for units of length

    x_start, x_end = x_range
    y_start, y_end = y_range

    for a, b in [(x_start, x_end), (y_start, y_end)]:
        assert b > a

    x_range_greater_than_0 = x_start > 0
    x_range_less_than_0 = x_end < 0
    y_range_greater_than_0 = y_start > 0
    y_range_less_than_0 = y_end < 0

    dotted_len = 40
    marker_size = 10

    if x_range_greater_than_0:
        x_intersection = dotted_len / 2
    elif x_range_less_than_0:
        x_intersection = x_axis_length + dotted_len / 2
    else:
        x_fraction_on_left_side = -x_start / (x_end - x_start)
        x_intersection = x_axis_length * x_fraction_on_left_side

    if y_range_greater_than_0:
        y_intersection = y_axis_length + dotted_len / 2 + marker_size
    elif y_range_less_than_0:
        y_intersection = dotted_len / 2 + marker_size
    else:
        y_fraction_on_left_side = -y_start / (y_end - y_start)
        y_intersection = y_axis_length * y_fraction_on_left_side + marker_size

    if x_range_greater_than_0:
        x_lines_kwargs = dict(
            dotted_x_line=dict(
                point_from=(0, y_intersection),
                point_to=(dotted_len, y_intersection),
                dotted=True,
            ),
            x_line=dict(
                point_from=(dotted_len, y_intersection),
                point_to=(dotted_len + x_axis_length, y_intersection),
                marker_end_id='arrow',
                marker_start_id='tick',
            ),
        )
    elif x_range_less_than_0:
        x_lines_kwargs = dict(
            x_line=dict(
                point_from=(0, y_intersection),
                point_to=(x_axis_length, y_intersection),
                marker_start_id='tick',
            ),
            dotted_x_line=dict(
                point_from=(x_axis_length, y_intersection),
                point_to=(dotted_len + x_axis_length, y_intersection),
                marker_end_id='arrow',
                dotted=True,
            ),
        )
    else:
        x_lines_kwargs = dict(
            x_line=dict(
                point_from=(0, y_intersection),
                point_to=(x_axis_length, y_intersection),
                marker_end_id='arrow',
                marker_start_id='tick',
            ),
        )

    if y_range_greater_than_0:
        y_lines_kwargs = dict(
            y_line=dict(
                point_from=(x_intersection, marker_size + y_axis_length),
                point_to=(x_intersection, marker_size),
                marker_end_id='arrow',
                marker_start_id='tick',
            ),
            dotted_y_line=dict(
                point_from=(
                    x_intersection,
                    marker_size + y_axis_length + dotted_len,
                ),
                point_to=(x_intersection, marker_size + y_axis_length),
                dotted=True,
            ),
        )
    elif y_range_less_than_0:
        y_lines_kwargs = dict(
            dotted_y_line=dict(
                point_from=(x_intersection, marker_size + dotted_len),
                point_to=(x_intersection, marker_size),
                marker_end_id='arrow',
                dotted=True,
            ),
            y_line=dict(
                point_from=(
                    x_intersection,
                    marker_size + y_axis_length + dotted_len,
                ),
                point_to=(x_intersection, marker_size + dotted_len),
                marker_start_id='tick',
            ),
        )
    else:
        y_lines_kwargs = dict(
            y_line=dict(
                point_from=(x_intersection, marker_size + y_axis_length),
                point_to=(x_intersection, marker_size),
                marker_end_id='arrow',
                marker_start_id='tick',
            ),
        )

    _line = line

    def l(kwargs):
        return _line(color='black', width=2, **kwargs)

    class g(E):

        class defs(E):

            class marker:
                id = 'arrow'
                viewBox = '0 0 10 10'
                refX = 0
                refY = marker_size / 2
                markerWidth = marker_size / 2
                markerHeight = marker_size / 2
                orient = 'auto-start-reverse'

                class path:
                    d = 'M 0 2 L 10 5 L 0 8 z'

            class marker:
                id = 'tick'
                viewBox = '0 0 5 5'
                refX = 0
                refY = 0
                orient = 'auto-start-reverse'

                class line:
                    x1, y1 = (0, 0)
                    x2, y2 = (0, 20)
                    stroke = 'black'
                    stroke_width = 2

        line = l(x_lines_kwargs['x_line'])
        if x_range_less_than_0 or x_range_greater_than_0:
            line = l(x_lines_kwargs['dotted_x_line'])

        line = l(y_lines_kwargs['y_line'])
        if y_range_less_than_0 or y_range_greater_than_0:
            line = l(y_lines_kwargs['dotted_y_line'])

    return g
