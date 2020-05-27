from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import xmlProcessing
import smtplib
from email.mime.text import MIMEText
from tkinter import messagebox


class GUI:
    def __init__(self):
        self.curSelectedLoc = None
        xmlProcessing.createXmlDoc()
        xmlProcessing.parseStationInfo()
        self.window = Tk()
        self.window.title("전기자동차 공공충전소 현황")
        self.window.geometry("800x600")
        self.font1 = Font(family="맑은 고딕", size=20, slant="italic")
        self.font2 = Font(family="Arial", size=10)
        self.font3 = Font(family="굴림", size=12)

        Label(self.window, text="전기자동차 공공충전소 현황", font=self.font1).pack()
        self.initButton()
        self.initListBox()
        self.imgTempMap = Image.open("img/tempMap.png")
        self.photoTempMap = ImageTk.PhotoImage(self.imgTempMap)
        Label(self.window, image=self.photoTempMap).place(x=350, y=100)
        Label(self.window, text="지도", font=self.font3).place(x=550, y=350)
        # 지도는 html frame이라는걸 사용하면 될 것 같습니다.

        self.MailIDinBox = StringVar()
        self.eMailEntry = Entry(self.window,textvariable= self.MailIDinBox)
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
        self.searchButton = Button(image=self.photo1, command=self.getStationList)
        self.specifiedSearchButton = Button(image=self.photo2, command=self.getSpecificInfo)
        self.sendMailButton = Button(image=self.photo3, command=self.SendMail)
        self.searchButton.place(x=10, y=50)
        Label(text="검색").place(x=30, y=130)
        self.specifiedSearchButton.place(x=10 + 64 + 15, y=50)
        Label(text="세부사항 보기").place(x=10 + 64 + 10, y=130)
        self.sendMailButton.place(x=10 + 128 + 35, y=50)
        Label(text="메일 보내기").place(x=10 + 128 + 35, y=130)

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
        # 여기까지 지역 리스트 만드는 코드

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

    def getStationList(self):
        # 리스트 박스의 curselection 메소드는 튜플의 형태로 반환함. 즉 첫번째 값에 인덱스 값이 들어있음!
        self.stationListBox.delete(0, 'end')
        index = 0
        self.curSelectedLoc = self.locationListBox.curselection()[0]
        for i in xmlProcessing.chargingStations[self.curSelectedLoc]:
            self.stationListBox.insert(index, i.stationName)
            index += 1

    def getSpecificInfo(self):
        self.specificInfoList.delete(0, 'end')

        tempList = list(xmlProcessing.chargingStations[self.curSelectedLoc])

        tempObj = tempList[self.stationListBox.curselection()[0]]

        self.specificInfoList.insert(0, "주소: " + tempObj.address)
        self.specificInfoList.insert(1, "충전소ID: " + tempObj.stationID)
        self.specificInfoList.insert(2, "충전소 이름: " + tempObj.stationName)
        self.specificInfoList.insert(3, "충전소 경도: " + tempObj.lat)
        self.specificInfoList.insert(4, "충전소 위도: " + tempObj.lng)
        self.specificInfoList.insert(5, "충전기 타입: " + tempObj.type)
        self.specificInfoList.insert(6, "충전소 상태: " + tempObj.stat)

    def SendMail(self):
        tempList = list(xmlProcessing.chargingStations[self.curSelectedLoc])
        tempObj = tempList[self.stationListBox.curselection()[0]]

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('poryou66@gmail.com', 'ftpzebchlgswtqzh')

        # 세부사항 내용을 가져와서 집어 넣기
        msg = MIMEText("주소: "+ tempObj.address + "\n 충전소ID: " + tempObj.stationID + "\n 충전소 이름: " + tempObj.stationName
                       +"\n 충전기 타입: " + tempObj.type +"\n 충전소 상태: " + tempObj.stat)
        msg['Subject'] = "****요청하신 "+ tempObj.stationName + "충전소의 정보 입니다.****"

        s.sendmail("poryou66@gmail.com",self.MailIDinBox.get() , msg.as_string())
        s.quit()
        messagebox.showinfo( "메일 전송 완료",self.MailIDinBox.get() + "로 성공적으로 전송을 완료하였습니다!")


    def __del__(self):
        xmlProcessing.deleteDoc()
        del self.curSelectedLoc
