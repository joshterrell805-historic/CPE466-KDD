## Lab6: Association Rules Mining
Team: Andrew Gilbert, Josh Terrell
Emails: apgilber@calpoly.edu, jmterrel@calpoly.edu


**Important: Run everything from the project's root directory**

Note: The executable has help functions. E.g `apriori --help`.

### Setup environment:
```
pyvenv virtual
source virtual/bin/activate
pip install --upgrade -e .
```

### Find association rules
Our rule mining script uses the out1 format (the sparse matrix representation).
```
apriori [options] <data.csv> <min_sup> <min_conf>
```

It supports one option: `--name-file` with the filename of a CSV dump of the goods table. A copy of such a file is included in our submission under the name `goods.csv`. When the `--name-file` option is specified, additional output will be printed after the usual output. This additional output will provide the data required in the report.