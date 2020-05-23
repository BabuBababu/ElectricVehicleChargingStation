import xmlProcessing


if __name__ == '__main__':
    xmlProcessing.createXmlDoc()
    xmlProcessing.parseStationInfo()
    xmlProcessing.deleteDoc()
    data=xmlProcessing.printSeoulData()