"""

"""

# Standard Library
import json
# Third Party
# Local
from . import stage, base, entity, graphic
from .base import GliffyObject
from .stage import Stage
from .entity import Entity, Group
from .graphic import Rectangle, Text


# this is going to be ugly as sin as i figure out the best way to set it up
class Gliffy(object):
    """
    The main Gliffy adapter object.
    """

    def __init__(self):
        self.stage = Stage()
        # iterator to keep elements numbered
        self.node_index = 0
        # z-index of elements
        self.order = 0
        # set of all defined Gliffy objects
        self.defined_objects = ()

    def __str__(self):
        return self.to_json()

    def add_to_stage(self, child):
        # type: (GliffyObject) -> Gliffy
        if not isinstance(child, GliffyObject):
            raise TypeError('Only GliffyObjects can be added to the stage.')
        self.stage.add_child(child)

        return self

    def to_json(self):
        # type: () -> str
        """
        :return: JSON string for use in Gliffy
        :rtype: str
        """
        return self.stage.to_json()

    def make_entity(self):
        return Entity()

    def make_group(self):
        return Group()

    def make_rectangle(self, properties={}):
        # type: (dict) -> Entity
        """
        :param dict properties:
        :return: Entity with a Rectangle graphic
        :rtype: Entity
        """
        ent = self.make_entity()
        ent.set_graphic(Rectangle(properties))

        return ent

    def make_text(self, properties={}):
        # type: (dict) -> Entity
        """
        :param dict properties:
        :return: Entity with a Text graphic
        :rtype: Entity
        """
        ent = self.make_entity()
        ent.set_graphic(Text(properties))

        return ent

    """
    def make_line(self, **kwargs):
        return shapes.Line(**kwargs)

    def make_constraint(self, **kwargs):
        return shapes.Constraint(**kwargs)
    """
