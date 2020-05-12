all: tsp_optimal

# it's possible to use python3 instead
python_interpreter = python3


# create files for the interpreter
tsp_optimal: cythonize
	$(python_interpreter) setup.py build_ext --inplace

# create ".cpp" file
cythonize: tsp_optimal.pyx
	python3 cythonize.py

# remove all created files
clean:
	rm -rf build
	rm -f tsp_optimal.cpp
	rm -f tsp_optimal.cpython*.so
	rm -f tsp_optimal.pypy*.so
