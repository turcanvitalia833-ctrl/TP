"""Ruleaza toate etapele pe probele demonstrative si salveaza output-ul."""
import json
import subprocess
import sys
from pathlib import Path

RADACINA = Path(__file__).resolve().parent


# Itemul 16
def main():
    comenzi = [
        ["probe/pregateste_demo.py"],
        ["-m", "unittest", "discover", "-s", "teste", "-v"],
        ["arsenal/forensics/decode.py", "probe/mesaj.txt", "--fisier"],
        ["arsenal/forensics/decode.py", "probe/xor.bin", "--fisier", "--mod", "xor",
         "--iesire", "rezultate/xor.json"],
        ["arsenal/forensics/decode.py", "probe/hashuri.txt", "--fisier", "--mod", "hash",
         "--iesire", "rezultate/hashuri.json"],
        ["forensics.py", "probe/foto.jpg"],
        ["forensics.py", "probe/ascuns.png", "--arhiva", "gasit.zip", "--extrage-in", "extras"],
        ["stego.py", "ascunde", "probe/foto.jpg", "FLAG{ascuns_in_pixeli}", "stego.png"],
        ["stego.py", "dezvaluie", "stego.png"],
    ]
    with (RADACINA / "output_demo.txt").open("w", encoding="utf-8") as output:
        output.write("REZULTATE EXCLUSIV DEMONSTRATIVE\n")
        for comanda in comenzi:
            proces = subprocess.run([sys.executable, *comanda], cwd=RADACINA,
                                     capture_output=True, text=True)
            output.write("\npython3 " + " ".join(comanda) + "\n")
            output.write(proces.stdout + proces.stderr)
            if proces.returncode:
                raise RuntimeError("Comanda esuata: " + " ".join(comanda))
    fisa = json.loads((RADACINA / "arsenal/forensics/fisa.json").read_text())
    assert fisa["rezultat"] == "FLAG{straturi_demo}"
    assert (RADACINA / "extras/secret.txt").read_text() == "FLAG{arhiva_demo}"
    print("Toate etapele au trecut. Output: output_demo.txt")


if __name__ == "__main__":
    main()
