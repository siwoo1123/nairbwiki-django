from django.urls import path, include
from wiki import views as v

urlpatterns = [
    path('',v.Idx),
    path('w/<name>/',v.Read),
    path('w/',v.Idx),
    path('redirect/',v.Redir),
    path('create/<name>/',v.Cre),
    path('createDoc/',v.CreDc),
    path('update/<name>',v.Update),
    path('delete/<name>',v.Delete),
    path('updateDoc/',v.updateDoc),
]
