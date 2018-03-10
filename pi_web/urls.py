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

admin.site.site_header = "Raspberry Pi Admin"
admin.site.site_title = "Raspberry Pi Web Portal"
admin.site.index_title = "Welcome to pi_web_dashboard admin site"

urlpatterns = [
    path('admin/', admin.site.urls),
    url("^$", views.DashboardIndex.as_view(), name="dashboard_index"),
    
    # For json data from server
    url("^index/ram$", views.IndexJsonRam.as_view(), name="index_ram"),
    url("^index/disk$", views.IndexJsonDisk.as_view(), name="index_disk"),
    url("^index/temp$", views.IndexJsonTemp.as_view(), name="index_temp"),
    url("^index/uptime$", views.IndexJsonUptime.as_view(), name="index_uptime"),
    url("^index/ext_ip$", views.IndexJsonExtIp.as_view(), name="index_extip"),
    
    # Home PC
    url("^home_pc$", views.HomePCPage.as_view(), name="home_pc"),
    url("^home_pc/poweron$", views.HomePCPowerOn.as_view(), name="home_pc_pon"),
    url("^home_pc/ping$", views.HomePCPing.as_view(), name="home_pc_ping"),
    
    # Tools
    url("^price_scrapper$", views.PriceScrapper.as_view(), name="price_scrapper"),

    url("^test$", views.TestPage.as_view(), name="test"),
]
