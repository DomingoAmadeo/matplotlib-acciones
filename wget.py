# Importamos la libreria requests
import requests

def wget(url):
    r = requests.get(url, allow_redirects=True)
    with open("data\\" + url[url.rfind('/') + 1::], 'wb') as f:
        f.write(r.content)
# Como usarla
wget(input("Url"))

