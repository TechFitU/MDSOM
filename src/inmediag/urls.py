try:
    from django.conf.urls import url, patterns
except:
    from django.conf.urls import *
from inmediag import views


urlpatterns = [
	url(r'dictado/(?P<identificador>[0-9a-zA-Z]+)/$', views.get_dictado_by_id, name="get_dictado_by_id")
]
