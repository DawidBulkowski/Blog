from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^post/(?P<post_slug>[-\w\d]+)$', views.post),
    url(r'^kategoria/(?P<category_slug>[-\w\d]+)$', views.category),
    url(r'^zglos$', views.report),
]
