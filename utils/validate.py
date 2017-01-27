"""
Validation methods
"""

# Standard Library
import inspect
# Third Party
# Local
from . import dump


def in_dict_as_type(dic, key, val_type, opt_convert=False, opt_raise=False):
    # type: (dict, str, Any, bool) -> Any
    """
    Checks that a dict key value is a certain type.

    If ``opt_convert`` = True & the value is the wrong type it will attempt conversion.
    If ``opt_raise`` = True it will raise a ``ValueError`` if the check and|or conversion fails.

    ** NOTE ** This method can return ``None`` or a ``bool``

    :param dict dic: Dict to check for the key.
    :param str key: Key to look for in the dict.
    :param Any val_type: Type of value to check for.
    :param bool opt_convert: Flag to (en|dis)able type conversion attempts.
    :param bool opt_raise: Flag to (en|dis)able raising ``ValueError`` on failure instead of just returning False.
    :return: None if key not in dict. False if not right type. True if in dict & right type.
    :rtype: Any
    :raises: :py:class:`ValueError`
    """

    # dump.dump_args(inspect.currentframe())
    # print('\n\n')

    if key not in dic:
        return None
    if isinstance(dic[key], val_type):
        return True

    err = "ERROR: Key '{}' value '{}' is '{}', not '{}'.".format(key, dic[key], type(dic[key]), val_type.__name__)
    if opt_convert:
        try:
            if val_type.__name__ == 'bool':
                dic[key] = True if str(dic[key]).lower() == 'true' else False
            else:
                dic[key] = val_type(dic[key])
            return True
        except ValueError:
            if opt_raise:
                raise ValueError(err)
    if opt_raise:
        raise ValueError(err)
    else:
        return False

