from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)

print("\n Partea 1: build_url")
print("Caz normal:", build_url("example.com", "login"))
print("Cu slash:", build_url("example.com", "/login"))

print("\n Partea 1: is_https")
print("HTTPS:", is_https("https://example.com"))
print("HTTP:", is_https("http://example.com"))



print("\nPartea 2: show_response")
show_response("https://example.com")
show_response("http://this-site-does-not-exist.invalid")



print("\n Partea 3: check_site")
print("Site funcțional:", check_site("https://example.com"))
print(
    "Site inexistent:",
    check_site("http://this-site-does-not-exist.invalid"),
)



print("\nPartea 4: scan_sites")
scan_sites()



print("\nPartea 5: check_headers")
print(
    "Site funcțional:",
    check_headers("https://example.com"),
)
print(
    "Site inexistent:",
    check_headers("http://this-site-does-not-exist.invalid"),
)



print("\nPartea 6: retry_check")
print(
    "Status 200:",
    retry_check("https://httpbin.org/status/200"),
)
print(
    "Status 404:",
    retry_check("https://httpbin.org/status/404"),
)
print(
    "Status 500:",
    retry_check("https://httpbin.org/status/500"),
)
print(
    "Site inexistent:",
    retry_check("http://this-site-does-not-exist.invalid"),
)