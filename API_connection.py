import requests

searchword = ""
response = requests.get("http://127.0.0.1:8000/ear_data/?search=%s&order=asc&offset=0" % searchword)
response_dic = response.json
response_text = response.text
print(response_text)