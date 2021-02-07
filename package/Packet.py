def discover_packet(name, ip, score):
    return {
        'type': 'discover',
        'name': name,
        'ip': ip,
        'score': score
    }


def discover_reply_packet(name, ip, score):
    return {
        'type': 'discover_reply',
        'name': name,
        'ip': ip,
        'score': score
    }


def goodbye_packet(name, ip):
    return {
        'type': 'goodbye',
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
        'has_accepted': accept,
    }


def game_move_packet(name, ip, col):
    return {
        'type': 'game_move',
        'name': name,
        'ip': ip,
        'col': col,
    }


def chat_message_packet(name, ip, message):
    return {
        'type': 'chat_message',
        'name': name,
        'ip': ip,
        'message': message,
    }
