"""

"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject
from . import graphics


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
                self.set_graphic(graphics.Text(graphic_props))
                self.type_def['order'] = 'auto'
            elif graphic_type == 'Line':
                self.set_graphic(graphics.Line(graphic_props))
            else:
                self.set_graphic(graphics.Shape(graphic_type, graphic_props))

    def __getattr__(self, attr):
        if attr == 'set_properties' and self.graphic:
            return self.graphic.set_properties

        raise AttributeError('\'Entity\' object has no attribute \'{}\''.format(attr))

    @property
    def coords(self):
        # type: () -> dict
        """
        :return: The Entity's x/y coordinates; {'x': :py:class:`int`, 'y': :py:class:`int`}
        :rtype: dict
        """
        return {'x': self.type_def['x'], 'y': self.type_def['y']}

    @coords.setter
    def coords(self, coords={}):
        # type: (dict) -> Entity
        """
        Sets the Entity's x/y coordinates

        ** NOTE ** The coordinates are relative to the Entity's parent.

        :param dict coords: The Entity's x/y coords as dict
        :keyword x: :py:class:`int` The Entity's x coordinate
        :keyword y: :py:class:`int` The Entity's y coordinate
        :rtype: Entity
        """
        if not coords:
            return
        for c in ['x', 'y']:
            if c in coords:
                self.type_def[c] = int(coords[c])

        return self

    @property
    def size(self):
        # type: () -> dict
        """
        :return: The Entity's width/height; {'width': :py:class:`int`, 'height': :py:class:`int`}
        :rtype: dict
        """
        return {'width': self.type_def['width'], 'height': self.type_def['height']}

    @size.setter
    def size(self, size={}):
        # type: (dict) -> Entity
        """
        Sets the Entity's width/height values

        :param dict size: The Entity's width/height size as dict
        :keyword width: :py:class:`int` The Entity's width
        :keyword height: :py:class:`int` The Entity's height
        :rtype: Entity
        """
        if not size:
            return
        for s in ['width', 'height']:
            if s in size:
                self.type_def[s] = int(size[s])

        return self

    @property
    def order(self):
        # type: () -> int
        """
        :return: The Entity's z-index order
        :rtype: int
        """
        return self.type_def['order']

    @order.setter
    def order(self, order=0):
        # type: (int) -> Entity
        """
        Sets the Entity's x/y coordinates

        :param int order: The z-index order of the Entity
        :rtype: Entity
        """
        self.type_def['order'] = order

        return self

    @property
    def id(self):
        # type: () -> int
        """
        :return: The Entity's id (Stage's nodeIndex)
        :rtype: int
        """
        return self.type_def['id']

    @id.setter
    def id(self, id=0):
        # type: (int) -> Entity
        """
        Sets the Entity's id (Stage's nodeIndex)

        :param int id: The id (nodeIndex) order of the Entity
        :rtype: Entity
        """
        self.type_def['id'] = id

        return self

    def set_graphic(self, new_graphic=None):
        # type: (graphics.Graphic) -> Entity
        """
        Assigns a ``Graphic`` object to the Entity & sets the Entity's uid property.

        :param graphics.Graphic new_graphic: The Graphic object to assign to the Entity
        :rtype: Entity
        """
        if not new_graphic or not isinstance(new_graphic, graphics.Graphic):
            raise ValueError('Cannot assign non-Graphic object as Entity\'s graphic')
        self.graphic = new_graphic
        self.type_def['uid'] = self.graphic.entity_uid

        return self

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
