# Lab 3

Team: Andrew Gilbert, Josh Terrell

**Important: Run everything from the project's root directory**

### Setup environment:
```
pyvenv virtual
source virtual/bin/activate
pip install --upgrade -e .
```

### Run all the tests:
`python3 -m unittest discover`

### Compute Page Rank
The ranker scripts assume the graph is directed.

Correctly parsed formats include:

SNAP (edges must be repeated if undirected) (weight is optional):
```
a b [weight]
```
CSVs, (edges must be repeated if undirected) (w\_a and w\_b are ignored unless
`--weighted` flag is specified):
```
a,w_a,b,w_b
```

To run:
```
ranker <filename.csv>            # unweighted
ranker <filename.csv> --weighted # weighted
ranker <filename.txt> --fmt=snap # option specifiying input file is snap format
```

You can use `ranker --help` for more options such as setting the pagerank `d`
parameter or tweaking parallel computation settings.

### Deactivate environment:
```bash
deactivate
```

#### (Optional) Manual Rebuild of Page Rank C-Implementation
```bash
python build_page_rank.py
```
