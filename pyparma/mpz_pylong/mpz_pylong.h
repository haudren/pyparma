#include <gmp.h>

#ifdef __cplusplus
extern "C" {
#endif
  //static size_t mpn_sizebits(mp_ptr up, size_t un);
  //static size_t pylong_sizebits(digit *digits, size_t size);
  //size_t mpn_pylong_size(mp_ptr up, size_t un);
  //void mpn_get_pylong(digit *digits, size_t size, mp_ptr up, size_t un);
  //size_t mpn_size_from_pylong(digit *digits, size_t size);
  //void mpn_set_pylong(mp_ptr up, size_t un, digit *digits, size_t size);
  //long mpn_pythonhash(mp_ptr up, mp_size_t un);
  //long mpz_pythonhash(mpz_srcptr z);
  PyObject* mpz_get_PyLong(mpz_srcptr z);
  void mpz_set_PyIntOrLong(mpz_ptr z, PyObject* lsrc);
#ifdef __cplusplus
}
#endif
