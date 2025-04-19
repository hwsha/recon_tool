from core.utils import run_command
import os

def passive_port_scan(ips, target, output_dir):
    print("[+] Passively scanning ports using Naabu...")
    ports = run_command("echo '" + "\n".join(ips) + "' | naabu -passive -silent -json")
    print("\n[+] Ports Found:")
    for port in ports:
        print(port)
    return save_new_results(os.path.join(output_dir, f"{target}_ports.txt"), ports)