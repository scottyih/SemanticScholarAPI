import json, sys
import urllib.request
from collections import defaultdict

def main(id):
    rec = json.loads(urllib.request.urlopen("http://es.development.s2.dev.ai2:9200/citation/citation/_search?q=citedPaper.id:%s&size=10000" % id).read())
    total = 0
    for p in rec['hits']['hits']:
        cp = defaultdict(lambda: '', p['_source']['citingPaper'])
        id = cp['id']
        cntRec = json.loads(urllib.request.urlopen("http://es.development.s2.dev.ai2:9200/citation/citation/_count?q=citedPaper.id:%s" % id).read())
        cCnt = cntRec['count']
        #print(id, cCnt)
        total += cCnt
    print(total)


def mainDedup(id):
    rec = json.loads(urllib.request.urlopen("http://es.development.s2.dev.ai2:9200/citation/citation/_search?q=citedPaper.id:%s&size=10000" % id).read())
    setId = set()
    for p in rec['hits']['hits']:
        cp = defaultdict(lambda: '', p['_source']['citingPaper'])
        cid = cp['id']
        rec1 = json.loads(urllib.request.urlopen("http://es.development.s2.dev.ai2:9200/citation/citation/_search?q=citedPaper.id:%s&size=10000" % cid).read())
        for p1 in rec1['hits']['hits']:
            cp1 = defaultdict(lambda: '', p1['_source']['citingPaper'])
            cid1 = cp1['id']
            setId.add(cid1)
    print(len(setId))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python citingPapers.py paper_id\n")
        sys.exit(-1)
    main(sys.argv[1])
    mainDedup(sys.argv[1])
