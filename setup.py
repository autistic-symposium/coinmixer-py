from setuptools import setup, find_packages

setup(
    name='jobcoin',
    version='0.0.1',
    packages=find_packages(include=['jobcoin', 'jobcoin.*']),
    author='Mia von Steinkirch',
    install_requires=[
        'click',
        'requests',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': ['jobcoin=jobcoin.cli:main']
    },
)
