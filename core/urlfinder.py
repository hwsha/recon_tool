from core.utils import run_command, get_diff


def passive_url_discovery(webservices, old_urls):
    print("[+] Running passive URL discovery with urlfinder...")
    input = "\n".join(webservices)
    urls = run_command("urlfinder -all -silent", input_data=input)
    print(f"\n[+] {len(urls)} urls found.")
    return get_diff(urls, old_urls, label="urls")

def active_url_discovery(webservices, old_urls):
    print("[+] Running active crawling with Katana...")
    input = "\n".join(webservices)
    urls = run_command("katana -silent", input_data=input)
    print(f"\n[+] {len(urls)} urls found.")
    return get_diff(urls, old_urls, label="urls")
