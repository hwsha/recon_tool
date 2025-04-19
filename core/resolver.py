from core.utils import run_command, get_diff
import os

def resolve_domains(domains, old_resolved_domains):
    print("[+] Resolving domains using dnsx...")
    input = "\n".join(domains)
    resolved_domains = run_command("dnsx -silent", input_data=input)
    print("\n[+] Resolved Domains:")
    for domain in resolved_domains:
        print(domain)
    return get_diff(resolved_domains, old_resolved_domains, label="resolved domains")

def gather_ips(domains, target, output_dir):
    print("[+] Extracting IP addresses...")
    ips = run_command("echo '" + "\n".join(domains) + "' | dnsx -resp-only -silent")
    print("\n[+] IP Addresses Found:")
    for ip in ips:
        print(ip)
    return save_new_results(os.path.join(output_dir, f"{target}_ips.txt"), ips)