import requests

searchword = "台中"
partSearchWord = "id=5"
response = requests.get("http://127.0.0.1:8000/ear_data/?search=%s&order=asc&limit=10" % partSearchWord)
response_dic = response.json
response_text = response.text
print(response_text)