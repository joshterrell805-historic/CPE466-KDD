## Lab4: C.45 Decision Trees
Team: Andrew Gilbert, Josh Terrell
Emails: apgilber@calpoly.edu, jmterrel@calpoly.edu


**Important: Run everything from the project's root directory**

Note: All build executables (induceC45, classier, and validation) have help
functions. E.g `induceC45 --help`.

### Setup environment:
```
pyvenv virtual
source virtual/bin/activate
pip install --upgrade -e .
```

### Run all the tests:
Run `python3 -m unittest discover` from the directory containing this file

### Build decision tree
```
induceC45 <domain.xml> <training_set.csv> [restrictions.txt]
```
Note: domain.xml is not used

### Classify dataset
For labeled dataset:
```
classifier <to_classify.csv> <decision_tree.xml> [restrictions.txt]
```

For unlabled dataset
```
classifier <to_classify.csv> <decision_tree.xml> [restrictions.txt]
--no_has_label_column
```

### Run Cross Validation
```
validation domain.xml <training_set.csv> <mainfold_value> [restrictions.txt]
```
Note: domain.xml is not used
