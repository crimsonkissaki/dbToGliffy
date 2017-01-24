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


def join_dicts(to_dict={}, from_dict={}):
    # type: (dict, dict) -> None
    """
    Recursively updates ``to_dict`` with the values from matching keys in ``from_dict``, if any.
    If both dicts have sub-dicts those dicts will also be joined.

    NOTE: This method will modify ``to_dict`` in place.

    :param dict to_dict: The dict whose values need to be updated
    :param dict from_dict: The dict that has new values
    :return: ``to_dict`` with values updated from ``from_dict``
    :rtype: dict
    """
    if not isinstance(to_dict, dict) or not isinstance(from_dict, dict):
        raise TypeError('Method `join_dicts()` only works with dict-like objects.')

    if not from_dict:
        return to_dict

    for d in to_dict:
        if d in from_dict:
            if isinstance(to_dict[d], dict) and isinstance(from_dict[d], dict):
                join_dicts(to_dict[d], from_dict[d])
            else:
                to_dict[d] = from_dict[d]
