"""
py2app setup script for Lucas Chess macOS app bundle.

This script creates a standalone macOS application bundle for Lucas Chess
with all dependencies included and optimized for minimal size.
"""

from setuptools import setup
import py2app
import os

# App configuration
APP = ['LucasR.py']
DATA_FILES = [
    ('Code', ['Code']),
    ('OS/darwin', ['OS/darwin']),
]

OPTIONS = {
    'argv_emulation': False,
    'includes': [
        'PySide2.QtCore',
        'PySide2.QtGui', 
        'PySide2.QtWidgets',
        'PySide2.QtSvg',
        'PySide2.QtMultimedia',
    ],
    'excludes': [
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'tornado',
        'zmq',
    ],
    'resources': [],
    'iconfile': None,  # Will add icon if available
    'plist': {
        'CFBundleName': 'Lucas Chess',
        'CFBundleDisplayName': 'Lucas Chess',
        'CFBundleIdentifier': 'com.lucaschess.app',
        'CFBundleVersion': '2.20c',
        'CFBundleShortVersionString': '2.20c',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'PGN Chess Game',
                'CFBundleTypeExtensions': ['pgn'],
                'CFBundleTypeRole': 'Editor',
            },
        ],
    },
    'packages': ['Code'],
    'optimize': 2,
    'compressed': True,
    'strip': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='Lucas Chess',
    version='2.20c',
    description='Open source chess application',
    author='Lucas Monge',
    url='https://lucaschess.pythonanywhere.com/',
)