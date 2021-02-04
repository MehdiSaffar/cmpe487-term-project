def discover_packet(name, ip):
    return {
        'type': 'discover',
        'name': name,
        'ip': ip,
    }
def discover_reply_packet(name, ip):
    return {
        'type': 'discover_reply',
        'name': name,
        'ip': ip,
    }

def game_request_packet(name, ip):
    return {
        'type': 'game_request',
        'name': name,
        'ip': ip,
    }

def game_reply_packet(name, ip, accept: bool):
    return {
        'type': 'game_reply',
        'name': name,
        'ip': ip,
        'payload': accept,
    }