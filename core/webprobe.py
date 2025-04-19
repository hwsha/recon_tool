from core.utils import run_command, get_diff
import os

def probe_web_services(to_probe, old_webservices):
    print("[+] Probing web services using HTTPX...")
    input = "\n".join(to_probe)
    web_services = run_command("httpx -mc 403,401,200 -nc -x all -sc -title -td -fr -silent -p 80,443,8080,8443,8000,8888,8080,3000,5000,7000,9000,9200,5601,10443", input_data=input)
    print("\n[+] Web Services Found:")
    for service in web_services:
        print(service)
    
    return get_diff(web_services, old_webservices, label="web services")
