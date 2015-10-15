from setuptools import setup, find_packages
setup(
    name = "PageRank-er",
    version = "0.1",
    install_requires=[
        'cffi',
    ],
    setup_requires=[
        'cffi'
    ],
    cffi_modules=[
        "build_page_rank.py:ffi"
    ],
)
