import socket

# Dynamically get the local IP address
local_ip = socket.gethostbyname(socket.gethostname())

# Update the DNS records with the local IP
dns_records = {"webcraft.local": local_ip}

def resolve(domain):
    return dns_records.get(domain, "Domain not found.")
