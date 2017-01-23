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





class Graphic(GliffyObject):
    type = None
    type_def = {}
    base = None

    def __init__(self):
        self.base = BaseEntity()

    def __str__(self):
        return json.dumps({'type': self.type, self.type: self.get_data()})

    def get_uid(self):
        """
        Returns the uid needed by the BaseEntity

        Returning false means "don't change it"
        Returning anything else means "set it to this"

        :return: False
        :rtype: bool
        """
        return False

    def get_data(self):
        raise Exception('Graphic object has no get_data() method defined')


# #cccccc is gray

# basic rectangle
# this will need to be added as an Entity.graphic child
class Rectangle(Graphic):

    # holds merged default + user-supplied CSS options
    opts = {
        'strokeWidth': 1,
        'strokeColor': '#000000',
        'fillColor': '#ffffff',
    }

    # type of Gliffy object
    type = 'Shape'

    # Gliffy JSON definition data
    type_def = {
        'tid': 'com.gliffy.stencil.rectangle.basic_v1',
        'strokeWidth': 0,
        'strokeColor': '',
        'fillColor': '',
        'gradient': False,
        'dropShadow': False,
        'state': 0,
        'shadowX': 0,
        'shadowY': 0,
        'opacity': 1
    }

    def __init__(self, opts={}):
        # type: (dict) -> Rectangle
        """
        Creates a new Gliffy Rectangle object

        :param dict opts: Options for styling the Rectangle
                          Valid options are ``strokeWidth`` (``int``), ``strokeColor`` & ``fillColor`` (``hex``)
        :rtype: Rectangle
        """
        super().__init__()
        self.set_opts(opts)
        self.base.set_graphic(self)

    def get_uid(self):
        return 'com.gliffy.shape.erd.erd_v1.default.entity'

    def get_type(self):
        return self.type

    def get_type_def(self):
        self.type_def = merge_dicts(self.type_def, self.opts)


    def set_opts(self, opts={}):
        # type: (dict) -> Rectangle
        if opts:
            tmp = merge_dicts(self.opts, opts)
            self.opts = tmp

        return self

    def to_json(self):
        """
        Returns the whole JSON data set for the Rectangle, including the
        outer BaseEntity code

        :rtype: str
        """

        return self.type_def


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


class Constraint(GliffyObject):
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
