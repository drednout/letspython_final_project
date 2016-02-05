from django.conf.urls import url
import views


urlpatterns = [
    url(r'^(?P<player_id>[0-9]+)/$', views.PlayerDetailView.as_view()),
    url(r'^(?P<player_id>[0-9]+)/changeexp/$', views.ExpUpdateView.as_view()),
    url(r'^$', views.PlayersListView.as_view()),

]
