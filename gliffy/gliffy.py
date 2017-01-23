"""

"""

# Standard Library
import json
from pprint import PrettyPrinter
# Third Party
# Local
from . import basics, graphics, stage


# this is going to be ugly as sin as i figure out the best way to set it up
class Gliffy(object):
    """
    The main Gliffy adapter object.
    """

    # iterator to keep elements numbered
    node_index = 0

    # z-index of elements
    order = 0

    # formatting options
    font = {
        'default': {
            'size': '12px',
            'font': 'Courier',
            'color': '#000000',
            'align': 'center'
        },
        'table_name': {
            'size': '14px',
        },
        'column_name': {
            'align': 'left'
        },
        'data_type': {
            'color': '#ff0000'
        }
    }

    def __init__(self):
        self.stage = stage.Stage()

    def __str__(self):
        return str(self.stage)

    def to_json(self):
        # type: () -> str
        """
        :return: JSON string for use in Gliffy
        :rtype: str
        """
        return str(self)

    def add_to_stage(self, obj):
        self.stage.add(obj)
        return self

    def make(self, el, **kwargs):
        # type: (str, dict) -> obj
        """
        Makes a basic Gliffy object

        :param str el:
        :param dict kwargs:
        :return:
        :rtype: object
        """

        fn = 'make_' + el
        # if the function exists
        if hasattr(self, fn):
            # get it & call
            return getattr(self, fn)(**kwargs)

    def make_group(self, **kwargs):
        return basics.Group(**kwargs)

    def make_rectangle(self, **kwargs):
        return graphics.Rectangle(**kwargs)

    """
    def make_text(self, **kwargs):
        return shapes.Text(**kwargs)

    def make_line(self, **kwargs):
        return shapes.Line(**kwargs)

    def make_constraint(self, **kwargs):
        return shapes.Constraint(**kwargs)
    """
