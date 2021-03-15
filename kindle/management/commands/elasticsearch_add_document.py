from .mysqlupdate import Command as Cmd


class Command(Cmd):
    """
    load ebookinfo from other table 
    """

    def handle(self, *args, **options):
        from elasticsearch import Elasticsearch
        from elasticsearch_dsl import Index, Mapping, Document, Keyword, Text
        ELASTICSEARCH_HOSTS = ['localhost']
        ELASTICSEARCH_INDEX = 'kindle2'
        
        es = Elasticsearch(ELASTICSEARCH_HOSTS)
        index = Index(ELASTICSEARCH_INDEX, using=es)

        class Ebookdoc(Document):
            title = Text()
            creator = Text()
            publisher = Text()
            iclass = Text()
            isbn = Text()
            asin = Keyword()

            class Index(object):
                name = ELASTICSEARCH_INDEX

        from kindle.models import Ebook
        books=Ebook.objects.all()
        for item in books:
            doc=Ebookdoc()
            try:
                doc.title=item.title
                doc.creator=item.creator
                doc.publisher=item.publisher
                doc.iclass=item.iclass
                doc.isbn=item.isbn
                doc.asin=item.asin
                doc.save(es)
            except Exception as err:
                print(err)
