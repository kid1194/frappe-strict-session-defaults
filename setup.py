from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

from strict_session_defaults import __version__ as version

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
