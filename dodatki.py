import re

#Seznam vseh podstrani glavne spletne strani iz katere pobiramo podatke.
LETNICE = ["pre1500", "1500s", "1600s", "1700s", "1800s", "1800-1824", "1825-1849", "nd"]

#Posebni znaki, ki se pojavljajo v html datoteki.
POSEBNI_ZNAKI = {"&#382;": "ž", "&ocirc;": "ô", "&#347;": "ś", "&szlig;": "ß", "&#324": "ń", "&#328;": "n", "&#322;": "ł", "&#345;": "ř", "&#269;": "č", "&yacute;": "ý", "&ecirc;": "ê", "&icirc;": "î", "&aring;": "å", "&atilde;": "ã", "&ntilde;": "ñ", "&nbsp;": "", "&euml;": "ë", "&iuml;": "ï", "&ouml;": "ö", "&auml;": "ä", "&uuml;": "ü", "e&#769;": "é", "&eacute;": "é", "&oacute;": "ó", "&aacute;": "á", "&iacute;": "í", "&ograve;": "ò", "&egrave;": "è", "&agrave;": "à", "&ccedil;": "ç", "&Scaron;": "Š", "&scaron;": "š"}

#Regularni izrazi za določen tip podatkov.
LETO_RE = r"([^\-]\d{4,}\??\/?\-?[a-z]*\s?\d*)[\;\:\(\)\sA-Za-z\]\[\&]*\s?[A-Za-z\]\[<\/>\?\]]*<br>"
AVTOR_RE = r"<br>([\d\#A-Za-z\'\s\?\;\&\-]{3,}\,?\s[\d\#A-Za-z\'\s\?\;\&\-]{3,})\.*"
KRAJ_RE1 = r"</em>[^\(]*\(([A-Z]+[A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
KRAJ_RE2 = r"<br>[^\(\[<>]*\(([A-Z]+[A-Za-z\s\,\[\;\&]*)[\)\:\]]+"
TABLATURA_RE = r"\w{3,}\stablature" 
LUTNJA_RE = r"\d+-course\s[A-Za-z]*\b"
TREATISE_RE = r"treatise"
STRING_RE = r"[\d\,and\-\s]+string"
COURSE_RE = r"[\d\,and\-\s]+course"

