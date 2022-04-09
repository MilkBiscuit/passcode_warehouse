"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['launcher.py']
DATA_FILES = []
OPTIONS = {
    'includes': ["pyperclip"],
    'iconfile': "resources/passcode_folder.icns",
    'plist': "Info.plist"
}

setup(
    app=APP,
    name="PasscodeWarehouse",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
