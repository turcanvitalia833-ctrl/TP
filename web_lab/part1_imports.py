# Laborator: functii, metode si importuri pe web
# Student: turcan vitalia

import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# Exercitiul 1:
import requests
print("Versiunea requests:", requests.__version__)

import urllib.request

# exercitiul 2: 
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (import requests):", response.status_code)

time.sleep(1)

from requests import get
response2 = get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (from requests import get):", response2.status_code)
time.sleep(1)


#  Exercitiul 3: 
import requests as rq
response3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (alias rq):", response3.status_code)
time.sleep(1)


#  Exercitiul 4: 
import urllib.request as urlreq

with urlreq.urlopen(BASE_URL, timeout=TIMEOUT) as raspuns:
    continut = raspuns.read()  
    print("Status (urllib):", raspuns.status)
    print("Primele 200 caractere:", continut.decode("utf-8")[:200])


# Exercitiul 5: 
print(dir(requests))



# Exercitiul 6: 
help(requests.get)
response4 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare cu timeout explicit:", response4.status_code)

time.sleep(1)


# Exercitiul 7: 
inceput = time.perf_counter()
response5 = requests.get(BASE_URL, timeout=TIMEOUT)
sfarsit = time.perf_counter()
print("Durata masurata manual:", sfarsit - inceput, "secunde")
print("response.elapsed:", response5.elapsed.total_seconds(), "secunde")



#  Exercitiul 8:
try:
    import bs4
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

