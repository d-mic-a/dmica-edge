"""
Observant Swarm package builder
"""
import os
import re

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


# Duplicate code to find version:

def package_information():
    """ get a tuple (name, version) from the changelog """
    if package_information.name is None:

        with open(os.path.join(
                os.path.dirname(__file__), "observant_swarm", "changelog.txt")
            ) as changelog:

            matches = re.compile(r"([^ ]+) \(([^\)]+)\) .*").match(changelog.readline()) # pylint: disable=invalid-name
            package_information.name = str(matches[1].replace("-", "_"))
            package_information.version = str(matches[2])

    return (package_information.name, package_information.version)

package_information.name = None
package_information.version = None



# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=package_information()[0],
    version=package_information()[1],
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Oservant Swarm Library Management',
    long_description=README,
    author='Florian Delizy',
    author_email='fdelizy.ee11@nycu.edu.tw',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Fog Computing Group',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: Network',
    ],
    install_requires=[
        'gobject',
        'psutil',
        'PyGObject',
    ]
)
