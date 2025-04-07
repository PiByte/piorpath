from setuptools import setup, find_packages

setup(
    name="piorpath",
    version="1.0.0",
    packages=find_packages(include=['main*']),
    package_data={
        'main': ['../images/*.jpg'],  # Include images
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'piorpath=main.piorpath:main',
        ],
    },
)