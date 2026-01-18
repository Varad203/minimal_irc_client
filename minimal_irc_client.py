import socket
import threading
import sys

SERVER = "irc.libera.chat"
PORT = 6667
CHANNEL = "#testchannel"
NICK = "PyUser123"

def receive(sock):
    while True:
        try:
            data = sock.recv(2048).decode("utf-8", errors="ignore")
            if data.startswith("PING"):
                sock.sendall(f"PONG {data.split()[1]}\r\n".encode())
            else:
                print(data.strip())
        except:
            break

def send(sock):
    while True:
        msg = input()
        if msg.startswith("/join"):
            chan = msg.split()[1]
            sock.sendall(f"JOIN {chan}\r\n".encode())
        elif msg.startswith("/quit"):
            sock.sendall(b"QUIT\r\n")
            sock.close()
            sys.exit()
        else:
            sock.sendall(f"PRIVMSG {CHANNEL} :{msg}\r\n".encode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER, PORT))

sock.sendall(f"NICK {NICK}\r\n".encode())
sock.sendall(f"USER {NICK} 0 * :{NICK}\r\n".encode())
sock.sendall(f"JOIN {CHANNEL}\r\n".encode())

threading.Thread(target=receive, args=(sock,), daemon=True).start()
send(sock)
