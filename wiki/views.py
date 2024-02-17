from django.shortcuts import render, redirect
from .models import Docs
from django.utils import timezone as datetime
from django.contrib.auth.decorators import login_required

only_admin=['네어브위키:대문','위키:문법']

# Create your views here.
def Idx(req):
    return redirect('/w/네어브위키:대문')

def Read(req,name):
    global only_admin
    noDoc=False
    try:
        doc=Docs.objects.get(title=name)
    except: noDoc=True
    if(noDoc):
        return render(req, 'read.html', {
            'title': name,
            'content': '',
            'exist': False,
            'update_date': '',
            'isnotad': name not in only_admin,
        })
    else:
        content = doc.content
        red=True
        try:
            if(req.GET["no_redirect"]=='true'): red=False
        except: pass
        if content[:10]=='<REDIRECT ' and content[10] is not ' ' and red:
            url = content.replace('<REDIRECT ','/w/')
            if(url != f'/w/{name}'):
                return redirect(f'{url}?redirect_by={name}')
        try:
            if(req.GET["redirect_by"]):
                content=f'<div class="alert alert-secondary" role="alert"><a href="/w/{req.GET["redirect_by"]}?no_redirect=true" class="alert-link">{req.GET["redirect_by"]}</a>에서 넘어옴</div>{content}'
        except: pass
        return render(req, 'read.html', {
            'title': doc.title,
            'content': content,
            'exist': True,
            'update_date': doc.update_date,
            'isnotad': doc.title not in only_admin,
        })

def Redir(req):
    if req.GET["title"]=='../../admin':
        return redirect(f'/w/네어브위키:대문')
    return redirect(f'/w/{req.GET["title"]}')

@login_required(login_url='/common/login/')
def Cre(req,name):
    try:
        if Docs.objects.get(title=name).content:
            return redirect(f'/w/{name}/')
    except: pass
    return render(req, 'create.html', {
        'title': name,
    })

@login_required(login_url='/common/login/')
def CreDc(req):
    doc={
        'title': req.POST.get("title"),
        'content': req.POST.get("content").replace('<script','&lt;script').replace('</script','&lt;/script&gt;'),
        'create_date': datetime.now(),
        'update_date': datetime.now(),
    }
    new_doc=Docs(
        title = doc['title'],
        content = doc['content'],
        create_date = doc['create_date'],
        update_date = doc['update_date'],
    )
    new_doc.save()
    url = f'/w/{doc["title"]}'
    return redirect(url)

@login_required(login_url='/common/login/')
def Update(req,name):
    try:
        if Docs.objects.get(title=name).content:
            return render(req, 'update.html', {
                'title': name,
                'content': Docs.objects.get(title=name).content,
            })
    except:
        return redirect(f'/create/{name}')
    

@login_required(login_url='/common/login/')
def updateDoc(req):
    doc={
        'title': req.POST.get("title"),
        'content': req.POST.get("content").replace('<script','&lt;script').replace('</script','&lt;/script&gt;'),
        'create_date': datetime.now(),
        'update_date': datetime.now(),
    }
    # new_doc=Docs(
    #     title = doc['title'],
    #     content = doc['content'],
    #     create_date = doc['create_date'],
    #     update_date = doc['update_date'],
    # )
    new_doc=Docs.objects.get(title=doc['title'])
    new_doc.content=doc['content']
    new_doc.update_date=datetime.now()
    new_doc.save()
    url = f'/w/{doc["title"]}'
    return redirect(url)

@login_required(login_url='/common/login/')
def Delete(req, name):
    doc=Docs.objects.get(title=name)
    doc.delete()
    return redirect('/')