import telepot
import time
from urllib.request import urlopen
import xmlProcessing
import GUI
import html5lib


Bot = telepot.Bot('1192566935:AAFRz0OjIbrHRMeeye1cij104HEI8892N0Q')
MyChatID = '1181841750'


class telegramBot:
    def __init__(self):
        self.locationListBox = []
        self.stationListBox = []
        Bot.message_loop(self.handle)

    def handle(self, msg):
        content_type, chat_type, MyChatID = telepot.glance(msg)
        if content_type != 'text':
            Bot.sendMessage(MyChatID, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        searchNumLocation = 0
        searchNumArea = 0
        text = msg['text']
        args = text.split()
        print(len(args))
        if len(args) > 1:
            print('try to 지역: ', args[0])
            print('try to 행정구역: ', args[1])
            # 여기에 지역을 먼저 찾고 인덱스를 받아서 다시 행정구역 찾기.
            isfind = False
            for i in range(len(xmlProcessing.locations)):
                if (args[0] == xmlProcessing.locations[i]):
                    searchNumLocation = i
                    for data in xmlProcessing.chargingStations[i]:
                        if args[1] in data.address:
                            isfind = True
                            Bot.sendMessage(MyChatID, data.address + '\n' + data.stationName + '\n' + data.stationID + '\n' + data.lat+ '\n' +data.lng+ '\n' + data.type+'\n' + data.stat)
            if not isfind :
                Bot.sendMessage(MyChatID, '그런 지역은 존재하지 않아요 ㅠㅠ 다시입력해주세용!')




        else:
            print(text.startswith(str(args[0])))

            print(str(args[0]))
            print('명령오류!')
            Bot.sendMessage(MyChatID, '모르는 명령어입니다.\n 찾고자하는 지역 이름과 행정구역을 입력해주세요. (EX : 서울특별시 종로구)')





print('Listening...')

