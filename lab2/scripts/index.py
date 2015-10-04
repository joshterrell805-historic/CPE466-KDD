import click
from elements.jsonreader import JsonReader
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.porterstemmer import PorterStemmerElement
import pickle
import sys

@click.command()
@click.argument('input', type=click.File('r'))
@click.option('--output', type=click.File('wb'))
def cli(input, output):
    """Example basic script"""
    doc_itr = JsonReader(input)
    with click.progressbar(doc_itr) as prog_doc_itr:
        freq_itr = FreqCounter(prog_doc_itr, 'text')
        stop_itr = StopwordElement(freq_itr, ['a', 'an', 'the'])
        stem_itr = PorterStemmerElement(stop_itr)
        res = list(stem_itr)
        if output:
            pickle.dump(res, output)
        else:
            for doc in res:
                click.echo(str(doc) + "\n")
