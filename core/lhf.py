from core.utils import run_command

# Path to your custom nuclei template
TEMPLATE_PATH = "custom-templates/open_redirect.yaml"

def scan_open_redirects(urls):
    print("[+] Scanning for open redirects...")
    print(f"\n[!] Loaded {len(urls)} URLs.")

    # Identify URLs with parameters
    urls_with_params = [url for url in urls if "?" in url and "=" in url]

    if not urls_with_params:
        print("[!] No URLs with parameters found to scan.")
        return

    print(f"\n[!] Found {len(urls_with_params)} URLs with parameters.")
    print(f"\n[+] Scanning {len(urls_with_params)} URLs for open redirects...")

    input = "\n".join(urls_with_params)
    results = run_command(f"nuclei -silent -dast -t '{TEMPLATE_PATH}'", input_data=input)

    for line in results:
        print(line)
