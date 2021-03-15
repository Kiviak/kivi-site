from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ebook(models.Model):
    title=models.CharField(max_length=512)
    publisher=models.CharField(max_length=512)
    language=models.CharField(max_length=64)
    # date=models.DateTimeField()
    creator=models.CharField(max_length=512)
    isbn=models.CharField(max_length=32)
    iclass=models.CharField(max_length=64)
    asin=models.CharField(max_length=32,primary_key=True)
class Ebookintro(models.Model):
    ebook=models.OneToOneField(Ebook,on_delete=models.CASCADE)
    intro=models.TextField()
class Ebookintro_clean(models.Model):
    ebook=models.OneToOneField(Ebook,on_delete=models.CASCADE)
    intro=models.TextField()

class Star(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ebook=models.ForeignKey(Ebook,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=['user','ebook']
class Ebookreal(models.Model):
    md5=models.CharField(max_length=64,primary_key=True)
    title=models.CharField(max_length=512)
    type=models.CharField(max_length=32)
    path=models.CharField(max_length=1024)
    size=models.BigIntegerField(null=True)
    asin=models.CharField(max_length=32,null=True)

class Ebookreview(models.Model):
    ebook=models.ForeignKey(Ebook,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    ebookreviews=models.ManyToManyField('self',symmetrical=False)
    createtime=models.DateTimeField(auto_now=True)
    edittime=models.DateTimeField(null=True)
