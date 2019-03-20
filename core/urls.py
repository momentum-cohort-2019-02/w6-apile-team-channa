from django.urls import path
from . import views

urlpatterns = [
    path('', PostList.as_view(), name='index')
]
