import pygtk; pygtk.require('2.0')
import gtk, os, cgi
from imageutils.size import scale_down
from unicodeutils import decode, normalize
from gtkutils.treeview import column_markup, column_pixbuf, column_text, column_toggle
from gtkutils.ui import UI, Dialog, ProgressDialog
from gtkutils import AboutDialog, ConfirmDialog, DirectoryChooserDialog
from gtkutils import pixbuf_from_file, pixbuf_from_url, pixbuf_from_url_scale
from gtkutils import text_trim

from . import __appname__, __author__, __url__, __license__
from .config import Config
from .utils import get_ui, get_icon

def main(): #{{{1
    ca = CoverArtGTK()
    gtk.main()

#}}}1

class SearchProgressDialog(ProgressDialog): #{{{1

    def __init__(self, **kwargs):
        kwargs['ui'] = get_ui('search_progress_dialog')
        super(SearchProgressDialog, self).__init__(**kwargs)



class AddFolderProgressDialog(ProgressDialog): #{{{1

    def __init__(self, **kwargs):
        kwargs['ui'] = get_ui('add_folder_progress_dialog')
        super(AddFolderProgressDialog, self).__init__(**kwargs)



class PatternsDialog(Dialog): #{{{1

    def __init__(self, patterns, underscore_to_space, **kwargs):
        kwargs['ui'] = get_ui('patterns_dialog')
        super(PatternsDialog, self).__init__(**kwargs)
        self.load_widgets([
            'patterns_view',
            'add_button',
            'remove_button',
            'up_button',
            'down_button',
            'pattern_entry',
            'underscore_check',
            ])
        self.patterns_list = gtk.ListStore(str)
        self.patterns_view.append_column(column_text('Pattern', 0))
        self.patterns_view.set_model(self.patterns_list)
        self.ui.connect_signals(self)
        for pattern in patterns:
            self.patterns_list.append([pattern])
        self.underscore_check.set_active(underscore_to_space)

    def on_patterns_view_cursor_changed(self, view):
        model, itr = self.patterns_view.get_selection().get_selected()
        order = model.get_path(itr)[0]
        self.remove_button.set_sensitive(True)
        if order != 0:
            self.up_button.set_sensitive(True)
        else:
            self.up_button.set_sensitive(False)
        if order != len(model)-1:
            self.down_button.set_sensitive(True)
        else:
            self.down_button.set_sensitive(False)

    def on_pattern_entry_changed(self, entry):
        if len(entry.get_text().strip()):
            self.add_button.set_sensitive(True)
        else:
            self.add_button.set_sensitive(False)

    def on_add_button_clicked(self, widget):
        self.patterns_list.append([self.pattern_entry.get_text().strip()])
        self.pattern_entry.set_text('')

    def on_remove_button_clicked(self, widget):
        model, itr = self.patterns_view.get_selection().get_selected()
        path = model.get_path(itr)
        del(model[path])
        self.remove_button.set_sensitive(False)

    def swap_rows(self, inc):
        model, itr = self.patterns_view.get_selection().get_selected()
        path = model.get_path(itr)[0]
        path_new = path + inc
        itr_new = model.get_iter(path_new)
        model.swap(itr, itr_new)
        if path_new == 0:
            self.up_button.set_sensitive(False)
        else:
            self.up_button.set_sensitive(True)
        if path_new == len(model)-1:
            self.down_button.set_sensitive(False)
        else:
            self.down_button.set_sensitive(True)

    def on_up_button_clicked(self, widget):
        self.swap_rows(-1)

    def on_down_button_clicked(self, widget):
        self.swap_rows(1)

    def get_patterns(self):
        return [row[0] for row in self.patterns_list]

    def get_underscore_to_space(self):
        return self.underscore_check.get_active()



class CoversDialog(Dialog): #{{{1

    def __init__(self, cover_filenames, cover_filename_output, **kwargs):
        kwargs['ui'] = get_ui('covers_dialog')
        super(CoversDialog, self).__init__(**kwargs)
        self.load_widgets([
            'cover_entry',
            'filename_entry',
            'add_button',
            'remove_button',
            'covers_view',
            ])
        self.cover_entry.set_text(cover_filename_output)
        self.covers_list = gtk.ListStore(str)
        self.covers_view.append_column(column_text('Filename', 0))
        self.covers_view.set_model(self.covers_list)
        self.ui.connect_signals(self)
        for filename in cover_filenames:
            self.covers_list.append([filename])

    def on_filename_entry_changed(self, entry):
        if len(entry.get_text().strip()):
            self.add_button.set_sensitive(True)
        else:
            self.add_button.set_sensitive(False)

    def on_add_button_clicked(self, widget):
        self.covers_list.append([self.filename_entry.get_text().strip()])
        self.filename_entry.set_text('')

    def on_remove_button_clicked(self, widget):
        model, itr = self.covers_view.get_selection().get_selected()
        path = model.get_path(itr)
        del(model[path])
        model.row_deleted(path)
        self.remove_button.set_sensitive(False)

    def on_covers_view_cursor_changed(self, widget):
        self.remove_button.set_sensitive(True)

    def get_cover_filenames(self):
        return [row[0] for row in self.covers_list]

    def get_cover_filename_output(self):
        return self.cover_entry.get_text().strip()



class SourcesDialog(Dialog): #{{{1

    COL_STATE, COL_SOURCE = range(2)

    def __init__(self, sources, excludes, **kwargs):
        kwargs['ui'] = get_ui('sources_dialog')
        super(SourcesDialog, self).__init__(**kwargs)
        self.load_widgets(['sources_view'])
        self.sources_list = gtk.ListStore(bool, str)
        self.sources_view.append_column(column_toggle('Enabled', self.COL_STATE, self.on_toggled))
        self.sources_view.append_column(column_text('Source', self.COL_SOURCE))
        self.sources_view.set_model(self.sources_list)
        for source in sorted(sources):
            self.sources_list.append([source not in excludes, source])

    def on_toggled(self, cell, path):
        self.sources_list[path][self.COL_STATE] = not cell.get_active()

    def get_sources(self):
        return [(row[self.COL_STATE], row[self.COL_SOURCE]) for row in self.sources_list]



class CoverArtGTK(UI): #{{{1

    COL_FILE, COL_DIR, COL_ALBUM, COL_ARTIST = range(4)
    COL_URL_S, COL_URL_L, COL_SOURCE, COL_SUMMARY = range(4)

    def __init__(self, **kwargs): #{{{2
        kwargs['ui'] = get_ui('main')
        super(CoverArtGTK, self).__init__(**kwargs)
        self.config = Config()
        self.ui.connect_signals(self)
        self._load_widgets()
        self._make_menus()
        self._make_views()
        self.context_id = self.statusbar.get_context_id(__appname__)
        self.album_count = 0
        self.update_album_count(self.album_count)
        self.no_cover_file = get_icon('no-cover.svg')
        self.main_window.set_icon_from_file(self.no_cover_file)
        self.size_small = (30, 30)
        self.size_medium = (75, 75)
        self.size_large = (200, 200)
        self.no_cover_small = pixbuf_from_file(self.no_cover_file, self.size_small)
        self.no_cover_medium = pixbuf_from_file(self.no_cover_file, self.size_medium)
        self.no_cover_large = pixbuf_from_file(self.no_cover_file, self.size_large)
        self.cover_large_image.set_from_pixbuf(self.no_cover_large)
        self.pixbuf_cache = {}

    def _load_widgets(self): #{{{2
        self.load_widgets([
            'album_view',
            'clear_button',
            'cover_large_image',
            'cover_large_label',
            'delete_button',
            'main_window',
            'save_button',
            'search_button',
            'search_entry',
            'search_menu',
            'search_popupmenu',
            'search_view',
            'statusbar',
            ])

    def _make_menus(self): #{{{2
        sources = self.config.sources
        for name in sorted(sources):
            source = sources[name]
            source_check = gtk.CheckMenuItem(name)
            source_check.connect('toggled', self.on_source_toggled, source)
            source.active = name not in self.config.excluded_sources
            source_check.set_active(source.active)
            source_check.show()
            self.search_popupmenu.append(source_check)
        self.search_menu.set_menu(self.search_popupmenu)

    def _make_views(self): #{{{2
        self.album_list = gtk.ListStore(str, str, str, str)
        self.album_view.append_column(column_pixbuf('Cover', self.COL_FILE, self.set_album_cover))
        self.album_view.append_column(column_markup('Album', self.COL_ALBUM, self.set_album_markup))
        self.album_view.set_model(self.album_list)
        self.search_list = gtk.ListStore(str, str, str, str)
        self.search_view.append_column(column_pixbuf('Cover', self.COL_URL_S, self.set_search_cover))
        self.search_view.append_column(column_markup('Description', self.COL_SUMMARY, self.set_search_markup))
        self.search_view.set_model(self.search_list)

    def on_about_menuitem_activate(self, widget): #{{{2
        AboutDialog(
                name=__appname__,
                authors=[__author__],
                website=__url__,
                license=__license__,
                logo=get_icon('no-cover.svg'),
                ).run()

    def on_add_folder_button_clicked(self, widget): #{{{2
        folder = DirectoryChooserDialog().run()
        if folder: self.add_albums(folder)

    def on_album_view_cursor_changed(self, view): #{{{2
        self.search_menu.set_sensitive(True)
        self.delete_button.set_sensitive(True)

    def on_album_view_row_activated(self, view, path, column): #{{{2
        row = view.props.model[path]
        album = row[self.COL_ALBUM]
        artist = row[self.COL_ARTIST]
        query = ' '.join([i for i in [artist, album] if i]).strip()
        self.search_entry.set_sensitive(True)
        self.search_button.set_sensitive(True)
        self.search_entry.set_text(query)
        self.search(query)

    def on_clear_button_clicked(self, widget): #{{{2
        self.search_menu.set_sensitive(False)
        self.delete_button.set_sensitive(False)
        self.save_button.set_sensitive(False)
        self.album_list.clear()
        self.album_count = 0
        self.update_album_count(self.album_count)

    def on_covers_menuitem_activate(self, widget): #{{{2
        dialog = CoversDialog(
                self.config.cover_filenames,
                self.config.cover_filename_output
                )
        if dialog.run() != gtk.RESPONSE_OK: return
        cover_filenames = dialog.get_cover_filenames()
        cover_filename_output = dialog.get_cover_filename_output()
        if cover_filenames:
            self.config.cover_filenames = cover_filenames
        if cover_filename_output:
            self.config.cover_filename_output = cover_filename_output
        self.config.write()

    def on_delete_button_clicked(self, widget): #{{{2
        model, itr = self.album_view.get_selection().get_selected()
        path = model.get_path(itr)
        row = model[path]
        cover = row[self.COL_FILE]
        album = row[self.COL_ALBUM]
        if cover and os.path.isfile(cover):
            response = ConfirmDialog("Delete album cover for '%s'?" % album).run()
            if response == gtk.RESPONSE_YES:
                row[self.COL_FILE] = None
                os.remove(cover)
                model.row_changed(path, itr)

    def on_main_window_destroy(self, widget): #{{{2
        gtk.main_quit()

    def on_patterns_menuitem_activate(self, widget): #{{{2
        dialog = PatternsDialog(
                self.config.folder_patterns,
                self.config.underscore_to_space
                )
        if dialog.run() != gtk.RESPONSE_OK: return
        self.config.folder_patterns = dialog.get_patterns()
        self.config.underscore_to_space = dialog.get_underscore_to_space()
        self.config.write()

    def on_save_button_clicked(self, widget): #{{{2
        model, itr = self.album_view.get_selection().get_selected()
        path = model.get_path(itr)
        row = model[path]
        cover = row[self.COL_FILE]
        folder = row[self.COL_DIR]
        if cover and os.path.isfile(cover): os.remove(cover)
        pb = self.cover_large_image.get_pixbuf()
        name = self.config.cover_filename_output + '.jpg'
        filename = os.path.join(folder, name)
        pb.save(filename, 'jpeg')
        row[self.COL_FILE] = filename
        model.row_changed(path, itr)

    def on_search_button_clicked(self, widget): #{{{2
        query = self.search_entry.get_text().strip()
        if query: self.search(query)

    def on_search_menu_clicked(self, widget): #{{{2
        model, itr = self.album_view.get_selection().get_selected()
        if not itr: return
        row = model[model.get_path(itr)]
        album = row[self.COL_ALBUM]
        artist = row[self.COL_ARTIST]
        query = ' '.join([i for i in (artist, album) if i]).strip()
        self.search_entry.set_text(query)
        self.search(query)

    def on_search_view_row_activated(self, view, path, column): #{{{2
        self.save_button.set_sensitive(True)
        row = view.props.model[path]
        pb = pixbuf_from_url_scale(row[self.COL_URL_L], (500, 500), scale_down)
        if not pb: del(view.props.model[path])
        self.cover_large_label.set_markup('<b>%s</b> (%sx%s)' % (cgi.escape(row[self.COL_SUMMARY]), pb.get_width(), pb.get_height()))
        self.cover_large_image.set_from_pixbuf(pb)

    def on_source_toggled(self, widget, source): #{{{2
        source.active = widget.get_active()

    def on_sources_menuitem_activate(self, widget): #{{{2
        dialog = SourcesDialog(self.config.sources.keys(), self.config.excluded_sources)
        if dialog.run() != gtk.RESPONSE_OK: return
        self.config.excluded_sources = [s[1] for s in dialog.get_sources() if not s[0]]
        self.config.write()

    def add_albums(self, directory): #{{{2
        dialog = AddFolderProgressDialog()
        dialog.run(self.add_albums_generator(directory, dialog))

    def add_albums_generator(self, directory, progressbar): #{{{2
        patterns = self.config.folder_patterns_re(directory)
        for root, dirs, files in os.walk(directory):
            if len(dirs): continue
            info = {'album': None, 'artist': None}
            for p in patterns:
                match = p.search(root)
                if not match: continue
                cover_file = self.cover_filename(root)
                info.update(match.groupdict())
                album = info['album']
                artist = info['artist']
                if self.config.underscore_to_space:
                    if album:  album  = album.replace('_', ' ')
                    if artist: artist = artist.replace('_', ' ')
                self.album_list.append([cover_file, root, album, artist])
                progressbar.set_text(album)
                progressbar.pulse()
                self.album_count += 1
                self.update_album_count(self.album_count)
                yield True
                break
        progressbar.dialog.hide()
        yield False

    def update_album_count(self, count): #{{{2
        self.statusbar.pop(self.context_id)
        message_id = self.statusbar.push(self.context_id, 'Albums: %s' % count)

    def search(self, query): #{{{2
        dialog = SearchProgressDialog()
        dialog.run(self.search_generator(normalize(decode(query)), dialog))

    def search_generator(self, query, progressbar): #{{{2
        self.search_list.clear()
        sources = self.config.sources
        for name in sorted(sources):
            source = sources[name]
            if not source.active: continue
            progressbar.label.set_text(name)
            for result in source.search(query):
                album = text_trim(result['album'])
                cover_small = result['cover_small']
                cover_large = result['cover_large']
                progressbar.set_text(album)
                self.search_list.append([cover_small, cover_large, name, album])
                progressbar.pulse()
                yield True
        progressbar.dialog.hide()
        yield False

    def cover_filename(self, folder): #{{{2
        for filename in self.config.cover_filenames:
            cover_path = os.path.join(folder, filename)
            if os.path.isfile(cover_path):
                return cover_path

    def set_album_cover(self, column, cell, model, itr): #{{{2
        filename = model.get_value(itr, self.COL_FILE)
        if filename:
            pb = self.get_pixbuf_cache(filename, pixbuf_from_file, self.size_small)
        else:
            pb = self.no_cover_small
        cell.set_property('pixbuf', pb)

    def set_album_markup(self, column, cell, model, itr): #{{{2
        artist = model.get_value(itr, self.COL_ARTIST)
        album = cgi.escape(model.get_value(itr, self.COL_ALBUM))
        markup = '<b>%s</b>' % album
        if artist: markup += '\n<i>%s</i>' % cgi.escape(artist)
        cell.set_property('markup', markup)

    def set_search_cover(self, column, cell, model, itr): #{{{2
        url = model.get_value(itr, 1)
        pb = self.get_pixbuf_cache(url, pixbuf_from_url, self.size_medium)
        cell.set_property('pixbuf', pb)

    def set_search_markup(self, column, cell, model, itr): #{{{2
        summary = cgi.escape(model.get_value(itr, self.COL_SUMMARY))
        source = cgi.escape(model.get_value(itr, self.COL_SOURCE))
        cell.set_property('markup', '<b>%s</b>\n<i>%s</i>' % (summary, source))

    def get_pixbuf_cache(self, key, func, size): #{{{2
        if key in self.pixbuf_cache:
            pb = self.pixbuf_cache[key]
        else:
            pb = func(key, size)
            self.pixbuf_cache[key] = pb
        return pb
