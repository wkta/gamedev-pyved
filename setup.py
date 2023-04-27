from distutils.core import setup
import sys
sys.path.append('src')
from pyved.ver_info import version_num


setup(
    name="pyved",
    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",
    package_dir={'':'src'},
    packages=[
        "pyved",
        ],
    include_package_data=True,  # to be sure we get _sm_shelf/legacy.py, etc.

    description='experimental toolbox for game devs who use python',
    license='MIT',
    version=str(version_num),
)
