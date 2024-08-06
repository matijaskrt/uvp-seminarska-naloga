import re
import requests

#poberemo podatke
VSEBINA = ""
SEZNAM = []
for x in ["pre1500", "1500s", "1600s", "1700s", "1800s", "1800-1824", "1825-1849", "nd"]:
    r = requests.get(f"https://music.library.appstate.edu/lute/{x}")
    VSEBINA = r.text[r.text.index("<li>"):]
    SEZNAM += VSEBINA.split("</li></ul></li><li>")


#Regularni izrazi za določen tip podatkov.
LETO_RE = r"(\d{4,}\??\/?\-?[a-z]*\s?\d*)[\;\:\(\)\sA-Za-z\]\[\&]*\s?[A-Za-z\]\[<\/>\?\]]*<br>"
AVTOR_RE = r"<br>([A-Za-z\'\,\s\?\;\&\-]+)\.*"
KRAJ_RE1 = r"</em>[^\(]*\(([A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
KRAJ_RE2 = r"<br>[^\(]*\(([A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
TABLATURA_RE = r"\w+\stablature" 
LUTNJA_RE = r"\d?-course"

with open("zbrani_podatki.txt", "w", encoding="UTF-8") as izhod:
    for DELO in SEZNAM:
        RAZDELJEN = DELO.split("<ul><li>")
        LETO = "NONE"
        if "<br>" in RAZDELJEN[-2]:
            if re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]) == None:
                LETO = "NONE"
            else:
                if "-" in re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1) or "/" in re.search(LETO_RE, RAZDELJEN[-2]).group(1):
                    LETO = "NONE"
                elif "?" in re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1):
                    LETO = re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1)[:5]
                else:
                    LETO = re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1)[:4]
        if re.search(AVTOR_RE, RAZDELJEN[-2]) == None:
            AVTOR = "NONE"
        else:
            AVTOR = re.search(AVTOR_RE, RAZDELJEN[-2]).group(1).strip()
        if re.search(KRAJ_RE1, RAZDELJEN[-2]) == None:
                KRAJ = "NONE"
        else:
            KRAJ = re.search(KRAJ_RE1, RAZDELJEN[-2]).group(1)
            if ", " in KRAJ:
                MESTO = KRAJ.split(", ")[0]
                DRŽAVA = re.sub(r"[^A-Za-z\?]+", "", KRAJ.split(", ")[1])
            else:
                MESTO = "NONE"
                DRŽAVA = re.sub(r"[^A-Za-z\?]+", "", KRAJ)
        if KRAJ == "NONE":      
            if re.search(KRAJ_RE2, RAZDELJEN[-2]) == None:
                KRAJ = "NONE"
            else:
                KRAJ = re.search(KRAJ_RE2, RAZDELJEN[-2]).group(1)
            if ", " in KRAJ:
                MESTO = KRAJ.split(", ")[0]
                DRŽAVA = re.sub(r"[^A-Za-z\?]+", "", KRAJ.split(", ")[1])
            else:
                MESTO = "NONE"
                DRŽAVA = re.sub(r"[^A-Za-z\?]+", "", KRAJ)

            TABLATURA = set(re.findall(TABLATURA_RE, RAZDELJEN[-1]))
            LUTNJA = set(re.findall(LUTNJA_RE, RAZDELJEN[-1])) | set(re.findall(r"guitar", RAZDELJEN[-1]))
        izhod.write(f"{LETO}, {AVTOR}, {MESTO}, {DRŽAVA}, {TABLATURA}, {LUTNJA}\n")