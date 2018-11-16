from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from personal_timeline import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^wall/(?P<username>\w+)/$', views.wall, name='wall'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
