from setuptools import setup, find_packages
setup(
    name='Steam workshop collection helper',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'steamcolprint = steamcollectionprint.colprint:parse_args',
        ],
    }
)
