import requests

#print(requests.__version__)

get_google = requests.get("https://www.google.com")
print(get_google)