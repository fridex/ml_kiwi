#!/usr/bin/env python3
"""Compute interpolating polynomial for kiwi.com machine learning weekend."""

import logging

import anymarkup
import progressbar
import daiquiri
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab

from .errors import InputError


daiquiri.setup(level=logging.INFO)
_logger = daiquiri.getLogger(__name__)


class Defaults(object):
    """Default values if not explicitly provided."""

    X_FROM = -100.0
    X_TO = 100.0
    X_STEP = 0.05
    MIN_DEGREE = 1
    MAX_DEGREE = 100


class DataSource(object):
    """Input data sources."""

    _API_ENDPOINT = 'http://165.227.157.145:8080/api/do_measurement?x={x}'

    @classmethod
    def get_data_api(cls, x_from, x_to, x_step):
        """Retrieve data from remote API server.

        :param x_from: get input starting with set x_from
        :param x_from: float
        :param x_to: gather input until x_to
        :type x_to: float
        :param x_step: incremental step
        :type x_step: float
        :return: tuple, x and y values of function to be interpolated
        :rtype: tuple
        """
        if x_from > x_to:
            raise InputError("x_from cannot be equal/bigger then x_to")

        if x_step <= 0.0:
            raise InputError("x_step has to be non-zero and positive")

        x = x_from
        x_values = []
        y_values = []

        _logger.info("Collecting data from remote API...")
        bar = progressbar.ProgressBar()
        for _ in bar(range(int((x_to - x_from) / x_step))):

            response = requests.get(cls._API_ENDPOINT.format(x=x))
            response.raise_for_status()
            _logger.debug("API responded for x=%f: %s", x, response.json())

            y = response.json()['data']['y']

            if y:
                # y values could be None, omit them in that case
                x_values.append(x)
                y_values.append(y)
            else:
                _logger.debug("Dropping y - no value for x=%f", x)

            x += x_step

        return x_values, y_values

    @staticmethod
    def get_data_file(file_path):
        """Retrieve data from local file.

        :param file_path: path to file to read data from
        :type file_path: str
        :return: tuple, x and y values of function to be interpolated
        :rtype: tuple
        """
        _logger.info("Collecting data from local file '%s'...", file_path)
        content = anymarkup.parse_file(file_path)
        x_values, y_values = content['x'], content['y']
        if len(x_values) != len(y_values):
            raise InputError("x and y vectors should be of same shape, got %d and %d (x and y) instead"
                             % (len(x_values), len(y_values)))

        return x_values, y_values


def do_interpolate(x_values, y_values, min_degree, max_degree):
    """Perform interpolating on x and y values.

    :param x_values: x values to be used for interpolating
    :type x_values: list
    :param y_values: y values to be used for interpolating
    :type y_values: list
    :param min_degree: minimal degree to be used for interpolating polynomial
    :type min_degree: int
    :param max_degree: maximum degree to be used for interpolating polynomial
    :type max_degree: int
    :return: best and all results for interpolating polynomials of different degree
    :rtype: tuple
    """
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    _logger.debug("x_values: %s", x_values)
    _logger.debug("y_values: %s", y_values)

    results = []
    best = None
    overfit_reported = False
    for degree in range(min_degree, max_degree):
        _logger.info("Computing interpolating polynomial for degree %d", degree)
        fit = np.polyfit(x_values, y_values, degree, full=True)
        _logger.debug("Result for polyfit: %s", fit)
        results.append({
            'coefficients': tuple(fit[0]),
            'squared_error': fit[1][0] if fit[1] else 0.0
        })

        if not best:
            best = results[-1]
        elif best and best['squared_error'] > results[-1]['squared_error']:
            best = results[-1]
        elif best and best['squared_error'] == 0.0 \
                and results[-1]['squared_error'] == 0.0 and not overfit_reported:
            _logger.warning('Multiple results with squared error equal to 0.0 found, overfitting data set?')
            overfit_reported = True

    return best, results


def do_plot(x, y, coefficients, show_plot=True, output_image=None):
    """Plot interpolating polynomial.

    :param x: interpolated x values
    :type x: list
    :param y: interpolated y values
    :type y: list
    :param coefficients: found coefficients when interpolation was performed
    :type coefficients: list
    :param show_plot: show plot to user (requires user's interaction)
    :type show_plot: bool
    :param output_image: path to output image file to be used for storing plot
    :type output_image: str
    """
    if not show_plot and not output_image:
        return

    f = np.poly1d(coefficients)
    x_new = np.linspace(x[0], x[-1])
    y_new = f(x_new)

    plt.plot(x, y, 'x', x_new, y_new)
    pylab.title('Interpolating polynomial')
    fig = plt.gcf()

    if show_plot:
        fig.show()
        input('Press <Enter> to continue...')

    if output_image:
        fig.savefig(output_image)
