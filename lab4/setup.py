from setuptools import setup, find_packages
setup(
    name = "The Decider",
    version = "0.1",
    install_requires=[
        'click',
        'tabulate'
    ],
    setup_requires=[
    ],
    cffi_modules=[
    ],
    entry_points={
        'console_scripts': [
            'induceC45 = scripts.induce_c45:main',
            'classifier = scripts.classify:main',
            'validation = scripts.validation:main'
        ]
    }
)
