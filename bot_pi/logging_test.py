# -*- coding: utf-8 -*-
import sys, os
import django
import logging
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi_web.settings")
django.setup()
logging.basicConfig(level=logging.DEBUG)