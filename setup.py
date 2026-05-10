from setuptools import setup, find_packages

setup(
    name='velix-osint',
    version='3.0.0',
    description='OSINT username finder for 480+ websites',
    author='Bachir',
    packages=find_packages(),
    include_package_data=True,
    package_data={'velix': ['data.json']},
    install_requires=[
        'colorama>=0.4.6',
        'requests>=2.31.0',
        'requests-futures>=1.0.1',
    ],
    entry_points={
        'console_scripts': [
            'velix=velix.cli:main',
        ],
    },
    python_requires='>=3.8',
)
