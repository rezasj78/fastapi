import json

import requests

url = 'http://localhost:8000/users'
myobj = {
	"phone_num": 78,
	"email": "email.2",
	"name": "reza",
	"home_num": "3",
	"role": 0,
	"password": "1234"
}
date = {
	"phone": 78,
	"password": "1234"
}
x = requests.get(url=url)

print(x.json()[1], )
