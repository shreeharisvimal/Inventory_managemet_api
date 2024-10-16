from django.urls import path
from . import views


urlpatterns = [
    path('UserAuth/', views.UserAuths.as_view(), name='UserAuths'),
    path('UserLogOut/', views.LogoutView.as_view(), name='UserLogOut')
]
