from .mysqlupdate  import Command as  Cmd

class Command(Cmd):
    """
    load ebookinfo from other table 
    """
    def handle(self, *args, **options):
        from kindle.models import Ebook,Ebookintro
        from django.db import connection
        with connection.cursor() as cursor:
            sql='''select * from kindler.book_amzhelp'''
            cursor.execute(sql)
            res = cursor.fetchall()
            for item in res:
                try:
                    book=Ebook.objects.get(pk=item[0])
                    bookintro=Ebookintro(ebook=book,intro=item[1])
                    bookintro.save()
                except Exception as identifier:
                    print(identifier)
