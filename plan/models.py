from django.db import models


class Station(models.Model):
    station_name = models.CharField(max_length=100)
    station_telecode = models.CharField(max_length=100)
    station_abbr = models.CharField(max_length=100)
    station_no = models.IntegerField()
    ch_pinyin = models.CharField(max_length=100)
    simp_pinyin = models.CharField(max_length=100)
    origin_info = models.CharField(max_length=200)


class Train(models.Model):
    station_train_code = models.CharField(max_length=100)
    train_no = models.CharField(max_length=100)
    train_type = models.CharField(max_length=10)
    train_sn = models.CharField(max_length=100)
    from_station = models.CharField(max_length=100)
    to_station = models.CharField(max_length=100)
    between_station = models.CharField(max_length=100)
