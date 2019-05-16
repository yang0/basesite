# -*- coding: utf-8 -*-

"""server URL Configuration

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
from django.conf.urls import url
from django.urls import path, include
# from rest_framework import routers
# from apps.user.views import UserViewSet
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# Routers provide an easy way of automatically determining the URL conf.
# confrouter = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls')),
    # path('admin/', admin.site.urls),
    # path('user/', include("apps.user.urls")),

]
