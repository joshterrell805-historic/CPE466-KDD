import click
from elements.queryparser import QueryParser
from elements.substitutable import SubstitutableElement
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.lowercaser import LowerCaser
from elements.porterstemmer import PorterStemmerElement
import pickle
from collections import deque
from matching.cosinesimilarity import CosineSimilarity
import heapq

@click.command()
@click.option('--docspath', type=click.File('rb'),
              default='data/parsed-docs.pkl')
@click.option('--metapath', type=click.File('rb'),
              default='data/doc-meta.pkl')
def cli(docspath, metapath):
    print('Specify no query to exit.')

    subs_itr = SubstitutableElement()
    freq_itr = FreqCounter(subs_itr, 'query')
    lowr_itr = LowerCaser(freq_itr)
    stop_itr = StopwordElement(lowr_itr, ['a', 'an', 'the'])
    stem_itr = PorterStemmerElement(stop_itr)

    indexList = pickle.load(docspath)
    metadata = pickle.load(metapath)
    matcher = CosineSimilarity(metadata)

    while True:
        query = input('\nEnter a query >> ')
        if query == '':
            break
        query_itr = QueryParser(query, 'query')
        subs_itr.setParent(query_itr)
        parsed_query = list(stem_itr)[0]

        for document in indexList:
            document['match'] = matcher.match(parsed_query['words'],
                    document['words'])

        winners = heapq.nlargest(10, indexList, key=lambda doc: doc['match'])

        for doc in winners:
            click.echo('\n' + str(doc['text']))

        click.echo('\n' + '-' * 80)
