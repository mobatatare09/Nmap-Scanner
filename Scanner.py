import socket  # Built-in Python network library to handle connections
from concurrent.futures import ThreadPoolExecutor  # Manager to handle simultaneous worker threads


# =========================================================
# STEP 1: THE GUARD'S CHECKLIST (Performs the raw scan)
# =========================================================
def scan_single_port(target, port): 
    """
    Attempts a raw TCP handshake connection to a single port.
    Returns a formatted result string specifying if the port is open or closed.
    """
    try:
        # Creates a fresh socket instance for this specific thread.
        # AF_INET = IPv4 address family, SOCK_STREAM = TCP protocol connection.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            # Sets a connection timeout (1.5 seconds) so individual threads don't hang forever
            s.settimeout(1.5)
            
            # connect_ex tries to complete a 3-way handshake. 
            # It returns a status code number instead of throwing an error if it fails.
            result = s.connect_ex((target, port)) 
            
            # If result is exactly 0, the TCP handshake was successful!
            if result == 0:
                # Try to guess the common service name based on the port number
                try:
                    service_name = socket.getservbyport(port, 'tcp')
                except:
                    service_name = "unknown"
                    
                return f"Port: {port}\tState: open\tService: {service_name}"
                
    except Exception as e:
        return f"Error scanning port {port} on {target}: {e}"
        
    # If the connection did not return 0, the port is considered closed
    return f"Port: {port}\tState: closed/filtered"


# =========================================================
# STEP 2: THE STARTING TRIGGER (The Supervisor Block at the Bottom)
# =========================================================
if __name__ == "__main__":
    # Prompts the user to enter the target details
    target = input("Enter the target IP address or Domain (e.g., 192.168.1.1): ") 
    port_list_input = input("Enter the ports to scan (e.g., 22,80, 1-443): ") 
    
    # Initialize an empty master list to hold our final integer ports
    port_list = []
    
    # Split the input string into individual parts using commas
    raw_parts = port_list_input.split(',')
    
    # Loop through each part to parse single numbers and ranges
    for part in raw_parts:
        part = part.strip()  # Clean up any accidental blank spaces
        
        # Check if this specific part is a range (contains a dash '-')
        if '-' in part:
            try:
                # Split at the dash to isolate the start and end port numbers
                start_str, end_str = part.split('-')
                start_port = int(start_str.strip())
                end_port = int(end_str.strip())
                
                # Generate all numbers from start to end (inclusive) and add them to the master list
                for p in range(start_port, end_port + 1):
                    port_list.append(p)
            except ValueError:
                print(f"[!] Skipping invalid range formatting: '{part}'")
                
        # If it's just a single independent number, verify it and add it directly
        elif part.isdigit():
            port_list.append(int(part))
            
    # Quick safety check to ensure we actually have valid ports to scan
    if not port_list:
        print("[!] No valid ports detected. Exiting program.")
        exit()
    
    print(f"\nScanning {target} on {len(port_list)} unique ports using pure Python sockets... Please wait...\n")
    
    # Uses a ThreadPoolExecutor to manage concurrent scanning of multiple ports.
    # max_workers limits the number of active threads to 10 for efficient scanning.
    with ThreadPoolExecutor(max_workers=10) as executor: 
        
        # executor.map automatically hands the target and individual port numbers 
        # out to the available worker threads.
        results = executor.map(lambda p: scan_single_port(target, p), port_list)
        
        print("--------------------------- RESULTS -------------------------") 
        
        # Loops through the collected results from all threads as they finish and prints them.
        for result in results: 
            if result:
                print(result)