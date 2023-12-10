import argparse
from netmiko import ConnectHandler

#Got the commands and synatx from various resource ,the commands I have explained to show what it does and the expected output
#used the vyos device 192.168.0.1 at mycanvas to configure https://mycanvas.mohawkcollege.ca/courses/93604/files/vyos.ova
#The VyOS documentation at https://mycanvas.mohawkcollege.ca/courses/93604/pages/week-four-second-class-operators-and-netmiko/netmikoexercise
# The VyOS documentation (https://docs.vyos.io/en/latest/automation/index.html) was used as a guide while developing this script for configuring VyOS devices.
# This script uses ChatGPT's recommendations to define command-line arguments for configuring a VyOS device.

# Functions for configuration tasks
def configure_vyos(device, interface, description):#this function will assign the vyos the configurations when called
    commands = [
        f'set interfaces ethernet {interface} description "{description}"',#this command assign the interface and the description of the vyos adapter
    ]
    device.send_config_set(commands)
    print(f"Interface {interface} description set to '{description}'")

def enable_nat(device):#NAT rules to be applied to the vyos when enabled
    commands = [
        'set nat source rule 100 outbound-interface eth0', # Outbound NAT rule for WAN interface traffic
        'set nat source rule 100 source address 192.168.56.0/24',# Source of the traffic
        'set nat source rule 100 translation address masquerade',# Use primary IP address of the outbound interface as its translation
    ]
    device.send_config_set(commands)
    print("NAT enabled")  # Output message 

def configure_dhcp(device, start_ip, end_ip):
    commands = [
        f'set service dhcp-server shared-network-name LAN subnet 192.168.56.0/24 start {start_ip} stop {end_ip}',# Setting DHCP scope
    ]
    device.send_config_set(commands)
    print(f"DHCP configured with scope {start_ip} - {end_ip}")

def enable_dns(device):
    commands = [
        'set service dns forwarding cache-size "0"',# Disabling DNS caching
        'set service dns forwarding listen-address "192.168.56.1"', # Listening address for DNS requests
        'set service dns forwarding allow-from "192.168.56.0/24"',  # Allowed subnet for DNS queries
    ]
    device.send_config_set(commands)
    print("DNS resolution enabled") # Output message

# CLI argument parser setup
parser = argparse.ArgumentParser(description="VyOS Configuration CLI")

# Arguments for configurations
parser.add_argument("--interface", help="Interface to configure")#This argument allows the user to specify the interface they want to configure on the VyOS device eg eth0
parser.add_argument("--description", help="Description for the interface")#This argument is used to provide a description for the specified interface.
parser.add_argument("--enable-nat", action="store_true", help="Enable NAT")#this flag is used in the , it triggers the script to enable  (NAT) on the VyOS device. 
parser.add_argument("--dhcp-scope", nargs=2, metavar=("START", "END"), help="DHCP scope addresses")#This argument expects two values - the starting and ending IP addresses for the DHCP scope.
parser.add_argument("--enable-dns", action="store_true", help="Enable DNS resolution")#enable DNS resolution on the VyOS device. DNS resolution translates domain names (like google.com) to IP addresses


# Request user to choose configurations
print("Choose configurations:")
print("1. Configure interface")#user will input an interface
print("2. Enable NAT")#user will decide whether to enable dns
print("3. Configure DHCP scope")#user will input the dhcp scope
print("4. Enable DNS resolution")#user will choose whether to perform dbs resolution

# Get user choices
user_choices = input("Enter the numbers (comma-separated) corresponding to your choices: ")
choices = [int(choice) for choice in user_choices.split(',')]

# Parse arguments and perform configurations based on user choices
# Process user choices
args = parser.parse_args()
# If the interface argument is not provided, prompt the user for input
if args.interface is None:
    args.interface = input("Enter interface: ")
    
    # If the description argument is not provided, prompt the user for input
if args.description is None:
    user_choice = input("Do you want to provide a description for the interface? (yes/no): ").lower()
    if user_choice == 'yes':
        args.description = input("Enter description for the interface: ")


# If enable_nat argument is False, ask the user whether to enable NAT
if not args.enable_nat:
    enable_nat_choice = input("Do you want to enable NAT? (yes/no): ").lower()
    args.enable_nat = enable_nat_choice == 'yes'

# If dhcp_scope argument is not provided, ask the user for DHCP scope information
if args.dhcp_scope is None:
    dhcp_scope_choice = input("Do you want to configure DHCP scope? (yes/no): ").lower()
    if dhcp_scope_choice == 'yes':
        start_ip = input("Enter DHCP start IP: ")
        end_ip = input("Enter DHCP end IP: ")
        args.dhcp_scope = [start_ip, end_ip]

# If enable_dns argument is False, ask the user whether to enable DNS resolution
if not args.enable_dns:
    enable_dns_choice = input("Do you want to enable DNS resolution? (yes/no): ").lower()
    args.enable_dns = enable_dns_choice == 'yes'

try:
    vyos_router = {
        "device_type": "vyos",
        "host": "192.168.56.1",
        "username": "vyos",  # Update with your VyOS username
        "password": "vyos",  # Update with your VyOS password
        "port": 22,
    }

    device = ConnectHandler(**vyos_router)
    print("Connected to VyOS device.")
# Perform configurations based on user choices
    if args.interface and args.description:
        configure_vyos(device, args.interface, args.description)#this will call the function and configure the device
    if args.enable_nat:
        enable_nat(device)
    if args.dhcp_scope:
        configure_dhcp(device, args.dhcp_scope[0], args.dhcp_scope[1])
    if args.enable_dns:
        enable_dns(device)

    device.disconnect()
    print("Disconnected from VyOS device.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

