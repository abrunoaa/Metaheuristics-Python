from distutils.core import setup
from Cython.Build import cythonize
from os import path

folder = path.dirname(__file__)
setup(
    ext_modules = cythonize(path.join(folder, "two_opt.pyx"), compiler_directives = {'language_level': "3"})
)
