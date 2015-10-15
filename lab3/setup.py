from setuptools import setup, find_packages
setup(
    name = "PageRank-er",
    version = "0.1",
    install_requires=[
        'cffi',
        'click'
    ],
    setup_requires=[
        'cffi'
    ],
    cffi_modules=[
        "build_page_rank.py:ffi"
    ],
    entry_points={
        'console_scripts': [
            'ranker = scripts.ranker:rank'
        ]
    }
)
