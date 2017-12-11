from __future__ import print_function

import pyparma
from pyparma.utils.representations import gen_from_line, ex_from_line,\
                                          fractionize
import cdd
import numpy as np
import sys
from fractions import Fraction

from nose.tools import raises

def equal_sorted(A, B):
    return np.array_equal(np.sort(A, axis=0),
                          np.sort(B, axis=0))

def test_from_points():
    A = np.array([[1, 0, 0],
                  [1, 1, 0],
                  [1, 0, 1]])

    mat = cdd.Matrix(A.tolist(), number_type='fraction')
    mat.rep_type = cdd.RepType.GENERATOR
    cdd_poly = cdd.Polyhedron(mat)

    ineq = np.array(cdd_poly.get_inequalities())

    ppl_poly = pyparma.Polyhedron(hrep=ineq)

    assert(equal_sorted(A, ppl_poly.vrep()))

def test_from_ineq():
    A = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, -1, 0]])

    mat = cdd.Matrix(A.tolist(), number_type='fraction')
    mat.rep_type = cdd.RepType.INEQUALITY
    mat.canonicalize()
    cdd_poly = cdd.Polyhedron(mat)

    gen = np.array(cdd_poly.get_generators())

    ppl_poly = pyparma.Polyhedron(vrep=gen)

    assert(equal_sorted(A, ppl_poly.hrep()))

def test_bignum():
    bignum = 2**128
    ex = pyparma.Linear_Expression([1, bignum], 0)
    assert(ex.coefficient(pyparma.Variable(1)) == bignum)

@raises(ValueError)
def check_gen_mix_types(l):
    gen_from_line(l)

@raises(ValueError)
def check_ex_mix_types(l):
    ex_from_line(l)

def test_mix_types():
    bignum = 2**128
    bigden = 2**64 - 1
    frac = Fraction(bignum, bigden)

    if sys.version_info >= (3,):
        lines = np.array([[1, 1, frac]])
    else:
        one_l = long(1)
        lines = np.array([[1, 1, frac],
                          [1, 1, one_l],
                          [1, one_l, frac]])

    for l in lines:
        yield check_gen_mix_types, l
        yield check_ex_mix_types, l

def test_gen_bignum():
    bignum = 2**128
    bigden = 2**64 - 1
    line = np.array([1, Fraction(bignum, bigden), Fraction(0)])
    p = gen_from_line(line)
    result = (bignum, 0)

    assert(p.coefficients() == result)
    assert(p.divisor() == bigden)

def test_add_ineq():
    hrep = np.array([[0, 1, 0],
                     [0, 0, 1]])
    line = np.array([[1, -1, -1]])

    poly = pyparma.Polyhedron(hrep=hrep)

    poly.add_ineq(line)

    assert(equal_sorted(poly.hrep(), np.vstack([hrep, line])))

def test_add_gen():
    vrep = np.array([[1, 0, 0],
                     [1, 1, 0],
                     [1, 0, 1]])

    point = np.array([[1, 1, 1]])
    point_2 = np.array([[1, Fraction('1/2'), Fraction('1/2')]])

    poly = pyparma.Polyhedron(vrep=vrep)
    poly.add_generator(point)
    assert(equal_sorted(poly.vrep(), np.vstack([vrep, point])))

    #Check that point_2 has no effect
    poly.add_generator(point_2)
    assert(equal_sorted(poly.vrep(), np.vstack([vrep, point])))

def test_vs_cdd():
    vrep = [[1.00000000e+00, 6.49999999e-01, 4.91264259e-19, 5.67434186e-07],
            [1.00000000e+00, -6.49999999e-01, -1.10024414e-19, 5.67434187e-07],
            [1.00000000e+00, 2.68036827e-19, 6.49999999e-01, 5.67434186e-07],
            [1.00000000e+00, -2.36423280e-18, -6.49999999e-01, 5.67434187e-07],
            [1.00000000e+00, -3.38321375e-15, 4.02250642e-14, 6.50000000e-01],
            [1.00000000e+00, 1.50481564e-14, 1.78805309e-15, -6.50000000e-01]]

    mat = cdd.Matrix(np.array(vrep), number_type='fraction')
    mat.rep_type = cdd.RepType.GENERATOR
    mat.canonicalize()

    hrep_cdd = np.array(cdd.Polyhedron(mat).get_inequalities())
    f = np.vectorize(lambda x: Fraction(x))
    poly = pyparma.Polyhedron(vrep=f(np.array(vrep)))
    hrep_parma = poly.hrep()

    assert(equal_sorted(np.array(mat), poly.vrep()))
    print(hrep_cdd)
    print(hrep_parma)
    assert(equal_sorted(hrep_cdd, hrep_parma))
