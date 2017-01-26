"""

"""

# Standard Library
# Third Party
# Local
from .base import GliffyObject
from .stage import Stage
from .entity import Entity, Group
from .graphic import Shape, Text, Line


# this is going to be ugly as sin as i figure out the best way to set it up
class Gliffy(object):
    """
    The main Gliffy adapter object.
    """

    __slots__ = 'stage'

    def __init__(self):
        # type: () -> Gliffy
        self.stage = Stage()

    def __str__(self):
        # type: () -> str
        return self.to_json()

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

    def add(self, child):
        # type: (Entity) -> Gliffy
        """
        Adds a Gliffy Entity object to the 'Stage', allowing it to be viewed/manipulated

        :param Entity child: The Entity to add to the 'stage'
        :return: Returns the Gliffy object for method chaining
        :rtype: Gliffy
        :raises: :py:class:`TypeError`
        """
        if not isinstance(child, GliffyObject):
            raise TypeError('Only GliffyObjects can be added to the stage.')

        self.stage.add(child)

        return self

    def to_json(self):
        # type: () -> str
        """
        :return: JSON string for use in Gliffy
        :rtype: str
        """
        return self.stage.to_json()


