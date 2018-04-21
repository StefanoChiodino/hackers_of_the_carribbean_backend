from django.urls import path

from fight import views

app_name = 'fight'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<uuid:pie_run_id>/', views.pie_run, name='pie_run'),
]