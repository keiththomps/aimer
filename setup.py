from setuptools import setup, find_packages

setup(
    name='ghost_writer',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ghostwriter=ghost_writer.main:main',
        ],
    },
)
