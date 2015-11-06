def read(raw, restrictions=None):
    row_strs = list(raw.splitlines())[4:]
    cols = [set() for _ in range(row_strs[0].count(',') + 1)]
    rows = []

    if restrictions and len(restrictions) + 1 != len(cols):
        raise Exception('len(restrictions) != #features')

    for row in row_strs:
        row = row.split(',')
        for k,v in enumerate(row):
            cols[k].add(v)
        if restrictions:
            attrs = [c for i,c in enumerate(row[:-1]) if restrictions[i]]
        else:
            attrs = row[:-1]
        rows.append((attrs, row[-1]))

    if restrictions:
        cols = [c for i,c in enumerate(cols) if i + 1 == len(cols) \
                or restrictions[i]]

    return cols, rows
