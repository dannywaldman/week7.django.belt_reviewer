from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^books$', views.books, name = 'books'),
    url(r'^books/add$', views.add, name = 'add'),
    url(r'^books/create$', views.create, name = 'create'),
    url(r'^books/(?P<id>\d+)$', views.show_book, name = 'show_book'),
    url(r'^users/(?P<id>\d+)$', views.show_user, name = 'show_user'),
    url(r'^books/(?P<id>\d+)/review$', views.add_review, name = 'add_review'),
    url(r'^bookse/review/(?P<id>\d+)/destroy$', views.delete_review, name = 'delete_review')
]
