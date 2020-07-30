from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='COGCCpy',
      version='0.0.1',
      description='A python package to easily access COGCC data.',
      url="https://github.com/Rocks-n-Code/COGCCpy"
      packages=['COGCCpy'],
      author='Matthew W. Bauer, P.G.',
      author_email='matthew.w.bauer.pg@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False,
      install_requires=['requests>=2.23.0',
                        'pandas>=1.0.3'],
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   "Operating System :: OS Independent",
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering'],
      python_requires='>=3.6')