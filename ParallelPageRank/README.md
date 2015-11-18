README
======

Dataset Format
--------------

The ranker scripts assume the graph is directed in the following form.

    # a comment
    # a comment
    # Nodes: <node count> Edges: <edge count>
    # a comment
    node_from<tab>node_to
    node_from<tab>node_to
    node_from<tab>node_to

All datasets not in the above format must be converted to this format
using the conversion script `reformat.py`.

To convert a dataset, run

    python3 reformat.py source_file.csv > output_filename.txt

This will create a file compatible with the C code, along with a Python
pickle named `source_file.csv.pickle` which contains mappings from the
node numbers in the new file to the node names in the old file, along
with the file load time in the Python code.

Next, run the ranker script as described below, then convert the results
back to the named-node format with

    python3 unformat.py source_file.csv.pickle \
      < output.out > results.txt

Compile
-------

To build for CPU:

    cd src
    make

To build for MIC offload:

    cd src
    make offload

To build for GPU:

    cd src/cuda
    make

Compute Page Rank
-----------------

    cd src
    ./pageRank <path/to/snap-formatted-dataset.csv>

For GPU:

    cd src/cuda
    ./pageRank <path/to/snap-formatted-dataset.csv>

To compute the page rank on lab3 so it will match that from the MIC
offload:

    ranker --dval 0.95  --epsilon 0.0000001 --fmt <format> \
      --no-scale <path/to/data.txt>

You will need to use the correct format for the data you’re working
with.

See the lab 3 documentation for more on how to run lab 3.

