import sys
from pathlib import Path

from setuptools import setup


sys.path.append('src')
from pyved.ver_info import version_num

# - fetch data from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# read the contents of the README file


this_directory = Path(__file__).parent
long_desc = (this_directory / "README.md").read_text()

setup(
    name="pyved",

    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",

    long_description=long_desc,
    long_description_content_type='text/markdown',

    install_requires=required,

    package_dir={'': 'src'},
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
