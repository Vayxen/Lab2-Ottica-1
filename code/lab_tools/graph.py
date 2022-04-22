from typing import Literal, Optional


def size(
    width: float,
    fraction: float = 1.0,
    subplots: tuple[int, int] = (1, 1),
    ratio: float = (5**(1/2) - 1) / 2,
    unit: Literal['pt', 'cm', 'in'] = 'pt',
    to_inches: Optional[float] = None,
) -> tuple[float, float]:
    """Given the page width in the specified unit and the figure aspect ratio, returns the width and height (in inches) of the figure

    Parameters
    ----------
    width: float
        width of the page in [unit]
    fraction: float, usually between 0 and 1
        fraction of page width that the image can fill
        (default is 1)
    subplots: tuple[int, int]
        number of rows and columns of the figure's subplots
        (default is (1, 1))
    ratio: float
        ratio width / height
        (default is golden ratio in portrait mode)
    unit: Literal['pt', 'cm', 'in']
        name of the unit of the width value
        (default is 'pt')
    to_inches: Optional[float]
        custom unit conversion number since the return unit is inches, overwrites unit
        (default is None)

    Returns
    -------
    tuple[float, float]
        figure (width, height) in inches
    """
    fig_width = width * fraction

    if to_inches is None:
        match unit:
            case 'pt':
                to_inches = 1 / 72.27
            case 'cm':
                to_inches = 1 / 2.54
            case 'in':
                to_inches = 1
            case _:
                raise NotImplementedError(
                    f'{unit} is not known. To add a custom unit conversion number use the parameter to_inches')

    fig_width_in = fig_width * to_inches
    fig_height_in = fig_width_in * ratio * (subplots[0] / subplots[1])

    return fig_width_in, fig_height_in
