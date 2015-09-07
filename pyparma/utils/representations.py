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
            d = g.divisor()
            if g.is_point():
                t = 1
            else:
                t = -1

            if d == 1:
                lines.append([t]+list(g.coefficients()))
            else:
                lines.append([Fraction(t)]+[Fraction(c, d)
                                            for c in g.coefficients()])
        return np.vstack(lines)

    def add_ineq(self, line):
        add_ineq(line, self.poly)

    def add_point(self, point):
        add_point(point, self.poly)

#Storage format b | A where b + Ax >= 0
def from_hrep(hrep):
    cs = Constraint_System()
    for l in hrep:
        offset = l[0]
        coeffs = l[1:]
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
        if l[0] == 1:
            ex = Linear_Expression(l[1:], 0)
            #TODO : Denominator stuff
            #gs.insert(point(ex*lcm, lcm))
            #TODO : Case when we have non-points i.e. rays/lines
            gs.insert(point(ex))
        else:
            raise ValueError("Sorry, the wrapper does not implement rays/lines")
    return C_Polyhedron(gs)

def add_point(point, poly):
    ex = Linear_Expression(point, 0)
    poly.add_generator(point(ex))
