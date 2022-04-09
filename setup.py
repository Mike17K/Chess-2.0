from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("filename.pyx")
)


#terminal command to build is "python3 setup.py build_ext --inplace"

#also on main program posible need "#import pyximport; pyximport.install()"



#using numba
#pip install numba

#from numba import njit
#
#c_std = njit(testfunct(np.arry))
#c_std(np.array)
#
#%timeit c_std(np.array)
#
#
#
#
#