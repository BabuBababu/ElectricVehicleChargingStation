from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import xmlProcessing

class GUI:
    def __init__(self):
        self.currentSelectedLocation=""
        self.window = Tk()
        self.window.title("전기자동차 공공충전소 현황")
        self.window.geometry("800x600")
        self.font1 = Font(family="맑은 고딕", size=20, slant="italic")
        Label(text="전기자동차 공공충전소 현황",font=self.font1).pack()
        self.initButton()
        self.initListBox()
        self.window.mainloop()

    def initButton(self):
        self.img1=Image.open("img/magGlass.png")
        self.photo1=ImageTk.PhotoImage(self.img1)
        self.img2 = Image.open("img/eye.png")
        self.photo2 = ImageTk.PhotoImage(self.img2)
        self.img3 = Image.open("img/mail.png")
        self.photo3 = ImageTk.PhotoImage(self.img3)
        self.searchButton=Button(image=self.photo1)
        self.specifiedSearchButton=Button(image=self.photo2)
        self.sendMailButton=Button(image=self.photo3)
        self.searchButton.place(x=10,y=50)
        Label(text="검색").place(x=30,y=130)
        self.specifiedSearchButton.place(x=10+64+15,y=50)
        Label(text="세부사항 보기").place(x=10+64+10,y=130)
        self.sendMailButton.place(x=10+128+35,y=50)
        Label(text="메일 보내기").place(x=10+128+35,y=130)


    def initListBox(self):
        self.frame1=Frame(self.window)
        self.frame1.place(x=10,y=200)
        self.scrollbarWithLocList=Scrollbar(self.frame1)
        self.scrollbarWithLocList.pack(side='right',fill='y')
        self.locationListBox = Listbox(self.frame1, selectmode='extended', yscrollcommand=self.scrollbarWithLocList.set)
        for i in range(len(xmlProcessing.locations)):
            self.locationListBox.insert(i,xmlProcessing.locations[i])
        self.locationListBox.pack()

    def getStationList(self):
        pass
