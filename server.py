#  coding: utf-8 
import SocketServer
import os.path
import mimetypes
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
        print ("Got a request of: %s\n" % self.data)

        #self.request.sendall("OK")


        #Only Handle GET Request. If not a GET return 405
        if self.data.split(' ')[0] != "GET":
            self.request.sendall("\\\nHTTP/1.1 405 Method Not Allowed\n\r405 Method Not Allowed\n")
            print("405 Method Not Allowed\n")
            return
     
        page = self.data.split(' ')[1]

        if page == '/':
            page = "/index.html"

        #fullname = os.path.join(path, )deep/index.html

        print "www" + page

        try:
            mimetypes.init()
            f = open("www" + page, 'rb')
        
        except IOError:
            self.request.sendall("\\\nHTTP/1.1 404 Not Found\n\r")
            self.request.sendall("404 page not found\n")
            print "page not found"
            return

        #http_response = """\
        #HTTP/1,1 200 OK\n\
        #self.request.sendall("\\\nHTTP/1.1 200 OK\n\r")

        #stack overflow https://stackoverflow.com/questions/947372/custom-simple-python-http-server-not-serving-css-files/947592
        mimetype, _ = mimetypes.guess_type("www" + page)

        self.request.sendall("\\\nHTTP/1.1 200 OK\nContent-type: " + mimetype + "\n")

        fs = os.fstat(f.fileno())

        self.request.sendall("Content-Length: " + str(fs[6]) + "\r\n\r\n")

        self.request.sendall(f.read())


'''
        self.do_GET()

    def do_GET(self):
        print "doing a get"
        path = self.translate_path(self.path)
'''

'''
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })
'''

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()




