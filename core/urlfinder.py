import os
from core.utils import run_command, get_diff


def passive_url_discovery(webservices, old_urls):
    print("[+] Running passive URL discovery with urlfinder...")
    urls = run_command("echo '" + "\n".join(webservices) + "' | urlfinder -all -silent")
    print("\n[+] URLs Found:")
    for url in urls:
        print(url)
    return get_diff(webservices, old_urls, label="urls")

def active_url_discovery(webservices, old_urls):
    print("[+] Running active crawling with Katana...")
    urls = run_command("echo '" + "\n".join(webservices) + "' | katana -silent")
    print("\n[+] URLs Found:")
    for url in urls:
        print(url)
    return get_diff(webservices, old_urls, label="urls")
