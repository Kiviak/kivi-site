from .mysqlupdate import Command as Cmd


class Command(Cmd):
    """
    load ebookinfo from other table 
    """

    def handle(self, *args, **options):
        from elasticsearch import Elasticsearch
        from elasticsearch_dsl import Index, Mapping
        ELASTICSEARCH_HOSTS = ['localhost']
        ELASTICSEARCH_INDEX = 'kindle2'

        es = Elasticsearch(ELASTICSEARCH_HOSTS)
        newindex = Index(ELASTICSEARCH_INDEX, using=es)
        if newindex.exists():
            exit('index already exists,change a new name')
        mp = Mapping()
        mp.field('title', 'text')
        mp.field('creator', 'text')
        mp.field('publisher', 'text')
        mp.field('iclass', 'text')
        mp.field('isbn', 'text')
        mp.field('asin', 'keyword')

        newindex.mapping(mp)
        newindex.create()
