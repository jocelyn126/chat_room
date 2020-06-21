"""
author: Jocelyn
email:baccy126@126.com
time:2020-6-14
env:Python3.6
socket and Process exercise
"""
from multiprocessing import Process,Queue
from socket import *
HOST="0.0.0.0"
PORT=6007
ADDR=(HOST,PORT)

user_info={}

def do_login(sock, name, address):
    if name in user_info:
        sock.sendto(b"Fail",address) #这边自己写的时候没有想到要发信号
        return
    else:
        sock.sendto(b"OK", address)
        msg="欢迎%s 进入聊天室"%name#格式化的字符串不能直接encode
        for key in user_info:
            sock.sendto(msg.encode(),user_info[key])
        user_info[name]=address


def do_chat(sock, name, contant):
    msg="%s :%s"%(name,contant)
    for key in user_info or "管理" in name:
        if name!=key:
            sock.sendto(msg.encode(),user_info[key])


def do_quit(sock, name):
    if name in user_info:
        del user_info[name]
    msg="%s已经退出聊天室"%name
    for key in user_info:
        sock.sendto(msg.encode(),user_info[key])

def do_request(sock):
    while True:
        data, address = sock.recvfrom(1024)
        temp = data.decode().split(" ", 2)
        if temp[0] == "L":
            do_login(sock, temp[1], address)
        elif temp[0] == "C":
            do_chat(sock, temp[1], temp[2])
        elif temp[0] == "Q":
            do_quit(sock, temp[1])

def main():
    sock=socket(AF_INET,SOCK_DGRAM)
    sock.bind(ADDR)
    p=Process(target=do_request,args=(sock,))
    p.daemon=True
    p.start()
    while True:
        content=input("管理员消息：")
        if content=="quit":
            break
        msg="C 管理员消息 "+content
        sock.sendto(msg.encode(),("127.0.0.1",6009))

if __name__ == '__main__':
    main()
