"""kanban URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from tasks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('tasks/', 
         views.TaskList.as_view(),
         name='task-list'),
    path('tasks/<int:pk>/',
         views.TaskDetail.as_view(), 
         name='task-detail'),
    path('users/', 
         views.UserList.as_view(), 
         name='user-list'),
    path('users/<int:pk>/', 
         views.UserDetail.as_view()),
])
