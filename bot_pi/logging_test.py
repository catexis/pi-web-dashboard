# -*- coding: utf-8 -*-
import sys, os
import django

sys.path.append(os.path.join(sys.path[0], ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi_web.settings")
django.setup()

from dashboard import models

# log_string = models.LogBotPi.objects.create(history = 'Hello World!')
# log_string.save()

print(
    models.LogBotPi.objects.all().first().time_stamp.strftime("%Y-%m-%d %H:%M"),
    models.LogBotPi.objects.all().first().history
)

