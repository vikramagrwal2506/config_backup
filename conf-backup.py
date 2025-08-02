import netmiko
import getpass # For securely getting password input

# --- User Credentials (can be hardcoded for testing, but secure input is recommended) ---
username = "vikram.agarwal"
password = "2Q90BhtyK-z-"

# --- Read Device List ---
devices_file = "devices.txt"
with open(devices_file, 'r') as f:
    device_ips = [line.strip() for line in f if line.strip()]

# --- Read Commands ---
commands_file = "commands.txt"
with open(commands_file, 'r') as f:
    commands_to_send = [line.strip() for line in f if line.strip()]

# --- Process Each Device ---
for ip in device_ips:
    print(f"\n--- Connecting to {ip} ---")
    try:
        device_info = {
            'device_type': 'cisco_ios',  # Adjust device_type as needed (e.g., 'juniper_junos', 'arista_eos')
            'host': ip,
            'username': username,
            'password': password,
        }
        
        net_connect = netmiko.ConnectHandler(**device_info)
        
        # --- Send Commands and Capture Output ---
        output_filename = f"{ip}_output.txt"
        with open(output_filename, 'w') as outfile:
            outfile.write(f"--- Output for Device: {ip} ---\n\n")
            for command in commands_to_send:
                print(f"Sending command: {command}")
                output = net_connect.send_command(command)
                outfile.write(f"Command: {command}\n")
                outfile.write(output)
                outfile.write("\n" + "="*80 + "\n\n") # Separator for clarity
        
        print(f"Output for {ip} saved to {output_filename}")
        net_connect.disconnect()
        
    except netmiko.NetmikoTimeoutException:
        print(f"Error: Timeout connecting to {ip}. Check connectivity or credentials.")
    except netmiko.NetmikoAuthenticationException:
        print(f"Error: Authentication failed for {ip}. Check username/password.")
    except Exception as e:
        print(f"An unexpected testing ke liye change kiya hai error occurred with {ip}: {e}")
