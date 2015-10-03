import json
def JsonReader(fh):
    list = json.load(fh)
    return list
