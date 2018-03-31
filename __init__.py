import sys
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileSystemModel

import window
import modinstaller


class interface(window.App):
    def __init__(self, args, ui):
        super().__init__(args, ui)
        self.old_model = QtWidgets.QFileSystemModel()
        
    def show_directory_select_dialog(self):
         home = os.environ.get('HOME')
         dialog = QtWidgets.QFileDialog(self.window,
                                        "Choose a Mod",
                                        (home))
         dialog.setNameFilter("Folders")
         directory = str(dialog.getExistingDirectory())
         return(directory)
    
    def create_old_file_view(self):
        self.window.Originals.setModel(self.old_model)
        
    def set_old_file_view_contents(self):
        global contents
        contents = self.show_directory_select_dialog()
        self.old_model.setRootPath(contents)
        self.window.Originals.setRootIndex(self.old_model.index(contents))

    def mod_dir_chooser(self):
        #making a hanging indent to comply with pep8 makes this harder
        #to read
        self.window.ModDirChooser.clicked.connect(self.set_old_file_view_contents)
    
    def normalize(self):
        self.window.normalize.clicked.connect(normalize_and_install)
    
    
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
    windowinterface = interface(args = sys.argv)
    windowinterface.make_window()
    windowinterface.create_old_file_view()
    windowinterface.mod_dir_chooser()
    windowinterface.normalize()
    windowinterface.set_window_title(name='Omi')
    windowinterface.show_window()
    sys.exit(windowinterface.exec_())
