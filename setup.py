"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup, find_packages

APP = ['PasscodeWarehouse/passcode_warehouse.py']
DATA_FILES = []
OPTIONS = {
    'includes': [
        "cffi",
        "pyperclip",
        "rncryptor",
    ],
    'iconfile': "resources/passcode_folder.icns",
    'plist': "Info.plist"
}

setup(
    app=APP,
    name="PasscodeBin",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    packages=find_packages(),
    setup_requires=['py2app'],
)
