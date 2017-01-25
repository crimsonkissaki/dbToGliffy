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

    The value from the last dict the key is found in (if any) becomes the final value
    of the key in the first dict.

    :param tuple dicts: Dicts to merge
    :return:
    :rtype: dict
    """
    # the only values that matter in the end are the ones in the right-most dicts
    # looping over them in 'right -> left' order saves time
    # TODO: how MUCH time does it save???
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
            if not isinstance(_d, dict):
                # you could raise here, but what if the dict has a 'none' value for the key that needs to be moved?
                continue
            if _key in _d:
                return _d[_key]
        raise ValueError('no value')

    for key in res:
        try:
            # if isinstance(res[key], dict) and isinstance(new_val, dict):
            if isinstance(res[key], dict):
                # need to grab all the sub-dicts from each of the remaining dicts
                # and un-reverse them so they will be handled properly
                dicts_key = [d[key] for d in dicts if d[key]]
                dicts_key.reverse()
                join_dicts(res[key], *dicts_key)
            else:
                res[key] = _find_key(key, dicts)
        except ValueError:
            continue

    return res


