"""Knjižnice in datoteke, ki jih potrebujemo."""
import re
import csv
import requests
import dodatki as dd


# Poberemo podatke.
VSEBINA = ""
SEZNAM = []
for x in dd.LETNICE:
    try:
        r = requests.get(f"https://music.library.appstate.edu/lute/{x}",
                         timeout=10)
    except requests.exceptions.Timeout:
        print("Čas je potekel.")
    VSEBINA = r.text[r.text.index("<li>"):]
    SEZNAM += VSEBINA.split("</li></ul></li><li>")

# Odpremo datoteko zbrani_podatki.csv, v katero bomo pisali podatke.
with open("zbrani_podatki.csv", "w", newline='', encoding="utf-8") as izhod:
    writer = csv.writer(izhod)
    # Zapišemo prvo vrsto, z opisom podatkov v stolpcu.
    writer.writerow(["ID", "LETO", "AVTOR", "MESTO", "DRŽAVA",
                     "TABLATURA", "INSTRUMENT", "STRUNE" , "RAZPRAVA"])
    ID = 0

    # Sedaj iz vsakega dela izluščimo želene podatke.
    for delo in SEZNAM:

        # Besedilo, ki opisuje eno izmed del na spletni strani,
        # razdelimo na dva dela. Podatki bodo tako natančneje
        # pridobljeni, saj se večina vedno pojavlja v istem delu.
        DELITEV = delo.split("<ul><li>")
        PRVI_DEL = DELITEV[-2]
        DRUGI_DEL = DELITEV[-1]

        # Leto izdaje.
        LETO = None
        if "<br>" in PRVI_DEL:
            LETO_ISKANJE = PRVI_DEL[:PRVI_DEL.index("<br>") + 4]
            if re.search(dd.LETO_RE, LETO_ISKANJE) is not None:
                if ("-" not in re.search(dd.LETO_RE, LETO_ISKANJE).group(1)
                    and "/" not in re.search(dd.LETO_RE, PRVI_DEL).group(1)
                    and "?" not in re.search(dd.LETO_RE, LETO_ISKANJE).group(1)):
                    LETO = int(re.search(dd.LETO_RE, LETO_ISKANJE).group(1)[1:5])

        # Avtor dela.
        if re.search(dd.AVTOR_RE, PRVI_DEL) is None:
            AVTOR = None
        else:
            AVTOR = re.search(dd.AVTOR_RE, PRVI_DEL).group(1).strip()

        # Mesto in država izdaje.
        KRAJ_SUB = r"[^A-Za-z\?\s\&\;\:]+"
        KRAJ, MESTO, DRZAVA = None, None, None
        # Če v prvem ciklu ne najdemo kraja, poskusimo še z drugim
        # regexom. Kraji se pojavljajo v različnih delih datoteke,
        # zato jih poskusimo natančneje zajeti.
        for kraj_re in [dd.KRAJ_RE1, dd.KRAJ_RE2]:
            if KRAJ is None:
                if re.search(kraj_re, PRVI_DEL) is not None:
                    KRAJ = re.search(kraj_re, PRVI_DEL).group(1)
                    if ", " in KRAJ:
                        MESTO = re.sub(KRAJ_SUB, "", KRAJ.split(", ")[0])
                        DRZAVA = re.sub(KRAJ_SUB, "", KRAJ.split(", ")[1])
                    else:
                        MESTO = None
                        DRZAVA = re.sub(KRAJ_SUB, "", KRAJ)

        # Tablatura v kateri je delo napisano.
        TABLATURA_SET = set(re.findall(dd.TABLATURA_RE, DRUGI_DEL))
        TABLATURA = ""
        for tab in TABLATURA_SET:
            TABLATURA = "".join([TABLATURA, f"{tab}, "])
        if TABLATURA == "":
            TABLATURA = None
        if TABLATURA is not None:
            TABLATURA = TABLATURA.strip(", ")

        # Vrsta instrumenta, za katerega je delo napisano.
        LUTNJA_SET = (set(re.findall(r"lute", DRUGI_DEL)) |
                      set(re.findall(r"guitar", DRUGI_DEL)))
        LUTNJA = ""
        for lute in LUTNJA_SET:
            LUTNJA = ", ".join([LUTNJA, f"{lute}"])
        if LUTNJA == "":
            LUTNJA = "drugo"
        INSTRUMENT = LUTNJA.strip(", ")

        # Število (parov) strun, ki jih ima instrument,
        # za katerega je delo napisano.
        STRUNE = (set(re.findall(dd.STRING_RE, DRUGI_DEL)) |
                  set(re.findall(dd.COURSE_RE, DRUGI_DEL)))
        STEVILO_STRUN_SET = set()
        if STRUNE is not set():
            for element in STRUNE:
                stevilo = re.sub(r"[^\d\s]+", "", element)
                STEVILO_STRUN_SET |= set(stevilo.split(" "))
        STEVILO_STRUN = ""
        if STEVILO_STRUN_SET is not set():
            STEVILO_STRUN_SET = list(STEVILO_STRUN_SET)
            for element in STEVILO_STRUN_SET:
                STEVILO_STRUN += f"{element}, "
            STEVILO_STRUN = STEVILO_STRUN.strip(", ")
        if STEVILO_STRUN == "":
            STEVILO_STRUN = None

        # Preverimo, če delo vsebuje razpravo ali ne.
        if len(re.findall(dd.TREATISE_RE, DRUGI_DEL,)) == 0:
            RAZPRAVA = "NE"
        else:
            RAZPRAVA = "DA"

        # Vrsta, kot bo izpisana v csv dokumentu.
        VRSTA = [ID, LETO, AVTOR, MESTO, DRZAVA, TABLATURA,
                 INSTRUMENT, STEVILO_STRUN, RAZPRAVA]

        # Preverimo še posebne znake in jih zamenjamo.
        for indeks in range(2, len(VRSTA)):
            kos = VRSTA[indeks]
            for znak, koda in dd.POSEBNI_ZNAKI.items():
                if kos is not None:
                    kos = re.sub(znak, koda, kos)
            VRSTA[indeks] = kos

        # Zapišemo izluščene podatke v datoteko zbrani_podatki.csv.
        writer.writerow(VRSTA)
        ID +=1
