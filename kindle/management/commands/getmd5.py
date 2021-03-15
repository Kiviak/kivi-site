from django.core.management.base import BaseCommand,CommandError

class Command(BaseCommand):
    help = 'get md5 of files'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        for item in options['path']:
            print(item)
            # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % item))
        from pathlib import Path
        mpath=Path(options['path'][-1])
        res=[]
        filter=['azw3','azw','mobi']
        self._filehash(mpath,filter,res)
        from kindle.models import Ebookreal,Ebook
        for item in res:
            try:
                ebook=Ebook.objects.filter(title=item['title'])
                if ebook:
                    bkr=Ebookreal(**item,ebook=ebook[0])
                else:
                    bkr=Ebookreal(**item)
                bkr.save()
            except expression as identifier:
                print(identifier)
        return            
    
    def _filehash(self,filepath,filter=[],result=[]):
        import hashlib
        if filepath.is_dir():
            for item in filepath.iterdir():
                self._filehash(item,filter,result) 
        else:
            filetype=filepath.suffix.strip('.')
            if filetype not in filter:
                return
            if filepath.is_file():
                filesize=filepath.stat().st_size
                content = filepath.read_bytes()
                md5 = hashlib.md5(content)
                md5str = md5.hexdigest()
                info={}
                info['title']=filepath.stem
                info['type']=filetype
                info['size']=filesize
                info['md5']=md5str
                info['path']=str(filepath)
                result.append(info)
        return result
