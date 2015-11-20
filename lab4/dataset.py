def read(raw, has_label=True, restrictions=None):
    row_strs = list(raw.strip().splitlines())
    cols = row_strs[0].split(',')

    if restrictions == None:
        if has_label:
            restrictions = [True] * (len(cols) - 1)
        else:
            restrictions = [True] * len(cols)
    else:
        if has_label:
            if len(restrictions) + 1 != len(cols):
                raise Exception('len(restrictions) != #features')
        else:
            if len(restrictions) != len(cols):
                raise Exception('len(restrictions) != #features')

    pluralities = [int(x) for x in row_strs[1].split(',')]
    for i,p in enumerate(pluralities):
        if p == -1:
            restrictions[i] = False

    rows = []
    for row in row_strs[3:]:
        row = row.split(',')
        if has_label:
            attrs = [c for i,c in enumerate(row[:-1]) if restrictions[i]]
            rows.append((attrs, row[-1]))
        else:
            attrs = [c for i,c in enumerate(row) if restrictions[i]]
            rows.append((attrs, None))

    if has_label:
        cols = [c for i,c in enumerate(cols[:-1]) if restrictions[i]]
    else:
        cols = [c for i,c in enumerate(cols) if restrictions[i]]

    return cols, rows

def restrictions_from_text(text):
    if text == None:
        return None
    else:
        return [False if x == '0' else True \
                for x in restrictionstxt.read().split(',')]
