from typing import Iterable
import pandas as pd


def sig_index(number: float, digits: int = 1, one_more_digit: str = '1', decimals: int = 20) -> int:
    """Get index relative to the '.' to get specific significant digits of a number

    Parameters
    ----------
    number: float
        Number to be rounded
    digits: int = 1
        Number of significant digits
    one_more_digit: str = '1'
        Digits that if at the end of the rounded number require 1 additional significant digit
    decimals: int = 20
        Max number of decimal to take into consideration when rounding

    Returns
    -------
    int
        Index relative to the '.' where to cut the number in order to have the right amount of significant digits
    """

    n_str = f'%.{decimals + digits}f' % number
    n_dot = n_str.index('.')
    n_cln = [digit for digit in n_str if digit != '.']

    # Cut the undesired digits
    removing_zeros = True
    digit_count = 0

    for i, digit in enumerate(n_cln):
        if digit in '-0' and removing_zeros:
            continue

        removing_zeros = False

        digit_count += 1

        if digit_count == digits:
            if digit in one_more_digit:
                i += 1
                digit = n_cln[i]

            n_cut = i - n_dot + 1
            return n_cut

    raise Exception("Something went wrong")


def preserve_zeros(number: float, n_digits: int) -> str:
    """Round a number given the last digit position relative to the '.' preserving final zeros
    Similar in behavior to the default round() function

    Parameters
    ----------
    number: float
        Number to be rounded
    n_digits: int
        Index relative to the '.' where to round the number

    Returns
    -------
    str
        Number rounded (of type string in order to preserve final zeros)
    """

    if n_digits <= 0:
        return str(int(round(number, n_digits)))
    return f'{number:.{n_digits}f}'


def significant(number: float, **kwargs) -> str:
    """Round a number to specific significant digits preserving final zeros.
    Faster way to call `zeros(number, sig_index(**kwargs))`

    Parameters
    ----------
    number: float
        Number to be rounded    
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    str
        Number rounded (of type string in order to preserve final zeros)    
    """

    i = sig_index(number, **kwargs)
    n_fin = preserve_zeros(number, i)

    return n_fin


def significant_array(numbers: Iterable[float], **kwargs) -> list[str]:
    """Round a list of numbers to specific significant digits preserving final zeros.

    Parameters
    ----------
    numbers: Iterable[float]
        Numbers to be rounded    
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    list[str]
        Numbers rounded (of type string in order to preserve final zeros)
    """

    n_fin = []

    for number in numbers:
        _n_fin = significant(number, **kwargs)
        n_fin.append(_n_fin)

    return n_fin


def significant_series(numbers: pd.Series, **kwargs) -> pd.DataFrame:
    """Round a pandas.Series of numbers to specific significant digits preserving final zeros.

    Parameters
    ----------
    numbers: pandas.Series
        Numbers to be rounded    
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    pandas.DataFrame
        A dataframe containing 1 column with the name of the numbers pandas.Series
    """

    n_values = significant_array(numbers.values, **kwargs)

    n_fin = pd.Series(n_values).to_frame(name=numbers.name)

    return n_fin


def measure(measure: float, error: float, **kwargs) -> tuple[str, str]:
    """Round a measure based on the decimal of its error preserving final zeros.

    Parameters
    ----------
    measure: float
        Measure to be rounded
    error: float
        Error of the measure that will be used to find the significant digits
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    tuple[str, str]
        - Measure rounded
        - Error rounded (will always be a positive number)
    """

    if error < 0:
        error = -error

    i = sig_index(error, **kwargs)

    m_fin = preserve_zeros(measure, i)
    e_fin = preserve_zeros(error, i)

    return m_fin, e_fin


def measure_array(measures: Iterable[float], errors: Iterable[float], **kwargs) -> tuple[list[str], list[str]]:
    """Round a list of measures based on the decimal of their errors preserving final zeros.

    Parameters
    ----------
    measures: Iterable[float]
        Measure to be rounded
    errors: Iterable[float]
        Error of the measure that will be used to find the significant digits
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    tuple[list[str], list[str]]
        - List of measures rounded
        - List of errors rounded (will always be positive numbers)
    """

    m_fin = []
    e_fin = []

    for value, error in zip(measures, errors, strict=True):
        _m_fin, _e_fin = measure(value, error, **kwargs)
        m_fin.append(_m_fin)
        e_fin.append(_e_fin)

    return m_fin, e_fin


def measure_dataframe(measures: pd.Series, errors: pd.Series, **kwargs) -> pd.DataFrame:
    """Round a pandas.Series of measures based on a pandas.Series of errors preserving final zeros.
    It returns the measures and errors as two separated columns in a pandas.Dataframe

    Parameters
    ----------
    measures: pandas.Series
        Measure to be rounded
    errors: pandas.Series
        Error of the measure that will be used to find the significant digits
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    pandas.DataFrame
        A dataframe containing 2 column with the name of the measures and errors pandas.Series
    """

    m_values, e_values = measure_array(measures.values, errors.values)

    m_fin = pd.Series(m_values).to_frame(name=measures.name)
    e_fin = pd.Series(e_values).to_frame(name=errors.name)

    return pd.concat([m_fin, e_fin], axis=1)


def measure_series(measures: pd.Series, errors: pd.Series, scale: int = 0, format_str: str = r"\num{%(m)s+-%(e)s}", **kwargs) -> pd.DataFrame:
    """Round a pandas.Series of measures based on a pandas.Series of errors preserving final zeros.
    It returns the measures and errors as two separated columns in a pandas.Dataframe

    Parameters
    ----------
    measures: pandas.Series
        Measure to be rounded
    errors: pandas.Series
        Error of the measure that will be used to find the significant digits
    **kwargs
        digits: int = 1
            Number of significant digits
        one_more_digit: str = '1'
            Digits that if at the end of the rounded number require 1 additional significant digit
        decimals: int = 20
            Max number of decimal to take into consideration when rounding

    Returns
    -------
    pandas.DataFrame
        A dataframe containing 2 column with the name of the measures and errors pandas.Series
    """

    m_values, e_values = measure_array(measures.values * 10**-scale, errors.values * 10**-scale)

    return pd.Series([
        format_str % {
            'm': m,
            'e': e,
        }
        for m, e in zip(m_values, e_values)
    ]).to_frame(name=measures.name)
