import os
#For finding the lib, we have to extend LD_LIBRARY_PATH
path = os.path.dirname(os.path.realpath(__file__))
print "Adding {} to the .so search path".format(path)
os.environ['LD_LIBRARY_PATH'] = os.environ.get('LD_LIBRAY_PATH', '')+":"+path

from ppl import *
#Note: this import will override the standard Polyhedron
#that is not instantiable anyway
from utils import Polyhedron
