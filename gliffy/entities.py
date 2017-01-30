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
    __slots__ = ('settings', 'graphic', 'children', 'type_def')

    def __init__(self, entity_settings={}, graphic_type='', graphic_props={}):
        # type: (dict, str, dict) -> Entity
        """
        :param dict entity_settings: Settings for the Entity object
        :keyword position: (``str``) How to determine Entity positioning: 'auto' or 'fixed'. (Default 'auto')
                           'Auto' will determine X/Y coords based on previous Entity positions/sizes. (relative)
                           'Fixed' puts it where you say. (absolute)
        :keyword x: (``int``) X coord for upper-left corner of Entity
        :keyword y: (``int``) Y coord for upper-left corner of Entity
        :keyword size: (``str``) How to determine Entity size: 'auto' or 'fixed'. (Default 'auto')
                                 'Auto' will determine size based on content/graphics.
                                 'Fixed' will make it whatever you say.
        :keyword width: (``int``) Width of Entity
        :keyword height: (``int``) Height of Entity
        :param str graphic_type: The type of Graphic object to add
        :param dict graphic_props: Properties to apply to the Graphic object
        :return: Returns a new base Entity object, which is the basic structure that Gliffy objects
                 are built on.
        :rtype: Entity
        """
        self.settings = {
            'position': 'auto',  # auto/fixed
            'size': 'auto',  # auto/fixed
            '_type': 'entity'
        }
        self.graphic = None
        self.children = []
        self.type_def = OrderedDict([
            ('x', None),
            ('y', None),
            ('rotation', 0),
            ('id', 0),
            ('uid', 'com.gliffy.shape.erd.erd_v1.default.entity'),
            ('width', None),
            ('height', None),
            ('lockAspectRatio', False),
            ('lockShape', False),
            ('order', 0),
            ('graphic', None),
            ('children', []),
            ('linkMap', []),
        ])

        self._define_graphic(graphic_type, graphic_props)

    def __getattr__(self, attr):
        if attr == 'set_properties' and self.graphic:
            return self.graphic.set_properties

        raise AttributeError('\'Entity\' object has no attribute \'{}\''.format(attr))

    def _define_graphic(self, graphic_type='', graphic_props={}):
        # type: (str, dict) -> None
        """
        Defines a Graphic to use with the Entity

        :param str graphic_type: Type of Graphic
        :param dict graphic_props: Graphic properties
        """
        if graphic_type:
            graphic_type = graphic_type.lower()
            self.settings['_type'] = graphic_type
            if graphic_type == 'text':
                self._set_graphic(graphics.Text(graphic_props))
                self.type_def['order'] = 'auto'
            elif graphic_type == 'line':
                self._set_graphic(graphics.Line(graphic_props))
            else:
                self._set_graphic(graphics.Shape(graphic_type, graphic_props))

    def _set_graphic(self, new_graphic=None):
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

    def set_settings(self, settings={}):
        # type: (dict) -> Entity
        """
        Sets important Entity values

        .. note:: The X/Y coordinates are relative to the Entity's parent.

        :param dict settings: Settings to apply to the Entity
        :keyword position: (``str``) How to determine Entity positioning: 'auto' or 'fixed'. (Default 'auto')
                           'Auto' will determine X/Y coords based on previous Entity positions/sizes. (relative)
                           'Fixed' puts it where you say. (absolute)
        :keyword x: (``int``) X coord for upper-left corner of Entity
        :keyword y: (``int``) Y coord for upper-left corner of Entity
        :keyword size: (``str``) How to determine Entity size: 'auto' or 'fixed'. (Default 'auto')
                                 'Auto' will determine size based on content/graphics.
                                 'Fixed' will make it whatever you say.
        :keyword width: (``int``) Width of Entity
        :keyword height: (``int``) Height of Entity
        :rtype: Entity
        """
        if not settings:
            return

        # these are used to help with calculations
        t = ('auto', 'fixed')
        for v in ('position', 'size'):
            if v in settings:
                settings[v] = settings[v].lower()
                if settings[v] in t:
                    self.settings[v] = settings[v]

        # these are inherent entity values
        for s in ['x', 'y', 'width', 'height']:
            self.type_def[s] = settings.get(s, 0)

        return self

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

    def is_type(self, ent_type):
        # type: (str) -> bool
        """
        Check if the Entity is of a certain type

        :param str ent_type: Type to check for
        :rtype: bool
        """
        # its always an entity ...
        if ent_type.lower() in ('entity', self.settings['_type'].lower()):
            return True
        else:
            return False

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

    __slots__ = ('settings', 'children', 'graphic', 'type_def')

    def __init__(self):
        """
        :return: A Group object to combine multiple child objects into a single 'linked object'
        :rtype: Group
        """
        super().__init__()
        self.type_def['uid'] = 'com.gliffy.shape.basic.basic_v1.default.group'
        self.settings['_type'] = 'group'
        del self.type_def['linkMap']
