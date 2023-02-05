import ipaddress

def get_subnet_range(ip_cidr):
    # Create an IPv4Network object from the IP address and subnet mask
    network = ipaddress.IPv4Network(ip_cidr, strict=False)
    # Get the first and last IP addresses in the subnet
    first_ip = str(network.network_address)
    last_ip = str(network.broadcast_address)
    return (first_ip, last_ip)

def get_subnet_range_binary(ip_cidr):
    ip_address, cidr = ip_cidr.split("/")
    # Convert IP address to binary
    ip_address_binary = '.'.join([bin(int(x) + 256)[3:] for x in ip_address.split(".")])
    # Get the number of bits in the subnet mask
    cidr = int(cidr)
    # Get the subnet mask in binary
    subnet_binary = "1"*cidr + "0"*(32-cidr)
    # Divide the subnet mask into four 8-bit octets
    subnet_binary = ".".join([subnet_binary[i:i+8] for i in range(0, len(subnet_binary), 8)])
    return (ip_address_binary, subnet_binary)

def binary_to_ipv4(binary_ip):
    # Split the binary IP address into octets
    octets = binary_ip.split(".")
    # Convert each octet to decimal
    decimals = [int(octet, 2) for octet in octets]
    # Join the decimal octets with '.' to form the normal IP address
    return '.'.join(map(str, decimals))


# Example usage
ip_cidr = "192.168.56.0/21"
first_ip, last_ip = get_subnet_range(ip_cidr)
print("First IP:", first_ip)
print("Last IP:", last_ip)
ip_address_binary, subnet_binary = get_subnet_range_binary(ip_cidr)
print("IP address in binary:",ip_address_binary)
print("Subnet mask in binary:",subnet_binary)
print("IP address:",binary_to_ipv4(ip_address_binary))
print("Subnet mask:",binary_to_ipv4(subnet_binary))
binary_ip = "11000000.10101000.00111000.00000000"
normal_ip = binary_to_ipv4(binary_ip)
print("Normal IP:", normal_ip)
