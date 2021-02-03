def discover_packet(name, ip):
    return {
        'type': 'discover',
        'name': name,
        'ip': ip,
    }
def respond_packet(name, ip):
    return {
        'type': 'respond',
        'name': name,
        'ip': ip,
    }