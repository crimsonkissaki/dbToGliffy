"""

"""

# Standard Library
import json
# Third Party
# Local
from .base import GliffyObject
from utils import util


class Graphic(GliffyObject):

    __slots__ = 'type_def'

    def __init__(self):
        self.type_def = {
            'type': 'UNDEFINED',
            'UNDEFINED': {}
        }

    def get_type(self):
        # type: () -> str
        return self.type_def['type']

    def set_type(self, type):
        # type: (str) -> Shape
        self.type_def['type'] = type

        return self

    def set_tid(self, tid):
        # type: (str) -> Shape
        self.type_def[self.get_type()]['tid'] = tid

        return self

    def get_entity_uid(self):
        # type: () -> bool
        """
        Returns the UID value required by the Entity.

        Returns ``False`` if there is no change required to the default UID

        :return: A value that tells the Entity no special UID value is required
        :rtype: bool
        """
        return False

    def get_type_def(self):
        # type: () -> dict
        return self.type_def

    def to_json(self):
        # type: () -> str
        return json.dumps(self.get_type_def())


class Shape(Graphic):

    __slots__ = ('type_def', 'properties')

    def __init__(self):
        self.type_def = {
            'type': 'Shape',
            'Shape': {
                'tid': None,
                'strokeWidth': 2,
                'strokeColor': '#000000',
                'fillColor': '#FFFFFF',
                'gradient': False,
                'dropShadow': False,
                'state': 0,
                'shadowX': 0,
                'shadowY': 0,
                'opacity': 1
            }
        }
        self.properties = {
            'strokeWidth': 2,
            'strokeColor': '#000000',
            'fillColor': '#FFFFFF',
        }

    def set_properties(self, props):
        # type: (dict) -> Shape
        util.join_dicts(self.properties, props)

        return self

    def get_type_def(self):
        # type: () -> dict
        util.join_dicts(self.type_def['Shape'], self.properties)

        return self.type_def


class Circle(Shape):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.set_tid('com.gliffy.stencil.ellipse.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.circle'


class Ellipse(Shape):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.set_tid('com.gliffy.stencil.ellipse.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.ellipse'


class Hexagon(Shape):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.set_tid('com.gliffy.stencil.hexagon.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.hexagon'


class Rectangle(Shape):

    __slots__ = 'type_def'

    def __init__(self, properties={}):
        super().__init__()
        self.set_tid('com.gliffy.stencil.rectangle.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.rectangle'


class Square(Shape):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.set_tid('com.gliffy.stencil.rectangle.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.square'


class Triangle(Shape):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.set_tid('com.gliffy.stencil.triangle.basic_v1')

    def get_entity_uid(self):
        # type: () -> str
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.triangle'


class Text(Graphic):

    __slots__ = ('type_def', 'properties')

    def __init__(self, properties={}):
        # type: (dict) -> Text
        """
        :param dict properties:
        :keyword properties.text:  ``str`` Text to display
        :keyword properties.css:   ``dict`` CSS settings to apply to the text.\n
                        Valid properties are:\n
                        ``str``:
                            ``text-align``  (left, middle, right)\n
                            ``font-size``   (9-14px, 18px, 24px, 36px, 48px)\n
                            ``font-family`` (Arial, Helvetica, Courier, Times, Verdana)\n
                            ``color``       (#xxxxxx)\n
                        ``bool``:
                            ``bold``, ``italics``, ``underline``
        """
        super().__init__()
        self.type_def = {
            'type': 'Text',
            'Text': {
                'tid': None,
                'valign': 'middle',
                'overflow': 'none',
                'vposition': 'none',
                'hposition': 'none',
                'html': '<p><span></span></p>',
                'paddingLeft': 2,
                'paddingRight': 2,
                'paddingBottom': 2,
                'paddingTop': 2
            }
        }
        # customizable Text settings
        self.properties = {
            # the text to show
            'text': '',
            'css': {
                'text-align': 'center',
                'font-size': '12px',
                'font-family': 'Courier',
                'color': '#000000',
                'bold': False,
                'italics': False,
                'underline': False,
            },
        }
        self.set_properties(properties)

    def set_properties(self, props):
        # type: (dict) -> Text
        util.join_dicts(self.properties, props)

        return self

    def get_entity_uid(self):
        # type: () -> None
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return None

    def get_type_def(self):
        # type: () -> dict

        def _build_html(props):
            css = props['css']
            p_css = 'text-align:{};'.format(css['text-align'])
            css_props = ['font-size: {};', 'font-family: {};', 'white-space: pre-wrap;',
                         'text-decoration: {};', 'line-height: {};', 'color: {};']
            td = 'none'
            if css['bold']:
                css_props.append('font-weight: bold;')
            if css['italics']:
                css_props.append('font-style: italic;')
            if css['underline']:
                td = 'underline'
            span_css = ' '.join(css_props).format(css['font-size'], css['font-family'], td,
                                                  css['font-size'], css['color'])

            return '<p style=\'{}\'><span style=\'{}\'>{}</span></p>'.format(p_css, span_css, props['text'])

        util.join_dicts(self.type_def['Text'], self.properties)
        self.type_def['Text']['html'] = _build_html(self.properties)

        return self.type_def


# this class requires constraints be added
class Line(Graphic):

    __slots__ = 'type_def'

    def __init__(self):
        super().__init__()
        self.type_def = {
            'type': 'Line',
            'Line': {
                'strokeWidth': 2,
                'strokeColor': '#000000',
                'fillColor': 'none',
                'dashStyle': None,
                'startArrow': 0,
                'endArrow': 1,
                'startArrowRotation': 'auto',
                'endArrowRotation': 'auto',
                'ortho': True,
                'interpolationType': 'linear',
                'cornerRadius': 10,
                'controlPath': [[9.740259795473818, 30.666666666666664], [9.740259795473818, 5.666666666666664],
                                [-14.906926462140476, 5.666666666666664], [-14.906926462140476, -19.333333333333336]],
                'lockSegments': {}
            }
        }

    def get_entity_uid(self):
        # type: () -> None
        """
        :return: The UID value required for the Entity
        :rtype: str
        """
        return 'com.gliffy.shape.basic.basic_v1.default.line'
