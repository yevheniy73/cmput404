import requests

#print(requests.__version__)

get_google = requests.get("https://www.google.com")
print(get_google)

get_me = requests.get("https://raw.githubusercontent.com/yevheniy73/cmput404/lab1/lab1.py")

print(get_me.text)