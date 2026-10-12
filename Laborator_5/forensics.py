import argparse
import json
import re
import struct
import zipfile
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from typing import Any

# Itemul 8
def tip_real(cale):
    with open(cale, "rb") as fisier:
        cap = fisier.read(8)
    for semnatura, nume in [(b"%PDF", "pdf"), (b"\x89PNG\r\n\x1a\n", "png"),
                            (b"\xff\xd8", "jpeg"), (b"PK\x03\x04", "zip/docx")]:
        if cap.startswith(semnatura):
            return nume
    return "necunoscut: " + cap.hex()


# Itemul 9
def extrage_text(cale):
    return [m.decode("ascii") for m in re.findall(rb"[ -~]{4,}", Path(cale).read_bytes())]


# Itemul 10
def grade_zecimale(valori, emisfera):
    grade, minute, secunde = map(float, valori)
    rezultat = grade + minute / 60 + secunde / 3600
    if isinstance(emisfera, bytes):
        emisfera = emisfera.decode()
    return -rezultat if emisfera in ("S", "W") else rezultat


def metadate(cale):
    with Image.open(cale) as imagine:
        exif = imagine.getexif()
        rezultat = {TAGS.get(tag, str(tag)): str(val) for tag, val in exif.items()
                    if tag != 34853}
        gps = exif.get_ifd(34853) if 34853 in exif else {}
    rezultat["GPS"] = {GPSTAGS.get(tag, str(tag)): str(val) for tag, val in gps.items()}
    if all(tag in gps for tag in (1, 2, 3, 4)):
        rezultat["latitudine"] = grade_zecimale(gps[2], gps[1])
        rezultat["longitudine"] = grade_zecimale(gps[4], gps[3])
    return rezultat


# Itemul 11
def sfarsit_png(date):
    if not date.startswith(b"\x89PNG\r\n\x1a\n"):
        return 0
    pozitie = 8
    while pozitie + 12 <= len(date):
        lungime = struct.unpack(">I", date[pozitie:pozitie + 4])[0]
        tip = date[pozitie + 4:pozitie + 8]
        urmatoare = pozitie + 12 + lungime
        if urmatoare > len(date):
            raise ValueError("PNG incomplet.")
        if tip == b"IEND":
            return urmatoare
        pozitie = urmatoare
    raise ValueError("Lipseste IEND.")


def extrage_arhiva(cale, iesire):
    date = Path(cale).read_bytes()
    pozitie = date.find(b"PK\x03\x04", sfarsit_png(date))
    if pozitie == -1:
        raise ValueError("Nu exista o arhiva ZIP la coada fisierului.")
    destinatie = Path(iesire)
    destinatie.parent.mkdir(parents=True, exist_ok=True)
    destinatie.write_bytes(date[pozitie:])
    with zipfile.ZipFile(destinatie) as arhiva:
        if arhiva.testzip() is not None:
            raise ValueError("Arhiva corupta.")
        nume = arhiva.namelist()
    return {"offset": pozitie, "arhiva": str(destinatie), "fisiere": nume}


def dezarhiveaza(cale, folder):
    folder = Path(folder).resolve()
    with zipfile.ZipFile(cale) as arhiva:
        for intrare in arhiva.infolist():
            tinta = (folder / intrare.filename).resolve()
            if not tinta.is_relative_to(folder):
                raise ValueError("Cale nepermisa in arhiva.")
            if (intrare.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Link simbolic nepermis.")
        arhiva.extractall(folder)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cale", type=Path)
    parser.add_argument("--arhiva", type=Path)
    parser.add_argument("--extrage-in", type=Path)
    args = parser.parse_args()
    rezultat = {"tip": tip_real(args.cale), "text": extrage_text(args.cale)}
    if rezultat["tip"] in ("jpeg", "png"):
        rezultat["metadate"] = metadate(args.cale)
    if args.arhiva:
        rezultat["carving"] = extrage_arhiva(args.cale, args.arhiva)
        if args.extrage_in:
            dezarhiveaza(args.arhiva, args.extrage_in)
    elif args.extrage_in:
        parser.error("--extrage-in necesita --arhiva")
    print(json.dumps(rezultat, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
