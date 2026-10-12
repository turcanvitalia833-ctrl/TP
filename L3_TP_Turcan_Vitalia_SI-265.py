NUME = "Colta"
PRENUME = "Iulian"
GRUPA = "SI-265"


# Itemul 1
def saluta():
    return "Hello, World!"


# Itemul 2
def celsius_in_fahrenheit(c):
    return c * 9 / 5 + 32


# Itemul 3
def cele_mai_mari_trei(numere):
    return sorted(numere, reverse=True)[:3]


# Itemul 4
def cat_si_rest(a, b):
    return a // b, a % b


# Itemul 5
def fisa_student(nume, grupa, media):
    return f"{nume} ({grupa}) - media {media:.2f}"


# Itemul 6
def initiale(nume_complet):
    rezultat = ""
    for cuvant in nume_complet.strip().split():
        rezultat += cuvant[0].upper() + "."
    return rezultat


# Itemul 7
def calificativ(nota):
    if nota >= 9:
        return "excelent"
    elif nota >= 7:
        return "bine"
    elif nota >= 5:
        return "satisfacator"
    else:
        return "nepromovat"


# Itemul 8
def fizzbuzz(n):
    rezultat = []
    for numar in range(1, n + 1):
        if numar % 3 == 0 and numar % 5 == 0:
            rezultat.append("FizzBuzz")
        elif numar % 3 == 0:
            rezultat.append("Fizz")
        elif numar % 5 == 0:
            rezultat.append("Buzz")
        else:
            rezultat.append(str(numar))
    return rezultat


# Itemul 9
def pret_final(pret, reducere=0):
    suma_reducerii = pret * reducere / 100
    return round(pret - suma_reducerii, 2)


# Itemul 10
class Student:
    def __init__(self, nume, grupa):
        self.nume = nume
        self.grupa = grupa
        self.note = []

    def adauga_nota(self, nota):
        self.note.append(nota)

    def media(self):
        if not self.note:
            return 0
        return round(sum(self.note) / len(self.note), 2)


# Itemul 11
def frecventa_litere(text):
    rezultat = {}
    for caracter in text:
        if caracter.isalpha():
            litera = caracter.lower()
            rezultat[litera] = rezultat.get(litera, 0) + 1
    return rezultat


# Itemul 12
def zile_intre(data1, data2):
    import datetime

    prima_data = datetime.datetime.strptime(data1, "%Y-%m-%d")
    a_doua_data = datetime.datetime.strptime(data2, "%Y-%m-%d")
    return abs((a_doua_data - prima_data).days)


# Itemul 13
def salveaza_si_incarca(cale, note):
    with open(cale, "w", encoding="utf-8") as fisier:
        for nota in note:
            fisier.write(str(nota) + "\n")

    rezultat = []
    with open(cale, "r", encoding="utf-8") as fisier:
        for rand in fisier:
            if rand.strip():
                rezultat.append(float(rand.strip()))
    return rezultat


# Misiunea 1
def misiunea_1(player):
    player.move_forward()
    player.move_forward()
    player.move_forward()
    player.move_forward()
    player.move_forward()


# Misiunea 2
def misiunea_2(player):
    player.move_forward()
    player.move_forward()
    player.move_forward()
    player.turn_right()
    player.move_forward()
    player.move_forward()
    player.move_forward()


# Misiunea 3
def misiunea_3(player):
    for pas in range(15):
        player.move_forward()


# Misiunea 4
def misiunea_4(player):
    for bustean in range(3):
        player.move_forward()
        player.move_forward()
        player.collect()
    player.move_forward()


# Misiunea 5
def misiunea_5(player):
    player.move_forward()
    player.move_forward()
    player.push()

    for pas in range(6):
        player.move_forward()


# Misiunea 6
def misiunea_6(player):
    player.move_forward()
    player.move_forward()
    player.collect()

    for bustean in range(3):
        player.move_forward()
        player.collect()

    player.move_forward()
    player.build("bridge")

    for pas in range(4):
        player.move_forward()


# Misiunea 7
def misiunea_7(player):
    player.move_forward()
    player.move_forward()
    player.push()

    for pas in range(3):
        player.move_forward()
    player.collect()

    for bustean in range(3):
        player.move_forward()
        player.collect()

    player.move_forward()
    player.turn_right()
    player.move_forward()
    player.move_forward()
    player.turn_right()
    player.move_forward()
    player.collect()