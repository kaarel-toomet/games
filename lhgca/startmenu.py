### load/save files, file dialogs and all that
import numpy as np
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

def startMenu():
    def on_button_toggled(button, name):
        nonlocal toggledButton
        toggledButton = name
    def on_ok_clicked(button):
        win.destroy()
        # have to destroy window, main_quit() does not do it
        Gtk.main_quit()
    toggledButton = "dense"
    ##
    win = Gtk.Window(title="Explosion type")
    win.set_border_width(20)
    hbox = Gtk.Box(spacing=10)
    win.add(hbox)

    button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Dense")
    button1.connect("toggled", on_button_toggled, "dense")
    hbox.pack_start(button1, False, False, 0)

    button2 = Gtk.RadioButton.new_from_widget(button1)
    button2.set_label("Shell")
    button2.connect("toggled", on_button_toggled, "shell")
    hbox.pack_start(button2, False, False, 0)

    button = Gtk.Button.new_with_label("OK")
    button.connect("clicked", on_ok_clicked)
    hbox.pack_start(button, True, True, 0)
    
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    ##
    Gtk.main()
    return toggledButton

## Global window
gtkRootWin = Gtk.Window(title="lhgca start menu")
gtkRootWin.connect("destroy", Gtk.main_quit)
gtkRootWin.hide()
