"""
chat room 客户端
发送请求， 获取结果
"""
import sys
from socket import *
from multiprocessing import Process

ADDR=("119.3.161.197",8000)


def login(sock):
    while True:
        name=input("Name:")
        msg="L "+name
        sock.sendto(msg.encode(),ADDR)
        result,add=sock.recvfrom(1024)
        if result.decode()=="OK":
            print("进入聊天室")
            return name
        else:
            print("该用户已存在")

#接收消息
def receive_msg(sock):
    while True:
        data,addr=sock.recvfrom(4096)
        msg="\n"+data.decode()+"\n发言："
        print(msg,end="") #打印之后不换行

#发送消息
def send_msg(sock,name):
    while True:
        try:
            message=input("发言：")
        except:
            message="quit"
        if message =="quit":
            msg="Q "+name
            sock.sendto(msg.encode(),ADDR)
            sys.exit("您已退出聊天室")
        msg="C %s %s"%(name,message)
        sock.sendto(msg.encode(),ADDR) #发送消息给服务器


def main():
    sock=socket(AF_INET,SOCK_DGRAM)
    sock.bind(("0.0.0.0",6009))
    name=login(sock) #name 进入聊天室 拿login的返回值
    #创建子进程
    p=Process(target=receive_msg,args=(sock,))
    p.daemon=True #这是个进程属性， 设置成True就是父进程退出带走子进程
    p.start()
    send_msg(sock,name) #发送消息

if __name__ == '__main__':
    main()