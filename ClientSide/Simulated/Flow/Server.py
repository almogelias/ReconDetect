import socket

PORT = 8080

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('0.0.0.0', PORT))
serv.listen(5)

while True:
    conn, addr = serv.accept()
    from_client = ''

    while True:
        data = conn.recv(4096)
        if not data: break
        from_client=''
        from_client += data.decode('utf-8')
        print (from_client)
        msg = "I am SERVER\n".encode('utf-8')
        conn.send(msg)

    conn.close()
    print ('client disconnected')
