from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<team_id>/', views.index2, name="team-page"),
    path('<team_id>/<player_id>/', views.index3, name="index3")
]