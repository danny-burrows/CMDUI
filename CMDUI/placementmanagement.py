class Pack:
    """Geometry manager Pack."""


    def pack_configure(self):
        """Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                  given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
        """
        pass

    pack = configure = config = pack_configure


    def pack_forget(self):
        """Unmap this widget and do not use it for the packing order."""
        pass

    forget = pack_forget


    def pack_info(self):
        """Return information about the packing options
        for this widget."""
        pass

    info = pack_info


class Place:
    """Geometry manager Place."""


    def place_configure(self):
        """Place a widget in the parent widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                      relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0
                          relative to width of master (1.0 is the same width
                          as the master)
        relheight=amount - height of this widget between 0.0 and 1.0
                           relative to height of master (1.0 is the same
                           height as the master)
        bordermode="inside" or "outside" - whether to take border width of
                                           master widget into account
        """
        pass

    place = configure = config = place_configure


    def place_forget(self):
        """Unmap this widget."""
        pass

    forget = place_forget


    def place_info(self):
        """Return information about the placing options
        for this widget."""
        pass

    info = place_info


class Grid:
    """Geometry manager Grid."""


    def grid_configure(self):
        """Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        pass

    grid = configure = config = grid_configure


    def grid_forget(self):
        """Unmap this widget."""
        pass

    forget = grid_forget


    def grid_remove(self):
        """Unmap this widget but remember the grid options."""
        pass

    remove = grid_remove


    def grid_info(self):
        """Return information about the options
        for positioning this widget in a grid."""
        pass

    info = grid_info


class Widget(Pack, Place, Grid):
    pass