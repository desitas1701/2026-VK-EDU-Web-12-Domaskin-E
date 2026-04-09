"""
URL configuration for questions app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from questions import views

urlpatterns = [
    # ============================ Index =============================
    path("", views.IndexView.as_view(), name='index'),

    # ========================== Questions ===========================
    path("questions/", views.QuestionsView.as_view(), name='questions'),
    path("questions/ask/", views.QuestionAskView.as_view(), name='question_ask'),
    path("questions/hottest/", views.QuestionsHottestView.as_view(), name='questions_hottest'),
    path("questions/newest/", views.QuestionsNewestView.as_view(), name='questions_newest'),
    path("questions/<int:id>/", views.QuestionView.as_view(), name='question'),
    path("questions/<int:id>/delete/", views.QuestionDeleteView.as_view(), name='question_delete'),
    path("questions/<int:id>/edit/", views.QuestionEditView.as_view(), name='question_edit'),
]
