import requests
import re
from heapq import *
from datetime import datetime
from address import area_data
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage
)


def parse_address(address):
    """
    Parse city and area from the whole address.
    :param address: <str> Chinese address
    :return:
    city: <str>縣市
    area: <str> 區/鎮
    """
    mt = re.search('台.(縣|市)', address)
    address = list(address)
    if mt:
        address[mt.start()] = '臺'
    address = ''.join(address)
    city_f = re.search('|'.join(list(area_data.keys())), address)
    city = city_f.group(0) if city_f else ''
    area_f = re.search('|'.join(area_data[city]), address) if city else ''
    area = area_f.group(0) if area_f else ''
    return (city, area)


def get_top_k_data(h):
    """
    Get top-2 nearest sites. Because the limitation of list of messages is 5, so we will choose top 2 site with location and text messages.
    :param h: <heap queue>
    :return: <list> [<Line Message>]
    """
    answer = []
    while h and len(answer) < 4:
        result = heappop(h)
        while h and not result[3]:
            result = heappop(h)
        if not result[3]:
            break
        cost, speed = cal_speed(result[10], result[3], result[9], result[8])
        res_text = "最近賣出數量: {} 速率: {}劑/分鐘 醫事場所電話: {} 醫事場所相關注意事項: {} 更新時間: {}".format(cost, speed, result[6], result[7],
                                                                                     result[8])
        loc_message = LocationSendMessage(
            title="{} 剩餘:{} 距離:{} km".format(result[1], result[3], round(result[0], 2)),
            address=result[2],
            latitude=result[5],
            longitude=result[4]
        )
        answer.append(loc_message)
        text_message = TextSendMessage(text=res_text)
        answer.append(text_message)
    return answer


def cal_speed(last, now, last_time, now_time):
    """
    Calculate selling speed of quick sieve.
    :param last: <int> the count at the previous point in time
    :param now: <int> the count at the current point in time
    :param last_time: <datetime> The previous point in time
    :param now_time: <datetime> The current point in time
    :return:
    cost: <int> The count of sold quick sieves.
    speed: <float> The speed of selling quick sieves.
    """
    if last_time == now_time:
        return None
    if last == now:
        return (0, 0)
    cost = int(last) - int(now)
    time_format = "%Y/%m/%d %H:%M:%S"
    last_time = datetime.strptime(last_time, time_format)
    now_time = datetime.strptime(now_time, time_format)
    seq = (now_time - last_time).seconds / 60
    speed = round(cost / seq, 2)
    return (cost, speed)


def parse_location_message(event):
    """
    Parse Line Location Message.
    :param event:
    :return:
    """
    record = {}
    line_id = event.source.user_id
    now = datetime.timestamp(datetime.now())
    address = event.message.address
    lon1 = event.message.longitude
    lat1 = event.message.latitude
    record["line_id"] = line_id
    record["record_time"] = int(now)
    record["address"] = address
    record["lon"] = str(lon1)
    record["lat"] = str(lat1)
    return record, address, lon1, lat1

