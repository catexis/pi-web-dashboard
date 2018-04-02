from django.views.generic import TemplateView, View
from django.http import HttpResponse
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
from wakeonlan import wol
from os import system
from message_system import msg
import requests
import json
import psutil
from . import models

# Index page
class DashboardIndex(TemplateView):
    template_name = "dashboard/index.html"
    
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret["disk_used"] = int(psutil.disk_usage("/").used / 1024 / 1024)
        ret["disk_free"] = int(psutil.disk_usage("/").free / 1024 / 1024)
        try:
            ret["ext_ip"] = requests.get("http://ipecho.net/plain", timeout=2).text
        except:
            ret["ext_ip"] = "127.0.0.1"
        return ret


# RAM
class IndexJsonRam(View):
    def get(self, *args, **kwargs):
        jsonData = {}
        used_ram = round((psutil.virtual_memory().total - psutil.virtual_memory().free) / 1024 / 1024, 1)
        free_ram = round(psutil.virtual_memory().available / 1024 / 1024, 1)
        jsonData['used_ram'] = used_ram
        jsonData['free_ram'] = free_ram
        return HttpResponse(json.dumps(jsonData))


# Temp
class IndexJsonTemp(View):
    def get(self, *args, **kwargs):
        jsonData = {}
        temp = Popen('vcgencmd measure_temp', shell=True, stdin=PIPE, stdout=PIPE).stdout.read().decode('utf-8')[5:9]
        jsonData['temp'] = temp
        jsonData['time'] = datetime.now().strftime("%H:%M:%S")
        return HttpResponse(json.dumps(jsonData))


# Uptime
class IndexJsonUptime(View):
    # Uptime
    def get(self, *args, **kwargs):
        jsonData = {}
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
        jsonData['uptime'] = uptime_string
        return HttpResponse(json.dumps(jsonData))


# Disk
class IndexJsonDisk(View):
    # Disk usage
    def get(self, *args, **kwargs):
        jsonData = {}
        jsonData["disk_used"] = int(psutil.disk_usage("/").used / 1024 / 1024)
        jsonData["disk_free"] = int(psutil.disk_usage("/").free / 1024 / 1024)
        return HttpResponse(json.dumps(jsonData))


# Ext ip
class IndexJsonExtIp(View):
    def get(self, *args, **kwargs):
        jsonData = {}
        try:
            jsonData["ext_ip"] = requests.get("http://ipecho.net/plain", timeout=2).text
        except:
            jsonData["ext_ip"] = "127.0.0.1"
        return HttpResponse(json.dumps(jsonData))


# Price scrapper
class PriceScrapper(TemplateView):
    template_name = "dashboard/price_scrapper.html"

    def get_context_data(self, **kwargs):

        # Create list of dictionarys with all data
        list_output = []
        positions = models.PricePosition.objects.all()
        for i in positions:
            output = {}
            list_price = []
            list_date = []
            output["id"] = i.id
            output["name"] = i.name
            output["url"] = i.url
            pr_pr = models.PricePrice.objects.filter(name_id=i.id).order_by('date')
            for t in pr_pr:
                list_price.append(t.price)
                list_date.append(t.date.strftime("%Y-%m-%d %H:%M"))
            output["price"] = list_price
            output["date"] = list_date
            output["in_stock"] = pr_pr.last().in_stock
            list_output.append(output)
            del output
            del list_date
            del list_price


        if 'view' not in kwargs:
            kwargs["view"] = self
            kwargs["positions"] = list_output
        return kwargs


# Home PC
class HomePCPage(TemplateView):
    template_name = "dashboard/home_pc.html"


class HomePCPowerOn(View):
    def get(self, *args, **kwargs):
        wol.send_magic_packet('E0-3F-49-16-37-BB')
        return HttpResponse("")


class HomePCPowerOff(View):
    def get(self, *args, **kwargs):
        try:
            msg.send_message("powerpcoff")
        except:
            pass
        return HttpResponse("")


class HomePCPing(View):
    def get(self, *args, **kwargs):
        ping = system("ping -c 1 192.168.1.4")
        if ping == 0:
            return HttpResponse("on")
        else:    
            return HttpResponse("off")


class Journals(TemplateView):
    template_name = "dashboard/journals.html"

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        log_botpi = models.LogBotPi.objects.all().order_by('-id').[:20]  # Последние 20 записей. Последние сверху.
        kwargs["log_botpi"] = log_botpi
        return kwargs


# Test page
class TestPage(TemplateView):
    template_name = "dashboard/for_test.html"
