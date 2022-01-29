"""novella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    # Here we are assigning the path of our url
    path('', views.signIn,name="signIn"),
    path('home/', include('main.urls'),name="home"),
    
    path('postsignin/', views.postsignIn,name="postsignIn"),
    path('postsignUp/', views.postsignUp,name="postsignUp"),
    path('signUp/', views.signUp,name="signup"),
]