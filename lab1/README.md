Team: Andrew Gilbert, Josh Terrell

To run all the tests:
Run `python3 -m unittest discover` from the directory containing this file

.:
__init__.py: (everywhere) Python package declaration
README.md: This file
text: Python package for text handling
vector: Python package for CSV and vector handling

./text:
__init__.py
pg1342.txt: Test data source: _Pride and Prejudice_ by Jane Austen (from Project Gutenberg)
test_texthandler.py: Tests for the texthandler module
test.txt: Test data for the tests
texthandler.py: The texthandler module. This contains the code and classes for working with text data

./vector:
csvhandler.py: The csvhandler module. This contains the code and class for reading CSV files into vectors
__init__.py
matrix.py: The matrix module. This contains the code to handle columnwise and rowwise computations on vectors
test.csv: Test data for test_csvhandler to use
test_csvhandler.py: Tests for the csvhandler module
test_vectorMatrix.py: Tests for the matrix module
test_vector.py: Tests for the vector module
vector.py: The vector module. This contains the code and class for handling vectors of numbers
