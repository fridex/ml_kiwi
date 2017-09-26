# kiwi.com Machine Learning Weekend

See description at [https://www.kiwi.com/mlweekend/](https://kiwi.com/mlweekend)

## Installation

This project is not available on PyPI, so to install it (directly master) issue:
```bash
$ pip3 install git+https://github.com/fridex/ml_kiwi
```

Once installation succeeds, run:

```
$ ml-kiwi --help
Usage: ml-kiwi [OPTIONS]

  Compute degree of polynomial for kiwi.com's weekend machine learning
  session.

Options:
  -i, --input PATH      Input file to be used - if omitted, remote API is
                        called to retrieve values.
  -o, --output PATH     Output file to be used - if omitted, defaults to
                        stdout).
  --output-image PATH   Output file where interpolation image should be
                        stored.
  --max-degree INTEGER  Maximal degree of fitting polynomial (default: 100).
  --min-degree INTEGER  Minimal degree of fitting polynomial (default: 1)
  --x-from FLOAT        Value on x axis to start with data gathering from API
                        (default: -100.000000).
  --x-to FLOAT          Value on x axis that shouldn't be reached when
                        gathering data from API (default: 100.000000).
  --x-step FLOAT        Step on x axis to start with (default: 0.050000).
  -v, --verbose         Turn on debug messages.
  --no-pretty           Turn off pretty formatted output.
  --no-show-plot        Do not show plot results.
  --help                Show this message and exit.
```

## Troubleshooting

I'm getting the following traceback when running `ml-kiwi` executable:

```
[root@host /]# ml-kiwi 
Traceback (most recent call last):
  File "/usr/bin/ml-kiwi", line 10, in <module>
    from ml_kiwi import Defaults, DataSource, do_interpolate, do_plot, json_dump
  File "/usr/lib/python3.5/site-packages/ml_kiwi/__init__.py", line 12, in <module>
    from .lib import DataSource
  File "/usr/lib/python3.5/site-packages/ml_kiwi/lib.py", line 11, in <module>
    import matplotlib.pyplot as plt
  File "/usr/lib64/python3.5/site-packages/matplotlib/pyplot.py", line 115, in <module>
    _backend_mod, new_figure_manager, draw_if_interactive, _show = pylab_setup()
  File "/usr/lib64/python3.5/site-packages/matplotlib/backends/__init__.py", line 32, in pylab_setup
    globals(),locals(),[backend_name],0)
  File "/usr/lib64/python3.5/site-packages/matplotlib/backends/backend_tkagg.py", line 6, in <module>
    from six.moves import tkinter as Tk
  File "/usr/lib/python3.5/site-packages/six.py", line 92, in __get__
    result = self._resolve()
  File "/usr/lib/python3.5/site-packages/six.py", line 115, in _resolve
    return _import_module(self.mod)
  File "/usr/lib/python3.5/site-packages/six.py", line 82, in _import_module
    __import__(name)
ImportError: No module named 'tkinter'
```

You need to install Python3 compliant version of tkinter (on Fedora):

```bash
$ dnf install python3-tkinter
$ # alternatively for deb based distributions
$ # apt-get install python3-tkinter
```

# Output

The script will by default query endpoint provided by kiwi.com and check for y values for the given x (x and step on x axis adjustable via CLI arguments). These values are used for interpolating polynomial (one can explicitly specify polynomial degree via CLI arguments). The result is plotted and, if requested, stored to output file.

The resulting JSON can be re-used for computing interpolating polynomial again, point to it using `--input` parameter. The API endpoint will not be queried in that case, but collected data would be reused.

## Example output

You can find examples of kiwi.com input in `results` directory. The script was run with default values as follows:
```bash
$ ml-kiwi -o results/output.json --output-image results/output.png
```

## License

MIT
