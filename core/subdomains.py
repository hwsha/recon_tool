from core.utils import run_command, get_diff

def gather_subdomains(target, old_subdomains):
    print(f"[+] Gathering subdomains for {target} ...")
    subdomains = run_command("subfinder -all -silent", input_data=target)
    print("\n[+] Subdomains Found:")
    for subdomain in subdomains:
        print(subdomain)
    
    return get_diff(subdomains, old_subdomains, label="subdomains")

def bruteforce_subdomains(target, old_resolved_domains):
    #This will actually bruteforce subdomains and resolve them
    print(f"[+] Brute-forcing subdomains for {target} ...")
    subdomains = run_command(f"dnsx -silent -w wordlists/subdomains.txt -d {target}")
    for subdomain in subdomains:
        print(subdomain)
    
    return get_diff(subdomains, old_resolved_domains, label="subdomains")