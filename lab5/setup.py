from setuptools import setup, find_packages
setup(
    name = "Grapevine",
    version = "0.1",
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
    ],
    setup_requires=[
    ],
    cffi_modules=[
    ],
    entry_points={
        'console_scripts': [
            'kmeans = kmeans:main',
            'hierarchical= hierarchical:main'
        ]
    }
)
