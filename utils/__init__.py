import pprint
from collections import defaultdict

from validate import validate_config, validate_input

_pp = pprint.PrettyPrinter( indent=4 )


def pp(arg):
    if type( arg ) == defaultdict:
        arg = dict( arg )
    return _pp.pformat( arg )
