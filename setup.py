# Strict Session Defaults © 2022
# Author:  Ameen Ahmed
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from setuptools import setup, find_packages
from strict_session_defaults import __version__ as version


with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')


setup(
    name='strict_session_defaults',
    version=version,
    description='Frappe plugin that enforces and manages the session defaults popup.',
    author='Ameen Ahmed (Level Up)',
    author_email='kid1194@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
