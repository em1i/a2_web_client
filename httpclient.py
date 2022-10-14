#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponseData:
    def __init__(self, data):
        self.data = data

    def getStatusLine(self):
        status_header = self.data.split("\r\n\r\n")[0]
        return status_header.split('\r')[0]

    def getStatusCode(self):
        code = self.getStatusLine().split()[1]
        return int(code)

    def getHeaders(self):
        status_header = self.data.split("\r\n\r\n")[0]
        headers = dict(h.split(":", 1) for h in status_header.split("\r\n")[1:])
        return headers
        
    def getBody(self):
        return self.data.split("\r\n\r\n")[1]


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    # def parseURL(url):
    #     try:
    #         return urllib.parse.urlparse(url)
    #     except:
    #         return None


    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return HTTPResponseData(data).getStatusCode()

    def get_headers(self,data):
        return HTTPResponseData(data).getHeaders()

    def get_body(self, data):
        return HTTPResponseData(data).getBody()
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # todo: what to do with args??


        # print("** TEST Print")
        # print("url:")
        # print(url)
        # print("** TEST end --")

        # parse URL into components
        # parsedUrl = self.parseURL(url)
        parsedUrl = urllib.parse.urlparse(url)

        # send the request to the server
        hostname = parsedUrl.hostname
        port = parsedUrl.port 
        port = 80 if port is None else port
        path = parsedUrl.path
        path = "/" if path is "" else path

    

        self.connect(hostname, port)

        # parse the response (code and body)
        request = "GET {} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(path, hostname)
        self.sendall(request)

        data = self.recvall(self.socket)

        #parse the data
        # status_header, body = data.split("\r\n\r\n")
        # statusLine = status_header.split('\r')[0]
        # headers = dict(h.split(":", 1) for h in status_header.split("\r\n")[1:])

        # d = HTTPResponseData(data)


        # print("** TEST Print")
        # print("--- parsedUrl ---")
        # print(parsedUrl)
        # print("\n--------\n")

        # print("hostname: {}" .format(hostname))
        # print("port: {}" .format(port))
        # print("path: {}" .format(path))
        # print("\n--------\n")


        # print("")
        # print("status line: {}\n".format(d.getStatusLine()))
        # print("status code: {}\n".format(d.getStatusCode()))
        # print("header: {}\n".format(d.getHeaders()))
        # print("body: {}\n".format(d.getBody()))
        # print("\n")

        # print("** TEST end --\n\n")

        code = self.get_code(data)
        body = self.get_body(data)
        self.close()
        # print("** TEST Print")
        # print(code)
        # print(body)
        # print("** TEST end --\n\n")

        # code = 500
        # body = ""

        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        # parse URL into components
        # parsedUrl = self.parseURL(url)
        parsedUrl = urllib.parse.urlparse(url)

        # send the request to the server
        hostname = parsedUrl.hostname
        port = parsedUrl.port
        path = parsedUrl.path
    
        self.connect(hostname, port)

        # parse the response (code and body)
        request = ""
        if args != None:
            encodedArgs = urllib.parse.urlencode(args)
            request = "POST  {} HTTP/1.1\r\nHost: {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{}".format(path, hostname, "www/x-form-urlencoded", len(encodedArgs), encodedArgs)
        else:
            request = "POST  {} HTTP/1.1\r\nHost: {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n".format(path, hostname, "www/x-form-urlencoded", 0)
        
        self.sendall(request)
        data = self.recvall(self.socket)
        code = self.get_code(data)
        body = self.get_body(data)

        self.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
