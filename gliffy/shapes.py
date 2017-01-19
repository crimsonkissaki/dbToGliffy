"""
Various Gliffy shapes that will be used.
"""

# Standard Library
import json
# Third Party
# Local

# root object for Gliffy files
_stage = {
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

VALIGN = {
    'TOP': 'top',
    'MIDDLE': 'middle',
    'BOTTOM': 'bottom'
}

ALIGN = {
    'LEFT': 'left',
    'CENTER': 'center',
    'RIGHT': 'right'
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
    'BOLD': 'bold',
    # text-decoration: none; font-style: italic;
    'ITALICS': 'italic',
    # text-decoration: underline;
    'UNDERLINE': 'underline',
}


class Entity(object):
    x = 0
    y = 0
    rotation = 0
    id = 0
    uid = None
    width = 0
    height = 0
    lockAspectRatio = False
    lockShape = False
    order = 0
    graphic = None
    children = []
    linkMap = []

    def add_child(self, child):
        self.children.append(child)


# group to hold multiple objects together
class Group(Entity):
    uid = 'com.gliffy.shape.basic.basic_v1.default.group'


class Graphic(object):
    type = None
    typeDef = {}

    def __str__(self):
        return json.dumps({'type': self.type, self.type: self.typeDef})


# #cccccc is gray

# basic rectangle
class Rectangle(Graphic):
    type = 'Shape'
    Shape = {
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
        'controlPath': [
            [9.740259795473818, 30.666666666666664], [9.740259795473818, 5.666666666666664],
            [-14.906926462140476, 5.666666666666664], [-14.906926462140476, -19.333333333333336]
        ],
        'lockSegments': {}
    }

    def get_uid(self):
        # type: () -> str
        """
        :return: The uid needed by the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.line'


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
