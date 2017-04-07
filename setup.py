from setuptools import setup

setup(name='taxaspec',
      version='0.1',
      description='Acquire & filter mass spectral libraries based on sample '
                  'taxonomy',
      url='http://github.com/JamesJeffryes/taxaspec',
      author='James Jeffryes',
      author_email='jamesgjeffryes@gmail.com',
      license='MIT',
      extras_require={'update':  ["pymongo"]},
      )
