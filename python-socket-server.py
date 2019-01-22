#!/usr/bin/env python3

import sys
import socket
import selectors
import types
#https://realpython.com/python-sockets/

class MaapiSocketServer(object):
    sel = selectors.DefaultSelector()
    host = "192.168.1.169"
    port = 12345
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen(1)
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)
        
    
        
    @classmethod
    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print("accepted connection from", addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)

    @classmethod
    def service_connection(self,key, mask): 
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            
            if recv_data:
                data.outb += recv_data
                print (data)
            else:
                print("closing connection to", data.addr)
                self.sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print("echoing", repr(data.outb), "to", data.addr)
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
    @classmethod
    def run(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()

if __name__ == "__main__":
    MaapiSocketServer.run()
