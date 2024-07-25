import re
import requests

VSEBINA = ""
SEZNAM = []
for x in ["pre1500", "1500s", "1600s", "1700s", "1800s", "1800-1824", "1825-1849", "nd"]:
    r = requests.get(f"https://music.library.appstate.edu/lute/{x}")
    VSEBINA = r.text[r.text.index("<li>"):]
    SEZNAM += VSEBINA.split("</li></ul></li><li>")
LETO_RE = r"(\d{4,}\??\/?\-?[a-z]?\d*)[\;\:\(\)\sA-Za-z\]\[\&]*\s?[A-Za-z\]\[<\/>\?\]]*<br>"
AVTOR_RE = r"<br>([A-Za-z\'\,\s\?]+)\.*"
KRAJ_RE = r"</em>[^\(]*\(([^<:\)]*)\)+"


#problemi = []
#for x in range(len(SEZNAM)):
#    r = SEZNAM[x].split("<ul><li>")
#    if re.search(LETO_RE, r[0]) == None:
#        problemi += [f"{x}"]
#print(problemi)

#seperation of lists - make different lists?

print(SEZNAM[0].split("<ul><li>")[-2])

##with open("zbrani_podatki.txt", "w", encoding="UTF-8") as izhod:
 #   for DELO in SEZNAM:
 #       RAZDELJEN = DELO.split("<ul><li>")
 #       if re.search(LETO_RE, RAZDELJEN[-2]) == None:
 #           LETO = "NONE"
 #       else:
 #           if "-" in re.search(LETO_RE, RAZDELJEN[-2]).group(1) or "/" in re.search(LETO_RE, RAZDELJEN[-2]).group(1):
 #               LETO = "NONE"
 #           else:
 #               LETO = re.search(LETO_RE, RAZDELJEN[-2]).group(1)[:4]
 #       if re.search(AVTOR_RE, RAZDELJEN[-2]) == None:
 #           AVTOR = "NONE"
 #       else:
 #           AVTOR = re.search(AVTOR_RE, RAZDELJEN[-2]).group(1)
 #       if re.search(KRAJ_RE, RAZDELJEN[-2]) == None:
 #           KRAJ = "NONE"
 #       else:
 #           KRAJ = re.search(KRAJ_RE, RAZDELJEN[-2]).group(1)
#
 #       if ", " in KRAJ:
 #           MESTO = KRAJ.split(", ")[0]
 #           DRŽAVA = re.sub(r"[^A-Za-z\?]+", "", KRAJ.split(", ")[1][:-1])
 #       else:
 #           MESTO = "NONE"
 #           DRŽAVA = KRAJ
 #       #TABLATURE = re.search(TABLATURE_RE, RAZDELJEN[1]).group(1)
 #       izhod.write(f"\n{LETO}, {AVTOR}, {MESTO}, {DRŽAVA}")
##lahko bi vsak člen razdelili na dva dela: nad alinejami in pod njimi z <ul><li>
#
##TABLATURE_RE = r"\b(\B*\btablature)"
##INSTRUMENT_RE = r""
#
##print(SEZNAM[25])
##vpis v datoteko
#
##zacetek = </li></ul></li><li>
##leto = na koncu pred <br>
##avtor = po <br>
##naslov = po <em>
##instrument = po <ul><li>, če več po </li><li>
#
#
#
##{"Naslov": , "Država": , "Leto": , "Vrsta lutnje": , "Vrsta tablature": }
#