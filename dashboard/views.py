from django.views.generic import TemplateView, View
from django.http import HttpResponse
from subprocess import Popen, PIPE
import json
import psutil

# Index page
class DashboardIndex(TemplateView):
    template_name = "dashboard/index.html"


# Index page refresh data as JSON
# RAM, temp
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
