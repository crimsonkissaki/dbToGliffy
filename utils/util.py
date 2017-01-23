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
    # python 3.5+ -> z = {**x, **y}
    # 2.6+
    r = {}
    for d in dicts:
        r.update(d)

    return r

