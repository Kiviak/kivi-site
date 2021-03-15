from .mysqlupdate  import Command as  Cmd

class Command(Cmd):
    """
    load ebookinfo_clean from other table 
    """
    def handle(self, *args, **options):
        from kindle.models import Ebook,Ebookintro,Ebookintro_clean
        import bleach
        tags=['h1','h2','h3','h4','div','br','p','span']
        src=Ebookintro.objects.all()
        for book in src:
            try:
                info = bleach.clean(book.intro, tags=tags, strip=True)
                newbook=Ebookintro_clean(ebook=book.ebook,intro=info)
                newbook.save()
            except Exception as identifier:
                print(identifier)
        return
