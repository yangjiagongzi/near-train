from django.urls import path
from . import views

app_name = 'update'
urlpatterns = [
    path('', views.update, name='update'),
]
