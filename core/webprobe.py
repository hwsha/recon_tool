from core.utils import run_command, get_diff

def probe_web_services(to_probe, old_webservices):
    print("[+] Probing web services using HTTPX...")
    input = "\n".join(to_probe)
    web_services = run_command("httpx -t 150 -nc -sc -title -td -fr -silent -random-agent -p 443,8080,8443,8000,8888,8080,8081,9000", input_data=input)
    print("\n[+] Web Services Found:")
    for service in web_services:
        print(service)
    
    return get_diff(web_services, old_webservices, label="web services")
