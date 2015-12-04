from setuptools import setup, find_packages
setup(
    name = "Associator",
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
            'apriori = scripts.apriori:main'
        ]
    }
)
