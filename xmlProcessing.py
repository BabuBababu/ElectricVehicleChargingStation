from xml.dom.minidom import parseString
import urllib.request
from xml.etree import ElementTree
import spam
import copy

locations = ['서울특별시', '인천광역시', '대전광역시', '대구광역시', '울산광역시', '부산광역시', '광주광역시', '세종특별자치시',
             '경기도', '강원도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']

AdmArea = {0:['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구', '노원구', '은평구',
                '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구', '관악구', '서초구', '강남구', '송파구', '강동구'],
           1:['중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구','강화군','옹진군'],
           2:['동구','중구','서구','유성구','대덕구'],
           3:['북구','동구','중구','서구','달서구','수성구','남구','달성군'],
           4:['울주군','중구','북구','남구','동구'],
           5:['중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군'],
           6:['광산구','북구','서구','동구','남구'],
           7:['세종특별자치시'],
           8:['수원시','고양시','용인시','성남시','화성시','부천시','남양주시','안산시','안양시','평택시','시흥시','파주시','의정부시','김포시','광주시',
              '광명시','하남시','군포시','오산시','양주시','이천시','구리시','안성시','의왕시','포천시','양평군','여주시','동두천시','가평군','과천시','연천군'],
           9:['원주시','춘천시','강릉시','동해시','속초시','삼척시','태백시','홍천군','철원군','횡성군','평창군','정선군','영월군','인제군','고성군','양양군','화천군','양구군'],
           10:['청주시','충주시','제천시','보은군','옥천군','영동군','증평군','진천군','괴산군','음성군','단양군'],
           11:['천안시','공주시','보령시','아산시','서산시','논산시','계룡시','당진시','금산군','부여군','서천군','청양군','홍성군','예산군','태안군'],
           12:['전주시','익산시','군산시','정읍시','김제시','남원시','완주군','고창군','부안군','임실군','순창군','진안군','무주군','장수군'],
           13:['목포시','여수시','순천시','나주시','광양시','담양군','곡성군','구례군','고흥군','보성군','화순군','장흥군','강진군','해남군','영암군','무암군','함평군',
               '영광군','장성군','완도군','진도군','신안군'],
           14:['포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','군위군','의성군','청송군','영양군','영덕군','청도군','고령군'
               ,'성주군','칠곡군','예천군','봉화군','울진군','울릉군'],
           15:['창원시','김해시','진주시','양산시','거제시','통영시','사천시','밀양시','함안군','거창군','창녕군','고성군','하동군','합천군','남해군','함양군','산청군',
               '의령군'],
           16:['제주시','서귀포시']}

chargingStations = [set() for i in range(len(locations))]


class Data:
    def __init__(self, address, stationID, stationName, lat, lng, type, stat):
        self.address = address
        self.stationID = stationID
        self.stationName = stationName
        self.lat = lat
        self.lng = lng
        if type == "01":
            self.type = "DC Chademo"
        elif type == "03":
            self.type = "DC Chademo +AC 3상"
        elif type == "06":
            self.type = "DC 차데모+AC 3상+ DC콤보"
        else:
            self.type = "확인 불가능"
        # 충전기 타입
        # (01:DC 차데모,
        # 03: DC 차데모+AC 3상,
        # 06: DC 차데모+AC 3상
        # +DC 콤보)
        if stat == "1":
            self.stat = "통신이상"
        elif stat == "2":
            self.stat = "충전대기"
        elif stat == "3":
            self.stat = "충전중"
        elif stat == "4":
            self.stat = "운영중지"
        elif stat == "5":
            self.stat = "점검중"
        else:
            self.stat = "확인불가능"
        # 충전기
        # 1. 통신이상
        # 2. 충전대기
        # 3. 충전중
        # 4. 운영중지
        # 5. 점검중

    def printData(self):
        print("지역:{0}\t충전소 이름:{1},\t충전소 ID:{2}\t경도:{3}\t위도:{4}\t사용가능시간:{5}".format(self.address, self.stationName,
                                                                                   self.stationID,
                                                                                   self.lng, self.lat, self.useTime))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.address == other.address and self.stationID == other.stationID and self.stationName == other.stationName

    def __hash__(self):
        return hash((self.address, self.stationID, self.stationName))

    # 위 두 함수는 셋에서 중복제거에 필요한 정보를 제공해줍니다.


xmlDocument = None

url = "http://open.ev.or.kr:8080/openapi/services/rest/EvChargerService?serviceKey=s%2F5nW%2BMXFPVjfdX5Mg0Z4Uo3OOmT0coY0%2BqBfxFYBQjNX%2FoVB0AmdMf1HOwQjTTybjApkg6F3V0vzqIzomndFQ%3D%3D"


def createXmlDoc():
    global xmlDocument
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    responseBody = resp.read()
    xmlDocument = parseString(responseBody.decode('utf-8'))


def parseStationInfo():
    global xmlDocument
    tree = ElementTree.fromstring(xmlDocument.toxml())
    items = tree.getiterator("item")
    index = 99999
    for item in items:
        address = item.find("addrDoro")
        for i in range(len(chargingStations)):
            if locations[i] in address.text:
                index = i
                break

        stationID = item.find("statId")  # 셋에 집어넣는 이유는 중복된 데이터가 다수 존재하기 때문입니다.
        stationName = item.find("statNm")  # 충전기 타입과 충전기상태는 제외했지만 언제든지 추가 가능합니다.
        lat = item.find("lat")  # chgerType: 충전기타입, stat: 충전기 상태
        lng = item.find("lng")
        useTime = item.find("useTime")
        chgerType = item.find("chgerType")
        stat = item.find("stat")
        chargingStations[index].add(
            Data(address.text, stationID.text, stationName.text, lng.text, lat.text,
                 chgerType.text, stat.text))

    print("XML Load complete")


def printSeoulData():
    for i in chargingStations[0]:
        i.printData()


def sortChargingStations():
    for i in range(len(chargingStations)):
        chargingStations[i] = list(chargingStations[i])
    for i in range(len(chargingStations)):
        temp = spam.sortByName(chargingStations[i], len(chargingStations[i]))
        chargingStations[i] = copy.deepcopy(temp)


def deleteDoc():
    global xmlDocument
    del xmlDocument
