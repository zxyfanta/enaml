#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Enum, Event, Coerced, Int, Tuple, Typed, ForwardTyped, observe,
    set_default,
)

from enaml.application import deferred_call
from enaml.core.declarative import d_
from enaml.layout.geometry import Size

from .container import Container
from .toolkit_object import ToolkitObject
from .widget import Widget, ProxyWidget


class ProxyPopup(ProxyWidget):
    """ The abstract definition of a proxy Popup object.

    """
    #: A reference to the Popup declaration.
    declaration = ForwardTyped(lambda: Popup)

    def setup_window(self):
        raise NotImplementedError

    def set_anchor(self, anchor):
        raise NotImplementedError

    def set_radius(self, radius):
        raise NotImplementedError

    def set_arrow(self, arrow):
        raise NotImplementedError

    def set_relative_pos(self, relative_pos):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

class Popup(Widget):
    """ A Popup component

    """

    #: An enum which indicates the which side of the parent will be used
    #: as the anchor point. The default value is 'bottom'
    anchor = d_(Enum('bottom', 'left', 'right', 'top'))

    #: The size in pixels of the x and y radii of the Popup's rounded
    #: corners
    radius = d_(Int(10))

    #: The size of the Popup's anchoring arrow
    arrow = d_(Int(20))

    #: The relative of the anchor relative to the Popup's bounds
    relative_pos = d_(Tuple(float, (0.5, 0.5)))

    #: An event fired when the popup is closed. This event is triggered
    #: by the proxy object when the popup is closed.
    closed = Event()

    #: Popups are invisible by default.
    visible = set_default(False)

    #: A reference to the ProxyPopup object.
    proxy = Typed(ProxyPopup)

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def central_widget(self):
        """ Get the central widget defined on the popup.

        The last `Container` child of the window is the central widget.

        """
        for child in reversed(self.children):
            if isinstance(child, Container):
                return child

    def close(self):
        """ Send the 'close' action to the client widget.

        """
        if self.proxy_is_active:
            self.proxy.close()

    def show(self):
        """ Show the popup.

        This is a reimplemented parent class method which will init
        and build the popup hierarchy if needed.

        """
        if not self.is_initialized:
            self.initialize()
        if not self.proxy_is_active:
            self.proxy.setup_window()
            for node in self.traverse():
                if isinstance(node, ToolkitObject):
                    node.proxy_is_active = True
        super(Popup, self).show()


    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe(('anchor', 'radius', 'arrow', 'relative_pos'))
    def _update_proxy(self, change):
        """ Update the ProxyPopup when the Popup data changes.

        """
        # The superclass handler implementation is sufficient.
        super(Popup, self)._update_proxy(change)

    #--------------------------------------------------------------------------
    # Private API
    #--------------------------------------------------------------------------
    def _handle_close(self):
        """ Handle the close event from the proxy widget.

        """
        self.visible = False
        self.closed()
        deferred_call(self.destroy)
