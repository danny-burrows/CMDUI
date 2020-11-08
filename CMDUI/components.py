import math
import random


class Pack:
    """Geometry manager Pack."""


    def pack(self, expand=False, side="top", fill="none"):
        assert isinstance(expand, bool), \
            "Parameter 'expand' must be a boolean!"
        assert side in ("top", "bottom", "left", "right"), \
            "Parameter 'side' must be one of the following 'top', 'bottom', 'left', or 'right'."
        assert fill in ("none", "both", "x", "y"), \
            "Parameter 'fill' must be one of the following 'none', 'both', 'x', or 'y'."

        if self in self.parent.packed_items:
            return False
        self.parent.packed_items.append(self)
        self.cmdui_obj.visable_widgets.append(self)
        
        self.expand = expand
        self.side = side
        self.fill = fill


class Frame(Pack):


    def __init__(self, parent, x=0, y=0, width=0, height=0):
        self.parent = parent
        self.cmdui_obj = self.parent.cmdui_obj
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.packed_items = []
        self.expand = False
        self.side = "top"
        self.fill = "none"


    def draw(self):
        x = ["a","c","d","0","1","2","3","4","5","6","7","8","9"]
        color_hex = int(f"0x{random.choice(x)}f", 16)
        self.paint_background(color_hex)


    def undraw(self):
        pass

    
    def paint_background(self, color):
        self.cmdui_obj.console_manager.color_area(
            self.x, 
            self.y, 
            self.width, 
            self.height, 
            color
        )

    
    def update_pack(self, force_draw=False):
        # https://www.tcl.tk/man/tcl8.6/TkCmd/pack.htm

        # PASS #1

        width = max_width = 0
        height = max_height = 0

        for widget in self.packed_items:
            if widget.side == "top" or widget.side == "bottom":
                tmp = widget.width + width
                if tmp > max_width:
                    max_width = tmp
                height += widget.height
            else:
                tmp = widget.height + height
                if tmp > max_height:
                    max_height = tmp
                width += widget.width
        
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

        # Expand window or frame if required...
        if max_width > self.width:
            self.width = max_width
        if max_height > self.height:
            self.height = max_height

        # If window size already changed then just stop and try again in a mo...
        # if max_width != self.width or max_height != self.height:
        #     self.update_pack()
        
        # PASS #2

        cavity_x = self.x
        cavity_y = self.y

        cavity_width = self.width
        cavity_height = self.height

        for widget_num, widget in enumerate(self.packed_items):
            if widget.side == "top" or widget.side == "bottom":
                frame_width = cavity_width
                frame_height = widget.height
                if widget.expand:
                    frame_height += self.y_expansion(widget_num, cavity_height)

                cavity_height -= frame_height
                if cavity_height < 0:
                    frame_height += cavity_height
                    cavity_height = 0

                frame_x = cavity_x
                if widget.side == "top":
                    frame_y = cavity_y
                    cavity_y += frame_height
                else:
                    frame_y = cavity_y + cavity_height
            else:
                frame_height = cavity_height
                frame_width = widget.width
                if widget.expand:
                    frame_width += self.x_expansion(widget_num, cavity_width)

                cavity_width -= frame_width
                if cavity_width < 0:
                    frame_width += cavity_width
                    cavity_width = 0

                frame_y = cavity_y
                if widget.side == "left":
                    frame_x = cavity_x
                    cavity_x += frame_width
                else:
                    frame_x = cavity_x + cavity_width

            widget.pack_frame = [frame_x, frame_y, frame_width, frame_height]            
            
            # Extra for CMDUI...
            x = ["a","c","d","1","2","3","4","5","6","7","8","9"]
            h = int(f"0x{random.choice(x)}f", 16)
            self.cmdui_obj.console_manager.color_area(frame_x, frame_y, frame_width, frame_height, h)
            #time.sleep(0.7)
            
            new_wx = math.floor((frame_width / 2) - (widget.width / 2)) + frame_x if widget.width <= frame_width else frame_x 
            new_wy = math.floor((frame_height / 2) - (widget.height / 2)) + frame_y if widget.height <= frame_height else frame_y    

            if not force_draw and new_wx == widget.x and new_wy == widget.y:
                return

            widget.x = new_wx
            widget.y = new_wy
            
            widget.draw()
            if isinstance(widget, Frame):
                widget.update_pack(force_draw=True)


    def x_expansion(self, widget_num, cavity_width):
        minExpand = cavity_width
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_items)):
            widget = self.packed_items[widget_n]
            child_width = widget.width
            
            if widget.side == "top" or widget.side == "bottom":
                if num_expand:
                    cur_expand = (cavity_width - child_width) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_width -= child_width
                if widget.expand:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_width / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


    def y_expansion(self, widget_num, cavity_height):
        minExpand = cavity_height
        num_expand = 0
        for widget_n in range(widget_num, len(self.packed_items)):
            widget = self.packed_items[widget_n]
            child_height = widget.height
            
            if widget.side == "left" or widget.side == "right":
                if num_expand:
                    cur_expand = (cavity_height - child_height) / num_expand
                    if cur_expand < minExpand:
                        minExpand = cur_expand
            else:
                cavity_height -= child_height
                if widget.expand:
                    num_expand += 1
        
        if num_expand:
            cur_expand = cavity_height / num_expand
            if cur_expand < minExpand:
                minExpand = cur_expand
        
        return int(minExpand) if not (minExpand < 0) else 0


class Widget(Pack):


    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.cmdui_obj = self.parent.cmdui_obj
        
        self.x = x
        self.y = y
        self.display = ""

        self.pack_frame = [0, 0, 0, 0]
        self.expand = False
        self.side = "top"
        self.fill = "none"
    

    def re_pack(self):

        # Need to check if the windows new position is too big for the current frame!
        if self.width > (self.pack_frame[2]-self.pack_frame[0]) or self.height > (self.pack_frame[3]-self.pack_frame[1]):
            self.cmdui_obj.update_pack(force_draw=True)
            return

        new_wx = math.floor((self.pack_frame[2] / 2) - (self.width / 2)) + self.pack_frame[0] if self.width <= self.pack_frame[2] else self.pack_frame[0] 
        new_wy = math.floor((self.pack_frame[3] / 2) - (self.height / 2)) + self.pack_frame[1] if self.height <= self.pack_frame[3] else self.pack_frame[1] 
        self.undraw()
        self.x = new_wx
        self.y = new_wy
        self.draw()


    def draw(self):
        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i, segment in enumerate(self.display):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, segment)


    def undraw(self):
        x_coord = self.x if self.x > 0 else 0
        y_coord = self.y if self.y > 0 else 0

        for i, segment in enumerate(self.display):
            self.cmdui_obj.console_manager.print_pos(x_coord, y_coord+i, " "*len(segment))


    def check_inside(self, x, y):
        if x >= self.x and x < self.x+self.width and \
           y >= self.y and y < self.y+self.height:
            return True
        else:
            return False


    def check_hover(self, x, y):
        pass


    def on_press(self, x, y):
        pass


    def on_release(self):
        pass

    
    @property
    def width(self):
        return len(self.display[0])


    @property
    def height(self):
        return len(self.display)
