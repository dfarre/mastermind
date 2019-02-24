import setuptools


tests_require = ['pytest', 'pytest-cov']

setuptools.setup(
    name='mastermind',
    version='0.1',
    packages=setuptools.find_packages(),
    install_requires=['Django', 'django-filter', 'djangorestframework', 'psycopg2',
                      'bdd-coder@git+https://bitbucket.org/coleopter/bdd-coder'],
    extras_require={'dev': ['ipdb', 'ipython'], 'test': tests_require},
    tests_require=tests_require
)
