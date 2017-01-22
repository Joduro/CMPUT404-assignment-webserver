#  coding: utf-8 
import SocketServer
import os.path
import mimetypes
import socket
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        #self.request.sendall("OK")


        #Only Handle GET Request. If not a GET return 405
        if self.data.split(' ')[0] != "GET":
            self.request.send("HTTP/1.1 405 Method Not Allowed\r\n")
            self.request.send("Connection: close\r\n\r\n")
            self.request.send("<html><body><h1>405 Method Not Allowed</body></html>")
            return
     
        page = self.data.split(' ')[1]

        #if page == '/':
        #    page = "/index.html"

        if(page[-1] == '/'):
            page = page + "index.html"

        #print "going to www" + page

        page = page.split('../')

        page = "".join(page)

        #print "after split going to www" + page

        try:
            mimetypes.init()
            f = open("www" + page, 'rb')
        
        except IOError:

            self.request.send("HTTP/1.1 404 Not Found\r\n")
            self.request.send("Connection: close\r\n\r\n")

            self.request.sendall('<html><body><h1>404 File Not Found</body></html>')
            #self.request.sendall("404 page not found\n")
            return

        #stack overflow https://stackoverflow.com/questions/947372/custom-simple-python-http-server-not-serving-css-files/947592
        mimetype, _ = mimetypes.guess_type("www" + page)

        if mimetype == None:
            return

        self.request.send("HTTP/1.1 200 OK\r\n")
        self.request.send("Content-type: " + mimetype + "\r\n")

        fs = os.fstat(f.fileno())

        self.request.send("Content-Length: " + str(fs[6]) + "\r\n\r\n")

        self.request.sendall(f.read())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()




