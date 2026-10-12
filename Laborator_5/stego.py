import argparse
from pathlib import Path
from PIL import Image


# Itemul 12
def ascunde(cale, mesaj, iesire):
    if "\0" in mesaj:
        raise ValueError("Mesajul nu poate contine octetul nul.")
    if Path(iesire).suffix.lower() != ".png":
        raise ValueError("Rezultatul trebuie salvat ca PNG.")
    with Image.open(cale) as sursa:
        imagine = sursa.convert("RGB")
    date = mesaj.encode("utf-8") + b"\0"
    biti = [int(bit) for octet in date for bit in f"{octet:08b}"]
    if len(biti) > imagine.width * imagine.height * 3:
        raise ValueError("Imaginea este prea mica pentru mesaj.")
    pixeli = list(imagine.get_flattened_data() if hasattr(imagine, "get_flattened_data") else imagine.getdata())
    for index, bit in enumerate(biti):
        pozitie, canal = divmod(index, 3)
        pixel = list(pixeli[pozitie])
        pixel[canal] = (pixel[canal] & ~1) | bit
        pixeli[pozitie] = tuple(pixel)
    imagine.putdata(pixeli)
    Path(iesire).parent.mkdir(parents=True, exist_ok=True)
    imagine.save(iesire, format="PNG")


# Itemul 13
def dezvaluie(cale):
    with Image.open(cale) as sursa:
        imagine = sursa.convert("RGB")
    rezultat = bytearray()
    octet = numar = 0
    for pixel in (imagine.get_flattened_data() if hasattr(imagine, "get_flattened_data") else imagine.getdata()):
        for canal in pixel:
            octet = (octet << 1) | (canal & 1)
            numar += 1
            if numar == 8:
                if octet == 0:
                    return rezultat.decode("utf-8")
                rezultat.append(octet)
                octet = numar = 0
    raise ValueError("Nu s-a gasit terminatorul mesajului.")


def main():
    parser = argparse.ArgumentParser()
    comenzi = parser.add_subparsers(dest="comanda", required=True)
    scriere = comenzi.add_parser("ascunde")
    scriere.add_argument("imagine")
    scriere.add_argument("mesaj")
    scriere.add_argument("iesire")
    citire = comenzi.add_parser("dezvaluie")
    citire.add_argument("imagine")
    args = parser.parse_args()
    if args.comanda == "ascunde":
        ascunde(args.imagine, args.mesaj, args.iesire)
        print("Mesaj salvat in", args.iesire)
    else:
        print(dezvaluie(args.imagine))


if __name__ == "__main__":
    main()
