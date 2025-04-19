import subprocess
import os

def run_command(command):
    try:
        return set(subprocess.check_output(command, shell=True, text=True).strip().split('\n'))
    except subprocess.CalledProcessError:
        return set()
    
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
        print(f"[+] New {label} found:")
        for entry in diff:
            print(entry)
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