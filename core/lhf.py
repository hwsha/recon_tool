from core.utils import run_command
from core.const import TEMPLATES

def scan_low_hanging_fruits(urls):
    print("[+] Preparing scan for low hanging fruits...")
    print(f"\n[!] {len(TEMPLATES)} templates loaded.")
    for template, path in TEMPLATES.items():
        print(template, "→", path)
    
    print(f"\n[!] Loaded {len(urls)} URLs.")
    # Identify URLs with parameters
    urls_with_params = [url for url in urls if "?" in url and "=" in url]

    if not urls_with_params:
        print("[!] No URLs with parameters found to scan.")
        return

    print(f"\n[!] Found {len(urls_with_params)} URLs with parameters.")
    
    input = "\n".join(urls_with_params)

    for template, path in TEMPLATES.items():
        print(f"\n[!] Running {template} scanner.")
        results = run_command(f"nuclei -silent -dast -t '{path}'", input_data=input)
        if results:
            print(f"[+] {template} findings:")
            for line in results:
                print(line)
        else:
            print(f"\n[!] No {template} found.")