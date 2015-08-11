import py2exe
from distutils.core import setup

setup(options = {'py2exe': {'bundle_files': True, 'compressed': True, 'optimize':2, }},
      windows = [{'script': "Main.py"}],      
      zipfile = None,
)

