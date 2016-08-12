#!/usr/bin/env python
"""
smap_nepse

Usage:
    smap_nepse scrapper [<path>]
    smap_nepse cleancsv <source> <destination>
    smap_nepse cleanall <source> [<destination>]
    smap_nepse csvtohdf <source> <destination>
    smap_nepse alltohdf <source> [<destination>]
    smap_nepse build_hdfstore <source> [<destination>]
    smap_nepse plot <name> [--cols=<arg>...] [--plot_kind=<arg>] [--start_date=<arg> ] [--end_date=<arg>]
    smap_nepse comparision_plot <name>... --cols=<arg>... --plot_kind=<arg> [--start_date=<arg>] [--end_date=<arg>]
    smap_nepse --version
    smap_nepse -h | --help

Options:
    -h --help   # show this page
    --version   # show version info
"""
from docopt import docopt
import inspect
from smap_nepse import preprocessing

from . import __version__ as VERSION

def is_command(s):
    if s.startswith('-'):
        return False
    if s.startswith('<'):
        return False
    return True

def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default

def dispatch_command(arguments, command):
    f = getattr(preprocessing, "{}".format(command))

    if f.__name__ == 'cleancsv':
        return f(arguments['<source>'], arguments['<destination>'])
    elif f.__name__ == 'scrapper':
        return f(arguments['<path>'])
    elif f.__name__ == 'cleanall':
        return f(arguments['<source>'], arguments['<destination>'])
    elif f.__name__ == 'csvtohdf':
        return f(arguments['<source>'], arguments['<destination>'])
    elif f.__name__ == 'alltohdf':
        return f(arguments['<source>'], arguments['<destination>'])
    elif f.__name__ == 'build_hdfstore':
        return f(arguments['<source>'], arguments['<destination>'])
    elif f.__name__ == 'plot':
        return f(arguments['<name>'], cols=arguments['--cols'],
                 plot_kind=arguments['--plot_kind'], start_date=arguments['--start_date'],
                 end_date=arguments['--end_date'])
    elif f.__name__ == 'comparision_plot':
        return f(arguments['<name>'], cols=arguments['--cols'],
                 plot_kind=arguments['--plot_kind'], start_date=arguments['--start_date'],
                 end_date=arguments['--end_date'])
    else:
        return None

def main():
    """Main CLI entrypoint."""

    arguments = docopt(__doc__, version=VERSION)
    print(arguments)
    command = get_first([k for (k,v) in arguments.items()
                         if (v and is_command(k))])
    dispatch_command(arguments,command)
