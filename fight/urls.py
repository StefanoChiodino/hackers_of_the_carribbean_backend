from django.urls import path

from fight import views

app_name = 'fight'
urlpatterns = [
    path('begin', views.begin, name='begin'),
    # path('<uuid:pie_run_id>/', views.pie_run, name='pie_run'),
]