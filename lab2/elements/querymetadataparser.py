class QueryMetadataParser:
    def __init__(self, parent, key='query'):
        self.__parent = iter(parent)
        self.__key = key

    def __iter__(self):
        return self

    def __next__(self):
        document = next(self.__parent)
        q = document[self.__key]
        self.metaData = {}
        if len(q) > 0 and q[0] == '<':
            idx = q.find('>', 1)
            if idx == -1:
                raise Exception('no closing ">" found in meta-data filter')
            metaData = q[1:idx]
            document[self.__key] = q[idx+1:]
            for opt in metaData.split(','):
                tokens = opt.split(':')
                key = tokens[0]
                val = tokens[1]
                if key not in self.metaData.keys():
                    self.metaData[key] = []
                self.metaData[key].append(val)
        return document
