from django.db import models

class PricePosition(models.Model):
    name = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=500)

    class Meta:
        ordering = ["name"]
        db_table = "price_position"


class PricePrice(models.Model):
    name = models.ForeignKey("PricePosition", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField(blank=True, default=0.0)
    in_stock = models.BooleanField(default=False)

    class Meta:
        ordering = ["date"]
        db_table = "price_price"


class LogBotPi(models.Model):
    time_stamp = models.DateTimeField(auto_now=True)
    history = models.TextField(blank = True)

    class Meta:
        ordering = ["time_stamp"]
        db_table = "log_botpi"
