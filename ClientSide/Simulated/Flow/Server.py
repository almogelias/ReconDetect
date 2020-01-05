import socket

port = 3389


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind(('0.0.0.0', port))

serv.listen(1)

print('socket binded to port', port)



serv.listen(5)

print("socket is listening")


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
