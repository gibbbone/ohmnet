#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
This setup has been lifted and adapted from word2vec in the gensim package. 

Run with:
python setup.py build_ext --inplace
"""

import os
import platform
import sys
import warnings
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

PY2 = sys.version_info[0] == 2

if sys.version_info[:2] < (2, 7) or ((3, 0) <= sys.version_info[:2] < (3, 5)):
    raise Exception('This version of gensim needs Python 2.7, 3.5 or later.')

# the following code is adapted from tornado's setup.py:
# https://github.com/tornadoweb/tornado/blob/master/setup.py
# to support installing without the extension on platforms where
# no compiler is available.


class custom_build_ext(build_ext):
    """Allow C extension building to fail.

    The C extension speeds up word2vec and doc2vec training, but is not essential.
    """

    warning_message = """
********************************************************************
WARNING: %s could not
be compiled. No C extensions are essential for gensim to run,
although they do result in significant speed improvements for some modules.
%s

Here are some hints for popular operating systems:

If you are seeing this message on Linux you probably need to
install GCC and/or the Python development package for your
version of Python.

Debian and Ubuntu users should issue the following command:

    $ sudo apt-get install build-essential python-dev

RedHat, CentOS, and Fedora users should issue the following command:

    $ sudo yum install gcc python-devel

If you are seeing this message on OSX please read the documentation
here:

http://api.mongodb.org/python/current/installation.html#osx
********************************************************************
"""

    def run(self):
        try:
            build_ext.run(self)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "Extension modules" +
                "There was an issue with your platform configuration - see above.")

    def build_extension(self, ext):
        name = ext.name
        try:
            build_ext.build_extension(self, ext)
        except Exception:
            e = sys.exc_info()[1]
            sys.stdout.write('%s\n' % str(e))
            warnings.warn(
                self.warning_message +
                "The %s extension module" % (name,) +
                "The output above this warning shows how the compilation failed.")

    # the following is needed to be able to add numpy's include dirs... without
    # importing numpy directly in this script, before it's actually installed!
    # http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        # https://docs.python.org/2/library/__builtin__.html#module-__builtin__
        if isinstance(__builtins__, dict):
            __builtins__["__NUMPY_SETUP__"] = False
        else:
            __builtins__.__NUMPY_SETUP__ = False

        import numpy
        self.include_dirs.append(numpy.get_include())

model_dir = os.path.join(
    os.path.dirname(__file__), 'ohmnet', 'gensimmod', 'model')
gensim_dir = os.path.join(
    os.path.dirname(__file__), 'ohmnet','gensimmod')

print(model_dir, os.path.exists(model_dir))
print(gensim_dir, os.path.exists(gensim_dir))

cmdclass = {'build_ext': custom_build_ext}

WHEELHOUSE_UPLOADER_COMMANDS = {'fetch_artifacts', 'upload_all'}
if WHEELHOUSE_UPLOADER_COMMANDS.intersection(sys.argv):
    import wheelhouse_uploader.cmd
    cmdclass.update(vars(wheelhouse_uploader.cmd))

if PY2:
    NUMPY_STR = 'numpy >= 1.11.3, <= 1.16.1'
    PYTEST_STR = 'pytest == 4.6.4'
else:
    NUMPY_STR = 'numpy >= 1.11.3'
    PYTEST_STR = 'pytest'

ext_modules = [
    Extension(
        'ohmnet.gensimmod.model.word2vec_inner',
        # sources=['.\ohmnet\gensimmod\model\word2vec_inner.c'],        
        sources=[os.path.join('.', 'ohmnet','gensimmod','model','word2vec_inner.c')],
        include_dirs=[model_dir])
]

print(model_dir, os.path.exists(model_dir))
print(gensim_dir, os.path.exists(gensim_dir))
print(find_packages())

setup(
    name='ohmnet', 
    version='1.0.0',
    description='Multi Layer Node Embedding',
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    packages=find_packages(),
    platforms='any',
    zip_safe=False,
    setup_requires=[
        NUMPY_STR,
    ],
    install_requires=[
        NUMPY_STR,
        'scipy >= 0.18.1',
        'six >= 1.5.0',
        'smart_open >= 1.7.0',
    ],
    include_package_data=True,
)
