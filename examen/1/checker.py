import requests

SITES = []

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    return "https://{host.rstrip('/')}/{path.lstrip("/")"


def is_https(url):
    return url.startswith("https://")


def show_response(url):
    try:
        r = requests.get(url, timeout=5)
        print("Status:", r.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))

    except requests.RequestException as error:
        print("Eroare:", str(error))


def check_site(url):
    try:
        response = requests.get(url, timeout=5)

        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)[:150],
        }


def scan_sites():
    results = []

    for url in SITES:
        result = check_site(url)
        results.append((url, result))

    successful = [
        (url, result)
        for url, result in results
        if result.get("status") == 200
    ]

    failed_count = len(results) - len(successful)

    successful.sort(
        key=lambda item: item[1].get("length", 0),
        reverse=True,
    )

    for url, result in successful:
        print(
            f"{url} -> {result['status']}, "
            f"{result['length']} octeți"
        )

    print(
        f"Reușite: {len(successful)} | "
        f"Eșuate: {failed_count}"
    )


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)

        received_headers = {
            name.lower()
            for name in response.headers.keys()
        }

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in received_headers:
                present.append(header)
            else:
                missing.append(header)

        if SECURITY_HEADERS:
            score = round(
                len(present) / len(SECURITY_HEADERS) * 100
            )
        else:
            score = 100

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error)[:150],
        }


def retry_check(url, attempts=3):
    attempts = max(0, attempts)

    last_status = None
    last_error = None
    attempts_made = 0

    for _ in range(attempts):
        attempts_made += 1

        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            last_error = None

            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": attempts_made,
                }

        except requests.RequestException as error:
            last_status = None
            last_error = str(error)[:150]

    result = {
        "status": last_status,
        "attempts": attempts_made,
    }

    if last_error is not None:
        result["error"] = last_error

    return result