def read(raw, restrictions=None):
    row_strs = list(raw.strip().splitlines())
    cols = row_strs[0].split(',')

    if restrictions == None:
        restrictions = [True] * (len(cols) - 1)
    elif len(restrictions) + 1 != len(cols):
        raise Exception('len(restrictions) != #features')

    pluralities = [int(x) for x in row_strs[1].split(',')]
    for i,p in enumerate(pluralities):
        if p == -1:
            restrictions[i] = False

    rows = []
    for row in row_strs[3:]:
        row = row.split(',')
        attrs = [c for i,c in enumerate(row[:-1]) if restrictions[i]]
        rows.append((attrs, row[-1]))

    cols = [c for i,c in enumerate(cols[:-1]) if i + 1 == len(cols) \
            or restrictions[i]]

    return cols, rows

def restrictions_from_text(text):
    if text == None:
        return None
    else:
        return [False if x == '0' else True \
                for x in restrictionstxt.read().split(',')]
