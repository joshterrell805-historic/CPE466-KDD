This is a parallel C implementation of the PageRank algorithm.

We have generally adhered to the C99 standard for the single-threaded main code.

# Building:
Create a directory to build in:

```
mkdir build
```

Change directory into the new directory:

```
cd build
```

Build with `cmake`:
```
cmake ..
make
```

Run the `ranker` program:
```
./src/ranker <datafile>
```
