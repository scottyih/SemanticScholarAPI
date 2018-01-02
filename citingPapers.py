import json, sys
import urllib.request
from collections import defaultdict

def main(id):
    rec = json.loads(urllib.request.urlopen("http://es.development.s2.dev.ai2:9200/citation/citation/_search?q=citedPaper.id:%s&size=10000" % id).read())

    print("Total citations: %d" % rec['hits']['total'])
    for p in rec['hits']['hits']:
        cp = p['_source']['citingPaper']
        if 'authors' in cp:
            authors = ', '.join([a['name'] for a in defaultdict(lambda: '', cp)['authors']])
        else:
            authors = ''

        strCp = defaultdict(lambda: '', cp)
        title = strCp['title']
        venue = strCp['venue']

        intCp = defaultdict(lambda: 0, cp)
        year = intCp['year']
        id = strCp['id']
        #print("%s" % id)
        print('%s\t%s. "%s." In %s %d' % (id, authors, title, venue, year))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python citingPapers.py paper_id\n")
        sys.exit(-1)
    main(sys.argv[1])
