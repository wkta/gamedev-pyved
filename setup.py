# from distutils.core import setup

from setuptools import setup

import sys
sys.path.append('src')
from pyved.ver_info import version_num


# read the contents of the README file
from pathlib import Path
this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()


setup(
    name="pyved",

    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",

    long_description=long_desc,
    long_description_content_type='text/markdown',

    package_dir={'':'src'},
    packages=[
        "pyved",
        ],
    include_package_data=True,  # to be sure we get _sm_shelf/legacy.py, etc.

    description='experimental toolbox for game devs who use python',
    license='MIT',
    version=str(version_num),

    entry_points={
        'console_scripts': [
            'pyved = pyved.__main__:main'
        ]
    }
)
