from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name="index"),
    path('create/',views.create,name='create'),
    path('<int:pk>/',views.contact_details_view,name='detail'),
    path('edit/<int:pk>/',views.edit,name='edit'),
    path('delete/<int:pk>/',views.delete,name='delete'),
]
