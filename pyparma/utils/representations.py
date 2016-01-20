from pyparma import C_Polyhedron, Constraint_System, Linear_Expression,\
                    Generator_System, point, ray

import numpy as np
from fractions import Fraction

_is_fraction = np.vectorize(lambda x: isinstance(x, Fraction))
_is_int = np.vectorize(lambda x: isinstance(x, int))
_is_long = np.vectorize(lambda x: isinstance(x, long))

fractionize = np.vectorize(lambda x: Fraction(str(x)))
floatize = np.vectorize(lambda x: float(x))
intize = np.vectorize(lambda x: int(x))
longize = np.vectorize(lambda x: long(x))

class Polyhedron(object):
    def __init__(self, **kwargs):
        if "hrep" in kwargs:
            self.poly = from_hrep(kwargs["hrep"])
            return
        if "vrep" in kwargs:
            self.poly = from_vrep(kwargs["vrep"])
            return
        if "poly" in kwargs:
            assert(isinstance(kwargs["poly"], C_Polyhedron))
            self.poly = kwargs["poly"]
        else:
            raise ValueError("Please provide a H-rep, V-rep or\
                              C_Polyhedron")

    def hrep(self):
        cs = self.poly.minimized_constraints()
        lines = []
        for c in cs:
            if c.inhomogeneous_term() != 0:
                lines.append([Fraction(1)] +
                             [Fraction(coeff, c.inhomogeneous_term())
                              for coeff in c.coefficients()])
            else:
                lines.append([c.inhomogeneous_term()]+list(c.coefficients()))
        return np.vstack(lines)

    def vrep(self):
        gs = self.poly.minimized_generators()
        lines = []
        for g in gs:
            #Divisor is only defined for points
            d = 1
            if g.is_point():
                t = 1
                d = g.divisor()
            else:
                t = 0

            if d == 1:
                lines.append([t]+list(g.coefficients()))
            else:
                lines.append([t]+[Fraction(c, d)
                                  for c in g.coefficients()])
        if lines:
            return np.vstack(lines)
        else:
            return np.array([])

    def add_ineq(self, line):
        add_ineq(line, self.poly)

    def add_generator(self, point):
        add_generator(point, self.poly)

    def copy(self):
        return Polyhedron(poly=C_Polyhedron(self.poly))

def is_int_long(array):
    return _is_int(array).all() or _is_long(array).all()

def is_fraction(array):
    return _is_fraction(array).all()

def lcm(iterable):
    return reduce(_lcm, iterable)

def _lcm(a, b):
    return a*b // _gcd(a, b)

def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_lcm(iterable):
    denoms = [c.denominator for c in iterable]
    nums = [c.numerator for c in iterable]
    d = lcm(denoms)
    coords = [d*n//de for n, de in zip(nums, denoms)]
    return coords, d

def ex_from_line(l):
    line = l.squeeze()
    if is_int_long(l):
        offset, coeffs = line[0], line[1:]
    elif is_fraction(l):
        scaled, _ = reduce_lcm(line)
        offset, coeffs = scaled[0], scaled[1:]
    else:
        raise ValueError("All values on a line should have the same type")
    return Linear_Expression(coeffs, offset)

def gen_from_line(l):
    line = l.squeeze()
    t, coords = line[0], line[1:]
    if is_int_long(coords):
        d = 1
    elif is_fraction(coords):
        coords, d = reduce_lcm(coords)
    else:
        raise ValueError("All values on a line should have the same type")
    ex = Linear_Expression(coords, 0)

    if t == 1:
        return point(ex, d)
    elif t == 0:
        return ray(ex)

#Storage format b | A where b + Ax >= 0
def from_hrep(hrep):
    cs = Constraint_System()
    for l in hrep:
        ex = ex_from_line(l)
        cs.insert(ex >= 0)
    return C_Polyhedron(cs)

def add_ineq(line, poly):
    ex = ex_from_line(line)
    poly.add_constraint(ex >= 0)

#Storage format type | points
#type = 1 for points
#type = 0 for rays
def from_vrep(vrep):
    gs = Generator_System()
    for l in vrep:
        gs.insert(gen_from_line(l))
    return C_Polyhedron(gs)

def add_generator(point, poly):
    p = gen_from_line(point)
    poly.add_generator(p)
