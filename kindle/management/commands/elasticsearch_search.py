from .mysqlupdate import Command as Cmd


class Command(Cmd):
    """
    load ebookinfo from other table 
    """

    def handle(self, *args, **options):
        from elasticsearch import Elasticsearch
        from elasticsearch_dsl import Index
        ELASTICSEARCH_HOSTS = ['localhost']
        ELASTICSEARCH_INDEX = 'kindle2'

        es = Elasticsearch(ELASTICSEARCH_HOSTS)
        newindex = Index('kindle2', using=es)

        msbody = {
            "from": 0,
            "size": 10,
            "query": {
                "multi_match": {
                    "query": "python",
                    "fields": ["title", "asin", "isbn", "publisher", "creator", "iclass"],
                    "type": "cross_fields",
                    "operator": "and",
                }
            },
        }
        query_word = 'python'
        msbody['query']['multi_match']['query'] = query_word
        res = es.search(index=ELASTICSEARCH_INDEX, body=msbody, _source=False)
        msbody['size'] = res['hits']['total']['value']+10
        res = es.search(index=ELASTICSEARCH_INDEX,body=msbody, _source=True)
        print(res['hits']['total']['value'])
