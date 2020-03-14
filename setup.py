import sys
import os

from setuptools import setup

# Get version and release info, which is all stored in shablona/version.py

ver_file = os.path.join('eisy', 'version.py')

with open(ver_file) as f:

    exec(f.read())


# Give setuptools a hint to complain if it's too old a version

# 24.2.0 added the python_requires option

# Should match pyproject.toml

# SETUP_REQUIRES = ['setuptools >= 24.2.0']
#
# # This enables setuptools to install wheel on-the-fly
#
# SETUP_REQUIRES += ['wheel'] if 'bdist_wheel' in sys.argv else []


setup(name='eisy',
      description='A package for classification of impedance\
                 spectroscopy data',
      description_content_type='text/markdown; \
                                charset=UTF-8; variant=GFM',
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown; \
                                     charset=UTF-8; variant=GFM',
      url='https://github.com/EISy-as-Py/eisy',
      license='MIT',
      author='Maria Polit, Abdul Moeez, David Hurt,\
            Mihyun Kim, Yao-Yu Li')

# if __name__ == '__main__':
#
#     setup(**opts)
