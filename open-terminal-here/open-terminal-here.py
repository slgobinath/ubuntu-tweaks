# open-terminal-here.py Open Terminal in Current Directory from Nemo
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, subprocess
import urllib

from gi.repository import Nemo, GObject, GConf

class OpenTerminalHereExtension(Nemo.MenuProvider, GObject.GObject):
    def __init__(self):
        self.client = GConf.Client.get_default()
        
    def _open_terminal(self, file):
        filename = urllib.unquote(file.get_uri()[7:])
        os.chdir(filename)

        # Select the 0th tab, rename the tab using current directory name, change the directory and clear the cd command
        # commad = "guake -s 0 --rename-tab=" + os.path.basename(filename) + " --show --execute-command=\"cd '" + filename + "'; clear\""
        
        # Select the 0th tab, change the directory and clear the cd command
        commad = "guake -s 0 --show --execute-command=\"cd '" + filename + "'; clear\""

        # Open a new tab, change the directory and clear the cd command
        # commad = "guake -n -s --show --execute-command=\"cd '" + filename + "'; clear\""
        subprocess.call(commad, shell=True)
        
    def menu_activate_cb(self, menu, file):
        self._open_terminal(file)
        
    def menu_background_activate_cb(self, menu, file): 
        self._open_terminal(file)
       
    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        
        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != 'file':
            return
        
        item = Nemo.MenuItem(name='NemoPython::open_terminal_item',
                                 label='Open Terminal Here' ,
                                 tip='Open Terminal In %s' % file.get_name())
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        item = Nemo.MenuItem(name='NemoPython::open_terminal_item',
                                 label='Open Terminal Here',
                                 tip='Open Terminal In This Directory')
        item.connect('activate', self.menu_background_activate_cb, file)
        return item,
