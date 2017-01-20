"""
Various Gliffy shapes that will be used.
"""

# Standard Library
import json
# Third Party
# Local

VALIGN = {
    'T': 'top',
    'M': 'middle',
    'B': 'bottom'
}

ALIGN = {
    'L': 'left',
    'C': 'center',
    'R': 'right'
}

FONT = {
    'ARIAL': 'Arial',
    'HELVETICA': 'Helvetica',
    'COURIER': 'Courier',
    'TIMES': 'Times',
    'VERDANA': 'Verdana'
}

SIZE = {
    9: '9px',
    10: '10px',
    11: '11px',
    12: '12px',
    13: '13px',
    14: '14px',
    18: '18px',
    24: '24px',
    36: '36px',
    48: '48px',
    64: '64px',
}

DECOR = {
    # font-weight: bold;
    'B': 'bold',
    # text-decoration: none; font-style: italic;
    'I': 'italic',
    # text-decoration: underline;
    'U': 'underline',
}


'''
__new__ -> object (new obj instance of 'cls')
  - create new instance of class 'cls'
  - static method; takes class of which an instance was requested as 1st arg
  - remaining args are those passed to obj constructor expr.

__init__
  - called after __new__, but before returned to caller
  - args are those passed to the class constructor
  - if base class has __init__, derived class's __init__ MUST explicitly call it for proper initialization
  - b/c __new__ works with __init__ (__new__ creates, __init__ customizes) no non-None value can be returned

__del__
  - called when instance is about to be destroyed
  - if base class has __del__, derived class's __del__ MUST explicitly call it for proper deletion

__repr__ -> str
  - called by repr()
  - computes 'official' str representation of the obj.
  - should look like a valid Python expression that could be used to recreate an object with the same value
  - if not possible, a str like <...some useful description...> should be returned
  - if class defines __repr__ but ! __str__ then __repr__ is used when 'informal' str value is required

__str__ -> str
  - called by str(), format(), print()
  - no expectation that __str__ returns valid Python expression

__bytes__ -> bytes
  - called by bytes()

__format__ -> str
  - called by format() & str.format()

__lt__
__le__
__eq__
__ne__
__gt__
__ge__
  - rich comparison methods
  - x < y => x.__lt__(y)
  - x <= y => x.__le__(y)
  - x == y => x.__eq__(y)
  - x != y => x.__ne__(y)
  - x > y => x.__gt__(y)
  - x >= y => x.__ge__(y)

__hash__ -> int
  - called by hash(), & for ops on members of hashed collections including set, frozenset, & dict
  - only required propertyis that obj that compare == must have same hash value
  - advised to mix hash values of comparable components into a tuple & hash the tuple
    - e.g.  return hash((self.name, self.nick, self.color))
  - if __eq__ is ! defined it should ! define __hash__
  - if __eq__ is defined but ! __hash__ instances will not be usable as items in hashable collections
  - if class defines mutable objs & implements __eq__ it should ! implement __hash__
    - the implementation of hashable collections requires that a key's hash value is immutable
  - class overriding __eq__ and ! define __hash__ has it's __hash__ set to None
    - attempts to get the hash value raise TypeError
    - will be identified as unhashable when shecking isinstance(obj, collections.Hashable)
  - if class overriding __eq__ needs to retain parent's __hash__, set __hash__ = <ParentClass>.__hash__
  - if class ! overriding __eq__ wants to suppress has support, include __hash__ = None in class definition
    - class defining __hash__ to raise a TypeError will be incorrectly identified as hashable by an
      isinstance(obj, collections.Hashable) call

__bool__ -> bool
  - called to implement truth value testing & by bool()
  - if ! defined __len__ is called (if defined) & obj is True if result is non-zero
  - if class ! define __len__ or __bool__ all instances considered True

'''


# root object for Gliffy files
class Stage(object):
    # settable values used in typeDef
    title = 'GliffyDB'
    width = 0
    height = 0

    # json object definition
    typeDef = {
        'contentType': 'application/gliffy+json',
        'version': '1.1',
        'metadata': {
            'title': 'GliffyDB',
            'revision': 0,
            'exportBorder': 'false'
        },
        'embeddedResources': {
            'index': 0,
            'resources': []
        },
        'stage': {
            'objects': [
                # the 'cells' go in here
            ],
            'background': '#FFFFFF',
            'width': 0,  # TODO: this will need to be changed later
            'height': 0,  # TODO: this will need to be changed later
            'maxWidth': 5000,
            'maxHeight': 5000,
            'nodeIndex': 0,
            'autoFit': True,
            'exportBorder': False,
            'gridOn': True,
            'snapToGrid': True,
            'drawingGuidesOn': True,
            'pageBreaksOn': False,
            'printGridOn': False,
            'printPaper': 'LETTER',
            'printShrinkToFit': False,
            'printPortrait': True,
            'shapeStyles': {},
            'lineStyles': {
                'global': {
                    'orthoMode': 1,
                    'startArrow': 0,
                    'endArrow': 1,
                    'stroke': '#000000',
                    'dashStyle': None
                }
            },
            'textStyles': {},
            'themeData': None
        }
    }

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', 'GliffyDB')
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)

    def __str__(self):
        self.typeDef['metadata']['title'] = self.title
        self.typeDef['stage']['width'] = self.width
        self.typeDef['stage']['height'] = self.height

        return json.dumps(self.typeDef)

    def add(self, obj):
        # type: (obj) -> Stage
        """
        Adds a Gliffy object to the stage

        :param obj obj: The object to add to the stage
        :return: Stage instance
        :rtype: Stage
        """
        if isinstance(obj, Entity):
            self.typeDef['stage']['objects'].append(obj)
        else:
            raise Exception('Unable to add invalid object type "{}" to Stage'.format(type(obj)))

        return self


class Entity(object):
    typeDef = {
        'x': 0,
        'y': 0,
        'rotation': 0,
        'id': 0,
        'uid': None,
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
        return json.dumps(self.typeDef)

    def add_child(self, child):
        self.typeDef['children'].append(child)


# group to hold multiple objects together
class Group(Entity):

    def __init__(self):
        self.typeDef['uid'] = 'com.gliffy.shape.basic.basic_v1.default.group'


class Graphic(object):
    type = None
    typeDef = {}

    def __str__(self):
        return json.dumps({'type': self.type, self.type: self.typeDef})

    def get_uid(self):
        return None


# #cccccc is gray

# basic rectangle
class Rectangle(Graphic):
    type = 'Shape'
    typeDef = {
        'tid': 'com.gliffy.stencil.rectangle.basic_v1',
        'strokeWidth': 1,
        'strokeColor': '#000000',
        'fillColor': '#ffffff',
        'gradient': False,
        'dropShadow': False,
        'state': 0,
        'shadowX': 0,
        'shadowY': 0,
        'opacity': 1
    }

    def get_uid(self):
        # type: () -> str
        """
        :return: The uid needed by the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.erd.erd_v1.default.entity'


class Text(Graphic):
    type = 'Text'
    typeDef = {
        'tid': None,
        'valign': 'middle',
        'overflow': 'none',
        'vposition': 'none',
        'hposition': 'none',
        'html': '<p style="{}"><span style="{}">{}</span></p>',
        'paddingLeft': 2,
        'paddingRight': 2,
        'paddingBottom': 2,
        'paddingTop': 2
    }


class Line(Graphic):
    type = 'Line'
    typeDef = {
        'strokeWidth': 2,
        'strokeColor': '#000000',
        'fillColor': 'none',
        'dashStyle': None,
        'startArrow': 0,
        'endArrow': 0,
        'startArrowRotation': 'auto',
        'endArrowRotation': 'auto',
        'ortho': True,
        'interpolationType': 'linear',
        'cornerRadius': 10,
        'controlPath': [],
        'lockSegments': {}
    }

    def get_uid(self):
        # type: () -> str
        """
        :return: The uid needed by the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.line'


class Constraint(object):
    _kind_map = {
        'startConstraint': 'StartPositionConstraint',
        'endConstraint': 'EndPositionConstraint',
    }

    nodeId = 0
    px = 0
    py = 0
    _kind = ''
    _type = ''

    def __init__(self, kind):
        if not self._kind_map[kind]:
            raise Exception('Invalid Constraint {}'.format(kind))

        # preserve the kind & type for later
        self._kind = kind
        self._type = t = self._kind_map[kind]
        # create property with name of indicated kind
        setattr(self, kind, {
            'type': t,
            t: {
                'nodeId': self.nodeId,
                'px': self.px,
                'py': self.py
            }
        })

    def __str__(self):
        k = getattr(self, self._kind)
        t = self._type
        k[t]['nodeId'] = self.nodeId
        k[t]['px'] = self.px
        k[t]['py'] = self.py

        return json.dumps(k)

    '''
    'constraints': {
        'constraints': [],
        'startConstraint': {
            'type': 'StartPositionConstraint',
            'StartPositionConstraint': {
                'nodeId': 0,
                'px': 0,
                'py': 0
            }
        },
        'endConstraint': {
            'type': 'EndPositionConstraint',
            'EndPositionConstraint': {
                'nodeId': 0,
                'px': 0,
                'py': 0
            }
        }
    },
    '''


# css used in text.graphic.Text.html
_textCSS = {
    'text-align': 'left',  # left, center, right
    'font-size': '12px',
    'font-family': 'Courier',
    'white-space': 'pre-wrap',
    'text-decoration': 'none',
    'font-style': 'none',
    'line-height': '12px',  # should = font-size
    'color': 'rgb(0, 0, 0)'
}

_line = {
    'x': 0,
    'y': 0,
    'rotation': 0,
    'id': 0,
    'uid': 'com.gliffy.shape.basic.basic_v1.default.line',
    'width': 0,
    'height': 0,
    'lockAspectRatio': False,
    'lockShape': False,
    'order': 0,
    'graphic': {
        'type': 'Line',
        'Line': {
            'strokeWidth': 2,
            'strokeColor': '#000000',
            'fillColor': 'none',
            'dashStyle': None,
            'startArrow': 0,
            'endArrow': 0,
            'startArrowRotation': 'auto',
            'endArrowRotation': 'auto',
            'ortho': True,
            'interpolationType': 'linear',
            'cornerRadius': 10,
            'controlPath': [
                [9.740259795473818, 30.666666666666664], [9.740259795473818, 5.666666666666664],
                [-14.906926462140476, 5.666666666666664], [-14.906926462140476, -19.333333333333336]
            ],
            'lockSegments': {}
        }
    },
    'children': None,
    'constraints': {
        'constraints': [],
        'startConstraint': {
            'type': 'StartPositionConstraint',
            'StartPositionConstraint': {
                'nodeId': 0,
                'px': 0,
                'py': 0
            }
        },
        'endConstraint': {
            'type': 'EndPositionConstraint',
            'EndPositionConstraint': {
                'nodeId': 0,
                'px': 0,
                'py': 0
            }
        }
    },
    'linkMap': []
}
