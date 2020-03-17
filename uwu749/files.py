### load/save files, file dialogs and all that
import pickle
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

def add_filters(dialog):
    filter_wrld = Gtk.FileFilter()
    filter_wrld.set_name("CrazyHat world file .wrld")
    filter_wrld.add_pattern("*.wrld")
    dialog.add_filter(filter_wrld)
    ##
    filter_any = Gtk.FileFilter()
    filter_any.set_name("all files")
    filter_any.add_pattern("*")
    dialog.add_filter(filter_any)

def onTimeout():
    Gtk.main_quit()
    return False
    
def fileChooser(save):
    ## response variables here
    response = None
    fName = None
    ##
    if save:
        dialog = Gtk.FileChooserDialog("File to save the current world:", gtkRootWin,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name("crazy-world.wrld")
    else:
        dialog = Gtk.FileChooserDialog("World to load:", gtkRootWin,
                                       Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    add_filters(dialog)
    dialog.connect("destroy", Gtk.main_quit)
    ##
    response = dialog.run()
    fName = dialog.get_filename()
    dialog.destroy()
    ##
    GLib.timeout_add(100, onTimeout)
    Gtk.main()
    return response, fName

def loadWorld():
    response, fName = fileChooser(False)
    if response == Gtk.ResponseType.OK:
        gameState = pickle.load(open(fName, "rb"))
        return gameState
    else:
        # cancel pressed
        return None
        
def saveWorld(world, gameState):
    response, fName = fileChooser(True)
    if response == Gtk.ResponseType.OK:
        pickler = pickle.Pickler(open(fName, "wb"))
        pickler.dump(gameState)

## Global window
gtkRootWin = Gtk.Window(title="File chooser GTK parent")
gtkRootWin.connect("destroy", Gtk.main_quit)
gtkRootWin.hide()
