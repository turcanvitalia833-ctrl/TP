"""Generator demonstrativ; nu este scriptul original al profesorului."""
import base64
import hashlib
import io
import zipfile
from pathlib import Path
from urllib.parse import quote
from PIL import Image
from PIL.TiffImagePlugin import IFDRational


# Itemul 14
def main():
    folder = Path(__file__).resolve().parent
    mesaj = "FLAG{straturi_demo}"
    url = quote(mesaj, safe="")
    folder.joinpath("mesaj.txt").write_text(
        base64.b64encode(url.encode().hex().encode()).decode(), encoding="utf-8")
    clar = b"The secret message is FLAG{xor_demo}."
    folder.joinpath("xor.bin").write_bytes(bytes(c ^ 42 for c in clar))
    parola = "student265"
    folder.joinpath("wordlist.txt").write_text("parola\npython\nstudent265\nsalut\n")
    folder.joinpath("hashuri.txt").write_text("\n".join(
        hashlib.new(a, parola.encode()).hexdigest() for a in ("md5", "sha1", "sha256")))
    imagine = Image.new("RGB", (160, 120), (120, 160, 200))
    exif = Image.Exif()
    exif[271] = "Camera demonstrativa"
    exif[315] = "Colta Iulian"
    exif[34853] = {1: "N", 2: (IFDRational(47), IFDRational(0), IFDRational(0)),
                   3: "E", 4: (IFDRational(28), IFDRational(50), IFDRational(0))}
    imagine.save(folder / "foto.jpg", exif=exif)
    png = io.BytesIO()
    imagine.save(png, format="PNG")
    arhiva = io.BytesIO()
    with zipfile.ZipFile(arhiva, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("secret.txt", "FLAG{arhiva_demo}")
    folder.joinpath("ascuns.png").write_bytes(png.getvalue() + arhiva.getvalue())
    print("Probe DEMONSTRATIVE generate; pentru predare foloseste probele originale.")


if __name__ == "__main__":
    main()
