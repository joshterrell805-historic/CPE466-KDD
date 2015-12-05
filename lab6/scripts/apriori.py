import click
import pandas as pd
import apriori
import csv

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('min_sup', type=click.FLOAT)
@click.argument('min_conf', type=click.FLOAT)
def main(datafile, min_sup, min_conf):
    # Expects the sparse vector format data
    reader = csv.reader(datafile)
    data = []
    max_val = 0
    ignore = {0}
    for row in reader:
        r = []
        for idx, val in enumerate(row):
            if idx in ignore:
                continue
            i = int(val)
            r.append(i)
            if i > max_val:
                max_val = i
        data.append(frozenset(r))
    freq_sets = apriori.find_frequent_itemsets(data, max_val + 1, min_sup)
    rules = apriori.find_association_rules(data, freq_sets, min_conf)
    for r in rules:
        print("{} -> {}".format(", ".join(str(i) for i in r[0]), r[1]))
