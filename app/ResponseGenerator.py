from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage, LocationSendMessage, ImageSendMessage,
    TemplateSendMessage, ButtonsTemplate, CarouselTemplate,
    ImageCarouselTemplate, ImageCarouselTemplate, CarouselColumn, URIAction, PostbackAction, PostbackTemplateAction, MessageAction, ImageCarouselColumn
)
image_urls = ["https://drive.google.com/uc?export=view&id=1hVW0Nmw6r8czjTuP5PbXkQGy0K_BKSst",
              "https://drive.google.com/uc?export=view&id=1FoCmTRHuiBoDaQZU7FlAh1ml7XBfv59-",
              "https://drive.google.com/uc?export=view&id=10nUQuJxIdNUC5bLo1ltnxmnpuYmQDalK",
              "https://drive.google.com/uc?export=view&id=1oE8giH-E5yuepe9Xm8x8bRRTvIbUOsiN",
              "https://drive.google.com/uc?export=view&id=1fiIGSTCiToIzf6aSxL-XibbYTv7f6gu6", ]


teach_message = [TemplateSendMessage(
    alt_text='查詢最近藥局販售快篩試劑',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(
                image_url=img,
                action=MessageAction(
                    label='步驟{}'.format(i + 1),
                    text='步驟{}'.format(i + 1)
                )
            )
            for i, img in enumerate(image_urls)]
    )
)]

sick_buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        title='不用緊張，讓我來幫你解釋接下來你需要怎麼做，請先告訴我你居住在哪^_^',
        text='請選擇你所居住的縣市',
        actions=[
            MessageAction(
                label='臺北市',
                text='快篩陽性 臺北市'
            ),
            MessageAction(
                label='新北市',
                text='快篩陽性 新北市'
            ),
            MessageAction(
                label='其他縣市',
                text='快篩陽性 其他縣市'
            )
        ]
    )
)

class SickResponse(object):
    def __init__(self, city):
        self.message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='我判斷完自己屬於哪個病症了，我現在該做什麼？',
                text='選擇自己屬於哪種程度的症狀',
                actions=[
                    MessageAction(
                        label='我的症狀屬於輕症，我該做什麼？',
                        text='快篩陽性 {} 輕症'.format(city)
                    ),
                    MessageAction(
                        label='我的症狀屬於中症，我該做什麼？',
                        text='快篩陽性 {} 中症'.format(city)
                    ),
                    MessageAction(
                        label='我的症狀屬於中重症，我該做什麼？',
                        text='快篩陽性 {} 重症'.format(city)
                    )
                ]
            )
        )


class ActionResponse(object):
    def __init__(self, city, sick):
        self.message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='上面處理流程，可以參考下面詳細資訊',
                text='選擇有問題的部分做進一步了解',
                actions=[
                    MessageAction(
                        label='1922打不通怎麼辦?',
                        text='處理狀況 1922打不通'
                    ),
                    MessageAction(
                        label='我需要做PCR怎麼辦?',
                        text='處理狀況 PCR篩檢 {} {}'.format(city, sick)
                    ),
                    MessageAction(
                        label='我身體不適怎麼辦?',
                        text='處理狀況 身體不適'
                    ),
                    MessageAction(
                        label='我需要視訊看診怎麼辦?',
                        text='處理狀況 視訊看診'
                    )
                ]
            )
        )


def generate_carousel(city):
    check_sick_text = """可以先透過以下，確認自己是否有較為嚴重的症狀：\n（一）輕症：流鼻水、打噴嚏
喉嚨痛／癢、乾咳、聲音啞、頭痛、全身肌肉酸痛、疲憊、食慾不振、噁心、拉肚子\n（二）中症：呼吸急促、血氧下降、嚴重脫水、劇烈頭痛\n（三）重症：呼吸困難、嘴唇發紫、皮膚冰冷
昏迷不醒、昏倒、胸痛\n針對輕症，及中重症的處理方式會略有不同，請等等按照這個分類去選擇屬於哪個症狀病徵（請注意隨時觀測自己身體狀況，隨時可能從輕－中－重）"""
    messages = [TextSendMessage(text=check_sick_text)]
    if city == "臺北市":
        buttons_template = SickResponse(city)
        messages.append(buttons_template.message)
    elif city == "新北市":
        buttons_template = SickResponse(city)
        messages.append(buttons_template.message)
    else:
        buttons_template = SickResponse(city)
        messages.append(buttons_template.message)
    return messages

def generate_final_carousel(city, sick):
    if sick == "輕症":
        check_sick_text = """您好。目前您的症狀為輕症，請您持續監測自己身體狀況。\n首先要做的事情是可以上網進行社區、醫院門診PCR篩檢的預約，不一定要預約當日，也可以預約1-2日後。\n輕症部分可以使用成藥(普拿疼、露露等等)先緩解症狀，若家裡沒有成藥，也可以使用視訊看診先看診，再透過郵寄或請人代領去領取應及感冒藥物。\n當務之急是監測身體狀況、減緩當下症狀並且多休息，詳情可以參考以下："""
    else:
        check_sick_text = """您好。目前您的症狀為中重症，若有符合中重症的情況一項，請先不用過於擔心，建議前往防疫急門診進行就醫及篩檢。另外提供以下狀況供詢問："""
    messages = [TextSendMessage(text=check_sick_text)]
    if city == "臺北市":
        buttons_template = ActionResponse(city, sick)
        messages.append(buttons_template.message)
    elif city == "新北市":
        buttons_template = ActionResponse(city, sick)
        messages.append(buttons_template.message)
    else:
        buttons_template = ActionResponse(city, sick)
        messages.append(buttons_template.message)
    return messages


def generate_act_message(status, city=None, sick=None):
    messages = []
    if not city:
        if status == "1922打不通":
            text_message = TextSendMessage(text="若1922打不通，可以先針對你目前的狀況做處理，不需要先回報狀況，等到您篩檢過後，政府自然就會掌握到您確診訊息囉。\n可以先進行網路預約PCR、現場PCR，或是針對你的症狀先進行吃藥、視訊看診、休息相關措施。")
            messages.append(text_message)
        elif status == "視訊看診":
            text_message = TextSendMessage(text="若需要視訊看診，目前主要有兩種方式：\n（一）地區配合的醫療院所\n（二）健康益友APP\n另外「健保快易通」APP可以先準備，裡面可以進行虛擬健保卡註冊以及視訊院所查詢。\n簡單講一下視訊看診主要是為了應急的看診及拿藥，另外健康益友APP以及醫院會提供視訊陽性門診，可以透過視訊判斷陽性及給藥，除此之外就是一般的就醫改成視訊進行\n這邊提供您小建議，若想要拿急用的感冒藥或是看診，也可以考慮致電給附近的診所，詢問他是否可以視訊約診，後面再請人拿健保卡去拿藥即可\n除此之外正規流程可以參考這個頁面：https://www.cool3c.com/article/177445")
            messages.append(text_message)
        elif status == "身體不適":
            text_message = TextSendMessage(text="""根據台北市防役專區：\n1. 大部分的 COVID-19 感染者症狀輕微，休養後即可自行康復，在居家照護期間，請補充水分、盡量臥床休息，並務必觀察自身症狀變化。\n2. 若您出現以下症狀時，請立即撥打 119 就醫或同住親友接送：喘、呼吸困難、持續胸痛、胸悶、意識不清、皮膚或嘴唇或指甲床發青、無法進食、喝水或服藥、過去24小時無尿或尿量顯著減少。""")
            messages.append(text_message)
        elif status == "解隔陽性":
            text_message = TextSendMessage(text="""根據指揮中心，經過七天隔離期滿不需要再進行快篩即可進入自主健康管理期間，解隔快篩陽性有可能為病毒屍體，且根據研究七天已幾乎無傳染力，但仍須自主健康管理期滿才能進行聚會，或是出入人口密集處""")
            messages.append(text_message)
    else:
        if status == "PCR篩檢":
            if city == "臺北市":
                if sick == "輕症":
                    res_text = """若您目前屬於輕症，想要預約PCR篩檢，可以優先考慮社區篩檢站。\n先進行網路預約，預約後再按時間去報到即可快速完成報到－篩檢－拿藥的手續：https://www.gov.taipei/covid19/News_Content.aspx?n=C2C9BA05AD4D1B1D&sms=B405E8ADC0D1FCB0&s=82B4763758735B4D\n若您為輕症，可以考慮預約當日或是隔一兩日去做都是可以的。\n另外也可以參考防疫急門診的掛號：https://www.gov.taipei/covid19/News_Content.aspx?n=47A5CA9705AD88D4&sms=38F5DB05507DAAB2&s=FD423C00E58331FD"""
                else:
                    res_text = """若您目前屬於中/重症，想要預約PCR篩檢，可以優先考慮防疫急門診，能夠有醫生進行問診（若為重症則可以直接考慮119急診就醫）\n防疫急門診的掛號：https://www.gov.taipei/covid19/News_Content.aspx?n=47A5CA9705AD88D4&sms=38F5DB05507DAAB2&s=FD423C00E58331FD\n"""
            elif city == "新北市":
                if sick == "輕症":
                    res_text = """若您目前屬於輕症，想要預約PCR篩檢，可以優先考慮社區篩檢站。\n先進行網路預約，預約後再按時間去報到即可快速完成報到－篩檢－拿藥的手續：https://www.health.ntpc.gov.tw/basic/?mode=detail&node=8650\n若您為輕症，可以考慮預約當日或是隔一兩日去做都是可以的。\n另外也可以參考防疫急門診的掛號：https://www.health.ntpc.gov.tw/basic/?mode=detail&node=9828"""
                else:
                    res_text = """若您目前屬於中/重症，想要預約PCR篩檢，可以優先考慮防疫急門診，能夠有醫生進行問診（若為重症則可以直接考慮119急診就醫）\n防疫急門診的掛號：https://www.health.ntpc.gov.tw/basic/?mode=detail&node=9828\n"""
            else:
                pass
            reserve_message = TextSendMessage(text=res_text)
            messages.append(reserve_message)
            res_text = """＊PCR若當日沒有空，可以預約一日或兩日後，可以先專注在身體、症狀的關注及改善\n＊網路預約可以定期重新整理，有時候會有人取消的就會有空檔\n＊若真的非常需要篩檢，也可排當場篩檢，但耗時會比較久，建議身體沒有不適再去排隊\n＊若目標為拿藥可以先透過附近診所視訊看診再請人或郵寄藥，先緩解症狀"""
            cant_message = TextSendMessage(text=res_text)
            messages.append(cant_message)
    return messages