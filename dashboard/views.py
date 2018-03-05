from django.views.generic import TemplateView, View
from django.http import HttpResponse
from subprocess import Popen, PIPE
from datetime import datetime
import json
import psutil

# Index page
class DashboardIndex(TemplateView):
    template_name = "dashboard/index.html"

# Test page
class TestPage(TemplateView):
    template_name = "dashboard/for_test.html"


# Index page refresh data as JSON
class IndexJSONData(View):
    def get(self, *args, **kwargs):
        jsonData = {}

        # Температура
        # temp = Popen('vcgencmd measure_temp', shell=True, stdin=PIPE, stdout=PIPE).stdout.read().decode('utf-8')[5:9]
        # jsonData['temp'] = temp

        # RAM
        used_ram = round(psutil.virtual_memory().used / 1024 / 1024, 1)
        free_ram = round(psutil.virtual_memory().free / 1024 / 1024, 1)
        jsonData['used_ram'] = used_ram
        jsonData['free_ram'] = free_ram

        return HttpResponse(json.dumps(jsonData))

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
