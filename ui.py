import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import os
import sys

import config
import util

class Window(Gtk.Window):
    def __init__(self, config_path=config.CONFIG):
        Gtk.Window.__init__(self, title="craftit")
        self.set_size_request(500, 500)

        self.conf = config.get_config(config_path)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        # the user input after they press enter
        self.entry_text = ""

        # creates the widgets needed and aligns them
        self._create_textview()
        self._create_entry()

    def _modify_color(self, widget, color_field):
        _ = util.hex2rgb(config.get_color_field(self.conf, color_field))

        if "fg" in color_field:
            widget.override_color(Gtk.StateType.NORMAL,
                                  Gdk.RGBA(_[0], _[1], _[2]))
        else:
            widget.override_background_color(Gtk.StateType.NORMAL,
                                             Gdk.RGBA(_[0], _[1], _[2]))
        
    def _create_textview(self):
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.grid.attach(self.scrolledwindow, 0, 0, 100, 90)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self._modify_color(self.textview, "window_bg")
        self._modify_color(self.textview, "window_fg")

        self.textbuffer = self.textview.get_buffer()
        self.scrolledwindow.add(self.textview)

    def show_image(self, image_path):
        try:
            image_path = os.path.abspath(image_path)
            if not os.path.isfile(image_path):
                raise ImageNotFoundError
        except:
            print(f"error: cannot load image {image_path}", file=sys.stderr)

        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path,
                                                             50,
                                                             50,
                                                             True)
        except:
            print(f"error: cannot load image {image_path}", file=sys.stderr)

        self.add_text("")
        self.textbuffer.insert_pixbuf(self.textbuffer.get_end_iter(), pixbuf)

    def add_text(self, text):
        self.textbuffer.insert(self.textbuffer.get_end_iter(),
                               f"\n{text}")

    def _create_entry(self):
        prompt_label = Gtk.Label()
        prompt_label.set_text(self.conf.get("prompt", ">"))
        prompt_label.set_selectable(False)
        prompt_label.set_justify(Gtk.Justification.RIGHT)
        self._modify_color(prompt_label, "window_bg")
        self._modify_color(prompt_label, "window_fg")
        
        self.grid.attach_next_to(prompt_label, self.scrolledwindow,
                                 Gtk.PositionType.BOTTOM, 2, 10)

        self.entry = Gtk.Entry()
        self.grid.attach_next_to(self.entry, prompt_label,
                                 Gtk.PositionType.RIGHT, 98, 10)

        self.entry.connect("activate", self._do_enter_entry)
        self.entry.set_inner_border(None)
        self._modify_color(self.entry, "input_bg")
        self._modify_color(self.entry, "input_fg")

    def _do_enter_entry(self, entry):
        self.entry_text = self.entry.get_text()
        self.entry.set_text("")
        # TODO: find a way to call an outside function cleanly
        self.add_text(self.entry_text)

    def get_input(self):
        return self.entry_text
