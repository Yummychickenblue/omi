import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileSystemModel

import window  #Module that just has a generic class to load PyQT UIs.
import modinstaller  #This module is where most of the work is done.


class Interface(window.App):
    #Initializes the required QApplication object. 
    #The window module is a generic skeleton I made for loading PyQT 
    #programs.
    def __init__(self, args):
        super().__init__(args)
        self.old_model = QtWidgets.QFileSystemModel()
        
    #Generic function to call a directory select dialog.
    #should the 'home' variable be made global?
    def show_directory_select_dialog(self):
         home = os.environ.get('HOME')
         dialog = QtWidgets.QFileDialog(self.window,
                                        "Choose a Mod",
                                        (home))
         dialog.setNameFilter("Folders")
         directory = str(dialog.getExistingDirectory())
         return(directory)
    
    #Sets the originals pane to a QFileSystemModel
    def create_old_file_view(self):
        self.window.Originals.setModel(self.old_model)
        
    #Sets the pane in the Mod Installer to the global contents
    #var based on the directory selected from the dialog that gets
    #called.
    def set_old_file_view_contents(self):
        global contents
        contents = self.show_directory_select_dialog()
        self.old_model.setRootPath(contents)
        self.window.Originals.setRootIndex(self.old_model.index(contents))
        self.window.normalize.setDisabled(False)

    #sets the functionality for the mod_dir_chooser pushbutton
    #(labeled as "Choose Mod" in the UI)
    def mod_dir_chooser(self):
        #making a hanging indent to comply with pep8 makes this harder
        #to read
        self.window.ModDirChooser.clicked.connect(self.set_old_file_view_contents)
    
    #Sets the functionality for the normalize button
    #(Labeled as "Normalize and Install" in the UI)
    def normalize(self):
        self.window.normalize.clicked.connect(normalize_and_install)
        self.window.normalize.setDisabled(True)
    
    
def normalize_and_install():
    #Global var contents from set_old_file_view_contents
    #if statement is used instead of try block because NameError
    #catches things we don't want to catch
    if len(contents) > 0:
        os.chdir(contents)
        modinstaller.normalize(contents)
        modinstaller.install(contents)
    else:
        print('contents was empty!')
    #except NameError:
        #print('NameError')
    modinstaller.write_openmwcfg(contents)
            
if __name__ == '__main__':
    #All this is to initialize the class and set everything defined
    #above. Maybe making a class and then calling every function 
    #isn't The Right Way to do things, but I'm not sure of a better
    #one.
    windowinterface = Interface(args = sys.argv)
    windowinterface.make_window()
    windowinterface.create_old_file_view()
    windowinterface.mod_dir_chooser()
    windowinterface.normalize()
    windowinterface.set_window_title(name='Omi')
    windowinterface.show_window()
    sys.exit(windowinterface.exec_())
