"""

"""

# Standard Library
import json
# Third Party
# Local
from .base import GliffyObject


class Entity(GliffyObject):
    """
    The basic building block for all Gliffy entity objects.

    You will mostly be setting .graphic or adding to .children.
    """

    # limit the instance variables created; no __dict__ or __weakref__ to save RAM
    # you have to set the variables in __init__ if you define this
    __slots__ = ('graphic', 'children', 'type_def')

    def __init__(self):
        self.graphic = None
        self.children = []
        self.type_def = {
            'x': 0,
            'y': 0,
            'rotation': 0,
            'id': 0,
            'uid': 'com.gliffy.shape.erd.erd_v1.default.entity',
            'width': 0,
            'height': 0,
            'lockAspectRatio': False,
            'lockShape': False,
            'order': 0,
            'graphic': None,
            'children': [],
            'linkMap': [],
        }

    def __str__(self):
        return self.to_json()

    def get_type_def(self):
        # type: () -> dict
        for c in self.children:
            self.type_def['children'].append(c.get_type_def())

        return self.type_def

    def set_graphic(self, graphic):
        if hasattr(graphic, 'get_entity_uid'):
            self.set_uid(graphic.get_entity_uid())
        self.graphic = graphic

        return self

    def set_uid(self, uid):
        # type: (str) -> Entity
        self.type_def['uid'] = uid

        return self

    def add_child(self, child):
        self.children.append(child)

        return self

    def to_json(self):
        # type: () -> str
        if self.graphic:
            self.type_def['graphic'] = self.graphic.get_type_def()

        for c in self.children:
            self.type_def['children'].append(c.get_type_def())

        return json.dumps(self.type_def)


class Group(Entity):

    __slots__ = ('children', 'graphic', 'type_def')

    def __init__(self):
        super().__init__()
        self.set_uid('com.gliffy.shape.basic.basic_v1.default.group')
        del self.type_def['linkMap']
