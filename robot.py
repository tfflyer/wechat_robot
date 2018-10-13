import itchat
from itchat.content import *
import time
import re
import threading

#自动回复开关
SWITCH_REPLY=True
#延迟回复开关
SWITCH_DELAY=False
#延迟时间
DELAY_TIME=150
#消息前缀开关
SWITCH_PREFIX=True
#消息前缀内容
PREFIX_CONTENT="[来自tfflyerのJarvis的自动回复]"
#回复内容字典
REPLY_DICT={}
#延迟回复字典
DELAY_REPLY_DICT={}

Ad_replyed=['a']
# 已回复人员列表

@itchat.msg_register([TEXT,PICTURE,RECORDING],isGroupChat=False)

# itchat装饰器

def auto_reply(msg):
    global SWITCH_REPLY
    global SWITCH_DELAY
    global DELAY_TIME
    global SWITCH_PREFIX
    global PREFIX_CONTENT
    global REPLY_DICT
    global DELAY_REPLY_DICT
    global Ad_replyed
    global nkname

    if msg['ToUserName']=='filehelper':
        args=re.compile(' ').split(msg['Text'])
        try:
            if args[0]=='/help':
                reply_content='''
                【功能列表】
                1./help             显示功能列表
                2./switch on        打开自动回复
                3./switch off       关闭自动回复
                4./prefix on        打开消息前缀
                5./prefix off       关闭消息前缀
                6./prefix set [T]   设置前缀内容
                7./delay on         打开延迟回复
                8./delay off        关闭延时回复
                9./delay set [T]    设置延迟时间
                10./dict set [F] [T] 定制好友回复
                11./dict show [F]    显示好友回复
                '''

            elif args[0]=='/switch':
                if args[1]=='on':
                    SWITCH_REPLY=True
                    reply_content="【Jarvis】自动回复已开启"

                elif args[1]=='off':
                    SWITCH_REPLY=False
                    reply_content="【Jarvis】自动回复已关闭"

                else:
                    reply_content="【Jarvis】未知指令"

            elif args[0]=='/prefix':
                if args[1]=='on':
                    SWITCH_PREFIX=True
                    reply_content = "【Jarvis】回复前缀已开启"

                elif args[1]=='off':
                    SWITCH_PREFIX=False
                    reply_content="【Jarvis】回复前缀已关闭"

                elif args[1]=='set':
                    PREFIX_CONTENT="["+args[2]+"]"
                    reply_content = "【Jarvis】回复前缀已设置为："+PREFIX_CONTENT

                else:
                    reply_content = "【Jarvis】未知指令"

            elif args[0]=='/delay':
                if args[1]=='on':
                    SWITCH_DELAY=True
                    reply_content="【Jarvis】延迟回复已开启"

                elif args[1]=='off':
                    reply_content="【Jarvis】延迟回复已关闭"

                elif args[1]=='set':
                    DELAY_TIME=args[2]
                    reply_content="【Jarvis】延迟时间被设置为："+DELAY_TIME

                else:
                    reply_content = "【Jarvis】未知指令"

            elif args[0]=='/dict':
                if args[1]=='show':
                    if REPLY_DICT.__contains__(args[2]):
                        reply_content="【Jarvis】好友["+args[2]+"]的自动回复为："+REPLY_DICT[args[2]]
                    else:
                        reply_content="【Jarvis】好友["+args[2]+"]的自动回复暂未设置"

                elif args[1]=='set':
                    REPLY_DICT[args[2]]=args[3]
                    reply_content="【Jarvis】好友["+args[2]+"的自动回复已设置为："+REPLY_DICT[args[2]]
                else:
                    reply_content = "【Jarvis】未知指令"
            else:
                reply_content = "【Jarvis】未知指令"


        except:
            reply_content="【Jarvis】系统异常"
            itchat.send(reply_content, toUserName='filehelper')
            raise

        itchat.send(reply_content, toUserName='filehelper')


    else:
        #获取发送消息的朋友的信息
        target_friend=itchat.search_friends(userName = msg['FromUserName'])
        if target_friend:
            #获取ta的昵称
            nickName=target_friend['NickName']
            nkname=str(nickName)


            if not any(str(nickName) in s for s in Ad_replyed):
                if not REPLY_DICT.__contains__(nickName):
                #设置默认回复
                    REPLY_DICT[nickName]="抱歉，腾飞暂时未看到您的消息，不能及时回复，如有急事，请电话联系TEL：13126883674(•ω•`)"

                reply_content=REPLY_DICT[nickName]
                #判断自动回复开关
                if SWITCH_REPLY:
                #判断延时回复开关
                    if SWITCH_DELAY:
                        localtime = time.time()
                        DELAY_REPLY_DICT[nickName]=[localtime,msg['FromUserName']]
                        print (DELAY_REPLY_DICT)

                    if not SWITCH_DELAY:
                        #判断消息前缀开关
                        if SWITCH_PREFIX:
                            reply_content = PREFIX_CONTENT + REPLY_DICT[nickName]
                        else:
                            reply_content = REPLY_DICT[nickName]
                        #发送消息
                        itchat.send(reply_content, toUserName=msg['FromUserName'])
                        Ad_replyed.append(str(nickName))



def delay_reply():
    print("开始执行")
    global DELAY_REPLY_DICT
    global PREFIX_CONTENT
    global Ad_replyed
    global nkname

    if not any(str(nkname) in s for s in Ad_replyed):
        if SWITCH_DELAY:
            while len(DELAY_REPLY_DICT)>0:
                localtime = time.time()
            # print (localtime)
            # print (DELAY_REPLY_DICT[item][0])
            # print (int(DELAY_TIME))
                for item in list(DELAY_REPLY_DICT.keys()):
                    if SWITCH_REPLY:
                        reply_content = PREFIX_CONTENT  + "," + str(round(int(DELAY_TIME) / 60, 1)) + "分钟过去了，" + REPLY_DICT[item]
                        itchat.send(reply_content, toUserName=DELAY_REPLY_DICT[item][1])
                        Ad_replyed.append(str(nkname))
                        print ("发送消息")
                del DELAY_REPLY_DICT[item]
                print (DELAY_REPLY_DICT)

    global timer1
    timer1=threading.Timer(DELAY_TIME,delay_reply)
    timer1.start()

def keep_alive():
    text="保持登录"
    itchat.send(text, toUserName="filehelper")
    global timer2
    global Ad_replyed
    Ad_replyed=['a']
    timer2 = threading.Timer(60*60,keep_alive)
    timer2.start()

if __name__ == '__main__':
    timer1 = threading.Timer(DELAY_TIME, delay_reply)
    timer1.start()
    timer2=threading.Timer(60*60,keep_alive)
    timer2.start()

    itchat.auto_login()
    itchat.run()
    # schedule=sched.scheduler(time.time,time.sleep)
    # schedule.enter(60,0,delay_reply())
    # schedule.run()







