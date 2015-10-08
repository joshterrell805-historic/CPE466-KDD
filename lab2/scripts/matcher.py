import click
from elements.queryparser import QueryParser
from elements.substitutable import SubstitutableElement
from elements.querymetadataparser import QueryMetadataParser
from elements.freqcounter import FreqCounter
from elements.stopword import StopwordElement
from elements.lowercaser import LowerCaser
from elements.porterstemmer import PorterStemmerElement
import pickle
from collections import deque
from matching.cosinesimilarity import CosineSimilarity
from matching.okapi import Okapi
import heapq

@click.command()
@click.option('--debug', is_flag=True)
@click.option('--docspath', type=click.File('rb'),
              default='data/parsed-docs.pkl')
@click.option('--metapath', type=click.File('rb'),
              default='data/doc-meta.pkl')
@click.option('--algorithm', default='okapi', help='okapi or cosine')
@click.option('--count', default=10)
def cli(debug, docspath, metapath, algorithm, count):
    print("""Query the utterance database by specifying a query at the prompt.
Specify no query to exit.

Meta data filters may be provided at the start of the query. Example query:
<house:Senate,PersonType:Lobbyist,PersonType:Legislator> strongly oppose""")

    subs_itr = SubstitutableElement()
    meta_itr = QueryMetadataParser(subs_itr, 'query')
    freq_itr = FreqCounter(meta_itr, 'query')
    lowr_itr = LowerCaser(freq_itr)
    stop_itr = StopwordElement(lowr_itr, ['a', 'an', 'the'])
    stem_itr = PorterStemmerElement(stop_itr)

    indexList = pickle.load(docspath)
    metadata = pickle.load(metapath)
    if algorithm == 'okapi':
        matcher = Okapi(metadata)
    elif algorithm == 'cosine':
        matcher = CosineSimilarity(metadata)
    else:
        raise Exception('invalid matching algorithm')

    while True:
        query = input('\nEnter a query >> ')
        if query == '':
            break
        query_itr = QueryParser(query, 'query')
        subs_itr.setParent(query_itr)
        parsed_query = list(stem_itr)[0]

        documents = [d for d in indexList if docHasMeta(d, meta_itr.metaData)]
        for document in documents:
            if algorithm == 'okapi':
                document['match'] = matcher.match(parsed_query['words'],
                        document['words'], len(document['text']))
            else:
                document['match'] = matcher.match(parsed_query['words'],
                        document['words'])

        winners = heapq.nlargest(count, documents, key=lambda doc: doc['match'])

        for doc in winners:
            click.echo("")
            if debug:
                click.echo(str(doc['match']))
                words = parsed_query['words']
                click.echo(["%s: %s" % (key, words[key]) for key in sorted(words.keys())])
                words = doc['words']
                click.echo(["%s: %s" % (key, words[key]) for key in sorted(words.keys())])
            click.echo("%s, %s (%s) %s" % (doc['last'], \
                    doc['first'], doc['PersonType'], doc['house']))
            click.echo(doc['text'])

        click.echo('\n' + '-' * 80)

def docHasMeta(doc, meta):
    """meta is a hash of {docKey: [possibleValues]} doc[docKey]
    must be in possibleValues"""
    for key, vals in meta.items():
        if key not in doc.keys():
            return False
        if doc[key] not in vals:
            return False
    return True
