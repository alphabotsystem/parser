import io
from setuptools import find_packages, setup, Command
from distutils.core import Extension

from Cython.Build import cythonize

REQUIRED = [
    "google-cloud-error-reporting", "pytz", "ccxt", "pycoingecko", "pyzmq", "orjson", "lark-parser",
]
EXTRAS = {}


packages = [
	Extension("parser", ["parser.pyx"], libraries=["m"], extra_compile_args = ["-O3", "-ffast-math", "-march=native", "-fopenmp" ], extra_link_args=['-fopenmp']),
]
setup(
    name="Parser Server",
    packages=[],
	ext_modules=cythonize(packages, language_level="3str", annotate=False),
	include_dirs=[],
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='no license',
	zip_safe=False
)