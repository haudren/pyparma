# -*- coding: utf-8 -*-

from setuptools import setup
#from distutils.extension import Extension
from setuptools import Extension
from Cython.Distutils import build_ext

with open('README') as f:
    long_desc = f.read()

classif = ['Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'Intended Audience :: Science/Research',
           'Topic :: Scientific/Engineering :: Mathematics',
           'License :: OSI Approved :: GNU General Public License (GPL)',
           'Programming Language :: Python :: 2.7']

setup(
    name="pyparma",
    version="0.3.2",
    description="Bindings to the parma polyhedra library,\
                 allowing to use double description from Python",
    long_description=long_desc,
    url="https://github.com/haudren/pyparma",
    author="Hervé Audren",
    author_email="h.audren@aist.go.jp",
    license="GPL",
    classifiers=classif,
    packages=["pyparma", "pyparma/utils"],
    cmdclass={'build_ext': build_ext},
    ext_modules=[
        Extension("pyparma.pylong",
            sources=["pyparma/pylong.pyx"],
            libraries=["gmp", "gmpxx"]
                  ),
        Extension("pyparma.ppl",
            sources=["pyparma/ppl.pyx",
                     "pyparma/ppl_shim.cc"],
            libraries=["ppl", "gmpxx"],
            language="c++",
            extra_compile_args=["-fPIC"]
                  )
                ]
)
