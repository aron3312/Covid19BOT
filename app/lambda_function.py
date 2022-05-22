import json
import boto3
from datetime import datetime, timedelta
from heapq import *
from boto3.dynamodb.conditions import Key
from get_data import parse_address, get_top_k_data, cal_speed, parse_location_message
from calculate import cal_distance
from ResponseGenerator import *
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage, ImageSendMessage,
    TemplateSendMessage, ButtonsTemplate,
    ImageCarouselTemplate, ImageCarouselTemplate, URIAction, PostbackAction, PostbackTemplateAction, MessageAction, ImageCarouselColumn
)
import os

# Initial

client = boto3.resource('dynamodb')
tb = client.Table('quick_sieve')
user_rec = client.Table('user_record')
tz = timedelta(hours=8)
line_bot_api = LineBotApi(os.environ['Channel_access_token'])
handler = WebhookHandler(os.environ['Channel_secret'])


def lambda_handler(event, context):
    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        split_text = event.message.text.split(' ')
        if event.message.text == "使用教學":
            messages = teach_message
        elif event.message.text == "相關資訊":
            res_text = "可以參考備註上藥局資訊，若有發放號碼牌，則必須注意發放時間，剩餘數量有可能已被預約；另外若近期賣出數量為0，則有可能剩餘數量為保留或是其他狀況"
            messages = [TextSendMessage(text=res_text)]
        elif event.message.text == "我快篩陽性":
            messages = [sick_buttons_template_message]
        elif event.message.text == "其他相關資訊":
            res_text = """臺北市其他防疫資訊：\nhttps://www.gov.taipei/covid19/Default.aspx\n新北市其他防疫資訊：\nhttps://www.health.ntpc.gov.tw/\n新冠確診使用者旅程地圖：\nhttps://nova-jumbo-a96.notion.site/3c934b7a75a2447d8f8fadb5bde63c42?fbclid=IwAR3NHzc7RQjorBov83nFXgk2wGW4egPmFKCDeE9S26tW_Oef9vRHk_vN9Y4"""
            messages = [TextSendMessage(text=res_text)]
        elif split_text[0] == '處理狀況':
            status = split_text[1]
            city = split_text[2] if len(split_text) > 2 else None
            sick = split_text[3] if len(split_text) > 3 else None
            messages = generate_act_message(status, city, sick)
        elif split_text[0] == '快篩陽性':
            if len(split_text) == 2:
                city = event.message.text.split(' ')[1]
                messages = generate_carousel(city)
            elif len(split_text) == 3:
                city = event.message.text.split(' ')[1]
                sick = event.message.text.split(' ')[2]
                messages = generate_final_carousel(city, sick)

        line_bot_api.reply_message(
            event.reply_token, messages
        )

    @handler.add(MessageEvent, message=LocationMessage)
    def handle_message(event):
        h = []
        record, address, lon1, lat1 = parse_location_message(event)
        user_rec.put_item(Item=record)
        site1 = (lon1, lat1)
        city, area = parse_address(address)
        response = tb.query(IndexName='city-index', KeyConditionExpression=
        Key('city').eq(city))
        for r in response['Items']:
            site2 = (float(r['經度']), float(r['緯度']))
            cal_num = cal_distance(site1, site2)
            last_time = r['last_time'] if 'last_time' in r else ''
            last_num = r['last_num'] if 'last_num' in r else r['快篩試劑截至目前結餘存貨數量']
            heappush(h, (cal_num, r['醫事機構名稱'], r['醫事機構地址'], r['快篩試劑截至目前結餘存貨數量'],
                         r['經度'], r['緯度'], r['醫事機構電話'], r['備註'], r['來源資料時間'], last_time, last_num))
        answer = get_top_k_data(h)
        if not answer:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="目前所查詢區域藥局皆沒有快篩試劑存貨，請隔一段時間再做查詢")

            )
        else:
            line_bot_api.reply_message(
                event.reply_token, answer

            )

    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
        }
    return {
        'statusCode': 200,
        'body': json.dumps("Success")
    }