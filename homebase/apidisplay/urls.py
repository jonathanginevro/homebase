from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('team/<team_id>/', views.index2, name="index2"),
    path('player/<player_id>/', views.index3, name="index3")
]