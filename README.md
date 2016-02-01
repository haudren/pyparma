[![Build Status](https://travis-ci.org/haudren/pyparma.svg?branch=topic/travis)](https://travis-ci.org/haudren/pyparma)

(_Note: travis build is failing because libppl is still not added to the whitelist_)

These are Python bindings to the [Parma Polyhedra Library][1].
They were extracted from the [sagemath][2] project, in order to be used in non-sage projects.
This is GPL-licensed, as is Sagemath.

To build it you need to have both the *ppl* and *gmp* libraries installed in a
place where distutils can find it. Then,
```
python setup.py build && python setup.py install
```
If you have trouble, try adding the desired paths to library_dirs in setup.py
as a keyword argument to the Extension constructor.

To use it, simply import the module, create a matrix of Fractions or integers,
and compute the double description !
```python
from pyparma import Polyhedron
import numpy as np
from fractions import Fraction

fractionize = np.vectorize(lambda x: Fraction(str(x)))
A = fractionize(np.random.rand(50,3))
poly = Polyhedron(hrep=A)
print poly.hrep()
```

Both H-representation and V-representation follow the CDD format i.e.:

- H_rep = [b | A] where the polyhedron is defined by b + A x >= 0
- V_rep = [t | V] where V are the stacked vertices (Horizontal vectors) and
t is the type: 1 for points, 0 for rays/lines.

To run the tests, simply run:
```
nosetests
```
From the top-level directory. To run the tests, you need to have the [CDD library][3]
installed. I assume that you installed the version that comes with the [pycddlib][4]
bindings.

[1]: http://bugseng.com/products/ppl/
[2]: http://www.sagemath.org/
[3]: http://www.inf.ethz.ch/personal/fukudak/cdd_home/
[4]: https://pypi.python.org/pypi/pycddlib/
