from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import xmlProcessing
import smtplib
from email.mime.text import MIMEText
from tkinter import messagebox
import folium
import webbrowser


class GUI:
    def __init__(self):
        self.curSelectedLoc = None
        xmlProcessing.createXmlDoc()
        xmlProcessing.parseStationInfo()
        xmlProcessing.sortChargingStations()
        self.lat = 0
        self.lng = 0
        self.stnName = ""
        self.window = Tk()
        self.window.title("전기자동차 공공충전소 현황")
        self.window.geometry("800x600")
        self.font1 = Font(family="맑은 고딕", size=20, slant="italic")
        self.font2 = Font(family="Arial", size=10)
        self.font3 = Font(family="굴림", size=12)

        Label(self.window, text="전기자동차 공공충전소 현황", font=self.font1).pack()
        self.initButton()
        self.initListBox()
        # self.imgTempMap = Image.open("img/tempMap.png")
        # self.photoTempMap = ImageTk.PhotoImage(self.imgTempMap)
        # Label(self.window, image=self.photoTempMap).place(x=350, y=100)
        # Label(self.window, text="지도", font=self.font3).place(x=550, y=350)

        self.MailIDinBox = StringVar()
        self.eMailEntry = Entry(self.window, textvariable=self.MailIDinBox)
        self.eMailEntry.place(x=10, y=160, width=200)
        Label(self.window, text="메일 주소 입력", font=self.font3).place(x=10, y=180)
        self.window.mainloop()

    def initButton(self):
        self.img1 = Image.open("img/magGlass.png")
        self.photo1 = ImageTk.PhotoImage(self.img1)
        self.img2 = Image.open("img/eye.png")
        self.photo2 = ImageTk.PhotoImage(self.img2)
        self.img3 = Image.open("img/mail.png")
        self.photo3 = ImageTk.PhotoImage(self.img3)
        self.img4 = Image.open('img/map.png')
        self.photo4 = ImageTk.PhotoImage(self.img4)
        self.searchButton = Button(image=self.photo1, command=self.getStationList)
        self.specifiedSearchButton = Button(image=self.photo2, command=self.getSpecificInfo)
        self.sendMailButton = Button(image=self.photo3, command=self.SendMail)
        self.openMapButton = Button(image=self.photo4, command=self.openMap)
        self.searchButton.place(x=10, y=50)
        Label(text="검색").place(x=30, y=130)
        self.specifiedSearchButton.place(x=10 + 64 + 15, y=50)
        Label(text="세부사항 보기").place(x=10 + 64 + 10, y=130)
        self.sendMailButton.place(x=10 + 128 + 35, y=50)
        Label(text="메일 보내기").place(x=10 + 128 + 35, y=130)
        self.openMapButton.place(x=10 + 192 + 55, y=50)
        Label(text='지도 보기').place(x=10 + 192 + 55, y=130)

    def initListBox(self):
        self.frame1 = Frame(self.window)
        self.frame1.place(x=10, y=220)
        self.locationListBox = Listbox(self.frame1, selectmode='extended',
                                       height=7, font=self.font2,
                                       relief='ridge', borderwidth=7)
        self.locationListBox.pack(side="left", fill="y")
        self.scrollbarWithLocList = Scrollbar(self.frame1, orient="vertical")
        self.scrollbarWithLocList.config(command=self.locationListBox.yview)
        self.scrollbarWithLocList.pack(side="right", fill="y")
        self.locationListBox.config(yscrollcommand=self.scrollbarWithLocList.set)

        for i in range(len(xmlProcessing.locations)):
            self.locationListBox.insert(i, xmlProcessing.locations[i])
        Label(self.window, text="지역 리스트", font=self.font3).place(x=40, y=360)

        self.locationListBox.bind('<Double-Button-1>', self.selectingLocation)  # 마우스클릭을 바인드한다.
        # 여기까지 지역 리스트 만드는 코드(서울 ~ 제주도까지 하나씩 집어넣는다.)

        self.frame2 = Frame(self.window)
        self.frame2.place(x=10, y=400)
        self.stationListBox = Listbox(self.frame2, selectmode='extended',
                                      height=7, width=42, font=self.font2,
                                      relief='ridge', borderwidth=7)
        self.stationListBox.pack(side="left", fill="y")

        self.scrollbarWithSpecificList = Scrollbar(self.frame2, orient="vertical")
        self.scrollbarWithSpecificList.config(command=self.stationListBox.yview)
        self.scrollbarWithSpecificList.pack(side="right", fill="y")
        self.stationListBox.config(yscrollcommand=self.scrollbarWithSpecificList.set)
        Label(self.window, text="지역 내 충전소 리스트", font=self.font3).place(x=70, y=550)
        # 여기까지 지역 스테이션 리스트박스 만들기

        self.frame3 = Frame(self.window)
        self.frame3.place(x=350, y=400)
        self.specificInfoList = Listbox(self.frame3, selectmode='extended',
                                        height=7, width=55, font=self.font2,
                                        relief='ridge', borderwidth=7)
        self.specificInfoList.pack(side="left", fill="y")

        self.scrollbarWithSpecificInfoList = Scrollbar(self.frame3, orient="vertical")
        self.scrollbarWithSpecificInfoList.config(command=self.specificInfoList.yview)
        self.scrollbarWithSpecificInfoList.pack(side="right", fill="y")
        self.specificInfoList.config(yscrollcommand=self.scrollbarWithSpecificInfoList.set)
        Label(self.window, text="충전소 세부사항", font=self.font3).place(x=500, y=550)
        # 여기까지 스테이션의 세부사항 리스트.

        self.frame4 = Frame(self.window)
        self.frame4.place(x=200, y=220)
        self.admListBox = Listbox(self.frame4, selectmode='extended',
                                  height=7, font=self.font2,
                                  relief='ridge', borderwidth=7)
        self.admListBox.pack(side="left", fill="y")

        self.scrollbarWithSpecificList = Scrollbar(self.frame4, orient="vertical")
        self.scrollbarWithSpecificList.config(command=self.admListBox.yview)
        self.scrollbarWithSpecificList.pack(side="right", fill="y")
        self.admListBox.config(yscrollcommand=self.scrollbarWithSpecificList.set)
        Label(self.window, text="행정구역 리스트", font=self.font3).place(x=220, y=360)
        # 여기까지 지역 스테이션 리스트박스 만들기

    def getStationList(self):
        # 리스트 박스의 curselection 메소드는 튜플의 형태로 반환함. 즉 첫번째 값에 인덱스 값이 들어있음!
        self.stationListBox.delete(0, 'end')  # 해당 지역을 선택하면 기존의 충전소 정보가 싹 제거된다.
        index = 0
        # self.curSelectedLoc = self.locationListBox.curselection()[0]
        selectedAdmLoc = self.admListBox.curselection()[0]

        for i in xmlProcessing.chargingStations[self.curSelectedLoc]:
            if xmlProcessing.AdmArea[self.curSelectedLoc][selectedAdmLoc] in i.address:#객체 행정구역정보가 내가 선택한 행정구역 정보와 일치하는가
                self.stationListBox.insert(index, i.stationName)  # 그 다음 해당 지역 충전소를 하나씩 리스트박스에 삽입한다.
            index += 1

    def getSpecificInfo(self):
        self.specificInfoList.delete(0, 'end')  # 세부 정보도 마찬가지로 기존의 리스트를 싹 비우고

        stnTuple=self.stationListBox.get(0,self.stationListBox.size()-1)
        for tempObj in xmlProcessing.chargingStations[self.curSelectedLoc]:
            if tempObj.stationName==stnTuple[self.stationListBox.curselection()[0]]:
                self.specificInfoList.insert(0, "주소: " + tempObj.address)
                self.specificInfoList.insert(1, "충전소ID: " + tempObj.stationID)
                self.specificInfoList.insert(2, "충전소 이름: " + tempObj.stationName)
                self.specificInfoList.insert(3, "충전소 경도: " + tempObj.lat)
                self.specificInfoList.insert(4, "충전소 위도: " + tempObj.lng)
                self.specificInfoList.insert(5, "충전기 타입: " + tempObj.type)
                self.specificInfoList.insert(6, "충전소 상태: " + tempObj.stat)
                self.lat = tempObj.lat
                self.lng = tempObj.lng
                self.stnName = tempObj.stationName
                break
        #새로운 코드. 해당 행정구역(은평구, 용산구 같은)의 충전소 리스트에서 내가 선택한 충전소 이름을 가지고 좀 더 큰 행정구역(서울특별시)의
        # 충전소를 뒤지면서 이름이 동일한 충전소가있는지검색.

        #tempObj = tempList[self.stationListBox.curselection()[0]]
        # 정보를 하나씩 삽입한다.
        """self.specificInfoList.insert(0, "주소: " + tempObj.address)
        self.specificInfoList.insert(1, "충전소ID: " + tempObj.stationID)
        self.specificInfoList.insert(2, "충전소 이름: " + tempObj.stationName)
        self.specificInfoList.insert(3, "충전소 경도: " + tempObj.lat)
        self.specificInfoList.insert(4, "충전소 위도: " + tempObj.lng)
        self.specificInfoList.insert(5, "충전기 타입: " + tempObj.type)
        self.specificInfoList.insert(6, "충전소 상태: " + tempObj.stat)
        self.lat = tempObj.lat
        self.lng = tempObj.lng
        self.stnName = tempObj.stationName"""
        #이전 코드.

    def SendMail(self):
        tempList = list(xmlProcessing.chargingStations[self.curSelectedLoc])
        tempObj = tempList[self.stationListBox.curselection()[0]]

        HostMail = smtplib.SMTP('smtp.gmail.com', 587)
        HostMail.starttls()
        HostMail.login('poryou66@gmail.com', 'ftpzebchlgswtqzh')

        # 세부사항 내용을 가져와서 집어 넣기
        msg = MIMEText("주소: " + tempObj.address + "\n 충전소ID: " + tempObj.stationID + "\n 충전소 이름: " + tempObj.stationName
                       + "\n 충전기 타입: " + tempObj.type + "\n 충전소 상태: " + tempObj.stat)
        msg['Subject'] = "****요청하신 " + tempObj.stationName + "충전소의 정보 입니다.****"

        HostMail.sendmail("poryou66@gmail.com", self.MailIDinBox.get(), msg.as_string())
        HostMail.quit()
        messagebox.showinfo("메일 전송 완료", self.MailIDinBox.get() + "로 성공적으로 전송을 완료하였습니다!")

    def openMap(self):
        # 위도 경도 지정
        map_osm = folium.Map(location=[self.lng, self.lat], zoom_start=18)
        # 마커 지정
        folium.Marker([self.lng, self.lat], popup=self.stnName).add_to(map_osm)
        # html 파일로 저장
        map_osm.save('map.html')
        webbrowser.open('map.html')

    def selectingLocation(self, event):
        print("you selected area")
        # 리스트 박스의 curselection 메소드는 튜플의 형태로 반환함. 즉 첫번째 값에 인덱스 값이 들어있음!
        self.admListBox.delete(0, 'end')  # 해당 지역을 선택하면 기존의 충전소 정보가 싹 제거된다.
        index = 0
        self.curSelectedLoc = self.locationListBox.curselection()[0]
        for i in xmlProcessing.AdmArea[self.curSelectedLoc]:
            self.admListBox.insert(index, i)  # 그 다음 해당 지역 충전소를 하나씩 리스트박스에 삽입한다.
            index += 1

    def __del__(self):
        xmlProcessing.deleteDoc()
        del self.curSelectedLoc
