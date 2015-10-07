import click
from elements.jsonreader import JsonReader
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.lowercaser import LowerCaser
from elements.summary import SummaryElement
from elements.porterstemmer import PorterStemmerElement
import pickle
import sys

@click.command()
@click.argument('input', type=click.File('r'))
@click.option('--docspath', type=click.File('wb'),
        default='data/parsed-docs.pkl')
@click.option('--metapath', type=click.File('wb'),
        default='data/doc-meta.pkl')
def cli(input, docspath, metapath):
    """Parse documents for word vectors and save."""
    doc_itr = JsonReader(input)
    with click.progressbar(doc_itr) as prog_doc_itr:
        freq_itr = FreqCounter(prog_doc_itr, 'text')
        lowr_itr = LowerCaser(freq_itr)
        stop_itr = StopwordElement(lowr_itr, ['a', 'an', 'the'])
        stem_itr = PorterStemmerElement(stop_itr)
        sumr_itr = SummaryElement(stem_itr)
        docs = list(sumr_itr)
        meta = {
            'docFreq': sumr_itr.DF(),
            'docCount': sumr_itr.N,
            'avgLength': sumr_itr.averageLength()
        }
        pickle.dump(docs, docspath)
        pickle.dump(meta, metapath)
