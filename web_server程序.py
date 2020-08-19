"""
web server
"""

from socket import *
from select import select
import re

class WebServer():
    def __init__(self,host='0.0.0.0',port=80,html=None):
        self.host=host
        self.port=port
        self.html=html
        self.rlist=[]
        self.wlist=[]
        self.xlist=[]
        self.creat_sock()
        self.sock_bind()

    def creat_sock(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def sock_bind(self):
        self.sock.bind((self.host, self.port))

    def start(self):
        self.sock.listen(5)
        print("listen the port %s"% self.port)
        self.rlist.append(self.sock)
        rs,ws,xs=select(self.rlist,self.wlist,self.xlist)
        while True:
            for r in rs:
                if r is self.sock:
                    connfd,addr=self.sock.accept()
                    print("connect from ",addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    self.handle(r)
    def handle(self,connfd):
        request=connfd.recv(1024*10).decode()
        zz=r"[A-Z]+\s+(?p<info>/\s*)"
        result=re.match(zz,request)
        if result:
            info=result.group("info")
            print("请求内容：",info)
            self.send_html(connfd,info)
        else:
            connfd.close()
            self.rlist.remove(connfd)
            return

    def send_html(self,connfd,info):
        if info =='/':
            filename=self.html+"/index.html"
        else:
            filename=self.html+info
        try:
            f=open(filename,"rb")
        except:
            rehtml='HTTP/1.1 404 FAIL\r\n'
            rehtml+='Content-Type:text/html\r\n'
            rehtml+='\r\n'
            rehtml+='sorry'
            rehtml=rehtml.encode()
        else:
            data=f.read()
            rehtml='HTTP/1.1 200 OK\r\n'
            rehtml+='Content-Type:text/html\r\n'
            rehtml+='Content-Length:%d\r\n'%len(data)
            rehtml+='\r\n'
            rehtml=rehtml.encode()+data
        finally:
            connfd.send(rehtml)



if __name__ == '__main__':
    httpd=WebServer(host='127.0.0.1',port=8000,html='./static')
    httpd.start()
