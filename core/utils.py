import subprocess
import os
import requests
from core.const import RESOLVERS_FILE, RESOLVERS_URL

def update_resolvers():
    print("[+] Updating resolvers list...")
    response = requests.get(RESOLVERS_URL, verify=False)
    if response.status_code == 200:
        with open(RESOLVERS_FILE, "w") as f:
            f.write(response.text)
        print(f"[+] {RESOLVERS_FILE} updated!")
    else:
        print("[-] Failed to download resolvers list.")
        return

def run_command(command, input_data=None):
    result = subprocess.run(
        command, input=input_data, shell=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output = result.stdout.strip().split('\n')
    return set(output) if output != [''] else set()
    
def extract_urls(httpx_output):
    urls = set()
    for line in httpx_output:
        parts = line.split(" ")
        if parts:
            url = parts[0].strip()
            if url.startswith("http"):
                urls.add(url)
    return urls 
    
def get_diff(new_set, old_set, label="placeholder"):
    diff = new_set - old_set
    if diff:
        print(f"[+] {len(diff)} new {label} found.")
        return diff
    else:
        print(f"[-] No new {label} found.")
        return set()

def load_old_results(path, target):
    subdomains_path = os.path.join(path, f"{target}_subdomains.txt")
    subdomains = set(open(subdomains_path).read().splitlines()) if check_path_exist(subdomains_path) else set()

    resolved_path = os.path.join(path, f"{target}_resolved.txt")
    resolved_domains = set(open(resolved_path).read().splitlines()) if check_path_exist(resolved_path) else set()

    webservices_path = os.path.join(path, f"{target}_webservices.txt")
    webservices = set(open(webservices_path).read().splitlines()) if check_path_exist(webservices_path) else set()

    urls_path = os.path.join(path, f"{target}_urls.txt")
    urls = set(open(urls_path).read().splitlines()) if check_path_exist(urls_path) else set()

    return subdomains, resolved_domains, webservices, urls


def check_path_exist(path):
    return os.path.exists(path)

def results_directory():
    target_name = input("Enter a name for saving results (e.g. netflix, facebook, etc.): ").strip()
    if not target_name:
        print("[!] Output name cannot be empty.")
        return
    
    results_directory_path = os.path.join("results", target_name)

    return target_name, results_directory_path

def save_results(file_path, results):
    with open(file_path, "a") as f:
        for item in sorted(results):
            f.write(item + "\n")