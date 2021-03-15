from django.core.management.base import BaseCommand,CommandError

class Command(BaseCommand):
    help = 'model update'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for item in options['path']:
            print(item)
            # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % item))
        from kindle.models import Ebookreal
        from django.db import connection
        with connection.cursor() as cursor: 
            cursor.execute('''SELECT kindler.book_zbookinfo.asin,kindler.book_zbook.id,kindler.book_zbook.md5Hash FROM kindler.book_zbookinfo
        JOIN kindler.book_zbook ON kindler.book_zbook.id=kindler.book_zbookinfo.zbook_id''') 
        #     cursor.execute('''SELECT kindle.kindle_ebook.asin,kindle.kindle_ebook.title,kindle.kindle_ebookreal.title FROM kindle.kindle_ebook
        # JOIN kindle.kindle_ebookreal ON kindle.kindle_ebook.asin=kindle.kindle_ebookreal.asin''') 
            res=cursor.fetchall()
            mset={}
            for item in res:
                mlist=list(item)
                if mlist[0]:
                    mset[mlist[-1]]=mlist[0]
            books=Ebookreal.objects.all()
            for book in books:
                if book.md5 in mset:
                    try:
                        book.asin=mset[book.md5]
                        book.save()
                    except Exception as identifier:
                        print(identifier)