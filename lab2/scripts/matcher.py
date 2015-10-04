import click
from elements.queryparser import QueryParser
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.lowercaser import LowerCaser
from elements.porterstemmer import PorterStemmerElement
import pickle
from collections import deque
from matching.cosinesimilarity import CosineSimilarity
import heapq

@click.command()
@click.argument('query')
@click.option('--docspath', type=click.File('rb'),
              default='data/parsed-docs.pkl')
@click.option('--metapath', type=click.File('rb'),
              default='data/doc-meta.pkl')
def cli(query, docspath, metapath):
    query_itr = QueryParser(query, 'query')
    freq_itr = FreqCounter(query_itr, 'query')
    lowr_itr = LowerCaser(freq_itr)
    stop_itr = StopwordElement(lowr_itr, ['a', 'an', 'the'])
    stem_itr = PorterStemmerElement(stop_itr)
    parsed_query = list(stem_itr)[0]

    indexList = pickle.load(docspath)
    metadata = pickle.load(metapath)

    matcher = CosineSimilarity(metadata)

    for document in indexList:
        document['match'] = matcher.match(parsed_query['words'], document['words'])

    winners = heapq.nlargest(10, indexList, key=lambda doc: doc['match'])

    for doc in winners:
        click.echo(str(doc['text']) + "\n")
