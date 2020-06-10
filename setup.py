"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytest-lockable',
    version='0.1.0',
    description='Release tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jupe/pytest-lockable',
    author='Jussi Vatjus-Anttila',
    author_email='jussiva@gmail.com',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['tests']),  # Required

    # Specify which Python versions you support.
    python_requires='>=3.6, <4',
    install_requires=[
        'pytest',
        'func_timeout',
        'filelock',
        'pydash'
    ],
    extras_require={  # Optional
        'dev': ['nose', 'pylint', 'coverage']
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jouzen/pyring/reltool',
        'Source': 'https://github.com/jouzem/reltool/',
    }
)