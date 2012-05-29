import os.path, re, sys
from glob import glob
from pkg_resources import Requirement, resource_filename

from . import __appname__

def get_resource(name): #{{{1
    return resource_filename(
            Requirement.parse(__appname__),
            '%s/%s' % (__appname__.lower(), name)
            )

def get_sources(source_dir=None): #{{{1
    if not source_dir: source_dir = get_resource('sources')
    sys.path.append(source_dir)
    source_files = glob(os.path.join(source_dir, '*.py'))
    source_mods = [os.path.basename(os.path.splitext(f)[0]) for f in source_files]
    return [__import__(m).CoverSource() for m in source_mods]

def get_icon(name): #{{{1
    return get_resource('%s/%s' % ('icons', name))

def get_ui(name): #{{{1
    return get_resource('%s/%s.ui' % ('ui', name))

def pattern_to_re(pattern): #{{{1
    return re.compile(re.sub(r'(<.*?>)', r'(?P\1.*)', pattern))
