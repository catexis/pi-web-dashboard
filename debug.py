# -*- coding: utf-8 -*-
import sys, os, django, logging
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi_web.settings")
django.setup()
# logging.basicConfig(level=logging.DEBUG)

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dashboard.models import PricePosition, PricePrice

# Для времени
# datetime.now().strftime("%Y-%m-%d %H:%M")

list_output = []
positions = PricePosition.objects.all()
for i in positions:
    output = {}
    list_price = []
    list_date = []
    output["id"] = i.id
    output["name"] = i.name
    pr_pr = PricePrice.objects.filter(name_id=i.id).order_by('date')
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

print(list_output)

print("End")