"""
author: Jocelyn
email:baccy126@126.com
time:2020-6-13
env:Python3.6
socket and Process exercise
"""
from multiprocessing import Process
from socket import *
#服务器地址
HOST="0.0.0.0"
PORT=8000
ADDR=(HOST,PORT)

#存储用户{name:address..}
user={}

#处理登录请求
def do_login(sock,name,address):
    if name in user:
        sock.sendto(b"Fail",address)
        return
    else:
        sock.sendto(b"OK", address)
        #通知其他人
        msg="欢迎%s进入聊天室"%name
        for i in user:
            sock.sendto(msg.encode(),user[i])
        #存储用户
        user[name]=address


#转发消息
def do_chat(sock,name,message):
    msg="%s :%s"%(name,message)
    for i in user or "管理" in name:
        if i != name:
            sock.sendto(msg.encode(),user[i])


#退出
def do_quit(sock, name):
    del user[name] #先删除这个人， 就不用跳过这个人去通知其他人了
    msg = "%s 退出聊天室" % name
    for i in user:
        sock.sendto(msg.encode(), user[i])

def do_request(sock):
    # 循环接收用户请求
    while True:
        # 接收用户请求(所有客户端的所有请求都向这里发送)
        data, addr = sock.recvfrom(1024)
        tmp = data.decode().split(" ", 2)
        # 根据请求调用模块
        if tmp[0] == "L":
            # tmp-->['L','name']
            do_login(sock, tmp[1], addr)
        elif tmp[0] == "C":
            # tmp-->['C','name','content']
            do_chat(sock, tmp[1], tmp[2])
        elif tmp[0] == "Q":
            # tmp-->['Q','name']
            do_quit(sock, tmp[1])

#程序启动函数
def main():
    sock=socket(AF_INET,SOCK_DGRAM) #UDP
    sock.bind(ADDR)
    do_request(sock)

    #创建进程
    p=Process(target=do_request,args=(sock,))
    p.daemon=True
    p.start()

    #父进程 发送管理员消息
    while True:
        content=input("管理员消息：")
        if content=="quit": #操作整个服务端程序的口令， 是quit整个服务器全部结束
            break
        msg="C 管理员消息 "+content
        sock.sendto(msg.encode(),("127.0.0.1",6009)) #发消息给子进程



if __name__ == '__main__':
    main()
