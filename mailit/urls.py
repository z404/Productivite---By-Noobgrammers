from django.urls import path

from . import views

app_name = 'mailit'
urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
]
