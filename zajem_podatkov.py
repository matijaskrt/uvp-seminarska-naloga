import re
import requests


VSEBINA = ""

for x in ["pre1500", "1500", "1600", "1700", "1800-1824", "1825-1849"]:
    r = requests.get(f"https://music.library.appstate.edu/lute/{x}")
    VSEBINA += r.text
#ustvarimo seznam
SEZNAM = VSEBINA.split("</li></ul></li><li>")

LETO_RE = r"(\d+\-*\d*)[a-z\[]*<br>"
AVTOR_RE = r"<br>(.+)\."
MESTO_RE = r""
DRŽAVA_RE = r"</em>[^\(]*\(([^<:]*)[:<]+"
INSTRUMENT_RE = r""

print(SEZNAM[59])



#vpis v datoteko
#with open("urejeni_podatki", "w", encoding=utf-8) as izhod:
#   for delo in seznam:
#       izhod.write()

#zacetek = </li></ul></li><li>
#leto = na koncu pred <br>
#avtor = po <br>
#naslov = po <em>
#instrument = po <ul><li>, če več po </li><li>



#{"Naslov": , "Država": , "Leto": , "Vrsta lutnje": , "Vrsta tablature": }
