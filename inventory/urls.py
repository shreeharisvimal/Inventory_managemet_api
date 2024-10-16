from django.urls import path
from . import views


urlpatterns = [
	path('item/<int:pk>/', views.ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
	path('item/', views.ItemViewSet.as_view({'post': 'create'})),		
]
