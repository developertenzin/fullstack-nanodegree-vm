from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant.name).all()
                for restaurant in restaurants:
                    output += "<p> %s <p>" % restaurant
                    output += "<a href='#'>Edit</a><br>"
                    output += "<a href='#'>Delete</a>"
                    output += "<div style='margin-bottom: 50px'></div>"

                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola <a href='/hello'> Back to hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            length = self.headers['content-length']
            post_data = self.rfile.read(int(length))
            # print("***********", post_data, "***********", type(post_data))
            # post_data is bytes!!!!!!!!!!!
            # resource-link: https://reecon.wordpress.com/2014/04/02/simple-http-server-for-testing-get-and-post-requests-python/
            post_data = str(post_data,'utf-8')
            print(type(post_data), "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            content = post_data.split("\r\n\r\n")[1].split("\r\n")[0]
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % content
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(bytes(output, "utf-8"))
        except:
            pass
            #python 2.7code
            '''
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')[0]
                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            '''


def main():
    try:
        port =  8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server runnig on port %s" % port)
        server.serve_forever()

    except:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
