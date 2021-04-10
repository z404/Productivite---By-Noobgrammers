from django.urls import path

from . import views

app_name = "mailit"
urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("test/", views.test, name="test"),
    path("compose/", views.compose, name="compose"),
    path("viewemail/", views.viewemail, name="viewemail"),
]
