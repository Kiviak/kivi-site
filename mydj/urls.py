"""mydj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from kindle import views as k_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/',k_views.Signup.as_view(),name='signup'),
    path('accounts/login/',k_views.Login.as_view(),name='login'),
    path('accounts/logout/',k_views.Logout.as_view(),name='logout'),
    path('accounts/changepassword/',k_views.Changepassword.as_view(),name='changepassword'),
    path('accounts/profile/',k_views.Profile.as_view(),name='profile'),
    path('accounts/profile/star/',k_views.Profilestar.as_view(),name='profilestar'),
    path("", include("kindle.urls")),
]

from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]