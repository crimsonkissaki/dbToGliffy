"""
This is the 'stage' for Gliffy; the primary container for all objects.
"""

# Standard Library
import json
from collections import OrderedDict
# Third Party
# Local
from .base import GliffyObject
from .entities import Entity, Group
from . import graphics


class Stage(GliffyObject):

    __slots__ = ('children', 'type_def')

    # json object definition
    def __init__(self):
        self.children = []
        self.type_def = OrderedDict([
            ('contentType', 'application/gliffy+json'),
            ('version', '1.1'),
            ('metadata', OrderedDict([
                ('title', 'GliffyDB'),
                ('revision', 0),
                ('exportBorder', 'false')
            ])),
            ('embeddedResources', OrderedDict([
                ('index', 0),
                ('resources', [])
            ])),
            ('stage', OrderedDict([
                # entities go in objects
                ('objects', []),
                ('background', '#FFFFFF'),
                ('width', 0),  # TODO, this will need to be changed later
                ('height', 0),  # TODO, this will need to be changed later
                ('maxWidth', 5000),
                ('maxHeight', 5000),
                ('nodeIndex', 0),
                ('autoFit', True),
                ('exportBorder', False),
                ('gridOn', True),
                ('snapToGrid', True),
                ('drawingGuidesOn', True),
                ('pageBreaksOn', False),
                ('printGridOn', False),
                ('printPaper', 'LETTER'),
                ('printShrinkToFit', False),
                ('printPortrait', True),
                ('shapeStyles', {}),
                ('lineStyles', OrderedDict([
                    ('global', OrderedDict([
                        ('orthoMode', 1),
                        ('startArrow', 0),
                        ('endArrow', 1),
                        ('stroke', '#000000'),
                        ('dashStyle', None)
                    ]))
                ])),
                ('textStyles', {}),
                ('themeData', None),
            ]))
        ])

    @property
    def node_index(self):
        # type: () -> int
        return self.type_def['stage']['nodeIndex']

    @node_index.setter
    def node_index(self, idx=None):
        # type: (int) -> Stage
        if idx is not None:
            self.type_def['stage']['nodeIndex'] = idx

        return self

    @property
    def size(self):
        # type: () -> dict
        """
        :return: The Stages's width/height; {'width': :py:class:`int`, 'height': :py:class:`int`}
        :rtype: dict
        """
        stg = self.type_def['stage']
        return {'width': stg['width'], 'height': stg['height']}

    @size.setter
    def size(self, width=None, height=None):
        # type: (int, int) -> Stage
        """
        Sets the Stages's width/height values

        :param int width: The Stage's width
        :param int height: The Stage's height
        :rtype: Stage
        """
        stg = self.type_def['stage']
        if width is not None:
            stg['width'] = width
        if height is not None:
            stg['height'] = height

        return self

    def add(self, children):
        # type: (Any) -> Stage
        """
        Adds a single Entity or :py:class:`list` of Entities to the Stage

        :param Any children: Single Entity or :py:class:`list` of Entities
        :rtype: Stage
        """
        for c in list(children):
            if not isinstance(c, GliffyObject):
                raise TypeError('Only GliffyObjects can be added to Stage.')
            else:
                self.children.append(c)

        self.test(self.children)
        # self.reorder_children()
        # self.update_coordinates()
        # self.update_sizes()

        return self

    def test(self, children, eid=0, order=0):
        # type: (list[Entity], int, int) -> tuple
        print('\n\n------------------- START --------------------------')
        print('\n-- eid = ', eid)
        print('\n-- order = ', order)
        print('\n', children)

        for c in children:
            # type: Entity

            # if it's a graphic, set eid = nodeIndex
            #   nodeIndex += 2
            if isinstance(c, Group):
                # groups can have an order AFTER their children are ordered
                print('\n- is Group')
                if c.children:
                    print('\n+++++++++++++++++++++++++ STARTING GROUP KIDS +++++++++++++++++++++++++')
                    eid, order = self.test(c.children, eid, order)
                    print('\n+++++++++++++++++++++++++ DONE WITH GROUP KIDS +++++++++++++++++++++++++')
                print('\n~~~~~ setting Group id to ', eid, ', order to ', order)
                c.id = eid
                eid += 1
                c.order = order
                order += 1
            else:
                print('\n- is Entity ', c.graphic.get_type_def()['type'])
                c.id = eid
                c.order = 'auto' if c.graphic and isinstance(c.graphic, graphics.Text) else order
                print('\n~~~~~ setting Entity id to ', c.id, ', order to ', c.order)
                eid += 2
                order += 2
                c.size = {'width': 100, 'height': 100}

        print('\n-- final eid: ', eid)
        print('\n-- final order: ', order)
        print('\n-------------------- FINISH -------------------------\n')
        return eid, order
        self.node_index = eid

    def reorder_children(self):
        pass

    def update_coordinates(self):
        pass

    def update_sizes(self):
        pass

    def get_type_def(self):
        # type: () -> dict
        # reset objects so we don't add copies
        self.type_def['stage']['objects'] = []
        for c in self.children:
            self.type_def['stage']['objects'].append(c.get_type_def())

        return self.type_def

    def to_json(self):
        # type: () -> str
        return json.dumps(self.get_type_def())
