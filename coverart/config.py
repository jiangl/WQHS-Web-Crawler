import os
from scriptutils.config import SimpleConfig

from . import __appname__
from .utils import pattern_to_re, get_sources

class Config(SimpleConfig): #{{{1

    def __init__(self):
        SimpleConfig.__init__(self,
                filename=os.path.join(
                    os.path.expanduser('~/.%s' % __appname__.lower()),
                    'main.cfg'
                    ),
                base={
                    'folder_patterns': [
                        'Soundtracks/<album>',
                        'Various/<album>',
                        '<artist>/<album>'
                        ],
                    'cover_filenames': [
                        'cover.png',
                        'cover.jpg',
                        'cover.gif'
                        ],
                    'underscore_to_space': True,
                    'cover_filename_output': 'cover.png',
                    'excluded_sources': [],
                    })
        self._load_sources()

    def _load_sources(self):
        self.sources = {}
        directory = os.path.join(self.directory, 'sources')
        if not os.path.isdir(directory):
            os.makedirs(directory)
        source_objs = get_sources() + get_sources(directory)
        for so in source_objs:
            self.sources[so.source_name] = so

    def folder_patterns_re(self, directory):
        return [pattern_to_re(os.path.join(directory, p)) for p in self.folder_patterns]

    def _get_folder_patterns(self):
        return self.getlist('folder_patterns', [])

    def _set_folder_patterns(self, values):
        self.set('folder_patterns', values)

    folder_patterns = property(_get_folder_patterns, _set_folder_patterns)

    def _get_cover_filenames(self):
        return self.getlist('cover_filenames', [])

    def _set_cover_filenames(self, values):
        self.set('cover_filenames', values)

    cover_filenames = property(_get_cover_filenames, _set_cover_filenames)

    def _get_underscore_to_space(self):
        return self.getboolean('underscore_to_space', True)

    def _set_underscore_to_space(self, value):
        self.set('underscore_to_space', value)

    underscore_to_space = property(_get_underscore_to_space, _set_underscore_to_space)

    def _get_cover_filename_output(self):
        return self.get('cover_filename_output', 'cover.png')

    def _set_cover_filename_output(self, value):
        self.set('cover_filename_output', value)

    cover_filename_output = property(_get_cover_filename_output, _set_cover_filename_output)

    def _get_excluded_sources(self):
        return self.get('excluded_sources', [])

    def _set_excluded_sources(self, values):
        self.set('excluded_sources', values)

    excluded_sources = property(_get_excluded_sources, _set_excluded_sources)
