from socket import socket

default_header_size = 10
default_size_pack = 1024
encoding = '866'  # OEM866 / cp866


def send_msg(conn: socket, msg: bytes, header_size: int = default_header_size) -> bool:
    size_msg = f'{len(msg):{header_size}}'


    if conn.send(size_msg.encode(encoding=encoding)) != header_size:
        print("ERROR: can't send size message")
        return False



    if conn.send(msg) != len(msg):
        print("ERROR: can't send message")
        return False

    return True


def recv_msg(conn: socket, header_size: int = default_header_size, size_pack: int = default_size_pack):
    data = conn.recv(header_size)
    if not data:
        return False

    size_msg = int(data.decode(encoding=encoding))
    msg = b''

    while True:
        if size_msg <= size_pack:
            data = conn.recv(size_msg)
            if not data:
                return False

            msg += data
            break

        data = conn.recv(size_pack)
        if not data:
            return False

        size_msg -= size_pack
        msg += data

    return msg.decode()
