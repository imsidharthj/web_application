from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message = "<html><body>"
            message = "Hello!"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
            message += "</body></html>"
            self.wfile.write(message.encode('utf-8'))
            print(message)
            return
        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body>"
            message += "&#161Hola <a href = '/hello' >Back to Hello</a>"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
            message += "</body></html>"
            self.wfile.write(message.encode('utf-8'))
            print(message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == "multipart/form-data":
                fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, howabout this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output.encode('utf-8'))
            print(output)

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()
