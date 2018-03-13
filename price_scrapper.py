# -*- coding: utf-8 -*-
import sys, os, django, logging
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi_web.settings")
django.setup()

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dashboard.models import PricePosition, PricePrice
headers = {'user-agent': 'Mozilla/5.0 (X25; Linux x_4096) AppleWebKit/537.36 (KHTML, like Gecko) Ribin Chromium/91.0.65.110 Chrome/91.0.65.110 Safari/537.36'}

for i in PricePosition.objects.all():
    print(i.name)
    r = requests.get(i.url, headers = headers).text
    soup = BeautifulSoup(r, 'html.parser')
    name = soup.find("h1", class_="producttitle fn").get_text()
    
    price_r = soup.find("font", class_="oldpricebolditalic").get_text()
    price_r = price_r.replace("руб.", "").replace(" ", "")

    in_stock = soup.find("div", class_="statushelp_layer").find('strong').get_text()
    if ("на складе и готов" in in_stock) or ("удет отправлен после" in in_stock):
        in_stock = True
    else:
        in_stock = False
    
    # Save to DB
    new_price = PricePrice(name=i, price=price_r, in_stock=in_stock)
    new_price.save()
    print("Done")