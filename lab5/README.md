Team: Andrew Gilbert, Josh Terrell

**Important: Run everything from the project's root directory**

### Setup environment:
```bash
pyvenv virtual
source virtual/bin/activate
pip install --upgrade -e .
```

### Cluster
#### Hierarchical
```bash
hierarchical data/<filename>.csv [cut_threshold]
```

#### K-Means
```bash
kmeans data/<filename>.csv <clusters>
```

### Visualize
After clustering, a file called `graph.csv` is created/overwritten which
contains clusterings per point. The R script, `graph.R` uses this list of
clusterings to produce a two dimensional visualization as shown in the report.

Note: ggplot2 must be installed.
```
R
...
> source('graph.R')
```
