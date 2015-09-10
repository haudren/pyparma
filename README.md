These are Python bindings to the [Parma Polyhedra Library][1].
They were extracted from the [sagemath][2] project, in order to be used in non-sage projects.
Additionally, the functions to convert unlimited precision integers between python and
mpz commes from [gmpy2][3] library, which was already adapted from sagemath.

This is GPL-licensed, as is Sagemath.

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

[1]: http://bugseng.com/products/ppl/
[2]: http://www.sagemath.org/
[3]: https://pypi.python.org/pypi/gmpy2/2.0.7
