from core.utils import run_command, get_diff
from core.const import RESOLVERS_FILE,SUBDOMAINS_WORDLIST

def gather_subdomains(target, old_subdomains):
    print(f"[+] Gathering subdomains for {target} ...")
    subdomains = run_command("subfinder -all -silent", input_data=target)
    print(f"\n[+] {len(subdomains)} subdomains found.")
    return get_diff(subdomains, old_subdomains, label="subdomains")

def bruteforce_subdomains(target, old_resolved_domains):
    #This will actually bruteforce subdomains and resolve them
    print(f"[+] Brute-forcing subdomains for {target} ...")
    subdomains = run_command(f"shuffledns -d {target} -r {RESOLVERS_FILE} -silent -w {SUBDOMAINS_WORDLIST} -mode bruteforce")
    print(f"\n[+] {len(subdomains)} subdomains found using bruteforce.")
    return get_diff(subdomains, old_resolved_domains, label="subdomains")