"""pi_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from dashboard import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", views.DashboardIndex.as_view(), name="dashboard_index"),
    
    # For json data from server
    url("^index/ram$", views.IndexJsonRam.as_view(), name="index_ram"),
    url("^index/disk$", views.IndexJsonDisk.as_view(), name="index_disk"),
    url("^index/temp$", views.IndexJsonTemp.as_view(), name="index_temp"),
    url("^index/uptime$", views.IndexJsonUptime.as_view(), name="index_uptime"),
    url("^index/ext_ip$", views.IndexJsonExtIp.as_view(), name="index_extip"),
    
    # Tools
    url("^price_scrapper$", views.PriceScrapper.as_view(), name="price_scrapper"),

    url("^test$", views.TestPage.as_view(), name="test"),
]
