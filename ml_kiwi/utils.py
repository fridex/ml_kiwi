#!/usr/bin/env python3
"""Helpers and utilities."""

import sys
import json


def json_dump(dictionary, output_file=None, pretty=True):
    """Dump dictionary to JSON file, do it pretty by default.

    :param dictionary: dictionary to serialize
    :type dictionary: dict|list
    :param output_file: path to output file (defaults to sys.stdout)
    :type output_file: str
    :param pretty: do pretty formatting
    :type pretty: bool
    """
    pretty_json_kwargs = {}
    if pretty:
        pretty_json_kwargs = {
            'sort_keys': True,
            'separators': (',', ': '),
            'indent': 2
        }

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(dictionary, f, **pretty_json_kwargs)
    else:
        json.dump(dictionary, sys.stdout, **pretty_json_kwargs)
