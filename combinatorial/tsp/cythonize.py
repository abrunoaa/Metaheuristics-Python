#  cythonize.py
#
#  Copyright (c) 2020 Bruno Almêda de Oliveira <abrunoaa@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
from Cython.Build import cythonize
from setuptools import Extension


"""
This file creates the C++ version tsp_optimal.cpp from tsp_optimal.pyx.
"""

extensions = Extension("tsp_optimal", ["tsp_optimal.pyx"],
                       language="c++", extra_compile_args=["-std=c++11"], extra_link_args=["-std=c++11"])

cythonize(extensions, language_level=3)
