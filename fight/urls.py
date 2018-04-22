from django.urls import path

from fight import views

app_name = 'fight'
urlpatterns = [
    path('begin', views.begin, name='begin'),
    path('step', views.step, name='step'),
    path('comeback', views.comeback, name='comeback'),
    path('seed', views.seed, name='seed'),
    path('deleteGames', views.delete_games, name='deleteGames')
]