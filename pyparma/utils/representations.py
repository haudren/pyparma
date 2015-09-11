from pyparma import C_Polyhedron, Constraint_System, Linear_Expression,\
                    Generator_System, point, ray

import numpy as np
from fractions import Fraction

class Polyhedron(object):
    def __init__(self, **kwargs):
        if "hrep" in kwargs:
            self.poly = from_hrep(kwargs["hrep"])
            return
        if "vrep" in kwargs:
            self.poly = from_vrep(kwargs["vrep"])
            return

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

def ex_from_line(l):
    if isinstance(l[0], Fraction):
        scaled, _ = reduce_lcm(l)
        offset, coeffs = scaled[0], scaled[1:]
    else:
        offset, coeffs = l[0], l[1:]
    return Linear_Expression(coeffs, offset)

def gen_from_line(l):
    t, coords = l[0], l[1:]
    if isinstance(coords[0], int) or isinstance(coords[0], long):
        d = 1
    elif isinstance(coords[0], Fraction):
        coords, d = reduce_lcm(coords)
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

#Storage format type | points : type = 1 for points
def from_vrep(vrep):
    gs = Generator_System()
    for l in vrep:
        gs.insert(gen_from_line(l))
    return C_Polyhedron(gs)

def add_point(point, poly):
    ex = Linear_Expression(point, 0)
    poly.add_generator(point(ex))
