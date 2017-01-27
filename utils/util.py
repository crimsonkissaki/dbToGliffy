"""
Generic utility functions
"""

# Standard Library
# Third Party
# Local


def merge_dicts(*dicts):
    # type: (dict, dict, ...) -> dict
    """
    Merges 2+ dicts; values in right-side dict replace left-side dict.

    :param dict dicts: 2+ dicts to merge
    :return: Merged dict
    :rtype: dict
    """
    c = 1
    for d in dicts:
        if not isinstance(d, dict):
            t = type(d)
            raise TypeError('`merge_dicts()` works with dict-like objects; arg #{} is type `{}`'.format(c, t))
        c += 1

    # python 3.5+ -> z = {**x, **y}
    # 2.6+
    r = {}
    for d in dicts:
        r.update(d)

    return r


def join_dicts(*dicts):
    # type: (*dict) -> dict
    """
    Recursively updates the first dict 'in place' with values from subsequent dicts if they have the same key.

    If the dicts have sub-dicts with the same key those will be updated in the same manner.

    The value from the last dict the key is found in (if any) becomes the final value
    of the key in the first dict.

    Example::

        a = { 'one': '1.a', 'two': '2.a', 'three': { 't_one': '3.1.a', 't_two': '3.2.a' } }
        b = { 'one': '1.b', 'three': { 't_one': '3.1.b', 't_three': '3.3.b' } }
        c = { 'two': '2.c', 'three': { 't_two': '3.2.c', 't_three': '3.3.c' } }

        join_dicts(a, b)
            a = { 'one': '1.b', 'two': '2.a', 'three': { 't_one': '3.1.b', 't_two': '3.2.a' } }

        join_dicts(a, b, c)
            a = { 'one': '1.b', 'two': '2.c', 'three': { 't_one': '3.1.b', 't_two': '3.2.c' } }


    :param tuple dicts: Dicts to merge. The first dict is updated 'in place'
    :raises: :py:class:`ValueError`
    """
    # have to make sure all arguments are dicts to prevent KeyErrors
    if any(not isinstance(d, dict) for d in dicts):
        raise ValueError('`join_dicts` can only process dict-like objects.')

    # the only values that matter in the end are the ones in the right-most dicts
    # looping over them in 'right -> left' order saves time
    dicts = list(dicts)
    res = dicts.pop(0)
    dicts.reverse()

    '''
    Using a function since there's no way to break out of nested loops, and
      we don't want to keep looking if we've already found a value to assign.
    We also have to raise an exception since there's no way to tell if the
      found value is actually 'None' or if the function is simply returning
      'None' by default because no value was found.
    '''
    def _find_key(_key, _dicts):
        # type: (str, list) -> Any
        for _d in _dicts:
            if isinstance(_d, dict) and _key in _d:
                return _d[_key]
        raise ValueError('no value')

    for key in res:
        try:
            if isinstance(res[key], dict):
                # grab sub-dicts from remaining dicts & un-reverse so they're handled properly
                dicts_key = [d[key] for d in dicts if key in d]
                dicts_key.reverse()
                join_dicts(res[key], *dicts_key)
            else:
                res[key] = _find_key(key, dicts)
        except ValueError:
            continue
        except KeyError:
            print('\n\n', 'KeyError in join_dicts:\n-------------------------\n', 'args: ', dicts, '\n\n')
            raise

