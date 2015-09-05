from setuptools import setup

def readme():
  with open('README.rst') as f:
    return f.read()

setup(
  name='pineapple',
  version='0.3',
  description='Utility functions for the Pineapple IPython/Jupyter front-end',
  long_description=readme(),
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: ISC License (ISCL)',
    'Programming Language :: Python :: 2.7',
    'Framework :: IPython',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
  url='https://github.com/nwhitehead/pineapple-module/',
  author='Nathan Whitehead',
  author_email='nwhitehe@gmail.com',
  license='ISC',
  keywords=['Pineapple', 'IPython', 'Jupyter', 'reproducible', 'versions', 'package', 'modules'],
  packages=['pineapple'],
  install_requires=[
    'pip',
  ],
  zip_safe=False
)
