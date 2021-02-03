def discover_packet(name, ip):
    return {
        'TYPE': 'DISCOVER',
        'NAME': name,
        'IP': ip,
    }