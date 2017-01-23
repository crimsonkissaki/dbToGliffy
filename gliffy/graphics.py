"""

"""

# Standard Library
import json
# Third Party
# Local
from gliffy.base import GliffyObject, BaseEntity
from utils import util


class Graphic(GliffyObject):
    """
    This is the base object for all Gliffy objects classified as 'graphics'
    """

    type = 'N/A'
    type_def = {}
    base = None

    def __init__(self):
        self.base = BaseEntity()

    def __str__(self):
        return json.dumps({'type': self.type, self.type: self.get_data()})

    def get_uid(self):
        """
        Returns the uid needed by the BaseEntity

        Returning false means "don't change it"
        Returning anything else (including None) means "set it to this"

        :return: False
        :rtype: bool
        """
        return False

    def to_json(self):
        raise Exception('Graphic object has no to_json() method defined')


# #cccccc is gray

# basic rectangle
# this will need to be added as an Entity.graphic child
class Rectangle(Graphic):

    # holds merged default + user-supplied CSS options
    opts = {
        'strokeWidth': 1,
        'strokeColor': '#000000',
        'fillColor': '#ffffff',
    }

    # Gliffy JSON definition data
    type_def = {
        'type': 'Shape',
        'Shape': {
            'tid': 'com.gliffy.stencil.rectangle.basic_v1',
            'strokeWidth': 0,
            'strokeColor': '',
            'fillColor': '',
            'gradient': False,
            'dropShadow': False,
            'state': 0,
            'shadowX': 0,
            'shadowY': 0,
            'opacity': 1
        }
    }

    def __init__(self, opts={}):
        # type: (dict) -> Rectangle
        """
        Creates a new Gliffy Rectangle object

        :param dict opts: Options for styling the Rectangle
                          Valid options are ``strokeWidth`` (``int``), ``strokeColor`` & ``fillColor`` (``hex``)
        :rtype: Rectangle
        """
        super().__init__()
        self.set_opts(opts)
        self.base.set_graphic(self)

    def _update_opts(self):
        self.type_def['Shape'] = util.merge_dicts(self.type_def['Shape'], self.opts)

    def set_opts(self, opts={}):
        # type: (dict) -> Rectangle
        if opts:
            tmp = util.merge_dicts(self.opts, opts)
            self.opts = tmp

        return self

    def get_uid(self):
        return 'com.gliffy.shape.erd.erd_v1.default.entity'

    def to_json(self):
        """
        Returns the whole JSON data set for the Rectangle, including the
        outer BaseEntity code

        :rtype: str
        """
        self._update_opts()

        return json.dumps(self.type_def)

