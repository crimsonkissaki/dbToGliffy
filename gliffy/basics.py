"""

"""

# Standard Library
# Third Party
# Local
from .base import BaseEntity


class Group(BaseEntity):
    """
    Used to group multiple GliffyObjects together
    """

    def __init__(self):
        self.set_uid('com.gliffy.shape.basic.basic_v1.default.group')

    # groups cant have graphics
    def set_graphic(self, graphic):
        pass
