from urllib.parse import urlencode, unquote
import requests
import json

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst"
queryString = "?" + urlencode(
{
  "ServiceKey": unquote("b58MyDUhHqCfbct6sxlCYnyzG6uSiFf8ZDeZXXvrZHLQSYT3zSL3SbOehZ60ZiNiny%2BZpsMSN4PuC59%2BtHvH%2BQ%3D%3D"),
  "base_date": "20210523",
  "base_time": "2000",
  "nx": 68, #서원구 개신동
  "ny": 106,
  "numOfRows": "10",
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

result = {}
for item in r_item:
        if(item.get("category") == "T1H"):
                result = item
                break
for item in r_item:
        if(item.get("category") == "RN1"):
                result2 = item
                break

print("=== response dictionary(python object) data start ===")
print(result.get("baseTime")[:-2] +" temp : " + result.get("obsrValue") + "C")
print(result2.get("baseTime")[:-2] +" rain : " + result2.get("obsrValue") + "mm")
print("=== response dictionary(python object) data end ===")
print()