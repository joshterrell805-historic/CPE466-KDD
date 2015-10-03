import json
def JsonReader(filename):
    with open(filename) as fh:
        list = json.load(fh)
    fh.close()
    return list
