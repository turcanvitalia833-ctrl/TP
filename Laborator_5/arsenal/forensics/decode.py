import argparse
import base64
import binascii
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote_to_bytes

RADACINA = Path(__file__).resolve().parents[2]


# Itemul 1
def text_octeti(text="Salut"):
    date = text.encode("utf-8")
    return date, date.hex(), bytes.fromhex(date.hex())


# Itemul 2
def ghici_strat(s):
    s = s.strip()
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    if s and len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"
    if s and len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        try:
            date = base64.b64decode(s, validate=True)
            if base64.b64encode(date).decode() == s:
                return "base64"
        except (ValueError, binascii.Error):
            pass
    return "necunoscut"


# Itemul 3
def desfa(s):
    strat = ghici_strat(s)
    if strat == "url":
        return strat, unquote_to_bytes(s)
    if strat == "hex":
        return strat, bytes.fromhex(s.strip())
    if strat == "base64":
        return strat, base64.b64decode(s.strip(), validate=True)
    return strat, s.encode("utf-8")


# Itemul 4
def citibil(date):
    return all(32 <= octet < 127 for octet in date)


def decodeaza_straturi(date, maxim=8):
    if isinstance(date, str):
        date = date.encode("utf-8")
    straturi = []
    vazute = {date}
    for _ in range(maxim):
        try:
            text = date.decode("utf-8")
        except UnicodeDecodeError:
            break
        strat, rezultat = desfa(text)
        if strat == "necunoscut" or rezultat in vazute:
            break
        straturi.append(strat)
        date = rezultat
        vazute.add(date)
    return straturi, date


# Itemul 5
def sparge_xor(date):
    candidati = []
    frecvente = " etaoinshrdlucmfwypvbgkjqxz"
    for cheie in range(256):
        clar = bytes(octet ^ cheie for octet in date)
        if clar and all(32 <= c < 127 or c in (9, 10, 13) for c in clar):
            text = clar.decode("ascii")
            scor = sum(27 - frecvente.index(c) if c in frecvente else -5
                       for c in text.lower())
            candidati.append({"cheie": cheie, "rezultat": text, "scor": scor})
    return sorted(candidati, key=lambda c: c["scor"], reverse=True)


# Itemul 6
def algoritm_hash(tinta):
    if not re.fullmatch(r"[0-9a-fA-F]+", tinta):
        raise ValueError("Hash-ul trebuie sa contina doar cifre hexazecimale.")
    nume = {32: "md5", 40: "sha1", 64: "sha256"}.get(len(tinta))
    if nume is None:
        raise ValueError("Lungime necunoscuta: se accepta MD5, SHA1, SHA256.")
    return nume


def sparge_hash(tinta, wordlist):
    algoritm = algoritm_hash(tinta)
    with open(wordlist, encoding="latin1") as fisier:
        for rand in fisier:
            parola = rand.rstrip("\r\n")
            calculat = hashlib.new(algoritm, parola.encode("utf-8")).hexdigest()
            if calculat == tinta.lower():
                return algoritm, parola
    return algoritm, None


# Itemul 7
def main():
    parser = argparse.ArgumentParser(description="Decoder pentru laboratorul 5")
    parser.add_argument("intrare", help="Sir sau cale de fisier")
    parser.add_argument("--fisier", action="store_true")
    parser.add_argument("--mod", choices=["straturi", "xor", "hash"], default="straturi")
    parser.add_argument("--wordlist", type=Path, default=RADACINA / "probe/wordlist.txt")
    parser.add_argument("--iesire", type=Path, default=RADACINA / "arsenal/forensics/fisa.json")
    args = parser.parse_args()
    date = Path(args.intrare).read_bytes() if args.fisier else args.intrare.encode()
    if args.mod == "xor":
        candidati = sparge_xor(date)
        fisa = {"strat": "xor", "candidati": candidati,
                "observatie": "Scorul este euristic; verifica textul si cheia."}
    elif args.mod == "hash":
        rezultate = []
        for tinta in date.decode().splitlines():
            tinta = tinta.strip()
            if tinta:
                algoritm, parola = sparge_hash(tinta, args.wordlist)
                rezultate.append({"algoritm": algoritm, "hash": tinta, "parola": parola})
        fisa = {"strat": "hash", "rezultat": rezultate}
    else:
        straturi, rezultat = decodeaza_straturi(date)
        try:
            text = rezultat.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        fisa = {"strat": straturi, "rezultat": text, "hex": rezultat.hex()}
    args.iesire.parent.mkdir(parents=True, exist_ok=True)
    args.iesire.write_text(json.dumps(fisa, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(fisa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
