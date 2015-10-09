# Lab 2

Team: Andrew Gilbert, Josh Terrell

**Important: Run everything from the project's root directory**

### Setup environment:
```bash
pyvenv virtual
source virtual/bin/activate
pip install --upgrade -e .
```

### Run all the tests:
Run `python3 -m unittest discover` from the directory containing this file

### Parse data and construct database:
```bash
parse_docs data/SB277Utter.json
```

### Query for utterances:
```bash
matcher
```

Includes help when you start the app. You can also use `matcher --help` for more information.

### Deactivate environment:
```bash
deactivate
```
