# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
#    OpenTranscribe.py
#
#    Adds an option to open the selected track in Transcribe
#    Copyright (C) 2012-2016 Donagh Horgan <donagh.horgan@gmail.com>
#
#    Partly based on open-containing-folder by Donagh Horgan
#    Copyright (C) 2012-2016 Donagh Horgan <donagh.horgan@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gio, GObject, Gtk, Peas, RB
import logging
import os
import subprocess
import urllib

class OpenTranscribe(GObject.Object, Peas.Activatable):

    """Adds an option to open the selected song in Transcribe to
    the right click context menu."""

    object = GObject.property(type=GObject.Object)

    _action = 'open-transcribe'
    _locations = ['browser-popup',
                  'playlist-popup',
                  'podcast-episode-popup',
                  'queue-popup']

    def __init__(self):
        super(OpenTranscribe, self).__init__()
        self._app = Gio.Application.get_default()

    def open_folder(self, *args):
        """Open the song in Transcribe

        Args:
            args: Additional arguments. These are ignored.
        """
        page = self.object.props.selected_page
        try:
            selected = page.get_entry_view().get_selected_entries()
            if selected:
                uri = selected[0].get_playback_uri()
                uri = urllib.parse.unquote(uri)
                dirpath = uri
                dirpath = '/' if not dirpath else dirpath[5:]
                # subprocess.check_call(['/home/pierpo/transcribe/transcribe', dirpath])
                subprocess.check_call(['transcribe', dirpath])
        except:
            logging.exception('Could not open folder')

    def do_activate(self):
        """Activate the plugin."""
        logging.debug('Activating plugin...')

        action = Gio.SimpleAction(name=OpenTranscribe._action)
        action.connect('activate', self.open_folder)
        self._app.add_action(action)

        item = Gio.MenuItem()
        item.set_label('Open in Transcribe')
        item.set_detailed_action('app.%s' % OpenTranscribe._action)

        for location in OpenTranscribe._locations:
            self._app.add_plugin_menu_item(location,
                                           OpenTranscribe._action,
                                           item)

    def do_deactivate(self):
        """Deactivate the plugin."""
        logging.debug('Deactivating plugin...')

        for location in OpenTranscribe._locations:
            self._app.remove_plugin_menu_item(location,
                                              OpenTranscribe._action)
