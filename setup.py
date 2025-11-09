import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='QT-PyQt-PySide-Custom-Widgets',
    packages=[
        'Custom_Widgets',
        'Custom_Widgets.iconify',
        'Custom_Widgets.Qss',
    ],
    include_package_data=True,
    version='2.0.1',
    license="GNU General Public License v3.0",
    description='A comprehensive library of custom Qt widgets, animations, and UI components for PySide and PyQt desktop applications.',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Khamisi Kibet',
    author_email='kibetkhamisi@gmail.com',
    url='https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets',
    download_url='https://github.com/SpinnCompany/QT-PyQt-PySide-Custom-Widgets/archive/refs/heads/main.zip',
    keywords=[
        'PySide', 'PyQt', 'Qt', 'Custom Widgets', 'Animations', 'Desktop GUI', 'QML',
        'Designer', 'Qt Creator', 'Python GUI', 'C++', 'Modern UI', 'Component Library'
    ],
    install_requires=[
        "qtpy",
        "cairosvg",
        "qtsass",
        "matplotlib",
        "mock",
        "termcolor",
        "watchdog",
        "lxml",
        "setuptools",
        "kids-cache",
        "perlin_noise"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        'console_scripts': [
            'Custom_Widgets=Custom_Widgets.CMD:run_command',
        ],
    },
)
