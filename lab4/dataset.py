def read(raw):
    row_strs = list(raw.splitlines())[4:]
    cols = [set() for _ in range(row_strs[0].count(',') + 1)]
    rows = []

    for row in row_strs:
        row = row.split(',')
        for k,v in enumerate(row):
            cols[k].add(v)
        rows.append((row[:-1], row[-1]))

    return cols, rows
