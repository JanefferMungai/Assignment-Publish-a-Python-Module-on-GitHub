# Assignment-Publish-a-Python-Module-on-GitHub
# NAME JANEFFER MUNGAI
# ID 000832881
# Configure vyos device
# The Vyos router virtual machine.
# The Vyos router device configuration is as follows:
 One HostOnly Network Adapter
 One Internal Network (DMZNet)
 The Internal Network (eth4) is the LAN interface
 The HostOnly adapter (eth5) is the WAN interface
 The LAN  address is 192.168.56.1/24
 The WAN address is configured for DHCP (enable VirtualBox DHCP services)
 The username is vyos
 The password is vyos
# The Windows 10 Virtual Machine:
 One HostOnly Network Adapter
 One NAT
# Run the file as follow
#first ensure you are in the right folder on your device
PS C:\Users\CSAIT> python vyos.py
# THIS IS THE OUTPUT FILL IT AS IT SHOWS
Choose configurations:
1. Configure interface
2. Enable NAT
3. Configure DHCP scope
4. Enable DNS resolution
Enter the numbers (comma-separated) corresponding to your choices: 1
Enter interface: eth5
Do you want to provide a description for the interface? (yes/no): yes
Enter description for the interface: WAN
Do you want to enable NAT? (yes/no): yes
Do you want to configure DHCP scope? (yes/no): yes
Enter DHCP start IP: 192.168.56.100
Enter DHCP end IP: 192.168.56.254
Do you want to enable DNS resolution? (yes/no): yes
Connected to VyOS device.
Interface eth5 description set to 'WAN'
NAT enabled
DHCP configured with scope 192.168.56.100 - 192.168.56.254
DNS resolution enabled
Disconnected from VyOS device.
PS C:\Users\CSAIT>