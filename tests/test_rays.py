import pyparma
from pyparma.utils.representations import gen_from_line, ex_from_line
import cdd
import numpy as np
from fractions import Fraction

from nose.tools import raises

def equal_sorted(A, B):
    return np.array_equal(np.sort(A, axis=0),
                          np.sort(B, axis=0))

def test_from_points():
    A = np.array([[1, 0, 0],
                  [1, 1, 0],
                  [1, 0, 1]])

    mat = cdd.Matrix(A, number_type='fraction')
    mat.rep_type = cdd.RepType.GENERATOR
    cdd_poly = cdd.Polyhedron(mat)

    ineq = np.array(cdd_poly.get_inequalities())

    ppl_poly = pyparma.Polyhedron(hrep=ineq)

    assert(equal_sorted(A, ppl_poly.vrep()))

def test_from_ineq():
    A = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, -1, 0]])

    mat = cdd.Matrix(A, number_type='fraction')
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
    lines = [[1, 1, frac],
             [1, 1, 1L],
             [1, 1L, frac]]

    for l in lines:
        yield check_gen_mix_types, l
        yield check_ex_mix_types, l

def test_gen_bignum():
    bignum = 2**128
    bigden = 2**64 - 1

    p = gen_from_line([1, Fraction(bignum, bigden), Fraction(0)])
    result = (bignum, 0L)

    assert(p.coefficients() == result)
    assert(p.divisor() == bigden)
