from django.views.generic import TemplateView, View
from django.http import HttpResponse
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
import requests
import json
import psutil

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


# Test page
class TestPage(TemplateView):
    template_name = "dashboard/for_test.html"
