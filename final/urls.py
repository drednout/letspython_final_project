from django.conf.urls import include, url
from django.contrib import admin
from admintool import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'final.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^players/', include('admintool.urls')),
    url(r'^access_denied/$', views.access_denied),
    url(r'^redis_data/$', views.show_redis_data),
    url(r'^$', views.mainpage),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.logout_user),

]
