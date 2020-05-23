import urllib.request


class GetData:
    open_api_key = 'CntB%2BiKL6vswxxgKpm%2F11dDLhcRXZwlmL0pp118SgLUUMcWmfaN09%2BZxWIoJBqzGUVQM41p%2FNBulbDrcmiAT0w%3D%3D'
    url = "http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api?serviceKey=" + open_api_key

    def main(self):

        data = urllib.request.urlopen(self.url).read()

        f = open("sample1.xml","wb")
        f.write(data)
        f.close()




getData = GetData()
getData.main()
