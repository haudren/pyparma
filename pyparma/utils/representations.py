from pyparma import C_Polyhedron, Constraint_System, Linear_Expression,\
                    Generator_System, point

import numpy as np
from fractions import Fraction

class Polyhedron(object):
    def __init__(self, **kwargs):
        if "hrep" in kwargs:
            self.poly = from_hrep(kwargs["hrep"])
        if "vrep" in kwargs:
            self.poly = from_vrep(kwargs["vrep"])

    def hrep(self):
        cs = self.poly.minimized_constraints()
        lines = []
        for c in cs:
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
        return np.vstack(lines)

    def add_ineq(self, line):
        add_ineq(line, self.poly)

    def add_point(self, point):
        add_point(point, self.poly)

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

#Storage format b | A where b + Ax >= 0
def from_hrep(hrep):
    cs = Constraint_System()
    for l in hrep:
        if isinstance(l[0], Fraction):
            scaled, _ = reduce_lcm(l)
            offset, coeffs = scaled[0], scaled[1:]
        else:
            offset, coeffs = l[0], l[1:]
        #We should also convert from Fraction to integer
        #ex = Linear_Expression(coeffs*lcm, offset*lcm)
        ex = Linear_Expression(coeffs, offset)
        cs.insert(ex >= 0)
    return C_Polyhedron(cs)

def add_ineq(line, poly):
    ex = Linear_Expression(line[0], line[1:])
    poly.add_constraint(ex >= 0)

#Storage format type | points : type = 1 for points
def from_vrep(vrep):
    gs = Generator_System()
    for l in vrep:
        t, coords = l[0], l[1:]
        if t == 1:
            if isinstance(coords[0], int) or isinstance(coords[0], long):
                d = 1
            elif isinstance(coords[0], Fraction):
                coords, d = reduce_lcm(coords)
            ex = Linear_Expression(coords, 0)
            #TODO : Case when we have non-points i.e. rays/lines
            gs.insert(point(ex, d))
        else:
            raise ValueError("Sorry, the wrapper does not implement rays/lines")
    return C_Polyhedron(gs)

def add_point(point, poly):
    ex = Linear_Expression(point, 0)
    poly.add_generator(point(ex))
