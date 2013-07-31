from setuptools import setup, find_packages
import sys, os


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'tables',
    'Pydap>=3.2',
    'Numpy',
]


setup(name='pydap.handlers.pytables',
    version=version,
    description="HDF5 handler for Pydap based on PyTables",
    long_description="""
This handler allows Pydap to serve data from HDF5 files using                   
`PyTables <http://pytables.github.io/>`_.
""",
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='HDF5 PyTables opendap dods dap science meteorology oceanography',
    author='Roberto De Almeida',
    author_email='roberto@dealmeida.net',
    url='https://github.com/robertodealmeida/pydap.handlers.pytables',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['pydap', 'pydap.handlers'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points="""
        [pydap.handler]
        hdf5 = pydap.handlers.pytables:HDF5Handler
    """,
)
