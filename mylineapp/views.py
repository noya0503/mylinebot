from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage

from datetime import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def index(request):
    return HttpResponse("阿母,我成功了~~!")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:

            # 若有訊息事件
            if isinstance(event, MessageEvent):

                currentDateAndTime = datetime.now()
                currentTime = currentDateAndTime.strftime("%H:%M:%S")

                txtmsg = "您所傳的訊是:\n"
                txtmsg += currentTime + "\n"
                txtmsg += event.message.text

                # 回傳收到的文字訊息
                line_bot_api.reply_message(
                    event.reply_token,
                    [TextSendMessage( text = txtmsg ),
                    StickerSendMessage(package_id=11537, sticker_id=52002735),
                    ImageSendMessage(original_content_url='https://c.files.bbci.co.uk/9922/live/9164f0d0-7bea-11ef-990e-5fdb59c2c48e.jpg',preview_image_url='https://c.files.bbci.co.uk/9922/live/9164f0d0-7bea-11ef-990e-5fdb59c2c48e.jpg'),
                    LocationSendMessage(title='Wenzao',address='Kaohsiung',latitude=22.994821,longitude=120.196452)
                    ])



        return HttpResponse()
    else:
        return HttpResponseBadRequest()