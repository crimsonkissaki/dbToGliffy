"""

"""

# Standard Library
import inspect
# Third Party
# Local


def dump_args(frame):
    # frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    print('function name "%s"' % inspect.getframeinfo(frame)[2])
    for i in args:
        print("    %s = %s" % (i, values[i]))
    return [(i, values[i]) for i in args]


def dump(data, dunder=False):
    # type: (obj, bool) -> None
    """
    Prints out an objects attributes -> values, similar to PHP's var_dump()

    :param obj data:
    :param bool dunder: Flag to print out the __xxx__ (dunder) properties
    """
    print("Object type is {}\n".format(type(data)))
    if not dunder:
        print("-- Ignoring __xx__ properties --\n")
    attr_width = 0
    type_width = 0
    for attr in dir(data):
        if not dunder and attr.startswith('__'):
            continue
        aw = len(attr)
        if aw > attr_width:
            attr_width = aw
        tw = len(type(getattr(data, attr)).__name__)
        if tw > type_width:
            type_width = tw

    attr_width += 2     # increase by 2 for better legibility
    for attr in dir(data):
        if not dunder and attr.startswith('__'):
            continue
        av = getattr(data, attr)
        at = type(av).__name__
        tw = type_width - len(at)
        tw = tw if tw == 0 else tw + 1
        out = "    {:<%i} ({}){:<%i}: {}" % (attr_width, tw)
        # prevent errors from types that don't easily convert to string
        pv = av if hasattr(type(av), '__format__') else type(av)
        print(out.format(attr, at, ' ', pv))
