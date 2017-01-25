"""

"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject
from . import graphic


class Entity(GliffyObject):
    """
    The basic building block for all Gliffy entity objects.

    You will mostly be setting .graphic or adding to .children.
    """

    # limit the instance variables created; no __dict__ or __weakref__ to save RAM
    # you have to set the variables in __init__ if you define this
    __slots__ = ('graphic', 'children', 'type_def')

    def __init__(self, graphic_type='', graphic_props={}):
        # type: (str, dict) -> Entity
        """
        :param str graphic_type: The type of Graphic object to add
        :param dict graphic_props: Properties to apply to the Graphic object
        :return: Returns a new base Entity object, which is the basic structure that Gliffy objects
                 are built on.
        :rtype: Entity
        :raises: :py:class:`ValueError`
        """
        if not isinstance(graphic_type, str):
            raise ValueError('Entity requires the graphic type (str) as its first argument.')
        if not isinstance(graphic_props, dict):
            raise ValueError('Entity requires the graphic props (dict) as its second argument.')

        self.graphic = None
        self.children = []
        self.type_def = OrderedDict([
            ('x', 0),
            ('y', 0),
            ('rotation', 0),
            ('id', 0),
            ('uid', 'com.gliffy.shape.erd.erd_v1.default.entity'),
            ('width', 0),
            ('height', 0),
            ('lockAspectRatio', False),
            ('lockShape', False),
            ('order', 0),
            ('graphic', None),
            ('children', []),
            ('linkMap', []),
        ])

        if graphic_type:
            # standardize for comparison
            graphic_type = graphic_type.capitalize()
            if graphic_type == 'Text':
                self.graphic = graphic.Text(graphic_props)
            elif graphic_type == 'Line':
                self.graphic = graphic.Line(graphic_props)
            else:
                self.graphic = graphic.Shape(graphic_type, graphic_props)
            self.type_def['uid'] = self.graphic.entity_uid

    # only here to allow the properties pass-through
    def __getattr__(self, item):
        if item == 'set_properties' and self.graphic:
            return self.graphic.set_properties

        raise AttributeError('\'Entity\' object has no attribute \'{}\''.format(item))

    def get_type_def(self):
        # type: () -> dict
        # reset so we don't add copies
        self.type_def['children'] = []
        if self.graphic:
            self.type_def['graphic'] = self.graphic.get_type_def()
        for c in self.children:
            self.type_def['children'].append(c.get_type_def())

        return self.type_def

    def add_child(self, child):
        # type: (Entity) -> Entity
        self.children.append(child)

        return self

    def to_json(self):
        # type: () -> str
        return json.dumps(self.get_type_def())


class Group(Entity):
    """
    Group objects allow multiple objects to be combined into a single 'linked object' for easy manipulation.
    """

    __slots__ = ('children', 'graphic', 'type_def')

    def __init__(self):
        """
        :return: A Group object to combine multiple child objects into a single 'linked object'
        :rtype: Group
        """
        super().__init__()
        self.type_def['uid'] = 'com.gliffy.shape.basic.basic_v1.default.group'
        del self.type_def['linkMap']
