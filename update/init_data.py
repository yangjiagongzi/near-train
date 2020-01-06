from plan.models import Station, Train, FromStation, ToStation
from urllib.request import urlretrieve
import os
import re

station_name_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
train_list_url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js?scriptVersion=1.0'


def download_callback(a, b, c):
    per = 100.0*a*b/c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def readPart(filePath, size=1024, encoding="utf-8"):
    with open(filePath, "r", encoding=encoding) as f:
        while True:
            part = f.read(size)
            if part:
                yield part
            else:
                return None


def init_stations():
    dir = os.path.abspath('./tmp')
    station_name_data_path = os.path.join(dir, 'station-name.txt')
    urlretrieve(station_name_url, station_name_data_path, download_callback)

    Station.objects.all().delete()

    stationlist = []
    strTmp = ''

    for part in readPart(station_name_data_path):
        dataList = []
        station_split = re.sub(
            r"(\s*var\s*station_names\s*=\s*')|(';)|(\s*)", "", strTmp + part).split('@')

        num = 0
        while num < len(station_split):
            if num == len(station_split) - 1:
                strTmp = station_split[num]
            elif len(station_split[num]) != 0 and not station_split[num].isspace():
                dataList.append(station_split[num])
            num += 1

        obj_list = []
        for data in dataList:
            station_data = data.split('|')
            if station_data[1] not in stationlist:
                stationlist.append(station_data[1])
                obj_list.append(Station(
                    station_name=station_data[1],
                    station_telecode=station_data[2],
                    station_abbr=station_data[0],
                    station_no=station_data[5],
                    ch_pinyin=station_data[3],
                    simp_pinyin=station_data[4],
                    origin_info=data
                ))
        Station.objects.bulk_create(obj_list)

    if len(strTmp) != 0 and not strTmp.isspace():
        last_station_data = strTmp.split('|')

        last_data = Station(
            station_name=last_station_data[1],
            station_telecode=last_station_data[2],
            station_abbr=last_station_data[0],
            station_no=last_station_data[5],
            ch_pinyin=last_station_data[3],
            simp_pinyin=last_station_data[4],
            origin_info=strTmp
        )

        last_data.save()


def init_from_stations(stations):
    FromStation.objects.all().delete()
    station_list = Station.objects.filter(station_name__in=stations)
    FromStation.objects.bulk_create(station_list)


def init_to_stations(stations):
    ToStation.objects.all().delete()
    station_list = Station.objects.filter(station_name__in=stations)
    ToStation.objects.bulk_create(station_list)


def init_trains():
    dir = os.path.abspath('./tmp')
    train_list_data_path = os.path.join(dir, 'train-list.txt')
    urlretrieve(train_list_url, train_list_data_path, download_callback)

    Train.objects.all().delete()

    strTmp = ''
    deDup = ''

    from_stations = []
    to_stations = []

    for part in readPart(train_list_data_path, 1024*512):
        dataList = []
        train_split = re.sub(
            r"\}|\{", "@", strTmp + part).split('@')

        num = 0
        while num < len(train_split):
            if num == len(train_split) - 1:
                strTmp = train_split[num]
            elif len(train_split[num]) != 0 and not train_split[num].isspace():
                analysis = re.match(
                    r'^"station_train_code"\:"(\w+)\((.*)-(.*)\)","train_no"\:"(\w+)"$', train_split[num])
                if analysis:
                    train_no = analysis.group(4)
                    if deDup.find(train_no) < 0:

                        train_sn = analysis.group(1)
                        from_station = analysis.group(2)
                        to_station = analysis.group(3)

                        if from_station not in from_stations:
                            from_stations.append(from_station)

                        if to_station not in to_stations:
                            to_stations.append(to_station)

                        deDup = deDup + '|' + train_no
                        dataList.append(Train(
                            station_train_code='{train_sn}({from_station}-{to_station})'.format(train_sn=train_sn,
                                                                                                from_station=from_station, to_station=to_station),
                            train_no=train_no,
                            train_type=re.match(
                                r'^(.*?)(\d+)$', train_sn).group(1),
                            train_sn=train_sn,
                            from_station=from_station,
                            to_station=to_station,
                            between_station='{from_station}-{to_station}'.format(
                                from_station=from_station, to_station=to_station)
                        ))
            num += 1

        if len(dataList):
            Train.objects.bulk_create(dataList)

    init_from_stations(from_stations)
    init_to_stations(to_stations)
