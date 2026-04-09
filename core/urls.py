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

from core import views

urlpatterns = [
    # =========================== Answers ============================
    path("answers/<int:id>/edit/", views.AnswerEditView.as_view(), name='answer_edit'),

    # ============================ Search ============================
    path("search/", views.SearchView.as_view(), name='search'),

    # ============================= Tags =============================
    path("tags/", views.TagsView.as_view(), name='tags'),
    path("tags/<slug:tag>/", views.TagView.as_view(), name='tag'),

    # ============================ Users =============================
    path("users/", views.UsersView.as_view(), name='users'),
    path("users/login/", views.UserLoginView.as_view(), name='user_login'),
    path("users/logout/", views.UserLogoutView.as_view(), name='user_logout'),
    path("users/settings/", views.UserSettingsView.as_view(), name='user_settings'),
    path("users/signup/", views.UserSignupView.as_view(), name='user_signup'),
    path("users/<int:id>/", views.UserView.as_view(), name='user'),
]
