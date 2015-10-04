from setuptools import setup, find_packages
setup(
    name = "Retriever",
    version = "0.1",
    install_requires=[
        'click',
        'nltk'
    ],
    entry_points={
        'console_scripts': [
            'parse_docs=scripts.parse_docs:cli'
            'matcher=scripts.matcher:cli'
        ],
    }
)
