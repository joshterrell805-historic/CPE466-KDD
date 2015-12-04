import click
import pandas as pd
import apriori

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('minSup', type=click.FLOAT)
@click.argument('minConf', type=click.FLOAT)
def main(datafile, minSup, minConf):
    data = pd.read_csv(datafile)
    freq_sets = apriori.find_frequent_itemsets(data, minSup)
    rules = apriori.find_association_rules(freq_sets, minConf)
