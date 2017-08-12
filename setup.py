import os
import platform
from cx_Freeze import setup, Executable

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

base = None
if platform.system() == 'Windows':
    base = 'Win32GUI'
    
setup(
    name = 'Sc2Builder',
    version = 1.0,
    description = 'Starcraft II build-order calculator',
    long_description = read('README.md'),
    author = 'Min Byeonguk',
    author_email = 'phraust1612@gmail.com',
    url = 'https://github.com/phraust1612/sc2builder',
    executables = [Executable("Sc2Builder.py",
                              base=base,
                              icon='sc2icon.ico')])
