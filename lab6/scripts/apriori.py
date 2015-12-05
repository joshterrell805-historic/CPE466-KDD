import click
import pandas as pd
import apriori
import csv

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('min_sup', type=click.FLOAT)
@click.argument('min_conf', type=click.FLOAT)
@click.option('--name-file', type=click.File('r'), default=None)
def main(datafile, min_sup, min_conf, name_file):
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
    for i, r in enumerate(rules):
        print("Rule {}:     {}  ---> {}    [sup={} conf={}]".format(i, ", ".join(str(i) for i in r[0]), r[1], r[2] * 100, r[3] * 100))
    if name_file:
        reader = csv.reader(name_file)
        lookup = {int(l[0]) : l[1] + l[2] for l in reader}
        print("Skyline frequent itemsets")
        for i, s in enumerate(freq_sets):
            print("Itemset {}:\n\tContains: {}\n\tSupport: {}".format(i, ", ".join(lookup[p] for p in s), apriori.support(s, data)))
        print("Skyline association rules")
        for i, r in enumerate(rules):
            print("Rule {}:\n\tLHS: {}\n\tRHS: {}\n\tSupport: {}\n\tConfidence: {}".format(i, ", ".join(lookup[p] for p in r[0]), lookup[r[1]], r[2] * 100, r[3] * 100))
