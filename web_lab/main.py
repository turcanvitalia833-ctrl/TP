# Laborator: functii, metode si importuri pe web
# Student: Turcan Vitalia


import argparse

# Exercitiul 44: 
import webtools

# Exercitiul 45: 
from webtools import get_title, security_headers, check_paths, save_report_csv



def main():
    # Exercitiul 48: 
    parser = argparse.ArgumentParser(
        description="Genereaza un raport despre un site web."
    )
    parser.add_argument(
        "url",
        nargs="?",
        default="https://cybercor.org",
        help="adresa site-ului de analizat (implicit: https://cybercor.org)",
    )
    argumente = parser.parse_args()
    url = argumente.url

    # Exercitiul 44: 
    raspuns_initial = webtools.fetch(url)
    print("Titlu (prin webtools.fetch + webtools.get_title):",
          webtools.get_title(raspuns_initial.text))

    # Exercitiul 45:
    print("Titlu (import direct get_title):", get_title(raspuns_initial.text))

    # Exercitiul 47: 
    print("DEFAULT_HEADERS:", webtools.DEFAULT_HEADERS)

    # Exercitiul 30: 
    print("Antete de securitate:", security_headers(url))

    # Exercitiul 49: 
    rezultate_cai = check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    save_report_csv(rezultate_cai, path="report.csv")
    print("Salvat in report.csv")

    # Exercitiul 50:
    webtools.site_report(url)


if __name__ == "__main__":
    main()

