import pyparma
import cdd
import numpy as np

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

    print np.array(cdd_poly.get_inequalities())
    print ppl_poly.hrep()

    assert(equal_sorted(A, ppl_poly.hrep()))
