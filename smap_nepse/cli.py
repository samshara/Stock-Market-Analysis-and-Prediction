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
    smap_nepse plot <name> [<cols>...] [--plot_kind=<arg>] [--start_date=<arg> ] [--end_date=<arg>]
    smap_nepse comparision_plot <names>... --col=<arg> --plot_kind=<arg> [--start_date=<arg>] [--end_date=<arg>]
    smap_nepse ann <source> [<window>] [<prop>] [<neurons>] [<nhorizon>] [<features>...]
    smap_nepse --version
    smap_nepse -h | --help

Options:
    -h --help   # show this page
    --version   # show version info
"""
from docopt import docopt
from dateutil.parser import parse
from schema import Schema, And, Or, Optional, SchemaError
import inspect
import os

from smap_nepse import preprocessing
from smap_nepse import prediction
#import smap_nepse 
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
    f = getattr(smap_nepse, "{}".format(command))

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
        return f(arguments['<name>'], cols=arguments['<cols>'],
                 plot_kind=arguments['--plot_kind'], start_date=arguments['--start_date'],
                 end_date=arguments['--end_date'])
    elif f.__name__ == 'comparision_plot':
        return f(arguments['<names>'], cols=arguments['--col'],
                 plot_kind=arguments['--plot_kind'], start_date=arguments['--start_date'],
                 end_date=arguments['--end_date'])
    elif f.__name__ == 'ann':
        return f(arguments['<source>'],window = arguments['<window>'],prop = arguments['<prop>'], neurons = arguments['<neurons>'], nhorizon = arguments['<nhorizon>'], features = arguments['<features>'])
    else:
        return None

def main():
    """Main CLI entrypoint."""

    arguments = docopt(__doc__, version=VERSION)
    print(arguments)
    schema = Schema({
        '<names>':list,
        '<path>':Or(str,None),
        '<source>':Or(os.path.exists,None),
        Optional('<destination>'):Or(str,None),
        '<name>':Or(os.path.exists, None),
        Optional('--col'):Or(And(str,lambda n: n in ['Date','Total Transactions','Traded Shares',
                                                          'TotalTraded Amount','Maximum Price',
                                                          'Minimum Price','Closing Price']), None),
        Optional('<cols>'):And(list
                               ,lambda n:set(n).issubset(['Date','Total Transactions','Traded Shares',
                                                          'TotalTraded Amount','Maximum Price',
                                                          'Minimum Price','Closing Price'])),
        Optional('--plot_kind'):Or(And(str,
                                       lambda n: n in ['line', 'box', 'hexbin','scatter_matrix']),None),
        Optional('--start_date'): Or(And(str,
                                        lambda n: True if parse(n) else False),None),
        Optional('--end_date'):Or(And(str,lambda n: True if parse(n) else False),None),
        Optional('<window>'):str,
        Optional('<prop>'):str,
        Optional('<neurons>'):str,
        Optional('<features>...'):list,
        Optional('<nhorizon>'):str,
        Optional('ann'):bool,
        Optional('scrapper'):bool,
        Optional('cleancsv'):bool,
        Optional('cleanall'):bool,
        Optional('csvtohdf'):bool,
        Optional('alltohdf'):bool,
        Optional('build_hdfstore'):bool,
        Optional('plot'):bool,
        Optional('comparision_plot'):bool,
        Optional('--version'):bool,
        Optional('-h'):bool,
        Optional('--help'):bool
        
    })
    # try:
    #     arguments = schema.validate(arguments)
    # except SchemaError as e:
    #     exit(e)
    print(arguments)
    command = get_first([k for (k,v) in arguments.items()
                         if (v and is_command(k))])
    dispatch_command(arguments,command)
