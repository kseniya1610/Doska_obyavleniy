"""Board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from lib2to3.pytree import Base
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic.base import RedirectView
from NBoard.views import mass_mail, otc, register_view, MyResponsesPost, accept, Board, CreateNotice, DeletePost, \
    DeleteResponce, EditNotice, MyResponses, NoticeDetail, RespondToPost

urlpatterns = [
    path('', RedirectView.as_view(url='board')),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view),
    path('accounts/register/otc/', otc),

    path('send_mass_mail/', mass_mail),

    path('board/', Board.as_view(), name='board'),
    path('board/post/create/', CreateNotice.as_view(), name='board_new'),
    path('board/post/<int:pk>/', NoticeDetail.as_view(), name='notice_detail'),
    path('board/post/<int:pk>/edit/', EditNotice.as_view(), name='board_new'),
    path('board/post/<int:pk>/respond/', RespondToPost.as_view(), name='respond'),
    path('board/post/<int:pk>/delete/', DeletePost.as_view()),

    path('board/response/<int:pk>/accept/', accept),
    path('board/response/<int:pk>/delete/', DeleteResponce.as_view()),

    path('accounts/profile/', MyResponses.as_view(), name='responses'),
    path('accounts/profile/post/<int:pk>/', MyResponsesPost.as_view(), name='response_post'),
]
