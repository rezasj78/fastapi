import json

import requests

url = 'http://localhost:8000/user'
myobj = {
	"phone_num": 78,
	"email": "em1",
	"name": "rza",
	"home_num": "5",
	"role": 0 ,
	"password": "1234"
}
date = {
	"phone": 78,
	"password": "1234"
}
x = requests.post(url=url, json=myobj)

print(x.json())
