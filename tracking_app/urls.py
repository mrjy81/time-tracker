from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('handle/<int:pk>', views.handler, name='handler'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login_view, name='login'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('csv', views.export_csv, name='csv'),
]
