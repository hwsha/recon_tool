from core.utils import run_command, get_diff
import os

def gather_subdomains(target, old_subdomains):
    print(f"[+] Gathering subdomains for {target} using Subfinder...")
    subdomains = run_command(f"subfinder -all -silent -d {target}")
    print("\n[+] Subdomains Found:")
    for subdomain in subdomains:
        print(subdomain)
    
    return get_diff(subdomains, old_subdomains, label="subdomains")