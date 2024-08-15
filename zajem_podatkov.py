import re
import requests
import csv

#poberemo podatke
VSEBINA = ""
SEZNAM = []
for x in ["pre1500", "1500s", "1600s", "1700s", "1800s", "1800-1824", "1825-1849", "nd"]:
    r = requests.get(f"https://music.library.appstate.edu/lute/{x}")
    VSEBINA = r.text[r.text.index("<li>"):]
    SEZNAM += VSEBINA.split("</li></ul></li><li>")

POSEBNI_ZNAKI = {"&#382;": "ž", "&ocirc;": "ô", "&#347;": "ś", "&szlig;": "ß", "&#324": "ń", "&#328;": "n", "&#322;": "ł", "&#345;": "ř", "&#269;": "č", "&yacute;": "ý", "&ecirc;": "ê", "&icirc;": "î", "&aring;": "å", "&atilde;": "ã", "&ntilde;": "ñ", "&nbsp;": "", "&euml;": "ë", "&iuml;": "ï", "&ouml;": "ö", "&auml;": "ä", "&uuml;": "ü", "e&#769;": "é", "&eacute;": "é", "&oacute;": "ó", "&aacute;": "á", "&iacute;": "í", "&ograve;": "ò", "&egrave;": "è", "&agrave;": "à", "&ccedil;": "ç", "&Scaron;": "Š", "&scaron;": "š"}

print(SEZNAM[1713])

#Regularni izrazi za določen tip podatkov.
LETO_RE = r"([^\-]\d{4,}\??\/?\-?[a-z]*\s?\d*)[\;\:\(\)\sA-Za-z\]\[\&]*\s?[A-Za-z\]\[<\/>\?\]]*<br>"
AVTOR_RE = r"<br>([\d\#A-Za-z\'\s\?\;\&\-]{3,}\,?\s[\d\#A-Za-z\'\s\?\;\&\-]{3,})\.*"
KRAJ_RE1 = r"</em>[^\(]*\(([A-Z]+[A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
KRAJ_RE2 = r"<br>[^\(\[<>]*\(([A-Z]+[A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
TABLATURA_RE = r"\w{3,}\stablature" 
LUTNJA_RE = r"\d+-course\s[A-Za-z]*\b"
TREATISE_RE = r"treatise"

with open("zbrani_podatki.csv", "w", newline='', encoding="utf-8") as izhod:
    writer = csv.writer(izhod)
    writer.writerow(["ID", "LETO", "AVTOR", "MESTO", "DRŽAVA", "TABLATURA", "INSTRUMENT", "STRUNE" , "RAZPRAVA"])
    ID = 0
    for DELO in SEZNAM:
        RAZDELJEN = DELO.split("<ul><li>")
        LETO = None
        if "<br>" in RAZDELJEN[-2]:
            if re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]) == None:
                LETO = 0
            else:
                if "-" in re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1) or "/" in re.search(LETO_RE, RAZDELJEN[-2]).group(1):
                    LETO = 0
                elif "?" in re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1):
                    LETO = 0
                else:
                    LETO = int(re.search(LETO_RE, RAZDELJEN[-2][:RAZDELJEN[-2].index("<br>") + 4]).group(1)[1:5])
        if re.search(AVTOR_RE, RAZDELJEN[-2]) == None:
            AVTOR = None
        else:
            AVTOR = re.search(AVTOR_RE, RAZDELJEN[-2]).group(1).strip()

        if re.search(KRAJ_RE1, RAZDELJEN[-2]) == None:
                KRAJ = None
        else:
            KRAJ = re.search(KRAJ_RE1, RAZDELJEN[-2]).group(1)
            if ", " in KRAJ:
                MESTO = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ.split(", ")[0])
                DRŽAVA = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ.split(", ")[1])
            else:
                MESTO = None
                DRŽAVA = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ)
        if KRAJ == None:      
            if re.search(KRAJ_RE2, RAZDELJEN[-2]) == None:
                KRAJ, MESTO, DRŽAVA = None, None, None
            else:
                KRAJ = re.search(KRAJ_RE2, RAZDELJEN[-2]).group(1)
                if ", " in KRAJ:
                    MESTO = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ.split(", ")[0])
                    DRŽAVA = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ.split(", ")[1])
                else:
                    MESTO = None
                    DRŽAVA = re.sub(r"[^A-Za-z\?\s\&\;\:]+", "", KRAJ)

        TABLATURA_SET = set(re.findall(TABLATURA_RE, RAZDELJEN[-1]))
        TABLATURA = ""
        for tab in TABLATURA_SET:
            TABLATURA += f"{tab}, "
        if TABLATURA == "":
            TABLATURA = None
        if TABLATURA != None:
            TABLATURA = TABLATURA.strip(", ")

        STRUNE_SET = set(re.findall(r"[\d\,and\-\s]+string", RAZDELJEN[-1])) | set(re.findall(r"[\d\,and\-\s]+course", RAZDELJEN[-1]))
            
        STEVILO_STRUN_SET = set()
        if STRUNE_SET != set():
            for element in STRUNE_SET:
                stevilo = re.sub(r"[^\d\s]+", "", element)
                STEVILO_STRUN_SET |= set(stevilo.split(" "))
            
        STEVILO_STRUN = ""
        if STEVILO_STRUN_SET != set():
            STEVILO_STRUN_SET = sorted([x for x in STEVILO_STRUN_SET])
            for element in STEVILO_STRUN_SET:
                STEVILO_STRUN += f"{element}, "
            STEVILO_STRUN = STEVILO_STRUN.strip(", ")
        if STEVILO_STRUN == "":
            STEVILO_STRUN = None

        LUTNJA_SET = set(re.findall(r"lute", RAZDELJEN[-1])) | set(re.findall(r"guitar", RAZDELJEN[-1]))
        LUTNJA = ""
        for lute in LUTNJA_SET:
            LUTNJA += f"{lute}, "
        if LUTNJA == "":
            LUTNJA = "drugo"
        INSTRUMENT = LUTNJA.strip(", ")

        if len(re.findall(TREATISE_RE, RAZDELJEN[-1],)) == 0:
            RAZPRAVA = "NE"
        else:
            RAZPRAVA = "DA"
        VRSTA = [ID, LETO, AVTOR, MESTO, DRŽAVA, TABLATURA, INSTRUMENT, STEVILO_STRUN, RAZPRAVA]
        for indeks in range(2, len(VRSTA)):
            kos = VRSTA[indeks]
            for znak in POSEBNI_ZNAKI:
                if kos != None:
                    kos = re.sub(znak, POSEBNI_ZNAKI[znak], kos)
            VRSTA[indeks] = kos
        writer.writerow(VRSTA)
        ID +=1