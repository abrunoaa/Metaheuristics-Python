#  setup.py
# 
#  Copyright (c) 2020 Bruno Almeda de Oliveira <abrunoaa@gmail.com>
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

from distutils.core import setup
from Cython.Build import cythonize
from os import path

folder = path.dirname(__file__)
setup(
    ext_modules = cythonize(path.join(folder, "two_opt.pyx"), compiler_directives = {'language_level': "3"})
)
