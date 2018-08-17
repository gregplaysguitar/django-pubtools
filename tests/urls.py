from django.conf.urls import url
try:
    from django.contrib.auth.views import LoginView
    login = LoginView.as_view()
except ImportError:
    from django.contrib.auth.views import login
    
from . import views


urlpatterns = (
    url(r'^login$', login),
    url(r'^(\d+)$', views.article, {}, 'article'),
)
