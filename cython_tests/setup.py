from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension("Network", ["Network.pyx"], include_dirs=[numpy.get_include()]),
    Extension("alg1", ["alg1.pyx"], include_dirs=[numpy.get_include()])
]

setup(
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
