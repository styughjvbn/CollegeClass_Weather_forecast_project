import tkinter as tk
from urllib.parse import urlencode, unquote
import requests
import json

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst"
queryString = "?" + urlencode(
{
  "ServiceKey": unquote("b58MyDUhHqCfbct6sxlCYnyzG6uSiFf8ZDeZXXvrZHLQSYT3zSL3SbOehZ60ZiNiny%2BZpsMSN4PuC59%2BtHvH%2BQ%3D%3D"),
  "base_date": "20210524",
  "base_time": "1730",
  "nx": 68, #서원구 개신동
  "ny": 106,
  "numOfRows": "40",
  "pageNo": 1,
  "dataType": "JSON"
}
)
queryURL = url + queryString
response = requests.get(queryURL)
print("=== response json data start ===")
print(response.text)
print("=== response json data end ===")
print()

r_dict = json.loads(response.text)
r_response = r_dict.get("response")
r_body = r_response.get("body")
r_items = r_body.get("items")
r_item = r_items.get("item")

result = []
result2=[]
for item in r_item:
    if(item.get("category") == "T1H"):
        result.append(item)

for item in r_item:
    if(item.get("category") == "REH"):
        result2.append(item)
a=[]
b=[]
for item in result:
    a.append(item.get("fcstValue"))
for item in result2:
    b.append(item.get("fcstValue"))
    
A=a[1]
B=b[1]
    
HEIGHT = 700
WIDTH = 800

def test_function():
    label["text"] = A+B

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()


frame = tk.Frame(root, bg='#80c1ff',bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor='n')

entry = tk.Entry(frame,font=40)
entry.place(relwidth=0.35,relheight=1 )


button = tk.Button(frame ,text = "Get Weather",font=40,command=test_function) 
button.place(relx=0.7,relheight=1,relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff',bd=10)
lower_frame.place(relx=0.5,rely=0.25,relwidth=0.75,relheight=0.6,anchor='n')

label = tk.Label(lower_frame, text = "This is a label")
label.place(relwidth=1,relheight=1)


root.mainloop()



