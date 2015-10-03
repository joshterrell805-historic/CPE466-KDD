import click
from elements.jsonreader import JsonReader
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.porterstemmer import PorterStemmerElement

@click.command()
@click.argument('input', type=click.File('r'))
def cli(input):
    """Example basic script"""
    doc_itr = JsonReader(input)
    with click.progressbar(doc_itr) as prog_doc_itr:
        freq_itr = FreqCounter(doc_itr, 'text')
        stop_itr = StopwordElement(freq_itr, ['a', 'an', 'the'])
        stem_itr = PorterStemmerElement(stop_itr)
        res = list(stem_itr)
    click.secho(str(res[0]), fg='green')
