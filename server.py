#  coding: utf-8 
import socketserver
import re
import os
import time



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


# Copyright 2020 Yuhang Ma

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.



class MyWebServer(socketserver.BaseRequestHandler):
    alow_path = './www'
    res_dir = re.compile('GET (.*?) HTTP')
    
    
    #recive requests
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        if self.data != b'':
            response = self.do_response(self.data)
            self.request.sendall(response.encode("utf-8"))

    #get resquest path    
    def do_response(self,data):
        if data[:3] == b'GET':
            path = self.res_dir.findall(data.decode())[0]
            print("loading page:",self.alow_path+path)

            if path == '/':
                response = self.deal_respose_head("301")
                return response
            try:
                response = self.deal_respose_head("200")
                response += self.deal_mime(path.split('.')[1])
                response += "\r\n" 
                with open(self.alow_path+path,'rb') as f:
                    result = f.read().decode()
                    response += result
                return response
            except:
                if os.path.isdir(self.alow_path+path):
                    if path[-1] !='/':
                        response_headers = "HTTP/1.1 {} Moved Permanently\r\n".format(301)  
                        response_headers += "Location:http://127.0.0.1:8080{}\r\n".format(path+'/')
                        response_headers += "\r\n" 
                        return response_headers
                    else:
                        print("1231231321")
                        response_headers = "HTTP/1.1 {} OK\r\n".format(200) 
                        response_headers += "Location:http://127.0.0.1:8080/index.html\r\n".format(path+'/')
                        
                        response_headers += self.deal_mime('html')
                        response_headers += "\r\n" 
                        # response_headers += ''.join(html_text)
                        with open('./www/deep/index.html','rb') as f:
                            result = f.read().decode()
                            response_headers += result
                        return response_headers
                else:
                    response = self.deal_respose_head("404")
                    response = response + "<h3>404 error, Access Forbidden</h3>"
                    return response
        else:
            response = self.deal_respose_head("405")
            response = response + "<h3>405 error, Method Not Allowed</h3>"
            return response
            #405


  
    def deal_respose_head(self,status_code):
        if status_code == '200':
            response_headers = "HTTP/1.1 {} OK\r\n".format(status_code) 
           
            return response_headers
        if status_code == '301':
            response_headers = "HTTP/1.1 {} Moved Permanently\r\n".format(status_code) 
            response_headers += "Location:http://127.0.0.1:8080/index.html\r\n"
            response_headers += "\r\n" 
            return response_headers
        if status_code == '404':
            response_headers = "HTTP/1.1 {} Not Found\r\n".format(status_code) 
            return response_headers
        if status_code == "405":
            response_headers = "HTTP/1.1 {} Method Not Allowed\r\n".format(status_code) # 200 表示找到这个资源
            return response_headers

    def deal_mime(self,kind):
        mimetype = {
            'css':'text/css',
            'html':'text/html',
            '/':'text/plain',

        }
        return "content-type: {};\r\n".format(mimetype[kind])

    
    



if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to 127.0.0.1 on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
