from setuptools import setup, find_packages
setup(
    name = "Project",
    version = "0.1",
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
           'cluster = scripts.cluster:main'
        ]
    }
)
