all: tsp_optimal

tsp_optimal: cythonize
	python3 setup.py build_ext --inplace

cythonize: tsp_optimal.pyx
	python3 cythonize.py

clean:
	rm -rf build
	rm -f tsp_optimal.cpp
	rm -f tsp_optimal.cpython*.so
