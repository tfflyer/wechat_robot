from twilio.rest import Client
from datetime import datetime
import time

account = "ACa52b7520cc7514d831e13c9502694cd1"
token = "42f21b95e0b53b436b4cf3c8c476d1b9"


def send_mes(to_l, text, tw_mobile='+16602353919'):
    client = Client(account, token)
    try:
        message = client.messages.create(to=to_l,
                                         from_=tw_mobile,
                                         body=text)
        print('message status:', message.status)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    greetings = {'6': '早上好，起床啦！多运动才能减肥', '12': '中午好，上课累了吧，好好吃饭',
                 '15': '下午好，吃个水果吧', '22': '晚上好，该休息了，晚安！'}

    print('Script running')
    while True:
        now = datetime.now()
        print('time', now)
        for key in greetings.keys():
            if now.hour == int(key):
                message = greetings.get(key, 'This is a message from tfflyer ')
                res = send_mes(to='+8613126883674', text=message)
                if res:
                    print('Message send ok at:',
                          datetime.strftime(now, '%Y-%m-%d %H:%M:%S'))
                    time.sleep(60*60)
                else:
                    print('Message send failure')
        time.sleep(5)
