# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name="pyparma",
    version="0.1.0",
    description="Bindings to the parma polyhedra library, allowing to use double description from Python",
    url="https://github.com/haudren/pyparma",
    author="Hervé Audren",
    license="GPL",
    packages=["pyparma", "pyparma/utils"],
    cmdclass={'build_ext': build_ext},
    ext_modules=[
       Extension("pyparma.ppl",
            sources=["pyparma/ppl.pyx", "pyparma/ppl_shim.cc", "pyparma/mpz_pylong/mpz_pylong.c"],
                  libraries=["ppl", "gmpxx"],
                  language="c++",
                  extra_compile_args=["-fPIC"]
                  )
                ]
)
