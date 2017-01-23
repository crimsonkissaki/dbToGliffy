"""

"""

# Standard Library
import json
# Third Party
# Local


class GliffyObject(object):
    """
    This is the 'root' of all Gliffy objects. It does nothing other than help with isinstanceof() checks.
    """
    pass


class BaseEntity(GliffyObject):
    """
    The basic building block for most Gliffy objects. These properties are virtually universal.

    You will mostly be setting .graphic or adding to .children.
    """
    graphic = None
    children = []

    type_def = {
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

    def set_uid(self, uid):
        # type: (str) -> BaseEntity
        self.type_def['uid'] = uid

        return self

    def set_graphic(self, graphic):
        """
        Sets the graphic object

        :param Graphic graphic:
        :return:
        :rtype: self
        """
        if not isinstance(graphic, graphics.Graphic):
            raise Exception('Unable to set non-Graphic object as BaseEntity.graphic')
        self.graphic = graphic

        return self

    def add_child(self, child):
        """
        Adds a child object to the base entity

        :param GliffyObject child:
        :return:
        :rtype: self
        """
        if not isinstance(child, GliffyObject):
            raise Exception('Unable to add non-GliffyObject object to BaseEntity.children')
        self.children.append(child)

        return self

    def to_json(self):
        if self.graphic:
            # update the base entity's uid if the graphic affects it
            uid = self.graphic.get_uid()
            if uid != False:
                self.set_uid(uid)
            self.type_def.graphic = self.graphic.to_json()

        for c in self.children:
            self.type_def.children.append(c.to_json())

        return json.dumps(self.type_def)

    def hrm_set_graphic(self, graphic):
        """
        Sets the graphic object & updates uid if required

        :param Graphic graphic:
        :return:
        :rtype: self
        """
        if not isinstance(graphic, graphics.Graphic):
            raise Exception('Unable to set non-Graphic object as BaseEntity.graphic')

        # update the base entity's uid if the graphic affects it
        uid = graphic.get_uid()
        if uid != False:
            self.set_uid(uid)
        self.type_def['graphic'] = graphic

        return self

    def hrm_add_child(self, child):
        if not isinstance(child, GliffyObject):
            raise Exception('Unable to add non-GliffyObject object to BaseEntity.children')

        self.type_def['children'].append(child)

        return self

