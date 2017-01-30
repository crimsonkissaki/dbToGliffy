"""

"""

# Standard Library
# Third Party
# Local
from .stage import Stage
from .entities import Entity, Group
from .graphics import Shape, Text, Line


# this is going to be ugly as sin as i figure out the best way to set it up
class Gliffy(object):
    """
    The main Gliffy facade object.

    NOTES:

        Outputting the right JSON is only 1/2 of the job. Gliffy files will not load properly
        unless the entity x/y coords & width/height values are also set.

        Properly sizing/positioning automatically generated objects can be somewhat of a pain.
    """

    __slots__ = 'stage'

    def __init__(self):
        # type: () -> Gliffy
        self.stage = Stage()
        self.set_start_coords()
        self.set_entity_padding()

    def __str__(self):
        # type: () -> str
        return self.to_json()

    def set_start_coords(self, coords={}):
        # type: (dict) -> Gliffy
        """
        Set the starting X/Y coords for the Gliffy Stage

        :param dict coords: The X/Y coords to set
        :keyword x: (``int``) X coordinate (Default 20)
        :keyword y: (``int``) Y coordinate (Default 20)
        :rtype: Gliffy
        """
        self.stage.x = coords.get('x', 20)
        self.stage.y = coords.get('y', 20)

        return self

    def set_entity_padding(self, padding={}):
        # type: (dict) -> Gliffy
        """
        Set the amount of horizontal (X) and vertical (Y) padding between Gliffy Entities

        :param dict padding: The horizontal/vertical (X/Y) padding to use
        :keyword pad_x: (``int``) Horizontal (X) padding (Default 20)
        :keyword pad_y: (``int``) Vertical (Y) padding (Default 20)
        :rtype: Gliffy
        """
        self.stage.pad_x = padding.get('pad_x', 20)
        self.stage.pad_y = padding.get('pad_y', 20)

        return self

    def entity(self):
        # type: () -> Entity
        """
        Creates a base Entity object which can be explicitly customized as you wish.

        You only need to use this if you want to exert precise control over the construction
        of a Gliffy object.

        If you want to assign a graphic to this Entity you will have to manually create one
        via the ``graphic()`` method, and manually assign it to the Entity via ``Entity.set_graphic()``

        :return: A base Entity object with no graphic or children.
        :rtype: Entity
        """
        return Entity()

    def graphic(self, graphic_type='', graphic_props={}):
        # type: (str, dict) -> Graphic
        """
        Creates a raw Graphic object that can be assigned to an Entity via ``Entity.set_graphic()``

        :param str graphic_type: Type of Graphic to create. E.g. Rectangle, Text, Line, etc.
        :param dict graphic_props: Properties to apply to the Graphic
        :return: A raw Graphic object for use in an Entity
        :rtype: Graphic
        """
        if not graphic_type:
            raise ValueError('The `graphic` method requires a valid Graphic type.')

        graphic = None
        # standardize for comparison
        graphic_type = graphic_type.capitalize()
        if graphic_type == 'Text':
            graphic = Text(graphic_props)
        elif graphic_type == 'Line':
            graphic = Line(graphic_props)
        else:
            graphic = Shape(graphic_type, graphic_props)

        return graphic

    def group(self):
        # type: () -> Group
        """
        Creates a Group object which allows multiple objects to be combined into
        a single 'linked object' for easy manipulation.

        Use ``Group.add_child()`` to include an Entity in the group

        :return: A Group object to combine multiple child objects into a single 'linked object'
        :rtype: Group
        """
        return Group()

    def rectangle(self, properties={}):
        # type: (dict) -> Shape
        """
        Creates a rectangle shape object in Gliffy

        :param dict properties: Properties to apply to the rectangle
        :keyword strokeWidth: (:py:class:`int`) Width of the rectangle's border
        :keyword strokeColor: (:py:class:`str`) Hex code for the rectangle's border color
        :keyword fillColor:   (:py:class:`str`) Hex code for the rectangle's fill color
        :return: Entity with a Rectangle graphic
        :rtype: Entity
        """
        return Entity('rectangle', properties)

    def text(self, properties={}):
        # type: (dict) -> Text
        """
        Creates a text object in Gliffy

        :param dict properties: Properties to apply to the text
        :keyword text:  (:py:class:`str`) Text to display
        :keyword css:   (:py:class:`dict`) CSS settings to apply to the text.\n
                        Valid properties are:\n
                        (:py:class:`str`):
                            ``text-align``  (left, middle, right)\n
                            ``font-size``   (9-14px, 18px, 24px, 36px, 48px)\n
                            ``font-family`` (Arial, Helvetica, Courier, Times, Verdana)\n
                            ``color``       (#xxxxxx)\n
                        (:py:class:`bool`):
                            ``bold``, ``italic``, ``underline``
        :rtype: Text
        """
        return Entity('text', properties)

    def add(self, children):
        # type: (Any) -> Gliffy
        """
        Adds a single Entity or list of Entities to the 'Stage', allowing them to be viewed/manipulated

        :param Any children: Single Entity or :py:class:`list` of Entities
        :rtype: Gliffy
        :raises: :py:class:`TypeError`
        """
        self.stage.add(list(children))

        return self

    def to_json(self):
        # type: () -> str
        """
        :return: JSON string for use in Gliffy
        :rtype: str
        """
        return self.stage.to_json()


