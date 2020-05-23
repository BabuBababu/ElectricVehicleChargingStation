from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import xmlProcessing


class GUI:
    def __init__(self):
        xmlProcessing.createXmlDoc()
        xmlProcessing.parseStationInfo()
        self.currentSelectedLocation = None  # 현재 선택된 지역 e.g.) 서울특별시, 인천광역시 등....
        self.window = Tk()
        self.window.title("전기자동차 공공충전소 현황")
        self.window.geometry("800x600")
        self.font1 = Font(family="맑은 고딕", size=20, slant="italic")
        self.font2 = Font(family="Arial", size=10)
        self.font3 = Font(family="굴림",size=12)

        Label(text="전기자동차 공공충전소 현황", font=self.font1).pack()
        self.initButton()
        self.initListBox()
        self.mapLabel=Label(text='이곳에 지도가 그려질 예정입니다.',font=self.font1,bg='white')
        #지도는 html frame이라는걸 사용하면 될 것 같습니다.
        self.mapLabel.place(x=350, y=100)
        self.window.mainloop()

    def initButton(self):
        self.img1 = Image.open("img/magGlass.png")
        self.photo1 = ImageTk.PhotoImage(self.img1)
        self.img2 = Image.open("img/eye.png")
        self.photo2 = ImageTk.PhotoImage(self.img2)
        self.img3 = Image.open("img/mail.png")
        self.photo3 = ImageTk.PhotoImage(self.img3)
        self.searchButton = Button(image=self.photo1, command=self.getStationList)
        self.specifiedSearchButton = Button(image=self.photo2)
        self.sendMailButton = Button(image=self.photo3)
        self.searchButton.place(x=10, y=50)
        Label(text="검색").place(x=30, y=130)
        self.specifiedSearchButton.place(x=10 + 64 + 15, y=50)
        Label(text="세부사항 보기").place(x=10 + 64 + 10, y=130)
        self.sendMailButton.place(x=10 + 128 + 35, y=50)
        Label(text="메일 보내기").place(x=10 + 128 + 35, y=130)

    def initListBox(self):
        self.frame1 = Frame(self.window)
        self.frame1.place(x=10, y=200)
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
        Label(self.window,text="지역 리스트",font=self.font3).place(x=40,y=340)
        # 여기까지 지역 리스트 만드는 코드

        self.frame2 = Frame(self.window)
        self.frame2.place(x=10, y=400)
        self.stationListBox = Listbox(self.frame2, selectmode='extended',
                                      height=7, width=40, font=self.font2,
                                      relief='ridge', borderwidth=7)
        self.stationListBox.pack(side="left", fill="y")

        self.scrollbarWithSpecificList = Scrollbar(self.frame2, orient="vertical")
        self.scrollbarWithSpecificList.config(command=self.stationListBox.yview)
        self.scrollbarWithSpecificList.pack(side="right", fill="y")
        self.stationListBox.config(yscrollcommand=self.scrollbarWithSpecificList.set)
        Label(self.window, text="지역 내 충전소 리스트", font=self.font3).place(x=70,y=550)
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
        #여기까지 스테이션의 세부사항 리스트.


    def getStationList(self):
        self.currentSelectedLocation = self.locationListBox.curselection()
        index = 0
        for i in xmlProcessing.chargingStations[self.currentSelectedLocation[0]]:
            self.stationListBox.insert(index, i.stationName)
            index += 1

    def __del__(self):
        xmlProcessing.deleteDoc()
        del self.currentSelectedLocation
