import socket
from concurrent.futures import ThreadPoolExecutor  # Manages multiple threads for fast scanning


def banner(ip, port):
    # 1. Initialize the socket wrapper.
    # AF_INET specifies IPv4 addresses, SOCK_STREAM specifies TCP connections.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    # 2. Set a 3second timeout so the script doesn't freeze forever if the host is silent
    s.settimeout(3.0)
    

    print(f"\n[!] Connecting to {ip} on port {port}...")
    
    try:
        # 3. Use connect_ex to safely check the connection status without crashing
        result = s.connect_ex((ip, int(port)))
        
        # If result is exactly 0, the TCP handshake succeeded and the port is open!
        if result == 0:
            print("[+] Connection successful! Waiting for banner...")
            
            # 4. If it's a web port (80, 8080), we must send an HTTP request to force it to reply
            if int(port) in [80, 8080]:
                s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            
            # 5. Receive the raw bytes from the target machine
            raw_data = s.recv(1024)
            
            # 6. Decode the raw network binary bytes into clean, human-readable text
            clean_banner = raw_data.decode('utf-8', errors='ignore').strip()
            
            print(f"\n------------------- SUCCESSFUL BANNER GRAB -------------------")
            print(clean_banner)
            print("-----------------------------------------------------------------")
        else:
            print(f"[-] Could not connect. Port {port} appears closed or filtered (Error Code: {result}).")
            
    except socket.timeout:
        print("[-] The connection timed out. The port is open but the service stayed silent.")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")
    finally:
        # 7. Always close the connection to clean up network resources
        s.close()

def main():
    # Prompt the user for clean target details
    ip = input("Enter the target IP Address or Domain: ")
    port = int(input("Enter the target port: "))
    banner(ip, port)

# Protects the script execution entry point
if __name__ == "__main__":
    main()