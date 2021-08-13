from typing import Optional, NamedTuple

from htmlclasses import E


class Point(NamedTuple):
    x: float
    y: float


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
        if b >= a:
            raise ValueError(
                'Axes must start at low value and end end at higher.'
                + f' Got: start:{a}, end:{b}'
            )

    x_range_greater_than_0 = x_start > 0
    x_range_less_than_0 = x_end < 0
    y_range_greater_than_0 = y_start > 0
    y_range_less_than_0 = y_end < 0

    dotted_len = 40
    arrow_size = 5
    left_margin = 5
    top_margin = arrow_size * 2 + 5

    if x_range_greater_than_0:
        x_intersection = dotted_len / 2
    elif x_range_less_than_0:
        x_intersection = x_axis_length + dotted_len / 2
    else:
        x_fraction_on_left_side = -x_start / (x_end - x_start)
        x_intersection = x_axis_length * x_fraction_on_left_side

    if y_range_greater_than_0:
        y_intersection = y_axis_length + dotted_len / 2 + arrow_size
    elif y_range_less_than_0:
        y_intersection = dotted_len / 2 + arrow_size
    else:
        y_fraction_on_left_side = -y_start / (y_end - y_start)
        y_intersection = y_axis_length * y_fraction_on_left_side + arrow_size

    if x_range_greater_than_0:
        x_lines_kwargs = dict(
            dotted_x_line=dict(
                point_from=Point(0, y_intersection),
                point_to=Point(dotted_len, y_intersection),
                dotted=True,
            ),
            x_line=dict(
                point_from=Point(dotted_len, y_intersection),
                point_to=Point(dotted_len + x_axis_length, y_intersection),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
        )
    elif x_range_less_than_0:
        x_lines_kwargs = dict(
            x_line=dict(
                point_from=Point(0, y_intersection),
                point_to=Point(x_axis_length, y_intersection),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
            dotted_x_line=dict(
                point_from=Point(x_axis_length, y_intersection),
                point_to=Point(dotted_len + x_axis_length, y_intersection),
                marker_end_id='arrow',
                dotted=True,
            ),
        )
    else:
        x_lines_kwargs = dict(
            x_line=dict(
                point_from=Point(0, y_intersection),
                point_to=Point(x_axis_length, y_intersection),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
        )

    if y_range_greater_than_0:
        y_lines_kwargs = dict(
            y_line=dict(
                point_from=Point(x_intersection, arrow_size + y_axis_length),
                point_to=Point(x_intersection, arrow_size),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
            dotted_y_line=dict(
                point_from=Point(
                    x_intersection,
                    arrow_size + y_axis_length + dotted_len,
                ),
                point_to=Point(x_intersection, arrow_size + y_axis_length),
                dotted=True,
            ),
        )
    elif y_range_less_than_0:
        y_lines_kwargs = dict(
            dotted_y_line=dict(
                point_from=Point(x_intersection, arrow_size + dotted_len),
                point_to=Point(x_intersection, arrow_size),
                marker_end_id='arrow',
                dotted=True,
            ),
            y_line=dict(
                point_from=Point(
                    x_intersection,
                    arrow_size + y_axis_length + dotted_len,
                ),
                point_to=Point(x_intersection, arrow_size + dotted_len),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
        )
    else:
        y_lines_kwargs = dict(
            y_line=dict(
                point_from=Point(x_intersection, arrow_size + y_axis_length),
                point_to=Point(x_intersection, arrow_size),
                marker_end_id='value-marker',
                marker_start_id='value-marker',
            ),
        )

    _line = line

    def draw_line(kwargs):
        return _line(color='black', width=2, **kwargs)

    x_line = x_lines_kwargs['x_line']
    # mypy getting confused...
    x0_marker: Point = x_line['point_from']  # type: ignore[assignment]
    x1_marker: Point = x_line['point_to']  # type: ignore[assignment]

    y_line = y_lines_kwargs['y_line']
    y0_marker: Point = y_line['point_from']  # type: ignore[assignment]
    y1_marker: Point = y_line['point_to']  # type: ignore[assignment]

    text_offset = Point(20, 20)

    class g(E):

        transform = f'translate({left_margin} {top_margin})'

        class defs(E):

            class marker:
                id = 'arrow'
                viewBox = f'0 0 {arrow_size * 2} {arrow_size * 2}'
                refX = 0
                refY = arrow_size / 2
                markerWidth = arrow_size * 2
                markerHeight = arrow_size * 2
                orient = 'auto-start-reverse'

                class path:
                    d = (
                            f'M 0 {arrow_size * 0.2}'
                            + f' L {arrow_size} {arrow_size / 2}'
                            + f' L 0 {arrow_size * 0.8} z'
                    )

            class marker:
                id = 'value-marker'
                viewBox = '0 0 10 10'
                refX = 0.25
                refY = 2.5
                orient = 'auto'
                markerWidth = 10
                markerHeight = 10

                class line:
                    x1, y1 = (0, 5)
                    x2, y2 = (0, 0)
                    stroke = 'black'
                    stroke_width = 1

        line = draw_line(x_lines_kwargs['x_line'])
        if x_range_less_than_0 or x_range_greater_than_0:
            line = draw_line(x_lines_kwargs['dotted_x_line'])

        line = draw_line(y_lines_kwargs['y_line'])
        if y_range_less_than_0 or y_range_greater_than_0:
            line = draw_line(y_lines_kwargs['dotted_y_line'])

        class text:

            TEXT = 'x0 value'
            x = x0_marker.x
            y = x0_marker.y + text_offset.y

        class text:

            TEXT = 'x1 value'
            x = x1_marker.x
            y = x1_marker.y + text_offset.y

        class text:

            TEXT = 'y0 value'
            x = y0_marker.x + text_offset.x
            y = y0_marker.y

        class text:

            TEXT = 'y1 value'
            x = y1_marker.x + text_offset.x
            y = y1_marker.y

    return g
