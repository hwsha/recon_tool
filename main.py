import argparse
import os
from core.utils import results_directory, check_path_exist, load_old_results, save_results, extract_urls, update_resolvers
from core.subdomains import gather_subdomains, bruteforce_subdomains
from core.resolver import resolve_domains
from core.webprobe import probe_web_services
from core.urlfinder import passive_url_discovery, active_url_discovery
from core.lhf import scan_low_hanging_fruits

def main():
    parser = argparse.ArgumentParser(description="Passive recon automation script")
    parser.add_argument("-t", "--target", help="Single target domain")
    parser.add_argument("-f", "--file", help="File containing list of targets")
    parser.add_argument("-b","--bruteforce-subdomains", action="store_true", help="Subdomain bruteforce")
    parser.add_argument("-puc","--passive-url-crawler", action="store_true", help="Passive URL discovery")
    parser.add_argument("-auc","--active-url-crawler", action="store_true", help="Active URL discovery")
    parser.add_argument("-lhf", "--low-hanging-fruit", action="store_true", help="Scan for low hanging fruits")
    parser.add_argument("-ss","--skip-subdomains", action="store_true", help="Skip subdomain enumeration")
    parser.add_argument("-sr","--skip-resolution", action="store_true", help="Skip DNS resolution")
    parser.add_argument("-sw","--skip-web", action="store_true", help="Skip web probing")
    args = parser.parse_args()

    target_name, results_path = results_directory()

    results_path_exist = check_path_exist(results_path)

    if results_path_exist:
        print(f"[!] Directory '{results_path}' already exists. Loading old results..")
        old_subdomains, old_resolved_domains, old_webservices, old_urls = load_old_results(results_path,target_name)
    else:
        print(f"[+] Creating directory '{results_path}' for results.")
        os.makedirs(results_path, exist_ok=True)
        old_subdomains, old_resolved_domains, old_webservices, old_urls = set(), set(), set(), set()

    targets = set()
    new_subdomains = set()
    to_resolve = set(old_subdomains)
    to_probe = set(old_resolved_domains)
    to_crawl = set(extract_urls(old_webservices))
    urls = set(old_urls)

    if args.target:
        targets.add(args.target)
    elif args.file:
        if os.path.exists(args.file):
            with open(args.file, "r") as f:
                targets.update(line.strip() for line in f.readlines() if line.strip())
        else:
            print("[!] File not found.")
            return
    else:
        print("[!] Please specify a target (-t) or a file (-f).")
        return

    update_resolvers()

    for target in targets:
        if not args.skip_subdomains:
            new_subdomains = gather_subdomains(target, old_subdomains)
            if new_subdomains:
                save_results(os.path.join(results_path, f"{target_name}_subdomains.txt"), new_subdomains)
                print(f"[+] Saved to {target_name}_subdomains.txt")
                to_resolve.update(new_subdomains)

    if not args.skip_resolution:
        if to_resolve:
            new_resolved_domains = resolve_domains(to_resolve, old_resolved_domains)
            if new_resolved_domains:
                save_results(os.path.join(results_path, f"{target_name}_resolved.txt"), new_resolved_domains)
                print(f"[+] Saved to {target_name}_resolved.txt")
                old_resolved_domains.update(new_resolved_domains)
                to_probe.update(new_resolved_domains)
    
    if args.bruteforce_subdomains:
        for target in targets:
            bf_subdomains = bruteforce_subdomains(target, old_resolved_domains)
            if bf_subdomains:
                save_results(os.path.join(results_path, f"{target_name}_resolved.txt"), bf_subdomains)
                print(f"[+] Saved to {target_name}_resolved.txt")
                to_probe.update(bf_subdomains)

    if not args.skip_web:
        if to_probe:
            new_web_services = probe_web_services(to_probe, old_webservices)
            if new_web_services:
                save_results(os.path.join(results_path, f"{target_name}_webservices.txt"), new_web_services)
                print(f"[+] Saved to {target_name}_webservices.txt")
                to_crawl.update(extract_urls(new_web_services))
        
    if args.passive_url_crawler:
        if to_crawl:
            new_urls = passive_url_discovery(to_crawl, old_urls)
            if new_urls:
                save_results(os.path.join(results_path, f"{target_name}_urls.txt"), new_urls)
                print(f"[+] Saved to {target_name}_urls.txt")
                urls.update(new_urls)
    
    if args.active_url_crawler:
        if to_crawl:
            new_urls = active_url_discovery(to_crawl, old_urls)
            if new_urls:
                save_results(os.path.join(results_path, f"{target_name}_urls.txt"), new_urls)
                print(f"[+] Saved to {target_name}_urls.txt")
                urls.update(new_urls)
    
    if args.low_hanging_fruit:
        if urls:
            scan_low_hanging_fruits(urls)


    print(f"\n[+] Automatic Recon Complete. Results saved in {results_path}.")

if __name__ == "__main__":
    main()
