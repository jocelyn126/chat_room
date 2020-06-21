"""
chat room 客户端
发送请求， 获取结果
"""
import sys
from multiprocessing import Process
from socket import *

ADDR=("127.0.0.1",6007)


def login(sock):
    while True:
        name=input("请输入姓名：")
        msg="L "+name
        sock.sendto(msg.encode(),ADDR)
        data,address=sock.recvfrom(128)
        if data.decode()=="Fail":
            print("用户名已存在")
        else:
            print("欢迎进入聊天室")
            return name


def receive_message(sock):
    while True:
        data,address=sock.recvfrom(4096)
        msg = "\n" + data.decode() + "\n发言："
        print(msg,end="")


def chat(sock,name):
    while True:
        try:
            content=input("发言：")
        except:
            content="quit"
        if content=="quit":
            msg="Q "+name
            sock.sendto(msg.encode(),ADDR)
            sys.exit("您已退出聊天室")
        msg="C %s %s"%(name,content)
        sock.sendto(msg.encode(),ADDR)


def main():
    sock=socket(AF_INET,SOCK_DGRAM)
    sock.bind(("0.0.0.0",6009))
    name=login(sock) #name作为返回值这一步很难想到
    p=Process(target=receive_message,args=(sock,))
    p.daemon=True
    p.start()
    chat(sock,name)

if __name__ == '__main__':
    main()