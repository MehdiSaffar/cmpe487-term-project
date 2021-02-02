# I had to use these because
# asyncio does not provide async methods for recvfrom and sendto
def sock_recvfrom(loop, sock, n_bytes, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_reader(fd)

    try:
        data, addr = sock.recvfrom(n_bytes)
    except (BlockingIOError, InterruptedError):
        loop.add_reader(fd, sock_recvfrom, loop, sock, n_bytes, fut, True)
    else:
        fut.set_result((data, addr))
    return fut


def sock_sendto(loop, sock, data, addr, fut=None, registed=False):
    """
    CREDITS TO https://pysheeet-kr.readthedocs.io/ko/latest/notes/python-asyncio.html#simple-asyncio-udp-echo-server 
    """
    fd = sock.fileno()
    if fut is None:
        fut = loop.create_future()
    if registed:
        loop.remove_writer(fd)
    if not data:
        return

    try:
        n = sock.sendto(data, addr)
    except (BlockingIOError, InterruptedError):
        loop.add_writer(fd, sock_sendto, loop, sock, data, addr, fut, True)
    else:
        fut.set_result(n)
    return fut
