import os
from core.utils import run_command


def passive_url_discovery(urls, target, output_dir):
    print("[+] Running passive URL discovery with urlfinder...")
    urls = run_command("echo '" + "\n".join(urls) + "' | urlfinder -all -silent")
    print("\n[+] Passive URLs Found:")
    for url in urls:
        print(url)
    return save_new_results(os.path.join(output_dir, f"{target}_passive_urls.txt"), urls)


def active_url_discovery(urls, target, output_dir):
    print("[+] Running active crawling with Katana...")
    urls = run_command("echo '" + "\n".join(urls) + "' | katana -silent")
    print("\n[+] Active URLs Found:")
    for url in urls:
        print(url)
    return save_new_results(os.path.join(output_dir, f"{target}_active_urls.txt"), urls)
