from setuptools import setup, find_packages
from codecs import open
from os.path import abspath, dirname, join

from smap_nepse import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(name='smap_nepse',
      version = __version__,
      description='Stock Market Analysis and Prediction of NEPSE.',
      long_description=long_description,
      url='https://github.com/samshara/Stock-Market-Analysis-and-Prediction/',
      author='Sameer Shakten Rai, Sankalpa Timilsina, Semanta Bhandari, Sumit Shrestha',
      author_email='sameerai2736@gmail.com, sankalpatimilsina12@gmail.com, semantabhandari@gmail.com, shresthasumit55@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests*']),
      zip_safe=False,
      entry_points = {
      'console_scripts': [
          'smap_nepse=smap_nepse.cli:main',
      ],
      }
)
