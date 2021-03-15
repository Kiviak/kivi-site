from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
import json
from time import sleep

from .models import Ebook,Ebookreal,Star
from . import forms
from django.core.cache import cache

PAGINATE_KEYWORD='page'
ELASTICSEARCH_HOSTS=['localhost']
ELASTICSEARCH_INDEX='kindle'


class Ebookmainpage(TemplateView):
    template_name='kindle/mainpage.html'
    http_method_names=['get']
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(''.join([reverse('list'),'?page=1']))
class Search(TemplateView):
    template_name='kindle/search.html'
    http_method_names=['get']

    paginate_by=20
    paginate_keyword=PAGINATE_KEYWORD
    db_table=Ebook
    def get(self, request, *args, **kwargs):

        return HttpResponseRedirect(reverse('noserve'))

        if self.paginate_keyword in request.GET:
            page_num = request.GET.get(self.paginate_keyword)
        else:
            para=request.GET.copy()
            para[self.paginate_keyword]=1
            murl=reverse('search')+'?'+para.urlencode()
            return redirect(murl)
        
        myform=forms.SearchForm(request.GET)
        if myform.is_valid():
            from elasticsearch import Elasticsearch
            es = Elasticsearch(hosts=ELASTICSEARCH_HOSTS)       
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
            msbody['query']['multi_match']['query']=myform.data['keyword']
            # res=es.search(index='kindle2',body=msbody,_source=False)
            msbody['from']=self.paginate_by*(int(page_num)-1)
            msbody['size']=self.paginate_by
            res=es.search(index='kindle2',body=msbody,_source=True)
            
            context = self.get_context_data(**kwargs)
            context['form']=myform
            context['current_page_num']=page_num
            import math
            context['current_page_totle']=math.ceil(int(res['hits']['total']['value'])/self.paginate_by)
            object_list=[]
            for item in res['hits']['hits']:
                object_list.append(item['_source'])
            context['object_list']=object_list
        return self.render_to_response(context)
class Ebooklist(TemplateView):
    template_name='kindle/list.html'
    http_method_names=['get']
    # extra_context={'mk':89}

    paginate_by=20
    paginate_keyword=PAGINATE_KEYWORD
    db_table=Ebook
    def get(self, request, *args, **kwargs):

        # use print(contact_list.query) to get the raw sql
        MYKEY='booklist'
        books=cache.get(MYKEY,None)
        if books is not None:
            contact_list=books
        else:
            contact_list = self.db_table.objects.all()
            cache.set(MYKEY,contact_list,60)

        paginator = Paginator(contact_list,self.paginate_by)

        page_num = request.GET.get(self.paginate_keyword)
        page = paginator.get_page(page_num)
        context = self.get_context_data(**kwargs)
        context['current_page']=page
        context['form']=forms.SearchForm()

        from django.db.models import Count
        res=self.db_table.objects.values('iclass').annotate(num=Count('iclass')).order_by('-num').exclude(iclass__isnull=True).exclude(iclass__exact='')
        context['class']=res

        return self.render_to_response(context)  
class Ebookdetail(TemplateView):
    template_name='kindle/detail.html'
    http_method_names=['get','post']
    db_table=Ebook

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        book=self.db_table.objects.get(pk=context['id'])
        context['book']=book
        from .forms import ReviewForm
        from .models import Ebookreview
        context['form']=ReviewForm()
        context['reviews']=Ebookreview.objects.filter(ebook=context['id'])
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        from .forms import ReviewForm
        from .models import Ebookreview,Ebook
        mform=ReviewForm(request.POST)
        if mform.is_valid():
            ebook=Ebook.objects.get(pk=context['id'])
            item=Ebookreview(ebook=ebook,user=request.user,**mform.cleaned_data)
            item.save()
            num=request.POST.get('code',0)
            if num:
                reve=Ebookreview.objects.get(pk=num)
                item.ebookreviews.add(reve)
            return redirect(reverse('detail',kwargs={'id':context['id']}))

class Ebookdownload(TemplateView):
    http_method_names=['get']
    db_table=Ebookreal

    def get(self, request, *args, **kwargs):
        book=self.db_table.objects.filter(asin=kwargs['id'])
        if not book:
            return HttpResponse('不存在')
        file_path=book[0].path
        from mydj.settings import STATIC_ROOT
        file_path=STATIC_ROOT+'/pytest.pdf'
        myfile=open(file_path,'rb')
        res=FileResponse(myfile)
        import os
        # Content-Disposition属性使用encode的原因是解决浏览器端下载文件文件名（如中文）乱码问题
        res['Content-Disposition'] = ('inline; filename=' + os.path.basename(file_path)).encode()
        # res['Content-Disposition'] = "inline; filename*=UTF-8''" + os.path.basename(file_path)
        return res
class Ebookstar(TemplateView):
    http_method_names=['get']
    def get(self, request, *args, **kwargs):
        from .models import Star,Ebook
        context = self.get_context_data(**kwargs)
        try:
            code=int(request.GET['code'])
            ebook=Ebook.objects.get(pk=context['id'])
            user=request.user
            if code:
                item=Star.objects.filter(user=user).filter(ebook=ebook)
                item.delete()
            else:
                item=Star(user=user,ebook=ebook)
                item.save()
        except :
            return JsonResponse({'code':2})

        return JsonResponse({'code':1-code})        
class Ebookstarjson(TemplateView):
    http_method_names=['post']
    def post(self, request, *args, **kwargs):
        from .models import Star,Ebook
        context = self.get_context_data(**kwargs)
        import json
        res=json.loads(request.POST['code'])
        mlist=[]
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({'code':0})
        for key in res:
            try:
                ebook=Ebook.objects.get(pk=key)
                item=Star.objects.filter(user=user).filter(ebook=ebook)
                if item:
                    mlist.append(1)
                else:
                    mlist.append(0)

            except expression as identifier:
                mlist.append(0)

        return JsonResponse({'code':1,'mlist':json.dumps(mlist)})         
class Profilestar(TemplateView):
    template_name='kindle/profile_star.html'
    http_method_names=['get','post']
    paginate_by=20
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        books=Star.objects.filter(user=request.user).order_by('-date')
        res=Paginator(books,per_page=self.paginate_by,allow_empty_first_page=True)
        pagenumber=1
        if 'p' in request.GET:
            pagenumber=int(request.GET['p'])
        context['page']=res.page(pagenumber)
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        for item in request.POST:
            if item=='csrfmiddlewaretoken':
                continue
            try:
                book=Star.objects.filter(ebook=Ebook.objects.get(asin=item),user=request.user)
                book.delete()
            except Exception as err:
                print(err)
        return redirect(reverse('profilestar'))

class Signup(TemplateView):
    template_name='kindle/auth/signup.html'
    http_method_names=['get','post']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)      
        context['form']=forms.SignUpForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        from django.contrib.auth import login,authenticate
        mform=forms.SignUpForm(request.POST)
        if mform.is_valid():
            from django.contrib.auth.models import User
            user=User.objects.filter(username=mform.cleaned_data['username'])
            if not user:
                try:
                    user=User.objects.create_user(**mform.cleaned_data)
                    user.save()
                    return redirect(reverse('login'))
                except Exception as identifier:
                    print(identifier)
            else:
                mform.add_error('username','用户名已被注册')

        context['form']=mform
        return self.render_to_response(context)
class Login(TemplateView):
    template_name='kindle/auth/login.html'
    http_method_names=['get','post']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)      
        context['form']=forms.UserForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        from django.contrib.auth import login,authenticate
        mform=forms.UserForm(request.POST)
        if mform.is_valid():
            user=authenticate(**mform.cleaned_data)
            if user is not None:
                login(request,user=user)
                return redirect(reverse('profile'))
        
        # mform.add_error('password','密码不正确')
        # mform.add_error('username','用户名不正确')
        mform.add_error(None,'用户名或密码不正确')
        context['form']=mform
        return self.render_to_response(context)
class Logout(TemplateView):
    template_name='kindle/auth/logout.html'
    http_method_names=['get']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        from django.contrib.auth import logout
        context['who']=request.user.username
        logout(request)
        # context['form']=forms.SearchForm()
        return self.render_to_response(context)
class Changepassword(TemplateView):
    template_name='kindle/auth/changepassword.html'
    http_method_names=['get','post']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)      
        context['form']=forms.ChangePasswordForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        from django.contrib.auth import login,authenticate
        mform=forms.ChangePasswordForm(request.POST)
        if mform.is_valid():
            user=authenticate(username=request.user.username,password=mform.cleaned_data['password'])
            if user is not None:
                if mform.cleaned_data['newpassword']==mform.cleaned_data['newpassword2']:
                    user.set_password(mform.cleaned_data['newpassword'])
                    user.save()
                    return redirect(reverse('login'))
                else:
                    mform.add_error('newpassword','新密码不一致')

            else:
                mform.add_error('password','密码不正确')
        context['form']=mform
        return self.render_to_response(context)
class Profile(TemplateView):
    template_name='kindle/auth/profile.html'
    http_method_names=['get'] 
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

def getpic(request):
    import requests
    import re
    import os
    from bs4 import BeautifulSoup as bs
    baseurl='https://www.amazon.cn/dp/'
    items=Ebook.objects.all()
    import random
    from requests_html import HTMLSession

    ses=HTMLSession()
    px=ses.get('https://www.xicidaili.com/')
    trs=px.html.find('tr')
    lss=[]
    for tr in trs:
        tds=tr.find('td')
        if tds:
            if tds[5].full_text=='HTTPS':
                lss.append(tds[1].full_text)
                lss.append(tds[2].full_text)


    proxies={ }
    num=len(lss)//2
    # io=random.randrange(0,num)

    header={
    # 'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
                #   'AppleWebKit/537.36 (KHTML, like Gecko) '
                #   'Chrome/57.0.2743.116 Safari/537.36',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
    'Accept':'text/html,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    "Referer": "https://www.amazon.cn/",
    
    }
    cook='session-id=459-8151064-4039433; ubid-acbcn=460-0090575-6766933; lc-acbcn=zh_CN; x-acbcn="H?jwbF9BKeo?RNxX2wDE53cOIB?cPGfT"; at-main=Atza|IwEBIAilBCNnkenSVIbPDbKTPxRTTwlMRF-CUOKhq8eIia6SKwHRQL8GKPqvvtqdtXTzlw2fryOZ_4nTK9XQGN0D3IhoNZmVgwL9H8WRXTQ8rKxJHS_4oGTJnQsPaTOidnwX6Ko05wytrGNl0zahHqcvcNWLpoLXJAzRco9yeTNhTxOnYpw8Uczj17pWZMz8NIA2ZIOy95wz3-csDmUCTHGeKOwPmHfN5j6K75Aqm5gXw-7Q1V_JYDnIRHT8cP6IK6pEZNbZrREZY4W0BF5cwevxPVeEjOWV3Y7hzDwBRdo53YFvmwrZqnjaiS1sF_VYzWHOV1Vj5lCkzccn5AXVIIifzZ5qekfs97OWoMMDsg5Hrurnu3p-BDtD42A1cfjwqNoQauQ4w8Rm2UBMickCPFXeAdIf; sess-at-main="R0pAdfDWc6HTWzGzX4vL6hvkBgv+bgr8PISCKbaK9DM="; sst-main=Sst1|PQG6ssdYAGzfwnCZyWl7o006C08EtyjgPe81sKLQM02vECLXV3QPAO7vSLcnbwZpl5a9UaOQ9dqwm7cWnamvPu3f27iEtiiZAkiFsG79o8wtpLK10mQzE3TsFMYi57A0vBl0boOawlO0hjo9kt_m0v0Df3a0sMDfBls0Qz4V0QWFKGAktfgxYV5lUP09eQ17VyKvn2VjNxEtL8KS_e99Xk9Qy5pPN-tlttFJi-NwM-dJfJ4274yrGlWRaIZVUaBSW3f0Uk2Lyow6tpbcmpiEhE6UVFiW56ixFkgq_mA1OtvWbDP84PS6h3BZUjzTEuP2ySQzlJQZPZYYaVicXcCa-wN-sA; i18n-prefs=CNY; x-wl-uid=1xJ3UwLR69YP8LzlseSZ+P7tDtNdH6hOPzOiGxIrjFtov7OCSkDj9rWrmL+uoNOT1k5o/jCpIxPfE+XmOpSLQjJoJKSPrC7fuWP9Bb4i4Hw6OYnLQ+xrXeQc30MRnDBYv+JQKvVwRcgc=; x-amz-captcha-1=1567779106902443; x-amz-captcha-2=vhGEVqKhzreGjcW/pF8wvw==; session-token="ZEgP8TQ+05UmFAARkTIJdWsmukbSpXufrTeXpcVs8Z1CThf5qpnwXsZZd418g5dRDgm3xSJ2UmpM4G4/Wef6SCrii8iK6crHR3RwKcBb68X3HkdCMEUDf7sradCfBjlrdDViKHox9/6YQ/nEVXw6AL1VgJyc+NZ8AUVl/KzWvT7D2Rxmfka2qtT23w5YDIdlYW8WTXEL5l7V8cdtXJ+YPBwgBYJwC9ReAnhawJYmd0faQZuIDqNRell7jb7LGVQ3HtWJSdl5ISs="; csm-hit=tb:s-X33G2N3DEA698F9MH0RT|1567772411468&adb:adblk_no&t:1567772413033; session-id-time=2082729601l'
    m=re.findall('[^=; "]+',cook)
    cookie={}
    for i in range(14):
        cookie[m[i*2]]=m[i*2+1]
    param={
        "storeType":"ebooks"
    }

    i=0
    session=HTMLSession()
    io=0
    proxies['https']='http://'+lss[io*2]+":"+lss[io*2+1]
    picnum=0
    pinno=0
    mlist=[]
    # proxies = { "https": "http://221.226.94.218:110",
    #          "https": "http://175.25.26.117:3128", } 
    with open('/home/soy/ubun/non.json','r',encoding="utf-8") as ferr:
        js=json.load(ferr)
    mlist=js
    for book in items:
        i+=1
        try:
            savepath=filepath+book.asin+'.jpg'
            if os.path.exists(savepath):
                picnum+=1
                continue
            if book.asin in mlist:
                pinno+=1
                continue
            # if book.asin=='B009D9YKIW':
            #     flag=False
            # if flag:
            #     continue
            # if i<5670:
            #     continue
            
            # io=random.randrange(0,num)
            # proxies['https']='http://'+lss[io*2]+":"+lss[io*2+1]
            r=session.get(baseurl+book.asin,headers=header)
            res=r.html.find('#ebooksImgBlkFront')
            picurl=res[0].attrs['data-a-dynamic-image']
            m=re.findall('https:[^,_]*.jpg',picurl)
            # io=random.randrange(0,num)
            # proxies['https']='http://'+lss[io*2]+":"+lss[io*2+1]
            pic=session.get(m[-1],stream=False)

            fd=open(savepath,'wb')
            fd.write(pic.content)
            fd.close()
            picnum+=1
            # sleep(1)
            print("get new pic:",book.asin,'\n' )
        except Exception:
            print(i)
            with open('/home/soy/ubun/err.html','wb') as ferr:
                ferr.write(r.content)
            try:
                res=r.html.find('title')
                if res[-1].text=='找不到页面':
                    print("no longer:",book.asin,'\n' )
                    pinno+=1
                    mlist.append(book.asin)
                else:
                    print("ban:",book.asin,'\n' )
                    break
                    # io+=1
                    # if io>=num:
                    #     print('no proxy')
                    #     break
                    # proxies['https']='http://'+lss[io*2]+":"+lss[io*2+1]
            except Exception as identifier:
                pass
            # io+=1
            # if io>=num:
            #     print('no proxy')
            #     break
            # proxies['https']='http://'+lss[io*2]+":"+lss[io*2+1]
            # print("fail:",book.asin,'\n' )
            # sleep(1)
    print(picnum,'\n',pinno,'\n')
    # with open('/home/soy/ubun/non.json','w') as ferr:
    #     json.dump(mlist,ferr)

    return HttpResponse('well done.')
def echo(request):
    return HttpResponse('well')
class Myself(TemplateView):
    template_name='kindle/myself.html'
    http_method_names=['get']
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
class Nosearch(TemplateView):
    template_name='kindle/nosearch.html'
    http_method_names=['get']
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)